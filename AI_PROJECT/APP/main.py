import json

from services.ai_service import process_ai_response


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
