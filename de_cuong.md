# ĐỀ TÀI: TỐI ƯU HÓA NGÂN SÁCH DIGITAL MARKETING ĐA KÊNH: PHÂN TÍCH TÁC ĐỘNG CỦA GOOGLE ADS VÀ MẠNG XÃ HỘI ĐẾN DOANH THU BẰNG MÔ HÌNH ĐA HỒI QUY TUYẾN TÍNH

---

## CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI (GIỚI THIỆU)

**1.1. Lý do chọn đề tài**
* Sự bùng nổ của Digital Marketing và áp lực tối ưu chi phí trong doanh nghiệp hiện đại.
* **Vấn đề thực tế:** Doanh nghiệp chi tiền cho nhiều kênh (Facebook, Google, Twitter, Instagram...) nhưng thiếu cơ sở định lượng để biết chính xác kênh nào mang lại hiệu quả doanh thu cao nhất (ROI).
* Sự cần thiết của việc chuyển dịch từ ra quyết định dựa trên cảm tính sang ra quyết định dựa trên dữ liệu (Data-driven decision making).

**1.2. Mục tiêu nghiên cứu**
* Xác định các yếu tố tiếp thị ảnh hưởng đến doanh thu (Chi phí quảng cáo, Lượt hiển thị, Loại kênh, Loại chiến dịch).
* Đo lường và so sánh mức độ tác động (Hệ số hồi quy) của từng kênh quảng cáo đối với doanh thu bán hàng.
* Đề xuất phương án phân bổ ngân sách tối ưu dựa trên kết quả phân tích thống kê.

**1.3. Đối tượng và Phạm vi nghiên cứu**
* **Dữ liệu:** Bộ "Media Dataset" (Dữ liệu thứ cấp mô phỏng chiến dịch Marketing đa kênh).
* **Phạm vi thời gian:** Dữ liệu ghi nhận trong giai đoạn [Năm X - Năm Y].
* **Phương pháp nghiên cứu:** Phân tích thống kê mô tả và Mô hình Đa hồi quy tuyến tính (Multiple Linear Regression - OLS).

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ PHƯƠNG PHÁP NGHIÊN CỨU

**2.1. Tổng quan về Digital Marketing**
* Các chỉ số đo lường hiệu quả: Impressions (Lượt hiển thị), Clicks (Lượt nhấp), CTR (Tỷ lệ nhấp), Conversion (Chuyển đổi), Cost (Chi phí), Revenue (Doanh thu).
* Đặc điểm của các kênh quảng cáo chính: Search Ads (Google), Social Ads (Facebook, Instagram, LinkedIn), Influencer Marketing.

**2.2. Mô hình Đa hồi quy tuyến tính (Multiple Linear Regression)**
* **Khái niệm:** Phương pháp thống kê dùng để mô hình hóa mối quan hệ giữa một biến phụ thuộc với hai hay nhiều biến độc lập.
* **Phương trình tổng quát:** $$Y = \beta_0 + \beta_1X_1 + \beta_2X_2 + ... + \beta_kX_k + \epsilon$$
* **Phương pháp ước lượng:** Bình phương tối thiểu (Ordinary Least Squares - OLS).
* **Các giả định bắt buộc (Assumptions):**
    1.  Tính tuyến tính (Linearity).
    2.  Không có đa cộng tuyến (No Multicollinearity).
    3.  Phương sai sai số đồng nhất (Homoscedasticity).
    4.  Phân phối chuẩn của phần dư (Normality of Residuals).
    5.  Tính độc lập của sai số (Independence of Errors).

**2.3. Quy trình kiểm định thống kê**
* Kiểm định ý nghĩa của từng hệ số hồi quy (t-test, p-value).
* Đánh giá độ phù hợp của toàn bộ mô hình (R-squared, Adjusted R-squared, F-test).

---

## CHƯƠNG 3: MÔ TẢ VÀ XỬ LÝ DỮ LIỆU

**3.1. Giới thiệu bộ dữ liệu**
* Nguồn gốc dữ liệu và kích thước mẫu ($n$ quan sát).
* **Biến phụ thuộc ($Y$):** `Revenue` (Doanh thu bán hàng).
* **Biến độc lập ($X$):**
    * Biến định lượng: `Cost` (Chi phí), `Impressions` (Lượt hiển thị), `Clicks` (Lượt nhấp).
    * Biến định tính: `Channel` (Kênh quảng cáo), `Campaign Type` (Loại chiến dịch).

**3.2. Làm sạch dữ liệu (Data Cleaning)**
* Kiểm tra và xử lý dữ liệu khuyết (Missing values).
* Phát hiện và xử lý giá trị ngoại lai (Outliers) bằng phương pháp IQR hoặc Boxplot.

**3.3. Mã hóa dữ liệu (Feature Engineering)**
* Tạo biến giả (Dummy Variables) cho biến định tính `Channel` và `Campaign Type`.
    * *Ví dụ:* Chuyển cột `Channel` thành các cột nhị phân: `Is_Facebook`, `Is_Google`, `Is_Twitter` (0/1).

**3.4. Thống kê mô tả (Descriptive Statistics)**
* Bảng thống kê tóm tắt: Mean, Median, Std. Dev, Min, Max của Doanh thu và Chi phí quảng cáo.
* **Trực quan hóa dữ liệu (Data Visualization):**
    * Biểu đồ cột (Bar Chart): So sánh tổng doanh thu và chi phí trung bình theo từng kênh.
    * Biểu đồ phân tán (Scatter Plot): Quan sát mối quan hệ tuyến tính giữa `Cost` và `Revenue`.
    * Ma trận tương quan (Correlation Matrix): Kiểm tra sơ bộ mức độ tương quan giữa các biến số (`Cost`, `Impressions`, `Clicks`, `Revenue`).

---

## CHƯƠNG 4: KẾT QUẢ NGHIÊN CỨU VÀ THẢO LUẬN

**4.1. Xây dựng mô hình hồi quy**
* **Mô hình cơ sở:** Hồi quy đơn biến giữa Tổng chi phí và Doanh thu.
* **Mô hình mở rộng (Đa biến):** Đưa thêm các biến `Impressions` và các biến giả `Channel` vào phương trình.
    * *Phương trình ước lượng:* $Revenue = \beta_0 + \beta_1(Cost) + \beta_2(Is\_Facebook) + \beta_3(Is\_Google) + ... + \epsilon$

**4.2. Kiểm định và Lựa chọn mô hình tối ưu**
* **Kiểm tra đa cộng tuyến (VIF):** Loại bỏ các biến có hệ số VIF > 5 hoặc 10 (ví dụ: `Impressions` và `Clicks` thường tương quan mạnh, cần chọn 1).
* **Kiểm định giả thiết thống kê (P-value):**
    * Giữ lại các biến có ý nghĩa thống kê ($P < 0.05$).
    * Loại bỏ các biến không có ý nghĩa thống kê ($P > 0.05$) – Kết luận sơ bộ về sự không hiệu quả của các kênh/yếu tố này.
* **Đánh giá độ phù hợp:** Sử dụng hệ số $R^2$ hiệu chỉnh (Adjusted R-squared) để kết luận mô hình giải thích được bao nhiêu % sự biến thiên của doanh thu.

**4.3. Kiểm tra các giả định của mô hình (Diagnostic Plots)**
* Phân tích biểu đồ phần dư (Residuals vs Fitted) để kiểm tra phương sai đồng nhất.
* Biểu đồ Q-Q Plot để kiểm tra phân phối chuẩn của phần dư.

**4.4. Thảo luận kết quả (Biện luận chi tiết)**
* **Phân tích hệ số hồi quy chuẩn hóa (Standardized Beta):** So sánh tầm quan trọng của các kênh. (Ví dụ: "Hệ số Beta của Google Ads lớn gấp 1.5 lần Facebook Ads...").
* **Hiệu quả theo loại chiến dịch:** Phân tích xem các chiến dịch như "Awareness" hay "Conversion" có tác động khác biệt thế nào đến doanh thu.

---

## CHƯƠNG 5: KIẾN NGHỊ VÀ KẾT LUẬN

**5.1. Kiến nghị quản trị (Tối ưu hóa ngân sách)**
* **Chiến lược tăng trưởng:** Đề xuất dồn ngân sách cho các kênh có hệ số hồi quy dương lớn nhất.
* **Chiến lược cắt giảm:** Đề xuất dừng hoặc xem xét lại nội dung cho các kênh có P-value không đạt yêu cầu.
* Gợi ý chiến lược phối hợp đa kênh (Cross-channel strategy).

**5.2. Hạn chế của đề tài và Hướng phát triển**
* Hạn chế về dữ liệu (thiếu yếu tố mùa vụ, kinh tế vĩ mô, đối thủ cạnh tranh).
* Hạn chế về mô hình (mối quan hệ thực tế có thể phi tuyến tính).

**5.3. Kết luận**
* Tóm tắt lại các phát hiện chính và đóng góp của bài nghiên cứu.

---

## TÀI LIỆU THAM KHẢO
1.  [Tên giáo trình Xác suất thống kê/Phân tích dữ liệu đang học]
2.  Dataset: Media Marketing Dataset (Kaggle/Mastering-DA).
3.  Hair, J. F., et al. (2010). *Multivariate Data Analysis*.