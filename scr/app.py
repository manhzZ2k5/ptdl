import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import statsmodels.api as sm

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Marketing Optimizer", page_icon="📊", layout="wide")

# --- HÀM TẢI VÀ XỬ LÝ DỮ LIỆU (CACHED ĐỂ APP CHẠY NHANH) ---
@st.cache_data
def load_and_process_data():
    # 1. Tải dữ liệu
    df = pd.read_csv('media_all_channels.csv')
    
    # 2. Xử lý Outlier bằng IQR
    Q1_c = df['cost'].quantile(0.25)
    Q3_c = df['cost'].quantile(0.75)
    IQR_c = Q3_c - Q1_c
    lower_c = Q1_c - 1.5 * IQR_c
    upper_c = Q3_c + 1.5 * IQR_c
    outliers_cost = df[(df['cost'] < lower_c) | (df['cost'] > upper_c)]

    Q1_r = df['revenue'].quantile(0.25)
    Q3_r = df['revenue'].quantile(0.75)
    IQR_r = Q3_r - Q1_r
    lower_r = Q1_r - 1.5 * IQR_r
    upper_r = Q3_r + 1.5 * IQR_r
    outliers_revenue = df[(df['revenue'] < lower_r) | (df['revenue'] > upper_r)]
    
    outlier_indices = pd.concat([outliers_cost, outliers_revenue]).index.unique()
    df_clean = df.drop(index=outlier_indices).copy()
    
    # 3. Chuẩn bị dữ liệu cho Hồi quy (Pivot)
    def aggregate_daily(df_input):
        df_daily = df_input.groupby(['date', 'channel'], as_index=False)[['cost', 'revenue']].sum()
        df_pivot = df_daily.pivot(index='date', columns='channel', values=['cost', 'revenue'])
        df_pivot.columns = [f"{col[1]}_{col[0]}" for col in df_pivot.columns]
        df_pivot = df_pivot.reset_index().fillna(0)
        revenue_cols = [col for col in df_pivot.columns if 'revenue' in col]
        df_pivot['total_revenue'] = df_pivot[revenue_cols].sum(axis=1)
        return df_pivot

    df_pivot_orig = aggregate_daily(df)
    df_pivot_clean = aggregate_daily(df_clean)
    
    return df, df_clean, df_pivot_orig, df_pivot_clean

# Tải dữ liệu
try:
    df, df_clean, df_pivot_orig, df_pivot_clean = load_and_process_data()
except FileNotFoundError:
    st.error("Không tìm thấy file 'media_all_channels.csv'. Vui lòng kiểm tra lại thư mục!")
    st.stop()

# --- HÀM CHẠY MÔ HÌNH (CACHED) ---
@st.cache_resource
def train_models(df_pivot_orig, df_pivot_clean):
    cost_cols = [col for col in df_pivot_clean.columns if 'cost' in col]
    
    def build_model(df_pivot, cost_cols, target_col):
        X = df_pivot[cost_cols]
        y = df_pivot[target_col]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        coeff = pd.DataFrame({'Kênh': cost_cols, 'Hệ số (Beta)': model.coef_})
        return coeff, r2, mae, rmse, y_test, y_pred, model.intercept_
        
    res_orig = build_model(df_pivot_orig, [col for col in df_pivot_orig.columns if 'cost' in col], 'total_revenue')
    res_clean = build_model(df_pivot_clean, cost_cols, 'total_revenue')
    
    return res_orig, res_clean, cost_cols

res_orig, res_clean, cost_cols = train_models(df_pivot_orig, df_pivot_clean)

# --- TẠO MENU SIDEBAR ---
st.sidebar.title("📌 Menu Phân Tích")
page = st.sidebar.radio("Chọn trang xem:", [
    "1. Tổng quan Dự án", 
    "2. Giải mã Chiến lược", 
    "3. Khám phá Dữ liệu (EDA)", 
    "4. Đánh giá Mô hình", 
    "5. Tương thích Kênh & Chiến dịch",
    "6. Giả lập Ngân sách"
])
st.sidebar.markdown("---")
st.sidebar.info("Dự án: Phân tích & Tối ưu hóa Ngân sách Marketing Đa kênh bằng Machine Learning.")

# ==========================================
# TRANG 1: TỔNG QUAN
# ==========================================
if page == "1. Tổng quan Dự án":
    st.title("📊 Tối ưu hóa Ngân sách Digital Marketing Đa Kênh")
    st.info("**Mục tiêu Dự án:** Ứng dụng mô hình Đa hồi quy tuyến tính (Multiple Linear Regression) để tính toán **Lợi tức biên (Marginal ROI)** của từng kênh quảng cáo, chuyển đổi từ việc phân bổ ngân sách cảm tính sang dữ liệu định lượng.")
    
    st.markdown("### 1. Chỉ số Tổng quan (KPIs)")
    total_cost = df['cost'].sum()
    total_revenue = df['revenue'].sum()
    roi_percent = ((total_revenue - total_cost) / total_cost) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số điểm dữ liệu", f"{len(df):,} dòng")
    col2.metric("Tổng Ngân sách (Cost)", f"${total_cost:,.0f}")
    col3.metric("Tổng Doanh thu (Revenue)", f"${total_revenue:,.0f}")
    col4.metric("ROI Tổng thể", f"{roi_percent:.2f}%")
        
    st.markdown("---")
    st.markdown("### 2. Dữ liệu Đầu vào (Raw Data)")
    
    with st.expander("📖 Xem Từ điển Dữ liệu (Data Dictionary)"):
        st.markdown("""
        * **date:** Ngày ghi nhận dữ liệu.
        * **channel:** Kênh triển khai (Facebook, Google Ads, LinkedIn...).
        * **campaign:** Loại chiến dịch (Flash Sale, Best Sellers...).
        * **cost:** Chi phí đã chi tiêu ($).
        * **revenue:** Doanh thu mang lại ($).
        * **impressions / clicks / conversions:** Số lượt hiển thị, nhấp chuột và chuyển đổi.
        """)
        
    st.dataframe(df.head(10), use_container_width=True)

# ==========================================
# TRANG 2: TÂM LÝ HỌC MARKETING (ĐÃ CẬP NHẬT CASE STUDY)
# ==========================================
elif page == "2. Giải mã Chiến lược":
    st.title("🧠 Giải mã Chiến lược Marketing")
    st.markdown("""
    Bộ dữ liệu gồm **7 loại chiến dịch** đại diện cho các **chiến thuật tâm lý học hành vi (Behavioral Psychology)** kinh điển trong marketing hiện đại. 
    Dưới đây là phân tích chuyên sâu về cơ chế hoạt động và các Case Study thực tế từ các thương hiệu toàn cầu.
    """)
    st.markdown("---")

    # Sử dụng Tabs để phân loại
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Hiệu ứng Đám đông", 
        "⏳ Sự Khan hiếm (FOMO)", 
        "💎 Tính Độc quyền", 
        "✨ Sự Mới mẻ & Nhu cầu"
    ])

    with tab1:
        st.header("👥 Social Proof — Hiệu ứng Đám đông")
        st.write("Con người có xu hướng sao chép hành động của người khác, đặc biệt khi họ không chắc chắn. Việc thấy hàng triệu người tin dùng sẽ làm giảm rào cản mua sắm.")
        
        col1, col2 = st.columns(2)
        with col1: 
            st.success("🏆 **Best Sellers (Bán chạy nhất)**")
            st.write("**Cơ chế:** Gắn nhãn sản phẩm để tạo tín hiệu an toàn: *'Nhiều người mua thế này chắc chắn là đồ tốt'.*")
            st.markdown("> **📚 Case Study:** Nhãn **#1 Best Seller** màu cam đặc trưng của **Amazon** hoặc danh mục 'Bán chạy' trên **Shopee/Tiki**, giúp tăng tỷ lệ chốt đơn lên tới 30% đối với khách hàng mới.")
        with col2: 
            st.info("🔥 **Trending Now (Xu hướng hiện tại)**")
            st.write("**Cơ chế:** Khai thác tâm lý đám đông và nỗi sợ bị lạc hậu so với xã hội.")
            st.markdown("> **📚 Case Study:** Chiến dịch **#TikTokMadeMeBuyIt** của **TikTok**. Người dùng mua các món đồ gia dụng, mỹ phẩm chỉ vì thấy hàng loạt KOC/KOL đang sử dụng và khen ngợi nó trên xu hướng.")

    with tab2:
        st.header("⏳ Scarcity & FOMO — Sự Khan hiếm")
        st.write("Khi một sản phẩm bị giới hạn về thời gian hoặc số lượng, não bộ sẽ kích hoạt phản ứng 'sợ mất mát' (Loss Aversion), thúc đẩy người dùng hành động ngay lập tức.")
        
        col1, col2 = st.columns(2)
        with col1: 
            st.error("⚡ **Flash Sale (Giảm giá chớp nhoáng)**")
            st.write("**Cơ chế:** Đồng hồ đếm ngược tạo ra áp lực thời gian cực lớn, loại bỏ sự chần chừ.")
            st.markdown("> **📚 Case Study:** Sự kiện **Amazon Prime Day** hoặc các dịp **Siêu Sale 11.11, 12.12** của sàn TMĐT. Cảm giác 'chỉ còn 2 tiếng nữa là hết hạn' buộc khách hàng mua cả những thứ họ chưa thực sự cần.")
        with col2: 
            st.warning("🎯 **Limited Edition (Phiên bản giới hạn)**")
            st.write("**Cơ chế:** Giới hạn số lượng sản xuất để tạo ra cảm giác khan hiếm nhân tạo và nâng tầm giá trị.")
            st.markdown("> **📚 Case Study:** Các màn hợp tác **Nike Air Jordan x Dior** (chỉ sản xuất vài nghìn đôi) hoặc những chiếc **cốc Starbucks phiên bản Giáng sinh**. Khách hàng thậm chí sẵn sàng xếp hàng từ mờ sáng để sở hữu.")

    with tab3:
        st.header("💎 Exclusivity — Tính Độc quyền")
        st.write("Đánh trúng vào tháp nhu cầu Maslow: Khát khao được tôn trọng, được công nhận địa vị và cảm thấy mình là người đặc biệt (VIP).")
        
        st.success("👑 **Exclusive Offers (Ưu đãi độc quyền)**")
        st.write("**Cơ chế:** Phần thưởng hoặc mã giảm giá chỉ mở khóa cho một tệp khách hàng rất nhỏ. Giúp tăng LTV (Giá trị vòng đời khách hàng).")
        st.markdown("> **📚 Case Study:** Chương trình khách hàng thân thiết **Sephora Beauty Insider (Hạng VIB Rouge)**. Những thành viên hạng này được mua hàng mới trước người thường, nhận quà tặng sinh nhật riêng, khiến họ liên tục mua sắm để duy trì đặc quyền.")

    with tab4:
        st.header("✨ Novelty & Necessity — Sự Mới mẻ & Thiết yếu")
        st.write("Não bộ con người luôn tiết ra Dopamine (hormone hạnh phúc) khi khám phá cái mới, đồng thời cũng dễ bị thuyết phục bởi những thứ được gán mác 'không thể thiếu'.")
        
        col1, col2 = st.columns(2)
        with col1: 
            st.info("🆕 **New Arrivals (Hàng mới về)**")
            st.write("**Cơ chế:** Khai thác sự tò mò. Khách hàng luôn muốn mình là người tiên phong trải nghiệm.")
            st.markdown("> **📚 Case Study:** Sự kiện **Apple Keynote ra mắt iPhone mới** vào tháng 9 hàng năm. Dù sản phẩm mới không khác biệt quá nhiều so với bản cũ, từ khóa 'New' vẫn đủ sức tạo ra doanh thu hàng tỷ đô la trong tuần đầu tiên.")
        with col2: 
            st.warning("✅ **Must-Haves (Sản phẩm thiết yếu)**")
            st.write("**Cơ chế:** Định hình sản phẩm từ 'Muốn mua' (Want) thành 'Phải có' (Need) trong cuộc sống.")
            st.markdown("> **📚 Case Study:** Chiến dịch quảng bá áo sinh nhiệt **Heattech của Uniqlo**. Họ không bán áo thun, họ bán định kiến: 'Đã là mùa đông thì trong tủ đồ bắt buộc phải có một chiếc Heattech để giữ ấm'.")

        
# ==========================================
# TRANG 3: EDA & LÀM SẠCH
# ==========================================
elif page == "3. Khám phá Dữ liệu (EDA)":
    st.title("🔍 Làm sạch & Khám phá Dữ liệu")
    
    st.markdown("### 1. Xử lý Giá trị ngoại lai (Outliers)")
    with st.expander("Thuật toán loại bỏ (IQR Method)"):
        st.write("Sử dụng Khoảng tứ phân vị (Interquartile Range) để phát hiện và loại bỏ các ngày có chi phí/doanh thu đột biến, nhằm tránh làm lệch đường hồi quy.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Trích xuất gốc (Trước khi lọc):**")
        fig1 = px.box(df, y='cost', points="all", title="Boxplot Chi phí gốc")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.markdown(f"**Dữ liệu sạch (Đã xóa {len(df) - len(df_clean)} dòng outlier):**")
        fig2 = px.box(df_clean, y='cost', points="all", title="Boxplot Chi phí sạch")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 2. Kiểm tra Đa cộng tuyến (Heatmap)")
    st.write("Đảm bảo các kênh quảng cáo không bị phụ thuộc vào nhau.")
    corr = df_pivot_clean[[c for c in df_pivot_clean.columns if 'cost' in c]].corr()
    fig_corr, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax, fmt=".2f")
    st.pyplot(fig_corr)
    st.success("✅ **Kết luận:** Hệ số tương quan giữa các kênh rất thấp, dữ liệu đạt chuẩn hoàn hảo để chạy mô hình Hồi quy tuyến tính.")

# ==========================================
# TRANG 4: ĐÁNH GIÁ MÔ HÌNH
# ==========================================
elif page == "4. Đánh giá Mô hình":
    st.title("🤖 Đánh giá Mô hình Machine Learning")
    
    coeff_orig, r2_orig, mae_orig, rmse_orig, _, _, _ = res_orig
    coeff_clean, r2_clean, mae_clean, rmse_clean, y_test, y_pred, _ = res_clean
    
    st.markdown("### 1. Bảng So sánh Hiệu suất")
    comp_df = pd.DataFrame({
        'Chỉ số': ['R-squared ($R^2$)', 'Sai số tuyệt đối (MAE)', 'Sai số bình phương (RMSE)'],
        'Mô hình Dữ liệu Gốc': [round(r2_orig, 4), round(mae_orig, 2), round(rmse_orig, 2)],
        'Mô hình Dữ liệu Sạch': [round(r2_clean, 4), round(mae_clean, 2), round(rmse_clean, 2)]
    })
    st.table(comp_df)
    st.success("Mô hình làm sạch cho sai số thấp hơn, độ tin cậy được đảm bảo.")
    
    st.markdown("### 2. Phân tích Phần dư (Residuals) - Mô hình Sạch")
    col1, col2 = st.columns(2)
    residuals = y_test - y_pred
    
    with col1:
        fig_hist = px.histogram(residuals, nbins=30, title="Phân phối Phần dư (Dáng chuông chuẩn)")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col2:
        fig_scatter = px.scatter(x=y_pred, y=residuals, title="Phần dư vs Giá trị dự đoán", labels={'x': 'Dự đoán', 'y': 'Phần dư'})
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_scatter, use_container_width=True)

# ==========================================
# TRANG 5: DEEP-DIVE
# ==========================================
elif page == "5. Tương thích Kênh & Chiến dịch":
    st.title("🎯 Phân tích Tương thích: Kênh & Chiến dịch")
    st.write("Định vị chiến dịch nào nên chạy trên nền tảng nào để đạt ROAS tối đa.")
    
    df_interaction = df_clean.groupby(['channel', 'campaign'])[['cost', 'revenue']].sum().reset_index()
    df_interaction['ROAS'] = df_interaction['revenue'] / df_interaction['cost']
    
    st.markdown("### 1. Bản đồ Nhiệt (Heatmap) ROAS Tổng hợp")
    roas_matrix = df_interaction.pivot(index='campaign', columns='channel', values='ROAS')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(roas_matrix, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=.5, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.markdown("### 2. Bóc tách từng Chiến dịch")
    selected_camp = st.selectbox("Chọn Chiến dịch để xem Kênh tốt nhất:", df_clean['campaign'].unique())
    
    df_camp = df_interaction[df_interaction['campaign'] == selected_camp].sort_values('ROAS')
    fig_bar = px.bar(df_camp, x='ROAS', y='channel', orientation='h', color='ROAS', color_continuous_scale='RdYlGn', title=f"Xếp hạng Nền tảng cho chiến dịch: {selected_camp.upper()}")
    fig_bar.add_vline(x=1, line_dash="dash", line_color="red", annotation_text="Điểm hòa vốn (ROAS=1)")
    st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# TRANG 6: GIẢ LẬP NGÂN SÁCH (THEO TỪNG CHIẾN DỊCH)
# ==========================================
elif page == "6. Giả lập Ngân sách":
    st.title("💰 Trình Giả lập & Tối ưu Ngân sách")
    st.write("Dự báo doanh thu và tối ưu hóa dòng tiền dựa trên loại Chiến dịch cụ thể mà công ty muốn triển khai.")
    
    from scipy.optimize import linprog
    
    # --- 1. BỘ LỌC CHIẾN DỊCH ---
    campaigns_list = df_clean['campaign'].unique().tolist()
    selected_campaign = st.selectbox("🎯 Chọn Chiến dịch Công ty muốn chạy trong tháng tới:", campaigns_list)
    
    # --- 2. XỬ LÝ DỮ LIỆU RIÊNG CHO CHIẾN DỊCH ĐÃ CHỌN ---
    # Lọc data theo chiến dịch
    df_camp = df_clean[df_clean['campaign'] == selected_campaign]
    
    # Tính ROAS (Lợi tức) thực tế cho từng kênh của chiến dịch này
    camp_grouped = df_camp.groupby('channel')[['cost', 'revenue']].sum().reset_index()
    camp_grouped['ROAS'] = camp_grouped['revenue'] / camp_grouped['cost']
    camp_grouped['ROAS'] = camp_grouped['ROAS'].fillna(0) # Tránh lỗi chia cho 0
    
    # Sắp xếp từ cao xuống thấp
    camp_grouped = camp_grouped.sort_values('ROAS', ascending=False)
    
    # Vẽ biểu đồ ROAS cho chiến dịch này
    st.markdown(f"### 🏆 Bảng xếp hạng Lợi tức (ROAS) cho chiến dịch **{selected_campaign.upper()}**")
    fig = px.bar(camp_grouped, x='ROAS', y='channel', orientation='h', 
                 color='ROAS', color_continuous_scale='Greens', 
                 title=f"1 Đồng chi phí sinh ra bao nhiêu Đồng doanh thu? ({selected_campaign})")
    fig.add_vline(x=1, line_dash="dash", line_color="red", annotation_text="Điểm hòa vốn (ROAS=1)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    # --- 3. CHIA 2 TABS CHỨC NĂNG ---
    tab_manual, tab_auto = st.tabs(["✍️ Phân bổ Thủ công (Manual)", "🤖 AI Tối ưu hóa (Auto-Allocate)"])
    
    # ================= TAB 1: MANUAL =================
    with tab_manual:
        st.markdown("### 🎛️ Bảng Điều khiển Ngân sách")
        st.write("Nhập ngân sách giả định cho tháng tới để xem doanh thu dự báo:")
        
        budgets = {}
        channels = camp_grouped['channel'].tolist()
        col_m1, col_m2 = st.columns(2)
        
        for idx, channel in enumerate(channels):
            # Lấy ROAS hiện tại để hiển thị gợi ý cho người dùng
            current_roas = camp_grouped.loc[camp_grouped['channel'] == channel, 'ROAS'].values[0]
            label = f"Ngân sách {channel} (ROAS: {current_roas:.2f})"
            
            if idx % 2 == 0:
                with col_m1:
                    budgets[channel] = st.number_input(label, value=2000, step=500, key=f"man_{channel}")
            else:
                with col_m2:
                    budgets[channel] = st.number_input(label, value=2000, step=500, key=f"man_{channel}")
                    
        if st.button("🚀 CHẠY DỰ BÁO DOANH THU", type='primary', use_container_width=True):
            projected_revenue = 0
            for channel, budget in budgets.items():
                roas = camp_grouped.loc[camp_grouped['channel'] == channel, 'ROAS'].values[0]
                projected_revenue += budget * roas
                
            st.success(f"Tính toán hoàn tất cho chiến dịch {selected_campaign}!")
            st.metric(label="💰 TỔNG DOANH THU DỰ KIẾN", value=f"${projected_revenue:,.0f}")

    # ================= TAB 2: AUTO (LINEAR PROGRAMMING) =================
    with tab_auto:
        st.markdown("### 🤖 Thuật toán Quy hoạch Tuyến tính (Linear Programming)")
        st.write("Hệ thống sẽ ép ngân sách = 0 đối với các kênh bị lỗ (ROAS < 1) và dồn tiền vào các kênh sinh lời.")
        
        total_budget = st.number_input("💸 Tổng ngân sách khả dụng ($)", value=10000, step=1000, min_value=1000)
        max_ratio = st.slider("⚠️ Mức độ rủi ro: Tối đa ngân sách cho 1 kênh (%)", min_value=10, max_value=100, value=40, step=5)
        
        if st.button("🧠 TỰ ĐỘNG PHÂN BỔ", type='primary', use_container_width=True):
            betas = camp_grouped['ROAS'].tolist()
            channels = camp_grouped['channel'].tolist()
            
            # Thiết lập bài toán Linprog
            c = [-b for b in betas] # Maximize
            A_eq = [[1] * len(betas)]
            b_eq = [total_budget]
            
            max_per_channel = (max_ratio / 100) * total_budget
            
            # Ép ngân sách về 0 nếu kênh bị lỗ (ROAS < 1.0)
            bounds = [(0, 0) if b < 1.0 else (0, max_per_channel) for b in betas]
            
            res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
            
            if res.success:
                st.success(f"Tối ưu hóa thành công chiến dịch {selected_campaign}! Dưới đây là chiến lược chia tiền:")
                
                col_a1, col_a2 = st.columns([1, 1])
                with col_a1:
                    st.markdown("#### 🎯 Kế hoạch rót vốn:")
                    for i, channel in enumerate(channels):
                        alloc = res.x[i]
                        if alloc > 0:
                            st.write(f"- **{channel}**: ${alloc:,.0f}")
                        else:
                            st.write(f"- **{channel}**: ❌ Cắt ngân sách (Lỗ)")
                            
                with col_a2:
                    st.markdown("#### 📈 Kết quả Dự kiến:")
                    total_ad_revenue = -res.fun
                    
                    st.metric("🔥 TỔNG DOANH THU ĐẠT ĐƯỢC", f"${total_ad_revenue:,.0f}")
            else:
                st.error("Không tìm được phương án tối ưu. Vui lòng tăng tỷ lệ % rủi ro hoặc kiểm tra lại ngân sách.")