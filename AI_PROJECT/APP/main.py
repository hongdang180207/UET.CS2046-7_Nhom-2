import sys
from pathlib import Path

# Cho phép chạy file trực tiếp từ thư mục khác mà vẫn tìm thấy package prompts.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from APP.services.ai_service import extract_with_gemini


# Chạy chương trình
if __name__ == "__main__":

    question = input("Bạn muốn hỏi AI điều gì? ")

    if not question.strip():
        print("Vui lòng nhập câu hỏi trước khi gửi.")
        raise SystemExit(1)

    try:
        print("ĐÃ NHẬN CÂU HỎI XIN VUI LÒNG CHỜ TRONG GIÂY LÁT (có thể mất vài giây)")
        result = extract_with_gemini(question)

        print("\nKẾT QUẢ TRÍCH XUẤT:")
        for transaction in result.transactions:
            print("-------------------")
            print("Số tiền:", transaction.amount)
            print("Danh mục:", transaction.category)
            print("Loại:", transaction.type)
            print("Mô tả:", transaction.description)
            print("Ngày:", transaction.date)
            print("Ngày mặc định:", transaction.date_is_default)

    except Exception as error:
        message = str(error)
        if "503" in message or "UNAVAILABLE" in message:
            print("Gemini đang quá tải hoặc tạm thời không khả dụng (503).")
            print("Hãy chờ một chút rồi thử lại.")
        elif "504" in message or "DEADLINE_EXCEEDED" in message:
            print("Gemini mất quá nhiều thời gian để xử lý câu hỏi (504).")
            print("Hãy chờ một chút rồi chạy lại; câu hỏi ngắn hơn thường phản hồi nhanh hơn.")
            print("Nếu lỗi lặp lại, kiểm tra trạng thái dịch vụ Gemini và kết nối mạng.")
        else:
            print("Không thể nhận phản hồi từ Gemini:", message)
