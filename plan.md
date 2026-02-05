# 📘 HƯỚNG DẪN CHI TIẾT: MÔ HÌNH ĐA HỒI QUY TUYẾN TÍNH

## 1. MỤC TIÊU CỦA MÔ HÌNH (OBJECTIVES)
Đa hồi quy tuyến tính là phương pháp thống kê mở rộng của hồi quy đơn, cho phép đánh giá mối quan hệ giữa một biến phụ thuộc ($Y$) với hai hay nhiều biến độc lập ($X$).

Trong các dự án phân tích dữ liệu (ví dụ: Marketing Analytics), mục tiêu chính bao gồm:

### 1.1. Dự báo (Prediction)
* **Mục đích:** Ước tính giá trị của biến phụ thuộc ($Y$) khi biết trước các thông tin của biến độc lập ($X$).
* **Ví dụ:** Dự báo doanh thu (`Revenue`) của tháng tới dựa trên ngân sách dự kiến chi cho Facebook, Google và lượt hiển thị (`Impressions`).

### 1.2. Giải thích và Định lượng tác động (Explanation)
* **Mục đích:** Hiểu rõ mức độ ảnh hưởng của từng yếu tố đến kết quả.
* **Ví dụ:**
    * Chi thêm 1 đồng cho Google Ads thì doanh thu tăng bao nhiêu đồng?
    * Yếu tố nào quan trọng hơn: Lượt nhấp (`Clicks`) hay Loại chiến dịch (`Campaign Type`)?

### 1.3. Đánh giá độ tin cậy và Tối ưu hóa (Optimization)
* **Mục đích:** Xác định xem các biến đầu vào có thực sự liên quan đến kết quả hay chỉ là ngẫu nhiên. Từ đó loại bỏ các yếu tố kém hiệu quả để tối ưu nguồn lực.

---

## 2. KIẾN THỨC VẬN DỤNG (THEORETICAL FRAMEWORK)

### 2.1. Phương trình toán học
Mô hình tổng quát có dạng:
$$Y = \beta_0 + \beta_1X_1 + \beta_2X_2 + ... + \beta_nX_n + \epsilon$$

* **$Y$ (Dependent Variable):** Biến phụ thuộc (VD: Doanh thu).
* **$X_1, X_2...$ (Independent Variables):** Các biến độc lập (VD: Chi phí, Kênh quảng cáo).
* **$\beta_0$ (Intercept):** Hệ số chặn (Giá trị của Y khi tất cả X = 0).
* **$\beta_1, \beta_2...$ (Coefficients):** Hệ số hồi quy riêng (Mức thay đổi của Y khi X tăng 1 đơn vị, giữ nguyên các biến khác).
* **$\epsilon$ (Error term):** Sai số ngẫu nhiên (Phần dư).

### 2.2. Phương pháp ước lượng (OLS)
Sử dụng phương pháp **Bình phương tối thiểu (Ordinary Least Squares - OLS)** để tìm ra đường hồi quy sao cho tổng bình phương sai số giữa giá trị thực tế và giá trị dự báo là nhỏ nhất.

### 2.3. Các giả định bắt buộc (Assumptions)
Để mô hình có ý nghĩa thống kê, dữ liệu phải thỏa mãn 5 giả định quan trọng:
1.  **Tính tuyến tính (Linearity):** Mối quan hệ giữa $X$ và $Y$ là tuyến tính.
2.  **Không có đa cộng tuyến (No Multicollinearity):** Các biến độc lập $X$ không được tương quan quá mạnh với nhau (VD: Không nên đưa cả `Số tiền giảm giá` và `% Giảm giá` vào cùng lúc).
3.  **Phương sai sai số đồng nhất (Homoscedasticity):** Sai số không thay đổi theo độ lớn của biến $X$.
4.  **Phân phối chuẩn của phần dư (Normality):** Phần dư phải tuân theo phân phối chuẩn.
5.  **Tính độc lập của sai số:** Các quan sát không ảnh hưởng lẫn nhau.

### 2.4. Các chỉ số đánh giá (Metrics)
* **$R^2$ (R-squared):** Cho biết mô hình giải thích được bao nhiêu % sự biến thiên của $Y$.
* **Adjusted $R^2$:** Dùng cho đa hồi quy, phạt mô hình khi thêm biến rác.
* **P-value:** Kiểm định ý nghĩa thống kê của từng biến (Thường yêu cầu P < 0.05).
* **VIF (Variance Inflation Factor):** Kiểm tra đa cộng tuyến (Yêu cầu VIF < 10, tốt nhất là < 5).

---

## 3. CÁCH LÀM & QUY TRÌNH THỰC HIỆN (METHODOLOGY)

Dưới đây là quy trình chuẩn 6 bước để thực hiện một bài toán Đa hồi quy tuyến tính:

### BƯỚC 1: Chuẩn bị và Làm sạch dữ liệu
* **Chọn biến:** Xác định biến mục tiêu ($Y$) và các biến nguyên nhân ($X$).
* **Xử lý dữ liệu:**
    * Loại bỏ dữ liệu khuyết (Missing values).
    * Xử lý giá trị ngoại lai (Outliers) có thể làm lệch mô hình.
* **Mã hóa biến phân loại (Encoding):**
    * Với các biến định tính (như `Channel`: Facebook, Google...), phải chuyển thành biến giả (Dummy Variables) dạng số (0 và 1) để đưa vào phương trình.

### BƯỚC 2: Phân tích khám phá (EDA)
* Vẽ biểu đồ phân tán (Scatter Plot) giữa từng $X$ và $Y$ để kiểm tra tính tuyến tính sơ bộ.
* Vẽ ma trận tương quan (Correlation Matrix) để phát hiện sớm các cặp biến bị đa cộng tuyến.

### BƯỚC 3: Chia tập dữ liệu (Train/Test Split)
* Chia dữ liệu thành 2 phần:
    * **Tập huấn luyện (Train set - 70% hoặc 80%):** Dùng để dạy mô hình học.
    * **Tập kiểm tra (Test set - 30% hoặc 20%):** Dùng để kiểm tra độ chính xác của mô hình trên dữ liệu mới chưa từng gặp.

### BƯỚC 4: Xây dựng mô hình
* Sử dụng các thư viện như `statsmodels` hoặc `scikit-learn` (Python) để chạy thuật toán OLS.
* Đưa dữ liệu Train vào để máy tính tìm ra các hệ số $\beta$.

### BƯỚC 5: Kiểm định và Tinh chỉnh
* **Đọc kết quả:** Xem bảng tóm tắt (Summary).
* **Loại biến xấu:** Loại bỏ các biến có **P-value > 0.05** (không có ý nghĩa thống kê).
* **Chạy lại mô hình:** Sau khi loại biến, chạy lại để xem $R^2$ có cải thiện không.
* **Kiểm tra giả định:** Vẽ biểu đồ phần dư (Residual Plot) và Q-Q Plot để đảm bảo các giả định ở mục 2.3 được thỏa mãn.

### BƯỚC 6: Biện luận và Báo cáo
* Viết phương trình hồi quy cuối cùng.
* Giải thích ý nghĩa kinh tế của các hệ số.
    * *Ví dụ:* "Hệ số của Facebook là 3.5, nghĩa là khi giữ nguyên các yếu tố khác, cứ tăng 1 đồng cho Facebook Ads thì doanh thu tăng 3.5 đồng."
* Đưa ra kiến nghị dựa trên kết quả (Tăng ngân sách cho kênh nào, cắt giảm kênh nào).

---

## 4. VÍ DỤ MINH HỌA (CASE STUDY: MARKETING MIX)
*Giả sử bạn áp dụng vào bộ dữ liệu Media của mình:*

* **Input:** Dữ liệu chi phí của Facebook, Google, Instagram và Doanh thu tổng.
* **Mô hình hồi quy:**
    $$DoanhThu = 1000 + 4.2 \times Cost_{Google} + 2.8 \times Cost_{Facebook} - 0.5 \times Cost_{Twitter}$$
* **Phân tích:**
    * Google hiệu quả nhất (Hệ số 4.2).
    * Twitter có hệ số âm (-0.5) hoặc P-value lớn $\rightarrow$ Kiến nghị dừng chạy quảng cáo Twitter.
    * $R^2 = 0.85$ $\rightarrow$ Mô hình giải thích được 85% biến động doanh thu, rất đáng tin cậy.