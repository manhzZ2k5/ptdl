# CHƯƠNG 3: XÂY DỰNG MÔ HÌNH VÀ KIỂM ĐỊNH THỐNG KÊ

Chương này trình bày quá trình huấn luyện thuật toán Đa hồi quy tuyến tính (Multiple Linear Regression) trên tập dữ liệu đã làm sạch. Mục tiêu là tìm ra phương trình tác động của các kênh quảng cáo đến doanh thu, đồng thời sử dụng các phép kiểm định thống kê để đảm bảo độ tin cậy của kết quả dự báo.

## 3.1. Đánh giá sai số và Lựa chọn mô hình
*(Trình bày kết quả huấn luyện từ thư viện `scikit-learn` để so sánh hiệu quả của việc làm sạch dữ liệu ở Chương 2)*

- **Thiết lập huấn luyện:** Tập dữ liệu được chia theo tỷ lệ 80% (Train) để máy học các hệ số và 20% (Test) để kiểm thử sai số thực tế. 
- **Bảng so sánh hiệu suất:** *(Chèn bảng kết quả so sánh $R^2$, MAE, RMSE của Mô hình gốc và Mô hình sạch)*
- **Biện luận lựa chọn:** Dựa vào kết quả trên, ta thấy **Mô hình Sạch** (đã loại bỏ Outliers bằng IQR) cho ra sai số RMSE thấp hơn hẳn so với Mô hình Gốc. Vì RMSE nhạy cảm với các sai số lớn, việc RMSE giảm mạnh chứng tỏ mô hình sạch ổn định và ít bị vặn vẹo hơn. Đồng thời, hệ số $R^2$ vẫn giữ ở mức cao, giải thích được phần lớn sự biến thiên của doanh thu. Do đó, nhóm quyết định sử dụng **Mô hình Sạch** làm cơ sở phân tích chính thức cho các bước tiếp theo.
> *[Note: Lấy bảng kết quả in ra từ Cell 8 (Xây dựng mô hình) và Cell 9 (So sánh kết quả) trong Jupyter Notebook]*


## 3.2. Kiểm định ý nghĩa thống kê của mô hình (OLS Summary)
*(Sử dụng thư viện `statsmodels` để thực hiện suy diễn thống kê, đảm bảo các kết quả tìm được không phải do ngẫu nhiên)*

- **Bảng tóm tắt hồi quy (OLS Regression Results):**
  *(Chụp ảnh và chèn toàn bộ bảng Summary của thư viện statsmodels vào đây)*


- **Đánh giá độ phù hợp toàn cục (Kiểm định F):**
  Nhìn vào góc phải trên cùng của bảng, chỉ số `Prob (F-statistic)` có giá trị rất nhỏ (gần bằng $0.00$) và $< 0.05$. Do đó, ta bác bỏ giả thuyết $H_0$, khẳng định phương trình Đa hồi quy tuyến tính được xây dựng có ý nghĩa thống kê cao. Ngân sách quảng cáo thực sự có tác động đến việc tạo ra doanh thu.

- **Đánh giá ý nghĩa cục bộ (Kiểm định t):**
  Kiểm tra cột `P>|t|` (P-value) đối với từng kênh quảng cáo:
  - **Các kênh có ý nghĩa:** Kênh *(Liệt kê tên các kênh có P-value < 0.05, ví dụ: Facebook, Website...)* có $P\text{-value} < 0.05$, chứng tỏ chi phí đổ vào các nền tảng này thực sự tạo ra sự thay đổi về doanh thu.
  - **Các kênh không có ý nghĩa:** Kênh *(Liệt kê kênh có P-value > 0.05, ví dụ: LinkedIn...)* có $P\text{-value} > 0.05$, nghĩa là hệ số tác động của kênh này không khác biệt so với 0 về mặt thống kê. Việc chi tiền cho nền tảng này đang không mang lại hiệu quả rõ rệt.
> *[Note: Lấy hình ảnh từ Cell C - Phân Tích Hồi Quy Chuyên Sâu bằng Statsmodels OLS]*


## 3.3. Kiểm tra các giả định của phần dư (Residual Diagnostics)
*(Chứng minh mô hình OLS hoàn toàn hợp lệ, không vi phạm các giả định toán học)*

- **Kiểm tra giả định phân phối chuẩn:** *(Chèn biểu đồ Histogram phần dư)*
  **Nhận xét:** Biểu đồ Histogram của phần dư có dáng hình chuông, phân bố đối xứng quanh giá trị $0$, thỏa mãn giả định sai số ngẫu nhiên tuân theo phân phối chuẩn.
  
- **Kiểm tra phương sai sai số không đổi (Homoscedasticity):** *(Chèn biểu đồ Scatter Phần dư vs Giá trị dự đoán)*
  **Nhận xét:** Các điểm dữ liệu phân tán hoàn toàn ngẫu nhiên quanh trục hoành ($0$), không tạo thành các mô hình dạng phễu (funnel) hay đường cong. Điều này chứng tỏ phương sai của phần dư là đồng đều, mô hình không bị hiện tượng phương sai thay đổi.
> *[Note: Lấy 2 hình ảnh biểu đồ từ Cell 10 - Phân tích phần dư]*


## 3.4. Bóc tách Tỷ suất Lợi tức quảng cáo biên (Marginal ROAS)
*(Dịch các hệ số Beta từ toán học sang ngôn ngữ kinh doanh để chuẩn bị cho bài toán tối ưu hóa dòng tiền)*

- **Bảng xếp hạng Tác động biên:**
  *(Chèn bảng xếp hạng các Hệ số Beta/ROAS của các kênh từ cao xuống thấp cùng Khoảng tin cậy 95%)*

- **Giải thích ý nghĩa kinh tế:** - Hệ số chặn (Intercept) đạt *(Điền giá trị Const)*: Đây là Doanh thu tự nhiên cơ bản mà doanh nghiệp thu được kể cả khi không chạy quảng cáo (nhờ khách tự tìm đến hoặc mua lại).
  - **Kênh dẫn đầu:** Kênh *(Điền tên kênh cao nhất, ví dụ: Website)* có hệ số $\beta$ cao nhất là *(Điền số)*. Trong điều kiện các yếu tố khác không đổi, cứ đầu tư thêm $1$ USD vào hệ thống Website, doanh nghiệp kỳ vọng thu về thêm *(Điền số)* USD doanh thu. Đây là kênh sinh lời tốt nhất cần được ưu tiên ngân sách.
  - **Kênh kém hiệu quả:** Kênh *(Điền tên kênh thấp nhất/có P-value > 0.05)* có hệ số rất thấp hoặc không có ý nghĩa thống kê. Doanh nghiệp cần cắt giảm ngân sách tại đây để tránh lãng phí (Stop-loss).
> *[Note: Lấy kết quả từ Cell 11 - Khoảng tin cậy và ROAS]*