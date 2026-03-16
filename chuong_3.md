# CHƯƠNG 3: XÂY DỰNG MÔ HÌNH VÀ KIỂM ĐỊNH THỐNG KÊ

Chương này trình bày quá trình huấn luyện thuật toán Đa hồi quy tuyến tính (Multiple Linear Regression) trên tập dữ liệu đã làm sạch. Mục tiêu là tìm ra phương trình tác động biên của các kênh quảng cáo đến doanh thu, sử dụng các phép kiểm định thống kê để đảm bảo độ tin cậy của kết quả, đồng thời bóc tách nguyên nhân gây nhiễu từ góc độ kinh doanh.

## 3.1. Đánh giá sai số và Lựa chọn mô hình
*(Trình bày kết quả huấn luyện từ thư viện `scikit-learn` để đánh giá hiệu quả của phương pháp Capping ở Chương 2)*

- **Thiết lập huấn luyện:** Tập dữ liệu được chia theo tỷ lệ 80% (Train) để máy học các hệ số và 20% (Test) để kiểm thử sai số thực tế trên dữ liệu chưa từng thấy, với `random_state` cố định nhằm đảm bảo tính tái lập.
- **Bảng so sánh hiệu suất:** *(Chèn bảng kết quả so sánh R², MAE, RMSE của Mô hình gốc và Mô hình sạch)*
- **Biện luận lựa chọn:** Dựa vào kết quả, ta thấy **Mô hình Sạch** (đã áp dụng Capping/Winsorization bằng IQR) cho ra sai số RMSE và MAE thấp hơn hẳn so với Mô hình Gốc. Bằng cách không xóa bỏ mà chỉ "kéo" các điểm dị biệt về ngưỡng an toàn, ta đã giữ được cấu trúc tuyến tính của dữ liệu, giúp mô hình không bị vặn vẹo và cứu chỉ số R² khỏi việc bị âm (suy thoái). Do đó, nhóm quyết định sử dụng **Mô hình Sạch** làm cơ sở phân tích chính thức.
> *[Note: Lấy bảng kết quả in ra từ Cell 17 - So sánh kết quả mô hình trong Jupyter Notebook]*


## 3.2. Kiểm định ý nghĩa thống kê của mô hình (OLS Summary)
*(Sử dụng thư viện `statsmodels` để thực hiện suy diễn thống kê, đảm bảo các kết quả tìm được không phải do ngẫu nhiên)*

- **Bảng tóm tắt hồi quy (OLS Regression Results):**
  *(Chụp ảnh và chèn toàn bộ bảng Summary của thư viện statsmodels vào đây)*

- **Đánh giá độ phù hợp toàn cục (Kiểm định F):**
  Nhìn vào góc phải trên cùng của bảng, chỉ số `Prob (F-statistic)` có giá trị rất nhỏ và < 0.05. Do đó, ta bác bỏ giả thuyết H₀, khẳng định phương trình Đa hồi quy tuyến tính tổng thể có ý nghĩa thống kê. Ngân sách quảng cáo thực sự có tác động đến việc tạo ra doanh thu.

- **Đánh giá ý nghĩa cục bộ (Kiểm định t):**
  Kiểm tra cột `P>|t|` (P-value) đối với từng kênh quảng cáo:
  - **Các kênh có ý nghĩa:** Kênh *(Liệt kê tên các kênh có P-value < 0.05, ví dụ: Website, Twitter...)* có P-value < 0.05, chứng tỏ chi phí đổ vào các nền tảng này thực sự tạo ra sự thay đổi về doanh thu.
  - **Các kênh không có ý nghĩa:** Kênh *(Liệt kê kênh có P-value > 0.05, ví dụ: Facebook...)* có P-value > 0.05, nghĩa là hệ số tác động của kênh này không khác biệt so với 0 về mặt thống kê. Việc chi tiền cho nền tảng này đang mang tính ngẫu nhiên, không tạo ra luồng tiền ổn định.
> *[Note: Lấy hình ảnh từ Cell 18 - Phân Tích Hồi Quy Chuyên Sâu bằng Statsmodels OLS]*


## 3.3. Kiểm tra các giả định của phần dư (Residual Diagnostics)
*(Chứng minh mô hình OLS hợp lệ, không vi phạm các giả định toán học)*

- **Kiểm tra giả định phân phối chuẩn:** *(Chèn biểu đồ Histogram phần dư)*
  **Nhận xét:** Biểu đồ Histogram của phần dư có dáng hình chuông, phân bố đối xứng quanh giá trị 0, thỏa mãn giả định sai số ngẫu nhiên tuân theo phân phối chuẩn.
  
- **Kiểm tra phương sai sai số không đổi (Homoscedasticity):** *(Chèn biểu đồ Scatter Phần dư vs Giá trị dự đoán)*
  **Nhận xét:** Các điểm dữ liệu phân tán ngẫu nhiên quanh trục hoành (0), không tạo thành các mô hình dạng phễu (funnel) hay đường cong. Điều này chứng tỏ phương sai của phần dư là đồng đều.
> *[Note: Lấy 2 hình ảnh biểu đồ từ Cell 19 - Phân tích phần dư]*


## 3.4. Phân tích mở rộng: Nguyên nhân R-squared thấp và Tính hợp lệ của mô hình
*(Giải thích sự thật về dữ liệu: Tại sao R² chỉ ở mức ~2.65% và tại sao mô hình vẫn dùng được)*

- **Đánh giá yếu tố gây nhiễu từ Nội dung chiến dịch (Campaign):**
  *(Chèn biểu đồ Barplot: Hiệu quả theo Chiến dịch - ROAS vs Conversion Rate)*
- **Biện luận góc độ kinh doanh:** Mô hình hiện tại chỉ giải thích được khoảng 2.65% sự biến thiên của doanh thu. Biểu đồ bóc tách theo Campaign cho thấy lý do: Doanh thu tạo ra không chỉ phụ thuộc vào việc "Bơm bao nhiêu tiền" (Cost), mà còn phụ thuộc rất lớn vào "Nội dung truyền thông là gì". Ví dụ, các đợt *Flash Sale* có Tỷ lệ chốt đơn (CR) và ROAS cao đột biến bất chấp chi phí. 
- **Kết luận tính hợp lệ:** Vì mô hình không chứa biến số về "Nội dung Campaign", việc không dự báo được tổng doanh thu chính xác là điều tất yếu. Tuy nhiên, bài toán đặt ra không phải là dự báo tổng, mà là **Tối ưu hóa ngân sách**. Các hệ số Beta (β) bóc tách từ mô hình vẫn hoàn toàn tin cậy để so sánh hiệu quả biên giữa các kênh.
> *[Note: Lấy biểu đồ và thông tin từ Cell 20 - Biện luận lý do R-squared thấp]*


## 3.5. Bóc tách Tỷ suất Lợi tức quảng cáo biên (Marginal ROAS)
*(Dịch các hệ số Beta từ toán học sang ngôn ngữ kinh doanh để chuẩn bị cho bài toán tối ưu hóa)*

- **Bảng xếp hạng Tác động biên:**
  *(Chèn bảng xếp hạng các Hệ số Beta/ROAS của các kênh từ cao xuống thấp cùng Khoảng tin cậy 95%)*

- **Giải thích ý nghĩa kinh tế:** - **Hệ số chặn (Intercept):** Đạt *(Điền giá trị Const)*. Đây là Doanh thu tự nhiên cơ bản kỳ vọng thu được nhờ uy tín thương hiệu hoặc khách hàng cũ mua lại, kể cả khi ngừng chạy quảng cáo.
  - **Kênh dẫn đầu:** Kênh *(Ví dụ: Website)* có hệ số β cao nhất là *(Điền số)*. Trong điều kiện các yếu tố khác không đổi, cứ đầu tư thêm 1 USD, doanh nghiệp kỳ vọng thu về thêm *(Điền số)* USD. Đây là "mỏ vàng" cần được ưu tiên ngân sách.
  - **Kênh kém hiệu quả (Stop-loss):** Các kênh có hệ số âm hoặc P-value > 0.05 *(Ví dụ: Facebook)* cho thấy việc tăng ngân sách không làm tăng doanh thu, thậm chí gây lỗ. Doanh nghiệp cần cắt giảm hoặc tạm dừng để đánh giá lại chất lượng tệp khách hàng.
> *[Note: Lấy kết quả từ Cell 22 & Cell 23 - Khoảng tin cậy và ROAS ước lượng]*