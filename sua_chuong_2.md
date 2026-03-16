### KHỐI 2: KỊCH BẢN CHI TIẾT (DÀN Ý ĐÃ ĐƯỢC CẬP NHẬT CHUẨN XÁC)

**CHƯƠNG 2: TIỀN XỬ LÝ VÀ KHÁM PHÁ DỮ LIỆU (EDA)**

Chương này trình bày các bước khảo sát đặc tính của tập dữ liệu `media_all_channels.csv`, giải nghĩa các biến số nghiệp vụ, áp dụng kỹ thuật Capping để xử lý các điểm dị biệt và kiểm tra các điều kiện tiên quyết trước khi đưa vào mô hình học máy.

## 2.1. Tổng quan bộ dữ liệu và Từ điển dữ liệu
**1. Từ điển dữ liệu (Data Dictionary):**
*(Trình bày đủ 15 trường dữ liệu chia làm 3 nhóm: Nhóm phân loại, Nhóm khối lượng phễu, Nhóm chỉ số hiệu quả ROI/ROAS)*

**2. Ý nghĩa các chiến dịch Marketing (Campaigns):**
*(Giải thích ngắn gọn 7 chiến dịch thực tế: Best Sellers, Exclusive Offers, Flash Sale, Limited Edition, Must-Haves, New Arrivals, Trending Now)*

**3. Thống kê mô tả:**
*(Chèn bảng kết quả Min, Max, Mean của các biến số dạng số từ Cell `df.describe()`)*


## 2.2. Xử lý giá trị ngoại lai (Outliers) bằng kỹ thuật Capping (Winsorization)
- **Minh họa bằng Boxplot:** *(Chèn hình ảnh Boxplot của biến Cost và Revenue trước khi xử lý)*
- **Áp dụng thuật toán:** Trình bày lý do không sử dụng lệnh xóa (Drop) để bảo vệ các "tín hiệu" chiến dịch thành công. Áp dụng phương pháp Capping (giới hạn trần/sàn theo IQR) để kéo các giá trị đột biến về ngưỡng an toàn.
- **Kết quả:** Kích thước dữ liệu được bảo toàn 100% (7644 dòng). Tạo ra tập dữ liệu sạch sẵn sàng cho mô hình tuyến tính.


## 2.3. Khám phá quy luật kinh doanh (Data Understanding)
- **2.3.1. Kiểm chứng Phễu Marketing:**
  *(Chèn biểu đồ Scatter giữa Impressions và Revenue)*
  **Biện luận:** Tương quan đồng biến. Càng nhiều hiển thị, doanh thu càng lớn.

- **2.3.2. Ma trận tương quan các chỉ số Hành trình khách hàng (Funnel Correlation):**
  *(Chèn biểu đồ Heatmap của Cost, Impressions, Clicks, Conversions, Revenue)*
  **Biện luận:** Đánh giá mức độ chuyển đổi của dòng tiền. Giải thích nguyên nhân phân tán dữ liệu thông qua chỉ số tương quan giữa Cost và Revenue để thiết lập kỳ vọng cho mô hình Hồi quy ở Chương 3.

- **2.3.3. Kiểm chứng Quy luật Lợi suất giảm dần:**
  *(Chèn biểu đồ Scatter có đường cong Lowess giữa Cost và ROAS)*
  **Biện luận:** Đường xu hướng võng xuống chứng minh điểm bão hòa của nền tảng khi tăng ngân sách vượt ngưỡng.


## 2.4. Kiểm tra Đa cộng tuyến (Multicollinearity)
- **Cấu trúc dữ liệu:** Pivot dữ liệu từ dạng dài (Long) sang dạng rộng (Wide) để phân tích chi phí từng ngày của các kênh độc lập.
- **Ma trận tương quan kênh:** *(Chèn biểu đồ Scatter Heatmap của các kênh)*
  **Nhận xét:** Giá trị tương quan giữa chi phí các kênh xấp xỉ 0.
- **Hệ số VIF:** *(Chèn Bảng kết quả VIF)*
  **Nhận xét:** Các kênh có VIF ~ 1.0, đạt điều kiện hoàn hảo, không bị phụ thuộc tuyến tính, đủ tiêu chuẩn để huấn luyện thuật toán Đa hồi quy.