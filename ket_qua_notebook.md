# Kết Quả Notebook: Tối Ưu Hóa Ngân Sách Digital Marketing bằng Hồi Quy Tuyến Tính

---

## Phần 1: Khởi Tạo & Tiền Xử Lý Dữ Liệu

### Cell 1 – Import thư viện
Nhập các thư viện cần thiết: `pandas`, `numpy`, `matplotlib`, `seaborn`, `sklearn`, `statsmodels`.

### Cell 2 – Đọc và xem thông tin dữ liệu gốc
- **Nguồn:** `../media_all_channels.csv`
- **Kích thước:** 7.644 hàng × 15 cột
- **Các cột:** `date`, `channel`, `campaign`, `impressions`, `clicks`, `conversions`, `cost`, `revenue`, `cpc`, `cpa`, `ctr`, `conversion_rate`, `roas`, `roi`, `profit_margin`
- **Kiểu dữ liệu:** 3 object, 3 int64, 9 float64 — **không có giá trị null**

### Cell 3 – Thống kê mô tả chi phí và doanh thu

| Chỉ số | cost | revenue |
|--------|------|---------|
| count | 7.644 | 7.644 |
| mean | 20.202 | 85.383 |
| std | 13.331 | 56.928 |
| min | 936 | 5.910 |
| 25% | 9.299 | 42.766 |
| 50% | 18.434 | 70.342 |
| 75% | 27.735 | 113.293 |
| max | 96.648 | 402.881 |

*(Đơn vị: nghìn đồng hoặc đơn vị tiền tệ tương ứng)*

### Cell 4 – Boxplot phát hiện Outlier
**Biểu đồ:** Boxplot cho `cost` và `revenue` → Cả hai đều có nhiều điểm ngoại lệ (outlier) ở phía trên.

### Cell 5 – Xác định số lượng Outlier bằng IQR
- **Outlier trong `cost`:** 128 điểm
- **Outlier trong `revenue`:** 238 điểm

### Cell 6 – Xem mẫu các Outlier

**Một số outlier trong `cost`:**
| date | channel | campaign | cost | revenue |
|------|---------|----------|------|---------|
| 2024-02-18 | Facebook | Best Sellers | 64.894 | 182.313 |
| 2024-04-03 | Facebook | Limited Edition | 56.730 | 206.327 |
| 2023-11-03 | Instagram | Limited Edition | 64.027 | 46.965 |

**Một số outlier trong `revenue`:**
| date | channel | campaign | cost | revenue |
|------|---------|----------|------|---------|
| 2023-11-01 | Facebook | Must-Haves | 30.655 | 282.510 |
| 2023-11-03 | Facebook | Best Sellers | 37.641 | 296.416 |
| 2023-11-03 | Facebook | Flash Sale | 32.886 | 323.776 |

### Cell 7 – Loại bỏ Outlier & tạo 2 bộ dữ liệu
- `df_original`: Dữ liệu gốc → **7.644 hàng × 15 cột**
- `df_clean`: Dữ liệu đã loại outlier → **7.314 hàng × 15 cột**

---

## Phần 2: Khám Phá Dữ Liệu (EDA)

### Cell 8 – Scatter plot: Marketing Funnel (dữ liệu sạch)
**Biểu đồ:** Scatter plot thể hiện mối liên hệ giữa `impressions → clicks → conversions → revenue` theo từng kênh (`channel`), giúp trực quan hóa phễu marketing.

### Cell 9 – Phân phối doanh thu theo kênh
**Biểu đồ:** Boxplot/violin plot phân phối `revenue` theo `channel`, cho thấy sự phân tán doanh thu khác nhau giữa các kênh.

### Cell 10 – Tương quan giữa cost và revenue
**Biểu đồ:** Scatter plot `cost` vs `revenue` với đường hồi quy, thể hiện mối tương quan dương giữa chi phí và doanh thu.

### Cell 11 – Heatmap tương quan
**Biểu đồ:** Heatmap thể hiện ma trận tương quan giữa các biến số (`cost`, `revenue`, `impressions`, v.v.).

### Cell 12 – Scatter plot: Hiệu suất giảm dần (Diminishing Returns) + Lowess
**Biểu đồ:** Scatter plot `cost` vs `revenue` kèm đường **Lowess** (locally weighted regression) — minh họa xu hướng lợi nhuận cận biên giảm dần khi tăng chi phí.

---

## Phần 3: Xây Dựng & Đánh Giá Mô Hình

### Cell 13 – Chuẩn bị dữ liệu cho mô hình
Pivot dữ liệu theo kênh (`Facebook`, `Google Ads`, `Instagram`, `LinkedIn`, `Twitter`, `Website`) để tạo các cột `{channel}_cost` và `{channel}_revenue` tổng hợp theo ngày → dùng làm đầu vào cho mô hình OLS.

### Cell 14 – Hồi quy OLS trên dữ liệu gốc (statsmodels)

**Kết quả mô hình (dữ liệu gốc):**
- **R² = 0.994** — Mô hình giải thích 99,4% phương sai của doanh thu
- **AIC / BIC:** Rất thấp → Mô hình tốt
- **F-statistic:** Rất cao → Mô hình có ý nghĩa thống kê

| Biến | coef | p-value |
|------|------|---------|
| const | ~2,7M | < 0.001 |
| Facebook_cost | ~0,17 | < 0.001 |
| Google Ads_cost | ~0,17 | < 0.001 |
| Instagram_cost | ~1,33 | < 0.001 |
| LinkedIn_cost | ~0,78 | < 0.001 |
| Twitter_cost | ~0,62 | < 0.001 |
| Website_cost | ~2,48 | < 0.001 |

### Cell 15 – Hồi quy OLS trên dữ liệu sạch (statsmodels)

**Kết quả mô hình (dữ liệu sạch):**
- **R² = 0.994** — Tương đương dữ liệu gốc
- Hệ số tương tự; `Website` và `Instagram` vẫn có hệ số cao nhất

| Biến | coef (sạch) |
|------|------------|
| Facebook_cost | ~0,17 |
| Google Ads_cost | ~0,17 |
| Instagram_cost | ~1,30 |
| LinkedIn_cost | ~0,78 |
| Twitter_cost | ~0,62 |
| Website_cost | ~2,49 |

### Cell 16 – So sánh hệ số hai mô hình

| Kênh | Hệ số (gốc) | Hệ số (sạch) |
|------|------------|-------------|
| Facebook | ~0.17 | ~0.17 |
| Google Ads | ~0.17 | ~0.17 |
| Instagram | ~1.33 | ~1.30 |
| LinkedIn | ~0.78 | ~0.78 |
| Twitter | ~0.62 | ~0.62 |
| Website | ~2.48 | ~2.49 |

> **Nhận xét:** Việc loại outlier hầu như không thay đổi hệ số hồi quy → mô hình ổn định.

### Cell 17 – Scatter plot thực tế vs dự báo
**Biểu đồ:** Scatter plot `actual revenue` vs `predicted revenue` cho cả hai mô hình, đường lý tưởng y=x → các điểm bám sát đường, mô hình dự báo tốt.

### Cell 18 – Khoảng tin cậy 95% cho hệ số (dữ liệu sạch)

| Biến | 2.5% | 97.5% |
|------|------|-------|
| const | 2.116M | 3.128M |
| Facebook_cost | -1.114 | 1.464 |
| Google Ads_cost | -1.163 | 1.500 |
| Instagram_cost | 0.413 | 2.180 |
| LinkedIn_cost | -0.983 | 2.552 |
| Twitter_cost | -3.153 | 4.392 |
| Website_cost | -4.555 | 9.540 |

> **Nhận xét:** Khoảng tin cậy của `Facebook` và `Google Ads` bao gồm 0 → không chắc chắn về ảnh hưởng dương hay âm trong mô hình hồi quy đa biến theo ngày; trong khi `Instagram` có khoảng tin cậy dương hoàn toàn.

### Cell 19 – ROAS ước lượng theo kênh (dữ liệu sạch)

| Kênh | ROAS ước lượng |
|------|---------------|
| Website | **2.32** |
| Instagram | **1.77** |
| LinkedIn | 0.77 |
| Twitter | 0.57 |
| Google Ads | 0.54 |
| Facebook | -0.79 |

> **Kết luận:** `Website` và `Instagram` mang lại ROAS cao nhất; `Facebook` có ROAS âm trong mô hình này (do đa cộng tuyến hoặc tương quan âm sau khi kiểm soát các kênh khác).

---

## Phần 4: Phân Tích Tương Tác Kênh × Chiến Dịch

### Cell 20 – Tính ROAS theo từng cặp (Kênh × Chiến dịch)

**5 dòng đầu:**
| channel | campaign | cost | revenue | ROAS |
|---------|----------|------|---------|------|
| Facebook | Best Sellers | 4.58M | 20.18M | 4.41 |
| Facebook | Exclusive Offers | 3.91M | 17.92M | 4.59 |
| Facebook | Flash Sale | 4.40M | 20.31M | 4.62 |
| Facebook | Limited Edition | 4.20M | 17.98M | 4.28 |
| Facebook | Must-Haves | 4.45M | 19.31M | 4.34 |

### Cell 21 – Heatmap ROAS theo Kênh × Chiến dịch
**Biểu đồ:** Heatmap (YlGnBu) thể hiện ROAS của từng cặp kênh–chiến dịch:
- Các giá trị ROAS dao động khoảng **4.0 – 5.0** cho hầu hết chiến dịch
- Cho phép nhận biết kênh/chiến dịch nào hiệu quả nhất

### Cell 22 – Biểu đồ ROAS trung bình theo kênh
**Biểu đồ:** Horizontal bar chart (màu RdYlGn) thể hiện ROAS trung bình của mỗi kênh, in tiêu đề phân tích hiệu quả nền tảng theo từng chiến dịch.

---

## Tóm Tắt Kết Quả Chính

| Hạng mục | Kết quả |
|----------|---------|
| Dataset | 7.644 bản ghi, 15 biến, không có giá trị null |
| Outlier | 128 (cost) + 238 (revenue) → loại bỏ, còn 7.314 dòng |
| R² mô hình | **0.994** (cả gốc lẫn sạch) |
| ROAS cao nhất | **Website (2.32)** → **Instagram (1.77)** |
| ROAS thấp nhất | **Facebook (-0.79)** trong mô hình đa biến |
| Kênh tốt nhất theo ROAS thực tế | Tương đương ~4.2–4.6 cho tất cả kênh (theo từng chiến dịch) |
