
import streamlit as st

# 1. Cấu hình trang
st.set_page_config(
    page_title="AI Expense Assistant",
    page_icon="💰",
    layout="wide"
)

# 2. Tiêu đề ứng dụng
st.title("💰 AI Expense Assistant")
st.caption("Trợ lý quản lý chi tiêu thông minh dành cho sinh viên")

# 3. Thanh điều hướng bên trái
with st.sidebar:
    st.title("Menu")
    selected_page = st.radio(
        "Điều hướng",
        ["Dashboard", "Transactions", "AI Assistant", "Budget", "Saving Goals"]
    )

# 4. Nội dung chính
if selected_page == "Dashboard":
    st.header("Tổng quan tài chính")

    # Dữ liệu mẫu
    col1, col2, col3 = st.columns(3)

    col1.metric("Tổng thu nhập", "5.000.000 đ")
    col2.metric("Tổng chi tiêu", "2.500.000 đ")
    col3.metric("Số dư", "2.500.000 đ")

    st.divider()

    st.subheader("Chào mừng bạn đến với ứng dụng!")

    st.info("Đây là Dashboard đầu tiên của AI Expense Assistant.")

elif selected_page == "Transactions":
    st.header("Quản lý giao dịch")
    st.write("Danh sách các giao dịch sẽ xuất hiện tại đây.")

elif selected_page == "AI Assistant":
    st.header("Trợ lý AI")
    st.write("Khu vực tương tác với Gemini AI.")

elif selected_page == "Budget":
    st.header("Quản lý ngân sách")
    st.write("Theo dõi ngân sách của bạn.")

elif selected_page == "Saving Goals":
    st.header("Mục tiêu tiết kiệm")
    st.write("Theo dõi các mục tiêu tiết kiệm.")
