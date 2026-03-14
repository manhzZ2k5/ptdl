# CHƯƠNG 1: CƠ SỞ LÝ THUYẾT VÀ PHƯƠNG PHÁP NGHIÊN CỨU

Trong chương này, nhóm nghiên cứu chỉ tập trung trình bày các cơ sở lý thuyết toán học và thuật toán được lập trình trực tiếp trong hệ thống phân tích. Quá trình này bao gồm 4 giai đoạn cốt lõi: Tiền xử lý dữ liệu, Kiểm tra giả định, Huấn luyện mô hình và Tối ưu hóa thuật toán.

## 1.1. Tiền xử lý dữ liệu: Phương pháp Khoảng Tứ phân vị (IQR)
Trong bài toán hồi quy tuyến tính, các giá trị ngoại lai (Outliers) có thể làm sai lệch nghiêm trọng đường xu hướng (OLS). Nhóm nghiên cứu áp dụng phương pháp thống kê vững (robust statistics) là **Khoảng Tứ phân vị (IQR)** để tự động nhận diện và loại bỏ nhiễu.

- **Tứ phân vị (Quartiles):** Chia tập dữ liệu đã sắp xếp thành 4 phần bằng nhau. $Q_1$ (25%) và $Q_3$ (75%).
- **Khoảng IQR:** $IQR = Q_3 - Q_1$.
- **Cận ranh giới:** Điểm dữ liệu được coi là ngoại lai nếu nhỏ hơn Cận dưới ($Q_1 - 1.5 \times IQR$) hoặc lớn hơn Cận trên ($Q_3 + 1.5 \times IQR$).



[Image of box plot with IQR and outliers]


## 1.2. Phân tích đa cộng tuyến (Multicollinearity) bằng VIF
Để các hệ số hồi quy (đại diện cho Lợi tức quảng cáo - ROAS của từng kênh) có ý nghĩa và độc lập, các kênh quảng cáo không được phép có sự tương quan tuyến tính mạnh với nhau. Nhóm sử dụng **Hệ số Phóng đại Phương sai (VIF)** để kiểm định điều kiện này:

$$VIF_i = \frac{1}{1 - R_i^2}$$
*(Trong đó, $R_i^2$ là hệ số xác định khi hồi quy biến độc lập thứ $i$ theo các biến độc lập còn lại).*
- **Tiêu chuẩn đánh giá:** Nếu $VIF < 10$, mức độ đa cộng tuyến ở ngưỡng an toàn, các biến đủ tiêu chuẩn đưa vào mô hình máy học.

## 1.3. Mô hình Đa hồi quy tuyến tính (Multiple Linear Regression)
Mô hình Đa hồi quy tuyến tính được sử dụng để định lượng tác động đồng thời của chi phí trên nhiều kênh Marketing ($X$) lên Tổng doanh thu ($Y$).

**1. Phương trình Hồi quy tổng quát:**
$$Y = \beta_0 + \beta_1X_1 + \beta_2X_2 + \dots + \beta_nX_n + \epsilon$$
Trong đó, $\beta_i$ chính là Tỷ suất lợi tức biên (Marginal ROAS) của kênh quảng cáo thứ $i$. Thuật toán **Bình phương tối thiểu (OLS)** được sử dụng để tìm ra các hệ số $\beta$ sao cho tổng bình phương phần dư (sai số) là nhỏ nhất.

**2. Đánh giá độ vặn vẹo của mô hình:**
Nhóm sử dụng 3 chỉ số từ thư viện `scikit-learn` để đo lường độ chính xác dự báo:
- **$R^2$ (Hệ số xác định):** Đo lường tỷ lệ biến thiên của Doanh thu được giải thích bởi Chi phí.
- **MAE (Sai số tuyệt đối trung bình):** Trung bình của các sai số dự báo tính bằng giá trị tuyệt đối.
- **RMSE (Sai số toàn phương trung bình gốc):** Căn bậc hai của trung bình bình phương sai số, giúp phạt nặng các dự báo có sai lệch lớn.

## 1.4. Kiểm định Thống kê mô hình (Hypothesis Testing)
Bên cạnh đánh giá sai số, nhóm sử dụng thư viện `statsmodels` để kiểm định tính chặt chẽ của mô hình về mặt thống kê suy diễn:
- **Kiểm định F (F-test):** Kiểm tra độ phù hợp của toàn bộ mô hình. Nếu $P\text{-value (F-statistic)} < 0.05$, mô hình thực sự có ý nghĩa thống kê (tồn tại ít nhất một kênh tác động đến doanh thu).
- **Kiểm định t (t-test):** Đánh giá ý nghĩa của từng hệ số $\beta_i$. Nếu $P\text{-value} < 0.05$, kênh quảng cáo đó mang lại hiệu quả thực sự. Nếu $P\text{-value} \ge 0.05$, kênh đó không có tác động rõ rệt và bị thuật toán coi là không hiệu quả.

## 1.5. Thuật toán Quy hoạch tuyến tính (Linear Programming)
Để nâng cấp từ việc "Dự báo" lên "Ra quyết định tối ưu", nhóm ứng dụng thuật toán Quy hoạch tuyến tính (`scipy.optimize.linprog`) để tự động phân bổ ngân sách.

- **Hàm mục tiêu (Objective Function):** Tối đa hóa (Maximize) Tổng doanh thu dự kiến.
  $$Max\ Z = \sum (\beta_i \times X_i)$$
- **Hệ phương trình Ràng buộc (Constraints):**
  1. $\sum X_i \le \text{Tổng Ngân sách}$ (Giới hạn tài nguyên).
  2. $X_i \le \text{Hạn mức rủi ro tối đa}$ (Không dồn quá nhiều tiền vào một kênh để tránh hiện tượng Lợi suất giảm dần).
  3. $X_i = 0$ nếu hệ số $\beta_i < 1$ (Cơ chế cắt lỗ tự động: Không cấp ngân sách cho các kênh làm ăn thua lỗ).