# 🎓 ĐỒ ÁN: TỐI ƯU HÓA NGÂN SÁCH DIGITAL MARKETING ĐA KÊNH
**Phương pháp: Mô hình Đa hồi quy Tuyến tính (Multiple Linear Regression)**

---

## 1. TỔNG QUAN DỮ LIỆU (DATA METADATA)
**File nguồn:** `media_all_channels.csv`

### 1.1. Biến Mục tiêu ($Y$ - Target Variable)
* **`Revenue`**: Doanh thu bán hàng (Biến phụ thuộc chính).
* *(Biến thay thế: `Conversions` - Số lượng đơn hàng, nếu muốn chạy mô hình phụ).*

### 1.2. Biến Nguyên nhân ($X$ - Independent Variables)
* **`Cost`**: Chi phí quảng cáo (Ngân sách đã chi).
* **`Impressions`**: Số lượt hiển thị (Độ phủ thương hiệu).
* **`Channel`**: Kênh quảng cáo (Facebook, Google, Instagram, LinkedIn, Twitter, Website).
* **`Campaign`**: Loại chiến dịch (Flash Sale, New Arrivals, Best Sellers...).

### 1.3. Lưu ý Quan trọng
* **Loại bỏ:** Các biến phái sinh (`ROAS`, `ROI`, `CTR`, `CPC`...) phải bị loại bỏ khỏi mô hình để tránh lỗi Rò rỉ dữ liệu (Data Leakage).
* **Xử lý:** Cần chuyển đổi `Channel` và `Campaign` thành dạng số (Dummy Encoding) trước khi chạy.

---

## 2. YÊU CẦU & MỤC TIÊU NGHIÊN CỨU

### 2.1. Mục tiêu Cơ bản (Basic Objectives)
1.  Xác định phương trình hồi quy tuyến tính: $Revenue = f(Cost, Channel, ...)$.
2.  So sánh hiệu quả đầu tư (ROI) giữa các kênh: "1 đồng chi cho Facebook mang lại bao nhiêu đồng doanh thu so với Google?".
3.  Kiểm định giả thiết thống kê: Loại bỏ các kênh không có ý nghĩa đóng góp vào doanh thu (P-value > 0.05).

### 2.2. Mục tiêu Nâng cao (Academic Enhancements)
*Để tăng tính học thuật và chiều sâu phân tích:*
1.  **Phát hiện quy luật Lợi suất giảm dần (Diminishing Returns):** Tìm điểm bão hòa chi tiêu.
2.  **Phân tích Hiệu ứng trễ (Carryover Effects):** Quảng cáo hôm nay có tác động đến ngày mai không?
3.  **Phân tích Mùa vụ (Seasonality):** Tách bạch tác động của ngày lễ/cuối tuần khỏi hiệu quả quảng cáo.

---

## 3. ĐỀ XUẤT BỔ SUNG DỮ LIỆU ĐỂ TĂNG TÍNH HỌC THUẬT
*Nếu bạn muốn thuật toán "xịn" hơn và bài báo cáo có sức nặng hơn, hãy cân nhắc thêm các trường dữ liệu sau (có thể tự tạo hoặc tìm thêm):*

### 3.1. Nhóm biến tự tạo từ dữ liệu có sẵn (Feature Engineering)
*(Không cần tìm dữ liệu mới, chỉ cần dùng code để tạo ra)*

* **Biến `Is_Weekend` (Cuối tuần):**
    * *Lý do:* Hành vi mua sắm cuối tuần thường khác ngày thường. Biến này giúp mô hình không bị nhầm lẫn giữa "hiệu quả quảng cáo" và "thói quen mua sắm".
    * *Cách làm:* Từ cột `date`, tạo cột mới: 1 nếu là T7/CN, 0 nếu là ngày thường.
* **Biến `Lagged_Cost` (Chi phí trễ):**
    * *Lý do:* Khách hàng thường không mua ngay khi thấy quảng cáo. Hiệu quả hôm nay có thể do tiền chi từ 2 ngày trước.
    * *Cách làm:* Tạo cột `Cost_Lag_1` (Chi phí của ngày hôm qua), `Cost_Lag_3` (Chi phí của 3 ngày trước).
* **Biến `Interaction` (Tương tác):**
    * *Lý do:* Để xem xét sự kết hợp. Ví dụ: Chiến dịch "Flash Sale" có thể rất tốt trên Facebook nhưng tệ trên LinkedIn.
    * *Cách làm:* Tạo cột mới = `Cost` * `Channel_Facebook`.

### 3.2. Nhóm biến bổ sung từ bên ngoài (External Factors) - *Rất khuyến khích*
*(Nếu thêm được các biến này, bài làm sẽ được đánh giá cực cao về tư duy thực tế)*

* **Biến `Google_Trends_Index` (Chỉ số xu hướng):**
    * *Ý nghĩa:* Thể hiện mức độ quan tâm tự nhiên của thị trường đối với thương hiệu hoặc ngành hàng (Ví dụ: Từ khóa "giày thể thao").
    * *Tác dụng:* Giúp tách bạch "Doanh thu tăng do thị trường đang hot" hay "Doanh thu tăng do quảng cáo giỏi".
* **Biến `Holiday_Flag` (Ngày lễ tết):**
    * *Ý nghĩa:* Các ngày như Black Friday, Valentine, Tết...
    * *Tác dụng:* Kiểm soát tính mùa vụ cực mạnh (Seasonality Control).
* **Biến `Competitor_Intensity` (Giả định):**
    * *Ý nghĩa:* Mức độ cạnh tranh (Ví dụ: Số lượng đối thủ đang chạy quảng cáo cùng thời điểm). Biến này khó kiếm, có thể giả định hoặc bỏ qua.

---

## 4. QUY TRÌNH THỰC HIỆN CHI TIẾT (WORKFLOW)

### Giai đoạn 1: Chuẩn bị Dữ liệu (Data Preparation)
1.  Load dữ liệu & Làm sạch (Cleaning).
2.  **Feature Engineering (Quan trọng):** Tạo các biến `Is_Weekend`, `Lagged_Cost` như mục 3.1.
3.  Mã hóa biến giả (One-Hot Encoding) cho `Channel` và `Campaign`.

### Giai đoạn 2: Phân tích Khám phá (EDA)
1.  Vẽ biểu đồ tương quan (Heatmap) để kiểm tra Đa cộng tuyến.
2.  Vẽ biểu đồ phân tán (Scatter Plot) giữa Cost và Revenue để xem có nên dùng hàm phi tuyến ($Cost^2$) không.

### Giai đoạn 3: Xây dựng & Kiểm định Mô hình
1.  **Mô hình 1 (Base Model):** Hồi quy tuyến tính cơ bản.
    * $Y = Cost + Channel + Campaign$
2.  **Mô hình 2 (Advanced Model):** Thêm biến tương tác và biến trễ.
    * $Y = Cost + Channel + Cost\_Lag1 + Is\_Weekend + (Cost \times Channel)$
3.  **So sánh:** Dùng chỉ số $R^2$ hiệu chỉnh (Adjusted R-squared) để chứng minh Mô hình 2 tốt hơn Mô hình 1.

### Giai đoạn 4: Kiến nghị Quản trị (Optimization)
1.  Dựa vào hệ số $\beta$ của Mô hình 2 để đề xuất phân bổ ngân sách.
2.  Ví dụ: "Kết quả cho thấy chi phí ngày hôm qua (`Lag_1`) có tác động dương mạnh, chứng tỏ cần duy trì quảng cáo liên tục thay vì ngắt quãng."

---

## 5. CÔNG CỤ THỰC HIỆN
* **Ngôn ngữ:** Python.
* **Thư viện:**
    * `Pandas`: Xử lý dữ liệu.
    * `Statsmodels`: Chạy hồi quy và xuất báo cáo thống kê chuyên sâu (P-value, t-test).
    * `Seaborn/Matplotlib/Streamlit`: Vẽ biểu đồ.