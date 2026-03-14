# CHƯƠNG 2: TIỀN XỬ LÝ VÀ KHÁM PHÁ DỮ LIỆU (EDA)

Chương này trình bày các bước khảo sát đặc tính của tập dữ liệu `media_all_channels.csv`, giải nghĩa các biến số nghiệp vụ, xử lý các điểm dị biệt và kiểm tra các điều kiện tiên quyết trước khi đưa vào mô hình học máy.

## 2.1. Tổng quan bộ dữ liệu và Từ điển dữ liệu
*(Trình bày thông tin cơ bản về file CSV, bao gồm số dòng, số cột và định nghĩa các trường dữ liệu)*

**1. Từ điển dữ liệu (Data Dictionary):**
- `date`: Ngày ghi nhận số liệu.
- `campaign`: Tên chiến dịch Marketing đang triển khai.
- `channel`: Kênh chạy quảng cáo (Facebook, Google Ads, Website, Instagram, TikTok, LinkedIn, Twitter).
- `cost`: Chi phí quảng cáo đã chi tiêu trong ngày (USD).
- `impressions`: Số lượt hiển thị quảng cáo đến người dùng.
- `clicks`: Số lượt người dùng bấm vào quảng cáo.
- `revenue`: Doanh thu trực tiếp mang lại từ kênh đó trong ngày (USD).

**2. Ý nghĩa các chiến dịch Marketing (Campaigns):**
*(Liệt kê và giải thích ngắn gọn mục đích kinh doanh của 7 chiến dịch có trong tập dữ liệu)*
- *Flash Sale:* Chiến dịch giảm giá chớp nhoáng, đẩy số lượng bán trong thời gian ngắn.
- *Black Friday:* Chiến dịch sale lớn nhất năm.
- *Influencer Collab:* Chiến dịch kết hợp với người nổi tiếng/KOLs.
- *Best Sellers:* Chiến dịch đẩy mạnh các sản phẩm đang bán chạy.
- *Brand Awareness:* Chiến dịch tăng độ phủ và nhận diện thương hiệu.
- *Holiday Promo:* Khuyến mãi theo các dịp lễ hội.
- *Exclusive Offers:* Ưu đãi độc quyền dành riêng cho tập khách hàng cụ thể.

**3. Thống kê mô tả:** *(Chèn bảng kết quả Min, Max, Mean của các biến số dạng số)*
> *[Note: Lấy kết quả từ Cell 2 `df.info()` và Cell 3 `df.describe()` trong Jupyter Notebook]*


## 2.2. Nhận diện và Xử lý giá trị ngoại lai (Outliers)
*(Trình bày quá trình lọc nhiễu bằng IQR)*

- **Minh họa bằng Boxplot:** *(Chèn hình ảnh Boxplot của biến Cost và Revenue)*
- **Áp dụng thuật toán IQR:** Trình bày kết quả lọc dữ liệu. Thuật toán đã phát hiện và bóc tách các dòng dữ liệu có chi phí hoặc doanh thu vượt xa mức bình thường.
- **Kết quả:** Tập dữ liệu được tách làm 2 phiên bản: `Tập dữ liệu gốc` và `Tập dữ liệu sạch`.
> *[Note: Lấy hình ảnh từ Cell 4 (vẽ Boxplot) và kết quả in ra từ Cell 5, 6, 7 (Hàm xử lý Outliers)]*


## 2.3. Khám phá quy luật kinh doanh (Data Understanding)
*(Sử dụng biểu đồ để xác nhận các lý thuyết Marketing trên dữ liệu thực tế)*

- **Kiểm chứng Phễu Marketing:**
  *(Chèn biểu đồ Scatter giữa Impressions và Revenue)*
  **Biện luận:** Biểu đồ cho thấy mối tương quan đồng biến. Lượt hiển thị càng cao, doanh thu càng lớn. Tuy nhiên, biến `impressions` sẽ được loại khỏi mô hình hồi quy để tránh đa cộng tuyến với biến `cost`.
> *[Note: Lấy hình ảnh biểu đồ từ Cell A - Biểu đồ Phễu Marketing]*

- **Kiểm chứng Quy luật Lợi suất giảm dần:**
  *(Chèn biểu đồ Scatter có đường cong Lowess giữa Cost và ROAS)*
  **Biện luận:** Đường xu hướng võng xuống chứng minh rằng khi chi phí quảng cáo tăng quá cao, tỷ suất sinh lời (ROAS) bắt đầu giảm do bão hòa nền tảng.
> *[Note: Lấy hình ảnh biểu đồ từ Cell B - Biểu đồ Lợi suất giảm dần]*


## 2.4. Kiểm tra Đa cộng tuyến (Multicollinearity)
*(Đánh giá mức độ độc lập của các kênh quảng cáo sau khi đã Pivot dữ liệu theo ngày)*

- **Ma trận tương quan:** *(Chèn biểu đồ Heatmap của các kênh)*
  **Nhận xét:** Giá trị tương quan giữa chi phí các kênh quảng cáo đều rất sát mức 0, cho thấy chúng không bị phụ thuộc tuyến tính vào nhau.
- **Hệ số VIF:** *(Chèn Bảng kết quả VIF)*
  **Nhận xét:** Tất cả các biến chi phí đều có VIF ~ 1.0 (nhỏ hơn rất nhiều so với ngưỡng rủi ro là 10). Dữ liệu đạt điều kiện hoàn hảo để chạy hồi quy.
> *[Note: Lấy hình ảnh Heatmap và Bảng VIF từ Cell 10 trong Jupyter Notebook]*