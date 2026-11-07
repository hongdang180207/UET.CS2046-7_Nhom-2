"""Kiểm tra Python có kết nối được tới MySQL hay không."""

from database.connection import get_connection


connection = None

try:
    connection = get_connection()
    print("Kết nối MySQL thành công!")
    print("Database đang kết nối:", connection.database)
except Exception as error:
    print("Kết nối thất bại:")
    print(error)
finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("Đã đóng kết nối.")
