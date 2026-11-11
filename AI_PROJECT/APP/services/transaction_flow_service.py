#----1.IMPORT----
"""Chuẩn bị giao dịch để xem trước và chỉ lưu sau khi xác nhận."""

from datetime import date

from APP.models.transaction import Transaction, TransactionDraft
from APP.services.transaction_service import create_transaction
from database.connection import get_connection

#----2.TÌM DANH MUC TRONG DB----
def _find_category_id(category_name: str, transaction_type: str) -> int:
    connection = get_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT category_id
            FROM categories
            WHERE name = %s
              AND type = %s
              AND is_active = TRUE
            """,
            (category_name, transaction_type),
        )
        row = cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    if row is None:
        raise ValueError(
            f"Không tìm thấy danh mục '{category_name}' "
            f"cho loại giao dịch '{transaction_type}'."
        )

    return int(row[0])

#----3.TẠO BẢN NHÁP, CHƯA LƯU----
def prepare_transaction_draft(data: dict) -> TransactionDraft:
    """Kiểm tra dữ liệu AI và chuyển thành bản nháp giao dịch."""

    required_fields = {"amount", "category", "type", "description", "date"}
    missing_fields = required_fields - data.keys()

    if missing_fields:
        raise ValueError(
            "Thiếu thông tin: " + ", ".join(sorted(missing_fields))
        )

    amount = data["amount"]
    category_name = data["category"]
    transaction_type = data["type"]
    description = data["description"]

    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("Số tiền phải là số nguyên dương.")

    if transaction_type not in {"income", "expense"}:
        raise ValueError("Loại giao dịch phải là income hoặc expense.")

    if not isinstance(category_name, str) or not category_name.strip():
        raise ValueError("Tên danh mục không được để trống.")

    if not isinstance(description, str) or not description.strip():
        raise ValueError("Mô tả không được để trống.")

    try:
        transaction_date = date.fromisoformat(data["date"])
    except (TypeError, ValueError) as error:
        raise ValueError("Ngày phải có dạng YYYY-MM-DD.") from error

    category_id = _find_category_id(
        category_name.strip(),
        transaction_type,
    )

    return TransactionDraft(
        category_id=category_id,
        transaction_type=transaction_type,
        amount_vnd=amount,
        description=description.strip(),
        transaction_date=transaction_date,
        input_source="natural_language",
        exclude_from_saving=bool(data.get("exclude_from_saving", False)),
    )

#----4.CHỈ LƯU KHI XÁC NHẬN----
def confirm_and_save_transaction(
    user_id: int,
    draft: TransactionDraft,
    confirmed: bool,
) -> Transaction | None:
    """Chưa xác nhận thì không lưu; xác nhận rồi mới gọi CRUD."""

    if not confirmed:
        return None

    return create_transaction(user_id=user_id, draft=draft)