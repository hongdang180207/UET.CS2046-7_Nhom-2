import json
import os
from services.ai_service import process_ai_response
from dotenv import load_dotenv
from google import genai



# Giả lập dữ liệu do AI trả về
ai_response = [
    {
        "amount": 40000,
        "category": "Ăn uống",
        "type": "expense",
        "description": "Ăn phở",
        "date": "2026-11-05"
    },
    {
        "amount": 500000,
        "category": "Khác",
        "type": "income",
        "description": "Mẹ chuyển tiền",
        "date": "2026-11-05"
    }
]


# Chuyển Python Dictionary thành JSON
json_data = json.dumps(
    ai_response,
    ensure_ascii=False
)


# Gửi dữ liệu đến AI Service để kiểm tra
result = process_ai_response(json_data)


# Hiển thị kết quả
print("Trạng thái:", result["success"])

print("Thông báo:", result["message"])

print("Các giao dịch hợp lệ:")

for transaction in result["data"]:
    print(transaction)

# Đọc biến môi trường
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL")

if not API_KEY or not MODEL:
    raise ValueError("Thiếu GEMINI_API_KEY hoặc GEMINI_MODEL")

# Khởi tạo Gemini Client
client = genai.Client(api_key=API_KEY)


# Gửi câu hỏi đến Gemini
def ask_gemini(question):

    response = client.models.generate_content(
        model=MODEL,
        contents=question
    )

    return response.text


# Chạy chương trình
if __name__ == "__main__":

    question = input("Bạn muốn hỏi AI điều gì? ")

    try:
        result = ask_gemini(question)

        print("\nPhản hồi từ Gemini:")
        print(result)

    except Exception as error:
        print("Đã xảy ra lỗi:", error)
