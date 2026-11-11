
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, timedelta, datetime


# 1. Cấu hình trang
st.set_page_config(
    page_title="AI Expense Assistant",
    page_icon="💰",
    layout="wide"
)

# 2. Tiêu đề ứng dụng
st.title(" AI Expense Assistant")
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

        st.plotly_chart(fig_pie, width="stretch")

    st.subheader("Chào mừng bạn đến với ứng dụng!")
    st.info("Đây là Dashboard đầu tiên của AI Expense Assistant.")

elif selected_page == "Transactions":
    st.header("Quản lý giao dịch")
    st.caption("Theo dõi và quản lý các khoản thu chi của bạn.")

    # 1. Khởi tạo dữ liệu giao dịch trong Session State
    if "transactions" not in st.session_state:
        st.session_state.transactions = pd.DataFrame({
            "Ngày": [
                "10/11/2026",
                "09/11/2026",
                "08/11/2026",
                "07/11/2026",
                "06/11/2026"
            ],
            "Tên giao dịch": [
                "Ăn trưa",
                "Tiền làm thêm",
                "Mua sách",
                "Đi xe bus",
                "Xem phim"
            ],
            "Danh mục": [
                "Ăn uống",
                "Thu nhập",
                "Học tập",
                "Đi lại",
                "Giải trí"
            ],
            "Loại": [
                "Chi tiêu",
                "Thu nhập",
                "Chi tiêu",
                "Chi tiêu",
                "Chi tiêu"
            ],
            "Số tiền": [
                35000,
                1500000,
                120000,
                7000,
                80000
            ]
        })

    # 2. Form thêm giao dịch
    with st.expander("➕ Thêm giao dịch mới", expanded=False):

        # Chọn loại giao dịch bên ngoài Form
        transaction_type = st.selectbox(
            "Loại giao dịch",
            ["Chi tiêu", "Thu nhập"],
            key="new_transaction_type"
        )

        # Danh mục thay đổi theo loại giao dịch
        if transaction_type == "Chi tiêu":
            category_options = [
                "Ăn uống",
                "Đi lại",
                "Học tập",
                "Giải trí",
                "Mua sắm",
                "Khác"
            ]
        else:
            category_options = [
                "Lương",
                "Làm thêm",
                "Thưởng",
                "Thu nhập khác"
            ]

        with st.form("add_transaction_form"):

            transaction_name = st.text_input(
                "Tên giao dịch",
                placeholder="Ví dụ: Ăn sáng, mua sách..."
            )

            transaction_amount = st.number_input(
                "Số tiền (VND)",
                min_value=0,
                step=1000
            )

            transaction_date = st.date_input(
                "Ngày giao dịch",
                value=date.today()
            )

            transaction_category = st.selectbox(
                "Danh mục",
                category_options,
                key="new_transaction_category"
            )

            submitted = st.form_submit_button(
                "Thêm giao dịch",
                width="stretch"
            )

            if submitted:

                if not transaction_name.strip():
                    st.error("Vui lòng nhập tên giao dịch.")

                elif transaction_amount <= 0:
                    st.error("Số tiền phải lớn hơn 0.")

                else:
                    new_transaction = pd.DataFrame([{
                        "Ngày": transaction_date.strftime("%d/%m/%Y"),
                        "Tên giao dịch": transaction_name.strip(),
                        "Danh mục": transaction_category,
                        "Loại": transaction_type,
                        "Số tiền": int(transaction_amount)
                    }])

                    st.session_state.transactions = pd.concat(
                        [st.session_state.transactions, new_transaction],
                        ignore_index=True
                    )

                    st.success("Thêm giao dịch thành công!")
    # 3. Lấy dữ liệu giao dịch mới nhất
    transaction_data = st.session_state.transactions.copy()

    # 4. Tìm kiếm và lọc giao dịch
    st.subheader("Lịch sử giao dịch")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        search_text = st.text_input(
            "Tìm kiếm giao dịch",
            placeholder="Nhập tên giao dịch..."
        )

    with filter_col2:
        selected_type = st.selectbox(
            "Loại giao dịch",
            ["Tất cả", "Thu nhập", "Chi tiêu"]
        )

    with filter_col3:
        categories = ["Tất cả"] + \
            transaction_data["Danh mục"].unique().tolist()

        selected_category = st.selectbox(
            "Danh mục",
            categories
        )

    # 5. Áp dụng bộ lọc
    filtered_data = transaction_data.copy()

    if search_text:
        filtered_data = filtered_data[
            filtered_data["Tên giao dịch"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    if selected_type != "Tất cả":
        filtered_data = filtered_data[
            filtered_data["Loại"] == selected_type
        ]

    if selected_category != "Tất cả":
        filtered_data = filtered_data[
            filtered_data["Danh mục"] == selected_category
        ]

    # 6. Định dạng dữ liệu để hiển thị
    display_data = filtered_data.copy()

    display_data["Số tiền"] = display_data["Số tiền"].map(
        lambda amount: f"{amount:,.0f} đ".replace(",", ".")
    )

    # 7. Hiển thị kết quả
    st.dataframe(
        display_data,
        width="stretch",
        hide_index=True
    )

    st.caption(f"Tìm thấy {len(filtered_data)} giao dịch.")
    # 8. Xóa giao dịch
    with st.expander("🗑️ Xóa giao dịch"):

        if filtered_data.empty:
            st.info("Không có giao dịch để xóa.")
        else:
            transaction_indices = filtered_data.index.tolist()

            selected_transaction_index = st.selectbox(
                "Chọn giao dịch cần xóa",
                transaction_indices,
                format_func=lambda index: (
                    f"{transaction_data.loc[index, 'Ngày']} - "
                    f"{transaction_data.loc[index, 'Tên giao dịch']} - "
                    f"{transaction_data.loc[index, 'Số tiền']:,} đ"
                )
            )

            if st.button("Xóa giao dịch", type="primary"):
                st.session_state.transactions = (
                    st.session_state.transactions.drop(
                        selected_transaction_index
                    ).reset_index(drop=True)
                )

                st.success("Đã xóa giao dịch thành công!")
                st.rerun()
                # 9. Chỉnh sửa giao dịch
    with st.expander("✏️ Chỉnh sửa giao dịch"):

        if transaction_data.empty:
            st.info("Chưa có giao dịch để chỉnh sửa.")

        else:
            transaction_indices = transaction_data.index.tolist()

            selected_edit_index = st.selectbox(
                "Chọn giao dịch cần chỉnh sửa",
                transaction_indices,
                format_func=lambda index: (
                    f"{transaction_data.loc[index, 'Ngày']} - "
                    f"{transaction_data.loc[index, 'Tên giao dịch']}"
                ),
                key="edit_transaction_selector"
            )

            # Lấy thông tin giao dịch đang chọn
            current_transaction = st.session_state.transactions.loc[
                selected_edit_index
            ]

            st.write("**Chỉnh sửa thông tin giao dịch**")

            # 1. Tên giao dịch
            edit_name = st.text_input(
                "Tên giao dịch",
                value=current_transaction["Tên giao dịch"],
                key=f"edit_name_{selected_edit_index}"
            )

            # 2. Số tiền
            edit_amount = st.number_input(
                "Số tiền (VND)",
                min_value=0,
                value=int(current_transaction["Số tiền"]),
                step=1000,
                key=f"edit_amount_{selected_edit_index}"
            )

            # 3. Ngày giao dịch
            edit_date = st.date_input(
                "Ngày giao dịch",
                value=datetime.strptime(
                    current_transaction["Ngày"], "%d/%m/%Y"
                ).date(),
                key=f"edit_date_{selected_edit_index}"
            )

            # 4. Loại giao dịch
            edit_type = st.selectbox(
                "Loại giao dịch",
                ["Chi tiêu", "Thu nhập"],
                index=["Chi tiêu", "Thu nhập"].index(
                    current_transaction["Loại"]
                ),
                key=f"edit_type_{selected_edit_index}"
            )

            # 5. Danh mục thay đổi theo loại giao dịch
            if edit_type == "Chi tiêu":
                edit_category_options = [
                    "Ăn uống", "Đi lại", "Học tập",
                    "Giải trí", "Mua sắm", "Khác"
                ]
            else:
                edit_category_options = [
                    "Lương", "Làm thêm", "Thưởng", "Thu nhập khác"
                ]

            current_category = current_transaction["Danh mục"]

            if current_category not in edit_category_options:
                edit_category_options.append(current_category)

            edit_category = st.selectbox(
                "Danh mục",
                edit_category_options,
                index=edit_category_options.index(current_category),
                key=f"edit_category_{selected_edit_index}_{edit_type}"
            )

            # 6. Lưu thay đổi
            if st.button("Lưu thay đổi", type="primary"):

                if not edit_name.strip():
                    st.error("Tên giao dịch không được để trống.")

                elif edit_amount <= 0:
                    st.error("Số tiền phải lớn hơn 0.")

                else:
                    st.session_state.transactions.loc[
                        selected_edit_index, "Tên giao dịch"
                    ] = edit_name.strip()

                    st.session_state.transactions.loc[
                        selected_edit_index, "Số tiền"
                    ] = int(edit_amount)

                    st.session_state.transactions.loc[
                        selected_edit_index, "Ngày"
                    ] = edit_date.strftime("%d/%m/%Y")

                    st.session_state.transactions.loc[
                        selected_edit_index, "Loại"
                    ] = edit_type

                    st.session_state.transactions.loc[
                        selected_edit_index, "Danh mục"
                    ] = edit_category

                    st.success("Cập nhật giao dịch thành công!")
                    st.rerun()

elif selected_page == "AI Assistant":
    st.header("Trợ lý AI")
    st.write("Khu vực tương tác với Gemini AI.")

elif selected_page == "Budget":
    st.header("Quản lý ngân sách")
    st.write("Theo dõi ngân sách của bạn.")

elif selected_page == "Saving Goals":
    st.header("Mục tiêu tiết kiệm")
    st.write("Theo dõi các mục tiêu tiết kiệm.")
