from pydantic import BaseModel, Field
from typing import Literal


class Transaction(BaseModel):

    amount: int = Field(
        ge=1,
        description="Số tiền giao dịch, tính bằng VND"
    )

    category: Literal[
        # Chi tiêu
        "Ăn uống",
        "Cà phê",
        "Đi lại",
        "Tiền trọ",
        "Học tập",
        "Giải trí",
        "Mua sắm",
        "Sức khỏe",
        "Khác",

        # Thu nhập
        "Gia đình gửi",
        "Làm thêm",
        "Học bổng",
    ]

    type: Literal[
        "income",
        "expense"
    ]

    description: str

    date: str | None = None

    date_is_default: bool = False


class TransactionList(BaseModel):

    transactions: list[Transaction]
