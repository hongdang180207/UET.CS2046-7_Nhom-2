import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts.transaction_prompt import SYSTEM_INSTRUCTION


load_dotenv()


def extract_with_gemini(user_input):
    """Trích xuất giao dịch từ nội dung người dùng bằng Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    if not api_key or not model:
        raise ValueError("Thiếu GEMINI_API_KEY hoặc GEMINI_MODEL trong cấu hình môi trường")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.2,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini không trả về nội dung.")

    return response.text


def validate_transaction(transaction):
    """
    Kiểm tra dữ liệu của một giao dịch.
    """

    required_fields = [
        "amount",
        "category",
        "type",
        "description",
        "date"
    ]

    # Kiểm tra các trường bắt buộc
    for field in required_fields:
        if field not in transaction:
            return False, f"Thiếu trường: {field}"

    # Kiểm tra số tiền
    if not isinstance(transaction["amount"], int):
        return False, "Số tiền phải là số nguyên"

    if transaction["amount"] <= 0:
        return False, "Số tiền phải lớn hơn 0"

    # Kiểm tra loại giao dịch
    if transaction["type"] not in ["income", "expense"]:
        return False, "Loại giao dịch không hợp lệ"

    # Kiểm tra các trường văn bản
    for field in ["category", "description", "date"]:
        if not isinstance(transaction[field], str):
            return False, f"{field} phải là chuỗi"

        if not transaction[field].strip():
            return False, f"{field} không được để trống"

    return True, "Dữ liệu hợp lệ"


def process_ai_response(json_data):
    """
    Nhận JSON từ AI và kiểm tra từng giao dịch.
    """

    try:
        transactions = json.loads(json_data)

        if not isinstance(transactions, list):
            return {
                "success": False,
                "message": "Dữ liệu phải là một danh sách",
                "data": []
            }

        valid_transactions = []

        for transaction in transactions:

            if not isinstance(transaction, dict):
                continue

            is_valid, message = validate_transaction(transaction)

            if is_valid:
                valid_transactions.append(transaction)
            else:
                print("Lỗi:", message)

        return {
            "success": True,
            "message": "Đã xử lý dữ liệu",
            "data": valid_transactions
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "message": "JSON không hợp lệ",
            "data": []
        }
