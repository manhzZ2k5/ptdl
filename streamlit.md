# 📱 KỊCH BẢN THIẾT KẾ DATA APP: TỐI ƯU HÓA NGÂN SÁCH MARKETING

**Mục tiêu App:** Chuyển đổi file phân tích Jupyter Notebook thành một Web App tương tác (Data Storytelling). Ứng dụng này phục vụ cho việc trình bày dự án (Presentation) trước Hội đồng môn học hoặc Nhà tuyển dụng vị trí Data Analyst / IT BA.

**Cấu trúc Điều hướng (Sidebar Menu):** Hệ thống được chia thành 6 trang (Pages) theo đúng luồng tư duy phân tích: từ Hiểu bài toán $\rightarrow$ Xử lý Dữ liệu $\rightarrow$ Xây dựng Mô hình $\rightarrow$ Ứng dụng Thực tế.

---

## 📄 TRANG 1: TỔNG QUAN DỰ ÁN (Project Overview)
**Mục tiêu:** Giới thiệu nhanh bối cảnh, quy mô dữ liệu và bài toán kinh doanh.

* **Tiêu đề (`st.title`):** 📊 Tối ưu hóa Ngân sách Digital Marketing Đa Kênh.
* **Tóm tắt bài toán (`st.info`):** * *Vấn đề:* Phân bổ ngân sách Marketing đang dựa trên cảm tính.
  * *Giải pháp:* Ứng dụng Đa hồi quy tuyến tính (Multiple Linear Regression) để tính toán Lợi tức biên (Marginal ROI) của từng kênh.
* **Chỉ số Tổng quan (`st.columns` & `st.metric`):** Hiển thị 3 thẻ số liệu lớn:
  1. Tổng số quan sát: 7,644 dòng.
  2. Tổng ngân sách đã chi ($).
  3. Tổng doanh thu đã tạo ra ($).
* **Bảng Dữ liệu (`st.dataframe`):** Hiển thị 5 dòng đầu tiên của dữ liệu gốc (`df.head()`) để người xem hình dung cấu trúc dữ liệu thô.

---

## 📄 TRANG 2: GIẢI MÃ CHIẾN LƯỢC MARKETING (Marketing Psychology)
**Mục tiêu:** Thể hiện tư duy nghiệp vụ (Business Domain Knowledge) bằng cách giải mã 7 loại chiến dịch trong dữ liệu.

* **Mô tả (`st.markdown`):** Giải thích rằng dữ liệu không chỉ là con số, mà đại diện cho hành vi tâm lý của khách hàng.
* **Phân nhóm Chiến lược (`st.tabs`):** Chia làm 4 Tabs:
  * *Tab 1 - Hiệu ứng Đám đông:* Chiến dịch Best Sellers, Trending Now.
  * *Tab 2 - Sự Khan hiếm/FOMO:* Chiến dịch Flash Sale, Limited Edition.
  * *Tab 3 - Tính Độc quyền:* Chiến dịch Exclusive Offers.
  * *Tab 4 - Sự Mới mẻ:* Chiến dịch New Arrivals, Must-Haves.
* **Biểu đồ Tần suất (`st.plotly_chart`):** Vẽ Horizontal Bar Chart thể hiện số lần từng chiến dịch được chạy trong năm.

---

## 📄 TRANG 3: LÀM SẠCH & KHÁM PHÁ DỮ LIỆU (EDA)
**Mục tiêu:** Trình bày kỹ thuật làm sạch dữ liệu và xử lý giá trị ngoại lai (Outliers).

* **Giải thích phương pháp (`st.expander`):** Giải thích ngắn gọn thuật toán IQR được sử dụng để lọc Outlier cho biến Cost và Revenue.
* **So sánh Trực quan (`st.columns` & `st.pyplot`):** * *Cột trái:* Boxplot của biến Cost TRƯỚC khi xử lý (hiện rõ các điểm dị biệt).
  * *Cột phải:* Boxplot của biến Cost SAU khi xử lý bằng IQR (sạch sẽ, chuẩn bị đưa vào mô hình).
* **Kiểm tra Đa cộng tuyến (`st.pyplot`):** Hiển thị Heatmap tương quan giữa các biến chi phí. 
* **Kết luận (`st.success`):** "Hệ số tương quan thấp và VIF < 10 chứng tỏ các kênh quảng cáo độc lập với nhau, đạt chuẩn chạy hồi quy."

---

## 📄 TRANG 4: ĐÁNH GIÁ MÔ HÌNH HỒI QUY (Model Evaluation)
**Mục tiêu:** Khoe kỹ năng Machine Learning/Thống kê và tính minh bạch của thuật toán cốt lõi.

* **Bảng So sánh Mô hình (`st.table`):** Đặt "Mô hình Gốc" và "Mô hình Sạch" cạnh nhau. Hiển thị rõ các chỉ số: $R^2$, MAE, RMSE để chứng minh việc làm sạch dữ liệu ở Trang 3 đã giúp mô hình chính xác hơn.
* **Biểu đồ Phần dư (`st.columns` & `st.pyplot`):**
  * *Cột trái:* Biểu đồ Histogram phân phối phần dư (Residuals Distribution) - Thể hiện dáng chuông chuẩn.
  * *Cột phải:* Scatter Plot giữa Giá trị dự báo (Predicted) và Phần dư (Residuals).

---

## 📄 TRANG 5: PHÂN TÍCH CHUYÊN SÂU KÊNH & CHIẾN DỊCH (Deep-Dive)
**Mục tiêu:** Đi tìm "Viên ngọc ẩn" - Kênh nào chạy chiến dịch nào là tốt nhất?

* **Bản đồ Nhiệt Tổng hợp (`st.pyplot`):** Hiển thị Heatmap giao thoa giữa 6 Kênh (Cột) và 7 Chiến dịch (Hàng). Ô màu xanh đậm là cặp mang lại ROAS (Return On Ad Spend) cao nhất.
* **Bộ lọc Chi tiết (`st.selectbox`):** Cho phép người dùng chọn 1 Chiến dịch cụ thể (Ví dụ: Flash Sale).
* **Biểu đồ Xếp hạng Động (`st.pyplot`):** Khi người dùng chọn chiến dịch ở trên, tự động vẽ Bar Chart nằm ngang sắp xếp các kênh từ Tệ Nhất (Đỏ) đến Tốt Nhất (Xanh) cho chiến dịch đó.
* **Đường Hòa Vốn (`axvline`):** Vẽ một vạch đỏ tại ROAS = 1. Cảnh báo sếp cắt ngay ngân sách của những thanh không vượt qua được vạch này.

---

## 📄 TRANG 6: TRÌNH GIẢ LẬP NGÂN SÁCH (Budget Simulator) 🌟
**Mục tiêu:** Tính năng "ăn tiền" nhất, biến thuật toán thành công cụ ra quyết định thực tế cho Doanh nghiệp.

* **Bảng xếp hạng Lợi tức biên (`st.bar_chart`):** Trực quan hóa hệ số $\beta$ của 6 kênh (Được trích xuất từ mô hình hồi quy).
* **Khu vực Giả lập (`st.container`):** Tạo 6 thanh kéo (`st.slider`) hoặc ô nhập số (`st.number_input`) để sếp thử "rót tiền" vào từng kênh (Ví dụ: Nhập $10,000 cho Facebook, $5,000 cho Google).
* **Dự báo Kết quả (`st.button` & `st.metric`):** * Khi bấm nút "🚀 Chạy Dự Báo", hệ thống lấy số tiền vừa nhập nhân với hệ số $\beta$ tương ứng.
  * Xuất ra màn hình thẻ số khổng lồ: **"💰 TỔNG DOANH THU DỰ KIẾN: $XXX,XXX"**.