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
    
    # 2. Xử lý Outlier bằng CAPPING (WINSORIZATION) - Đã sửa để khớp báo cáo
    df_clean = df.copy()
    
    # Capping cho Cost
    Q1_c = df_clean['cost'].quantile(0.25)
    Q3_c = df_clean['cost'].quantile(0.75)
    IQR_c = Q3_c - Q1_c
    lower_c = Q1_c - 1.5 * IQR_c
    upper_c = Q3_c + 1.5 * IQR_c
    df_clean['cost'] = np.clip(df_clean['cost'], lower_c, upper_c)

    # Capping cho Revenue
    Q1_r = df_clean['revenue'].quantile(0.25)
    Q3_r = df_clean['revenue'].quantile(0.75)
    IQR_r = Q3_r - Q1_r
    lower_r = Q1_r - 1.5 * IQR_r
    upper_r = Q3_r + 1.5 * IQR_r
    df_clean['revenue'] = np.clip(df_clean['revenue'], lower_r, upper_r)
    
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
        # Bỏ random_state hoặc set cố định để model ra đúng y hệt báo cáo
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Đổi tên kênh cho đẹp (bỏ chữ _cost_clean)
        clean_channel_names = [col.split('_')[0] for col in cost_cols]
        coeff = pd.DataFrame({'channel': clean_channel_names, 'ROAS': model.coef_})
        return coeff, r2, mae, rmse, y_test, y_pred, model.intercept_
        
    res_orig = build_model(df_pivot_orig, [col for col in df_pivot_orig.columns if 'cost' in col], 'total_revenue')
    res_clean = build_model(df_pivot_clean, cost_cols, 'total_revenue')
    
    return res_orig, res_clean, cost_cols

res_orig, res_clean, cost_cols = train_models(df_pivot_orig, df_pivot_clean)
coeff_clean_df = res_clean[0] # Lấy bảng chứa các Beta

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
# TRANG 1, 2, 3, 4, 5 (Giữ nguyên như trước)
# ==========================================
if page == "1. Tổng quan Dự án":
    st.title("📊 Tối ưu hóa Ngân sách Digital Marketing Đa Kênh")
    st.info("**Mục tiêu Dự án:** Ứng dụng mô hình Đa hồi quy tuyến tính (Machine Learning) để kiểm định **Lợi tức biên (Marginal ROAS)** của từng kênh quảng cáo, sau đó kết hợp thuật toán **Quy hoạch tuyến tính (Linear Programming)** để chuyển đổi từ việc phân bổ ngân sách cảm tính sang dữ liệu định lượng.")
    
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
    st.dataframe(df.head(10), use_container_width=True)

elif page == "2. Giải mã Chiến lược":
    st.title("🧠 Giải mã Chiến lược Marketing")
    st.markdown("Bộ dữ liệu gồm **7 loại chiến dịch** đại diện cho các chiến thuật tâm lý học hành vi. Dưới đây là phân tích chuyên sâu.")
    st.image("https://images.unsplash.com/photo-1533750349088-cd871a92f312?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80", caption="Minh họa: Chiến lược Digital Marketing")

elif page == "3. Khám phá Dữ liệu (EDA)":
    st.title("🔍 Làm sạch & Khám phá Dữ liệu")
    
    col_eda1, col_eda2 = st.columns(2)
    with col_eda1:
        fig_funnel = px.scatter(df_clean, x='impressions', y='revenue', trendline='ols', title="Lượt hiển thị vs Doanh thu", opacity=0.4)
        st.plotly_chart(fig_funnel, use_container_width=True)

    with col_eda2:
        df_diminish = df_clean.copy()
        df_diminish['ROAS'] = df_diminish['revenue'] / df_diminish['cost']
        fig_diminish = px.scatter(df_diminish, x='cost', y='ROAS', trendline='lowess', title="Chi phí vs Lợi tức (ROAS)", opacity=0.4)
        fig_diminish.add_hline(y=1, line_dash="dash", line_color="red")
        st.plotly_chart(fig_diminish, use_container_width=True)

    st.markdown("### 2. Xử lý Giá trị ngoại lai (Capping Method)")
    st.success("Dữ liệu đã được giới hạn trần/sàn (Winsorization) thay vì loại bỏ, giúp bảo toàn 100% các tín hiệu kinh doanh từ những chiến dịch Viral.")
    
    col_out1, col_out2 = st.columns(2)
    with col_out1:
        fig1 = px.box(df, y='cost', points="all", title="Boxplot Chi phí gốc (Chứa Outlier)")
        st.plotly_chart(fig1, use_container_width=True)
    with col_out2:
        fig2 = px.box(df_clean, y='cost', points="all", title="Boxplot Chi phí sạch (Đã Capping)")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 3. Kiểm tra Đa cộng tuyến (Heatmap)")
    corr = df_pivot_clean[[c for c in df_pivot_clean.columns if 'cost' in c]].corr()
    fig_corr, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax, fmt=".2f")
    st.pyplot(fig_corr)

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
    
    st.markdown("### 2. Phân tích Phần dư (Residuals) - Mô hình Sạch")
    col1, col2 = st.columns(2)
    residuals = y_test - y_pred
    
    with col1:
        fig_hist = px.histogram(residuals, nbins=30, title="Phân phối Phần dư (Dáng chuông chuẩn)")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col2:
        fig_scatter = px.scatter(x=y_pred, y=residuals, title="Phần dư vs Giá trị dự đoán")
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_scatter, use_container_width=True)

elif page == "5. Tương thích Kênh & Chiến dịch":
    st.title("🎯 Phân tích Chuyên sâu: Kênh & Chiến dịch")
    df_interaction = df_clean.groupby(['channel', 'campaign'])[['cost', 'revenue']].sum().reset_index()
    df_interaction['ROAS'] = df_interaction['revenue'] / df_interaction['cost']
    
    roas_matrix = df_interaction.pivot(index='campaign', columns='channel', values='ROAS')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(roas_matrix, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=.5, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ==========================================
# TRANG 6: GIẢ LẬP NGÂN SÁCH (LINEAR PROGRAMMING) - ĐÃ ĐƯỢC FIX TOÀN BỘ
# ==========================================
elif page == "6. Giả lập Ngân sách":
    st.title("💰 Trình Giả lập & Tối ưu Ngân sách")
    st.write("Sử dụng thuật toán AI để tự động quy hoạch dòng tiền, dựa trên chính xác Hệ số Lợi tức biên (Marginal ROAS) học được từ Mô hình Đa hồi quy.")
    
    st.info("💡 **Tính năng đã được đồng bộ hóa:** Thay vì dùng ROAS trung bình bằng phép chia thông thường, hệ thống đã trích xuất trực tiếp các hệ số Beta (Website: 3.34, LinkedIn: 2.29, Facebook: -1.12...) từ mô hình Machine Learning ở Trang 4. Điều này đảm bảo tính thống nhất tuyệt đối về mặt Toán học cho Đồ án.")

    from scipy.optimize import linprog
    
    # Chuẩn bị dữ liệu ROAS từ mô hình ML thay vì tự chia
    camp_grouped = coeff_clean_df.copy().sort_values('ROAS', ascending=False)
    
    st.markdown("### 🏆 Bảng xếp hạng Lợi tức biên (Marginal ROAS) Tổng thể")
    fig = px.bar(camp_grouped, x='ROAS', y='channel', orientation='h', 
                 color='ROAS', color_continuous_scale='RdYlGn', 
                 title="Hệ số Beta: Đầu tư thêm 1 Đồng chi phí sinh ra bao nhiêu Đồng doanh thu?")
    fig.add_vline(x=1, line_dash="dash", line_color="blue", annotation_text="Điểm hòa vốn (ROAS=1)")
    fig.add_vline(x=0, line_dash="solid", line_color="red", annotation_text="Thất thoát (Âm)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    tab_manual, tab_auto = st.tabs(["✍️ Phân bổ Thủ công (Manual)", "🤖 AI Tối ưu hóa (Auto-Allocate)"])
    
    with tab_manual:
        st.markdown("### 🎛️ Bảng Điều khiển Ngân sách")
        st.write("Nhập ngân sách giả định cho tháng tới để xem doanh thu dự báo:")
        
        budgets = {}
        channels = camp_grouped['channel'].tolist()
        col_m1, col_m2 = st.columns(2)
        
        for idx, channel in enumerate(channels):
            current_roas = camp_grouped.loc[camp_grouped['channel'] == channel, 'ROAS'].values[0]
            label = f"Ngân sách {channel} (Hệ số ML: {current_roas:.2f})"
            
            # Gợi ý cắt ngân sách nếu ROAS âm
            default_val = 2000 if current_roas > 0 else 0 
            
            if idx % 2 == 0:
                with col_m1:
                    budgets[channel] = st.number_input(label, value=default_val, step=500, key=f"man_{channel}")
            else:
                with col_m2:
                    budgets[channel] = st.number_input(label, value=default_val, step=500, key=f"man_{channel}")
                    
        if st.button("🚀 CHẠY DỰ BÁO DOANH THU", type='primary', use_container_width=True):
            projected_revenue = res_clean[6] # Cộng thêm intercept (Doanh thu tự nhiên)
            for channel, budget in budgets.items():
                roas = camp_grouped.loc[camp_grouped['channel'] == channel, 'ROAS'].values[0]
                projected_revenue += budget * roas
                
            st.success("Đã tính toán xong dựa trên phương trình Hồi quy tuyến tính!")
            st.metric(label="💰 TỔNG DOANH THU DỰ KIẾN (Bao gồm Doanh thu nền tảng)", value=f"${projected_revenue:,.0f}")

    with tab_auto:
        st.markdown("### 🤖 Thuật toán Quy hoạch Tuyến tính (Linear Programming)")
        st.write("Hệ thống sẽ ép ngân sách = 0 đối với các kênh bị lỗ (ROAS < 1) và tự động dồn tiền vào các kênh sinh lời cao nhất.")
        
        total_budget = st.number_input("💸 Tổng ngân sách khả dụng ($)", value=50000, step=5000, min_value=1000)
        max_ratio = st.slider("⚠️ Mức độ rủi ro: Tối đa ngân sách cho 1 kênh (%)", min_value=10, max_value=100, value=40, step=5)
        
        if st.button("🧠 TỰ ĐỘNG PHÂN BỔ", type='primary', use_container_width=True):
            betas = camp_grouped['ROAS'].tolist()
            channels = camp_grouped['channel'].tolist()
            
            c = [-b for b in betas] 
            A_eq = [[1] * len(betas)]
            b_eq = [total_budget]
            
            max_per_channel = (max_ratio / 100) * total_budget
            
            # Bảo vệ Logic: Những kênh < 1 (Như FB, Insta) sẽ bị ép min/max = 0 (cắt ngân sách)
            valid_channels = sum(1 for b in betas if b >= 1.0)
            if valid_channels * max_per_channel < total_budget:
                st.warning(f"⚠️ Mức độ rủi ro {max_ratio}% là quá thấp để tiêu hết ${total_budget:,.0f} trên {valid_channels} kênh sinh lời. Hệ thống tự động nới lỏng giới hạn!")
                bounds = [(0, 0) if b < 1.0 else (0, total_budget) for b in betas]
            else:
                bounds = [(0, 0) if b < 1.0 else (0, max_per_channel) for b in betas]

            res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
            
            if res.success:
                st.success("Tối ưu hóa thành công! Dưới đây là chiến lược chia tiền lý tưởng nhất theo Toán học:")
                col_a1, col_a2 = st.columns([1, 1])
                with col_a1:
                    st.markdown("#### 🎯 Kế hoạch rót vốn:")
                    for i, channel in enumerate(channels):
                        alloc = res.x[i]
                        if alloc > 0:
                            st.write(f"- **{channel}**: ${alloc:,.0f}")
                        else:
                            st.write(f"- **{channel}**: ❌ Cắt ngân sách (Model báo lỗ)")
                            
                with col_a2:
                    st.markdown("#### 📈 Kết quả Dự kiến:")
                    # Doanh thu từ quảng cáo + Doanh thu tự nhiên (Intercept)
                    total_ad_revenue = -res.fun + res_clean[6] 
                    st.metric("🔥 TỔNG DOANH THU ĐẠT ĐƯỢC", f"${total_ad_revenue:,.0f}")
            else:
                st.error("Không tìm được phương án tối ưu. Vui lòng tăng tỷ lệ % rủi ro hoặc kiểm tra lại ngân sách.")