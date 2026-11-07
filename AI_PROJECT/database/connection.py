"""Tạo kết nối Python tới MySQL Server."""

import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


# connection.py nằm trong AI_PROJECT/database, nên parents[1] là AI_PROJECT.
PROJECT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_DIR / ".env")


def get_connection():
    """Mở và trả về một kết nối tới database của ứng dụng."""

    required_settings = ("DB_USER", "DB_PASSWORD")
    missing_settings = [name for name in required_settings if not os.getenv(name)]

    if missing_settings:
        names = ", ".join(missing_settings)
        raise RuntimeError(
            f"Thiếu cấu hình {names}. Hãy tạo AI_PROJECT/.env "
            "dựa trên AI_PROJECT/.env.example."
        )

    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "chi_tieu_sinh_vien"),
            connection_timeout=5,
        )
    except Error as exc:
        raise RuntimeError(
            "Không kết nối được MySQL. Hãy kiểm tra MySQL Server đang chạy, "
            "địa chỉ host/port, tài khoản và tên database trong AI_PROJECT/.env. "
            f"Chi tiết lỗi: {exc}"
        ) from exc
