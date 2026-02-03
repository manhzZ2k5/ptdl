import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os


# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Phân tích Marketing Đa Kênh", layout="wide")

st.title("📊 Phân Tích Hiệu Quả Digital Marketing Đa Kênh")
st.markdown("""
Ứng dụng này hỗ trợ thực hiện:
1. **Chương 2:** Trực quan hóa dữ liệu mô tả.
2. **Chương 3:** Xử lý dữ liệu (Làm sạch & Mã hóa) để chuẩn bị chạy mô hình Hồi quy.
""")

# --- 1. TẢI DỮ LIỆU ---
@st.cache_data
def load_data():
    try:
        # Đọc file CSV
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'media_all_channels.csv'))
        return df
    except FileNotFoundError:
        st.error("Không tìm thấy file 'media_all_channels.csv'. Hãy đảm bảo file nằm cùng thư mục với code.")
        return None

df = load_data()

if df is not None:
    # Chuyển đổi cột date sang datetime để vẽ biểu đồ thời gian chuẩn hơn
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # Tạo Tab để phân chia công việc
    tab1, tab2, tab3 = st.tabs(["📂 Dữ liệu Gốc", "📈 Trực quan hóa (Chương 2)", "⚙️ Xử lý Dữ liệu (Chương 3 -> 6)"])

    # --- TAB 1: XEM DỮ LIỆU GỐC ---
    with tab1:
        st.header("Xem trước dữ liệu gốc")
        st.dataframe(df.head(10))
        st.write(f"Kích thước dữ liệu: {df.shape[0]} dòng, {df.shape[1]} cột")
        
        # Kiểm tra dữ liệu khuyết
        missing = df.isnull().sum().sum()
        if missing == 0:
            st.success("✅ Dữ liệu sạch, không có giá trị Null.")
        else:
            st.warning(f"⚠️ Có {missing} giá trị bị thiếu.")

    # --- TAB 2: TRỰC QUAN HÓA (DÀNH CHO CHƯƠNG 2) ---
    with tab2:
        st.header("Trực quan hóa Thống kê Mô tả")
        
        # Layout chia 2 cột
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("1. Cơ cấu Doanh thu theo Kênh")
            # Tính tổng doanh thu theo kênh
            revenue_by_channel = df.groupby('channel')['revenue'].sum().reset_index()
            fig_pie = px.pie(revenue_by_channel, values='revenue', names='channel', title='Tỷ trọng Doanh thu')
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.subheader("2. Tương quan: Chi phí vs Doanh thu")
            fig_scatter = px.scatter(df, x='cost', y='revenue', color='channel',
                                     title='Mối quan hệ Cost - Revenue', hover_data=['campaign'])
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.divider()

        st.subheader("3. Xu hướng theo Thời gian")
        # Gom nhóm theo ngày
        daily_trend = df.groupby('date')[['cost', 'revenue']].sum().reset_index()
        fig_line = px.line(daily_trend, x='date', y=['cost', 'revenue'], 
                           title='Biến động Chi phí và Doanh thu theo ngày',
                           labels={'value': 'Số tiền', 'variable': 'Chỉ số'})
        st.plotly_chart(fig_line, use_container_width=True)

        st.divider()

        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("4. Hiệu quả ROAS trung bình")
            avg_roas = df.groupby('channel')['roas'].mean().reset_index().sort_values(by='roas', ascending=False)
            fig_bar = px.bar(avg_roas, x='channel', y='roas', color='channel',
                             title='So sánh ROAS (Doanh thu / Chi phí)')
            # Thêm đường tham chiếu
            fig_bar.add_hline(y=4, line_dash="dot", annotation_text="Mục tiêu = 4.0", line_color="red")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col4:
            st.subheader("5. Ma trận Tương quan (Kiểm tra Đa cộng tuyến)")
            # Chỉ chọn các cột số quan trọng
            corr_cols = ['cost', 'impressions', 'clicks', 'revenue']
            corr_matrix = df[corr_cols].corr()
            
            # Vẽ bằng Seaborn và Matplotlib
            fig_corr, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            st.pyplot(fig_corr)
            st.caption("Lưu ý: Nếu hệ số > 0.9 (màu đỏ đậm) chứng tỏ có đa cộng tuyến mạnh.")

    # --- TAB 3: XỬ LÝ DỮ LIỆU (CHUẨN BỊ CHO CHƯƠNG 6) ---
    with tab3:
        st.header("Chuẩn bị dữ liệu chạy Mô hình Hồi quy")
        st.markdown("Bước này sẽ loại bỏ các cột phái sinh và mã hóa biến chữ thành số.")

        # 1. Chọn cột để xóa
        cols_to_drop = ['cpc', 'cpa', 'ctr', 'conversion_rate', 'roas', 'roi', 'profit_margin']
        if 'date' in df.columns:
            cols_to_drop.append('date') # Xóa ngày tháng cho hồi quy cắt ngang
        
        st.write("🔻 **Các cột sẽ bị loại bỏ (Data Cleaning):**")
        st.code(f"{cols_to_drop}")

        # Thực hiện xóa
        df_model = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')

        # 2. Mã hóa biến giả (Dummy Variables)
        st.write("🔄 **Tạo biến giả (One-Hot Encoding) cho 'Channel' và 'Campaign':**")
        df_model = pd.get_dummies(df_model, columns=['channel', 'campaign'], drop_first=True)
        # drop_first=True để tránh bẫy đa cộng tuyến (Dummy Trap)
        
        # 3. Hiển thị dữ liệu sau xử lý
        st.subheader("Dữ liệu sau khi xử lý (Sẵn sàng chạy hồi quy)")
        st.dataframe(df_model.head())
        st.write(f"Kích thước mới: {df_model.shape[0]} dòng, {df_model.shape[1]} cột")

        # 4. Nút tải xuống
        csv = df_model.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Tải xuống file dữ liệu sạch (Final_Model_Data.csv)",
            data=csv,
            file_name='Final_Model_Data.csv',
            mime='text/csv',
        )
        st.success("Bạn hãy tải file này về để nộp hoặc dùng cho Python/SPSS chạy hồi quy ở Chương 6!")

else:
    st.info("Vui lòng tải file 'media_all_channels.csv' vào cùng thư mục.")