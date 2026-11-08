import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Đọc biến môi trường
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL")

if not API_KEY or not MODEL:
    raise ValueError("Thiếu GEMINI_API_KEY hoặc GEMINI_MODEL")

# Khởi tạo Gemini Client
client = genai.Client(
    api_key=API_KEY,
    # HttpOptions.timeout được tính bằng mili giây.
    http_options=types.HttpOptions(timeout=90000),
)


# Gửi câu hỏi đến Gemini
def ask_gemini(question):

    response = client.models.generate_content(
        model=MODEL,
        contents=question,
        # Giảm thời gian suy luận cho ứng dụng hỏi đáp thông thường.
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="low"),
            max_output_tokens=1024,
        ),
    )

    return response.text


# Chạy chương trình
if __name__ == "__main__":

    question = input("Bạn muốn hỏi AI điều gì? ")

    if not question.strip():
        print("Vui lòng nhập câu hỏi trước khi gửi.")
        raise SystemExit(1)

    try:
        print("Đang gửi câu hỏi đến Gemini... (có thể mất vài giây)")
        result = ask_gemini(question)

        print("\nPhản hồi từ Gemini:")
        print(result or "Gemini trả về phản hồi trống.")

    except Exception as error:
        message = str(error)
        if "504" in message or "DEADLINE_EXCEEDED" in message:
            print("Gemini mất quá nhiều thời gian để xử lý câu hỏi (504).")
            print("Hãy chờ một chút rồi chạy lại; câu hỏi ngắn hơn thường phản hồi nhanh hơn.")
            print("Nếu lỗi lặp lại, kiểm tra trạng thái dịch vụ Gemini và kết nối mạng.")
        else:
            print("Không thể nhận phản hồi từ Gemini:", message)
