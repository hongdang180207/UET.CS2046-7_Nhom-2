import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from APP.schemas.transaction_schema import TransactionList
from prompts.transaction_prompt import SYSTEM_INSTRUCTION


load_dotenv()


def extract_with_gemini(user_input: str) -> TransactionList:
    """Trích xuất giao dịch từ câu nhập và kiểm tra bằng schema Pydantic."""
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    if not api_key or not model:
        raise ValueError("Thiếu GEMINI_API_KEY hoặc GEMINI_MODEL trong cấu hình môi trường")
    if not user_input or not user_input.strip():
        raise ValueError("Nội dung nhập không được để trống")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=TransactionList,
            temperature=0.1,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini không trả về nội dung.")

    # Pydantic xác thực JSON và các kiểu/ràng buộc trong TransactionList.
    return TransactionList.model_validate_json(response.text)
