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

    # --- SIDEBAR: BỘ LỌC (FILTERS) ---
    st.sidebar.header("🔍 Bộ lọc Dữ liệu")
    
    # 1. Lọc theo Khoảng thời gian
    min_date = df['date'].min()
    max_date = df['date'].max()
    date_range = st.sidebar.date_input(
        "Chọn khoảng thời gian:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # 2. Lọc theo Kênh (Channel) - Bao gồm Social & Search
    all_channels = df['channel'].unique().tolist()
    selected_channels = st.sidebar.multiselect(
        "Chọn Kênh Marketing:",
        options=all_channels,
        default=all_channels
    )

    # 3. Lọc theo Chiến dịch (Campaign) - 7 loại chiến dịch
    all_campaigns = df['campaign'].unique().tolist()
    selected_campaigns = st.sidebar.multiselect(
        "Chọn Chiến dịch:",
        options=all_campaigns,
        default=all_campaigns
    )

    # --- ÁP DỤNG BỘ LỌC ---
    # Lọc theo ngày
    mask_date = (df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))
    # Lọc theo kênh & chiến dịch
    mask_channel = df['channel'].isin(selected_channels)
    mask_campaign = df['campaign'].isin(selected_campaigns)

    df_filtered = df[mask_date & mask_channel & mask_campaign]

    st.sidebar.markdown("---")
    st.sidebar.write(f"Số dòng dữ liệu hiển thị: **{len(df_filtered)}**")

    # --- TAB 1: XEM DỮ LIỆU GỐC ---
    with tab1:
        st.header("📂 Dữ liệu Gốc và Dữ liệu đã Lọc")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.subheader("Dữ liệu Gốc (Toàn bộ)")
            st.dataframe(df.head(5))
        with col_d2:
            st.subheader("Dữ liệu đang xem (Đã lọc)")
            st.dataframe(df_filtered.head(5))
        
        st.write(f"Kích thước dữ liệu gốc: {df.shape[0]} dòng | Dữ liệu lọc: {df_filtered.shape[0]} dòng")
        
        # Kiểm tra dữ liệu khuyết
        missing = df.isnull().sum().sum()
        if missing == 0:
            st.success("✅ Dữ liệu sạch, không có giá trị Null.")
        else:
            st.warning(f"⚠️ Có {missing} giá trị bị thiếu.")

    # --- TAB 2: TRỰC QUAN HÓA CHI TIẾT ---
    with tab2:
        st.header("📈 Dashboard Phân tích Hiệu quả Marketing")
        
        if len(df_filtered) == 0:
            st.warning("⚠️ Không có dữ liệu nào thỏa mãn điều kiện bộ lọc. Vui lòng chọn lại!")
        else:
            # --- PHẦN 1: KPI METRICS CARDS ---
            st.subheader("1. Chỉ số Tổng quan (KPIs)")
            
            total_cost = df_filtered['cost'].sum()
            total_revenue = df_filtered['revenue'].sum()
            total_impressions = df_filtered['impressions'].sum()
            total_conversions = df_filtered['conversions'].sum()
            avg_roas = total_revenue / total_cost if total_cost > 0 else 0
            
            kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
            kpi1.metric("Tổng Chi Phí", f"${total_cost:,.0f}")
            kpi2.metric("Tổng Doanh Thu", f"${total_revenue:,.0f}")
            kpi3.metric("Lợi nhuận (Profit)", f"${(total_revenue - total_cost):,.0f}")
            kpi4.metric("Tổng Chuyển đổi", f"{total_conversions:,.0f}")
            kpi5.metric("ROAS Trung bình", f"{avg_roas:.2f}x")
            
            st.divider()

            # --- PHẦN 2: PHỄU MARKETING (FUNNEL) ---
            st.subheader("2. Phễu Chuyển đổi (Conversion Funnel)")
            # Tính các giai đoạn của phễu
            funnel_data = dict(
                number=[total_impressions, df_filtered['clicks'].sum(), total_conversions],
                stage=["Impressions (Hiển thị)", "Clicks (Nhấp chuột)", "Conversions (Chuyển đổi)"]
            )
            fig_funnel = px.funnel(funnel_data, x='number', y='stage', title="Hiệu suất Phễu Marketing")
            st.plotly_chart(fig_funnel, width="stretch")
            
            st.divider()

            # --- PHẦN 3: SO SÁNH DOANH THU & CHI PHÍ ---
            st.subheader("3. Hiệu quả theo Kênh & Chiến dịch")
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.markdown("**Doanh thu theo Kênh (Social/Search)**")
                rev_by_channel = df_filtered.groupby('channel')['revenue'].sum().reset_index()
                fig_pie = px.pie(rev_by_channel, values='revenue', names='channel', hole=0.4)
                st.plotly_chart(fig_pie, width="stretch")
                
            with col_chart2:
                st.markdown("**Doanh thu theo Chiến dịch (7 campaigns)**")
                rev_by_campaign = df_filtered.groupby('campaign')['revenue'].sum().reset_index().sort_values('revenue', ascending=True)
                fig_bar_camp = px.bar(rev_by_campaign, x='revenue', y='campaign', orientation='h', 
                                      color='revenue', title="")
                st.plotly_chart(fig_bar_camp, width="stretch")

            # --- PHẦN 4: BIỂU ĐỒ XU HƯỚNG ---
            st.subheader("4. Xu hướng theo Thời gian")
            
            # Group by theo ngày (hoặc tuần nếu dữ liệu quá dài, ở đây giữ theo ngày)
            daily_trend = df_filtered.groupby('date')[['cost', 'revenue', 'conversions']].sum().reset_index()
            
            # Vẽ biểu đồ 2 trục Y (Dual Axis) nếu cần, hoặc đơn giản là Multi-line
            fig_trend = px.line(daily_trend, x='date', y=['cost', 'revenue'], 
                                title='Tương quan Chi tiêu và Doanh thu theo ngày',
                                markers=True)
            st.plotly_chart(fig_trend, width="stretch")
            
            # --- PHẦN 5: CHI TIẾT HIỆU QUẢ ---
            st.subheader("5. Tương quan Cost vs Revenue (ROI Analysis)")
            fig_scatter = px.scatter(df_filtered, x='cost', y='revenue', 
                                     color='channel', size='conversions', 
                                     hover_data=['campaign'],
                                     title='Phân bố hiệu quả đầu tư (Bóng bóng = Số chuyển đổi)')
            st.plotly_chart(fig_scatter, width="stretch")

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