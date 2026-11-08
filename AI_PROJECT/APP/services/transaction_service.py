"""Các thao tác CRUD cho giao dịch trong database."""

# --- (1. IMPORT THƯ VIỆN) ---
from contextlib import contextmanager
from datetime import date
from typing import Any, Iterator

from APP.models.transaction import Transaction, TransactionDraft
from database.connection import get_connection


# --- (2. CÂU SQL DÙNG CHUNG) ---
# Liệt kê rõ tên cột, viết một lần, nơi nào cần thì dùng lại.
SELECT_COLUMNS = """
    SELECT
        transaction_id, user_id, category_id, transaction_type,
        amount_vnd, description, transaction_date, input_source,
        exclude_from_saving, created_at, updated_at
    FROM transactions
"""


# --- (3. MỞ KẾT NỐI VÀ CURSOR) ---
@contextmanager
def _open_cursor() -> Iterator[Any]:
    """Mở kết nối và cursor.

    - Chạy xong không lỗi  -> commit (lưu thay đổi)
    - Có lỗi               -> rollback (hủy thay đổi)
    - Dù thế nào           -> đóng cursor và kết nối
    """
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        yield cursor          # trả cursor cho hàm bên ngoài dùng
        connection.commit()   # hàm bên ngoài chạy xong -> lưu
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


# --- (4. CHUYỂN DÒNG DATABASE THÀNH OBJECT) ---
def _row_to_transaction(row: dict) -> Transaction:
    """Chuyển một dòng MySQL thành đối tượng Transaction của Python."""
    return Transaction(
        transaction_id=row["transaction_id"],
        user_id=row["user_id"],
        category_id=row["category_id"],
        transaction_type=row["transaction_type"],
        amount_vnd=row["amount_vnd"],
        description=row["description"],
        transaction_date=row["transaction_date"],
        input_source=row["input_source"],
        exclude_from_saving=bool(row["exclude_from_saving"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


# --- (5. KIỂM TRA DỮ LIỆU ĐẦU VÀO) ---
def _check_positive(value: int, name: str) -> None:
    """Báo lỗi nếu giá trị không phải số nguyên dương."""
    if value <= 0:
        raise ValueError(f"{name} phải là số nguyên dương.")


def _validate_draft(user_id: int, draft: TransactionDraft) -> None:
    """Kiểm tra dữ liệu cơ bản trước khi gửi xuống MySQL."""
    _check_positive(user_id, "user_id")
    _check_positive(draft.category_id, "category_id")

    if draft.amount_vnd <= 0:
        raise ValueError("Số tiền phải lớn hơn 0.")

    if draft.transaction_type not in {"income", "expense"}:
        raise ValueError("Loại giao dịch phải là income hoặc expense.")

    if draft.input_source not in {"manual", "natural_language"}:
        raise ValueError("Nguồn nhập phải là manual hoặc natural_language.")


# --- (6. HÀM PHỤ: ĐỌC 1 DÒNG THEO ID) ---
def _fetch_row(cursor: Any, transaction_id: int, user_id: int) -> dict | None:
    """Đọc một dòng giao dịch theo transaction_id và user_id."""
    cursor.execute(
        SELECT_COLUMNS + " WHERE transaction_id = %s AND user_id = %s",
        (transaction_id, user_id),
    )
    return cursor.fetchone()


# --- (7. CREATE: THÊM GIAO DỊCH) ---
def create_transaction(
    user_id: int,
    draft: TransactionDraft,
) -> Transaction:
    """Lưu giao dịch đã được người dùng xác nhận và trả về giao dịch mới."""
    # Bước 1: kiểm tra dữ liệu
    _validate_draft(user_id, draft)

    with _open_cursor() as cursor:
        # Bước 2: thêm dòng mới vào bảng
        cursor.execute(
            """
            INSERT INTO transactions (
                user_id, category_id, transaction_type, amount_vnd,
                description, transaction_date, input_source,
                exclude_from_saving
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                draft.category_id,
                draft.transaction_type,
                draft.amount_vnd,
                draft.description,
                draft.transaction_date,
                draft.input_source,
                draft.exclude_from_saving,
            ),
        )

        # Bước 3: đọc lại dòng vừa thêm (lastrowid là id mới tạo)
        row = _fetch_row(cursor, cursor.lastrowid, user_id)

        if row is None:
            raise RuntimeError("Không đọc lại được giao dịch vừa tạo.")

        # Bước 4: đổi thành object và trả về
        return _row_to_transaction(row)


# --- (8. READ: ĐỌC MỘT GIAO DỊCH) ---
def get_transaction_by_id(
    user_id: int,
    transaction_id: int,
) -> Transaction | None:
    """Đọc một giao dịch; trả về None nếu không tìm thấy."""
    # Bước 1: kiểm tra dữ liệu
    _check_positive(user_id, "user_id")
    _check_positive(transaction_id, "transaction_id")

    with _open_cursor() as cursor:
        # Bước 2: đọc dòng theo id
        row = _fetch_row(cursor, transaction_id, user_id)

        # Bước 3: không có thì trả None, có thì đổi thành object
        if row is None:
            return None

        return _row_to_transaction(row)


# --- (9. READ: ĐỌC DANH SÁCH GIAO DỊCH) ---
def get_transactions(
    user_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Transaction]:
    """Đọc giao dịch của một người, có thể lọc theo khoảng ngày."""
    # Bước 1: kiểm tra dữ liệu
    _check_positive(user_id, "user_id")

    if start_date and end_date and start_date > end_date:
        raise ValueError("start_date không được sau end_date.")

    # Bước 2: ghép câu SQL (thêm điều kiện lọc nếu có)
    query = SELECT_COLUMNS + " WHERE user_id = %s"
    parameters: list = [user_id]

    if start_date is not None:
        query += " AND transaction_date >= %s"
        parameters.append(start_date)

    if end_date is not None:
        query += " AND transaction_date <= %s"
        parameters.append(end_date)

    query += " ORDER BY transaction_date DESC, transaction_id DESC"

    # Bước 3: chạy câu SQL và đổi từng dòng thành object
    with _open_cursor() as cursor:
        cursor.execute(query, tuple(parameters))
        rows = cursor.fetchall()

        return [_row_to_transaction(row) for row in rows]


# --- (10. UPDATE: SỬA GIAO DỊCH) ---
def update_transaction(
    user_id: int,
    transaction_id: int,
    draft: TransactionDraft,
) -> Transaction | None:
    """Sửa giao dịch; trả về None nếu giao dịch không tồn tại."""
    # Bước 1: kiểm tra dữ liệu
    _validate_draft(user_id, draft)
    _check_positive(transaction_id, "transaction_id")

    with _open_cursor() as cursor:
        # Bước 2: cập nhật dòng
        cursor.execute(
            """
            UPDATE transactions
            SET
                category_id = %s,
                transaction_type = %s,
                amount_vnd = %s,
                description = %s,
                transaction_date = %s,
                input_source = %s,
                exclude_from_saving = %s
            WHERE transaction_id = %s AND user_id = %s
            """,
            (
                draft.category_id,
                draft.transaction_type,
                draft.amount_vnd,
                draft.description,
                draft.transaction_date,
                draft.input_source,
                draft.exclude_from_saving,
                transaction_id,
                user_id,
            ),
        )

        # Bước 3: đọc lại dòng sau khi sửa
        row = _fetch_row(cursor, transaction_id, user_id)

        # Bước 4: không có dòng nào thì trả None
        if row is None:
            return None

        return _row_to_transaction(row)


# --- (11. DELETE: XÓA GIAO DỊCH) ---
def delete_transaction(user_id: int, transaction_id: int) -> bool:
    """Xóa giao dịch; trả về True nếu xóa được, False nếu không tìm thấy."""
    # Bước 1: kiểm tra dữ liệu
    _check_positive(user_id, "user_id")
    _check_positive(transaction_id, "transaction_id")

    with _open_cursor() as cursor:
        # Bước 2: xóa dòng
        cursor.execute(
            """
            DELETE FROM transactions
            WHERE transaction_id = %s AND user_id = %s
            """,
            (transaction_id, user_id),
        )

        # Bước 3: rowcount > 0 nghĩa là có ít nhất 1 dòng bị xóa
        return cursor.rowcount > 0