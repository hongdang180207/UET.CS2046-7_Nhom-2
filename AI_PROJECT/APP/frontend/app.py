
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta


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
    # 1. Chọn khoảng thời gian
    period = st.selectbox(
        "Chọn khoảng thời gian",
        ["Tháng này", "Tháng trước", "Tùy chỉnh"]
    )

    today = date.today()

    # 2. Xác định ngày bắt đầu và kết thúc
    if period == "Tháng này":
        start_date = today.replace(day=1)
        end_date = today

    elif period == "Tháng trước":
        last_day_previous_month = today.replace(day=1) - timedelta(days=1)
        start_date = last_day_previous_month.replace(day=1)
        end_date = last_day_previous_month

    else:
        col_start, col_end = st.columns(2)

        with col_start:
            start_date = st.date_input(
                "Từ ngày",
                value=today.replace(day=1)
            )

        with col_end:
            end_date = st.date_input(
                "Đến ngày",
                value=today
            )

    # 3. Kiểm tra khoảng thời gian
    if start_date > end_date:
        st.error("Ngày bắt đầu không được sau ngày kết thúc.")

    else:
        st.info(
            f"Đang xem dữ liệu từ "
            f"{start_date.strftime('%d/%m/%Y')} đến "
            f"{end_date.strftime('%d/%m/%Y')}"
        )

    st.divider()

    # Dữ liệu mẫu
    col1, col2, col3 = st.columns(3)

    col1.metric("Tổng thu nhập", "5.000.000 đ")
    col2.metric("Tổng chi tiêu", "2.500.000 đ")
    col3.metric("Số dư", "2.500.000 đ")

    st.divider()

    st.subheader("Phân tích thu chi")

# 1. Dữ liệu thu nhập và chi tiêu theo tuần
    weekly_data = pd.DataFrame({
        "Tuần": ["Tuần 1", "Tuần 2", "Tuần 3", "Tuần 4"],
        "Thu nhập": [1200000, 1300000, 1200000, 1300000],
        "Chi tiêu": [500000, 700000, 600000, 700000]
    })

# 2. Dữ liệu chi tiêu theo danh mục
    category_data = pd.DataFrame({
        "Danh mục": [
            "Ăn uống",
            "Đi lại",
            "Học tập",
            "Giải trí",
            "Khác"
        ],
        "Số tiền": [
            1000000,
            400000,
            600000,
            300000,
            200000
        ]
    })

    # Chia giao diện thành hai cột
    chart_col1, chart_col2 = st.columns(2)

    # 3. Biểu đồ cột
    with chart_col1:
        st.subheader("Thu nhập và chi tiêu theo tuần")

        fig_bar = px.bar(
            weekly_data,
            x="Tuần",
            y=["Thu nhập", "Chi tiêu"],
            barmode="group",
            title="So sánh thu nhập và chi tiêu"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # 4. Biểu đồ tròn
    with chart_col2:
        st.subheader("Cơ cấu chi tiêu")

        fig_pie = px.pie(
            category_data,
            names="Danh mục",
            values="Số tiền",
            title="Chi tiêu theo danh mục"
        )

    st.plotly_chart(fig_pie, use_container_width=True)

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
