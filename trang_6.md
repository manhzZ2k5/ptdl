## CHƯƠNG 6: HỆ THỐNG HỖ TRỢ RA QUYẾT ĐỊNH VÀ GIẢ LẬP NGÂN SÁCH (DECISION SUPPORT SYSTEM)

**Mục tiêu của Chương:**
Trang Giả lập Ngân sách đóng vai trò là điểm chạm cuối cùng (End-user Application) của dự án. Chức năng này nâng cấp bài toán từ Phân tích Dự báo (Predictive Analytics) lên Phân tích Đề xuất (Prescriptive Analytics). Thay vì chỉ cung cấp các con số thống kê khô khan, hệ thống cho phép Ban Giám đốc tương tác trực tiếp với mô hình để lập kế hoạch dòng tiền cho các chiến dịch tương lai.

Hệ thống vận hành thông qua bộ lọc chiến dịch (Campaign Filter), cho phép tính toán Lợi tức quảng cáo (ROAS) riêng biệt cho từng loại chiến dịch, sau đó cung cấp hai công cụ phân bổ: **Thủ công (Manual)** và **Tối ưu hóa bằng thuật toán (AI Auto-Allocate)**.

---

### 1. Cơ chế Phân bổ Thủ công (Manual "What-If" Analysis)

**Mục đích:**
Cung cấp cho người dùng quyền kiểm soát tuyệt đối để thử nghiệm các kịch bản phân bổ ngân sách khác nhau (What-If Scenarios) dựa trên kinh nghiệm thực tiễn hoặc linh cảm kinh doanh.

**Cách hoạt động:**
* **Nhập liệu:** Hệ thống cung cấp các ô nhập số liệu trực quan cho 6 kênh quảng cáo.
* **Xử lý:** Khi người dùng nhập một mức ngân sách dự kiến, hệ thống sẽ lấy số tiền đó nhân với chỉ số Lợi tức quảng cáo (ROAS) tương ứng của kênh đó trong chiến dịch đã chọn.
* **Công thức Toán học:**
    $$Projected\_Revenue = \sum_{i=1}^{n} (Budget_i \times ROAS_i)$$
    *(Trong đó: $i$ là từng kênh quảng cáo)*
* **Kết quả:** Hệ thống lập tức trả về **Tổng Doanh thu Dự kiến**, giúp người quản lý nhanh chóng đánh giá xem phương án chia tiền của mình có mang lại hiệu quả mong đợi hay không.

---

### 2. Cơ chế AI Tối ưu hóa (Linear Programming / Quy hoạch Tuyến tính)

**Mục đích:**
Loại bỏ yếu tố cảm tính và việc "thử sai" thủ công. Tính năng này đóng vai trò như một "Giám đốc Tài chính Ảo", tự động giải bài toán tối ưu hóa nguồn lực, tìm ra phương án chia tiền sinh lời cao nhất trong giới hạn ngân sách và rủi ro cho phép.

**Cách hoạt động:**
Hệ thống ứng dụng thuật toán **Quy hoạch tuyến tính (Linear Programming)** thông qua thư viện `SciPy` của Python. Thuật toán xử lý bài toán dựa trên 3 thành phần cốt lõi:

* **Hàm mục tiêu (Objective Function):**
    Hệ thống được lập trình để tìm giá trị **Lớn nhất (Maximize)** cho phương trình Doanh thu:
    $$Max\_Revenue = (ROAS_{FB} \times X_{FB}) + (ROAS_{GG} \times X_{GG}) + \dots + (ROAS_{Web} \times X_{Web})$$
    *(Trong đó: $X$ là số tiền cần phân bổ cho mỗi kênh)*

* **Các Ràng buộc Kinh doanh (Business Constraints):**
    Để đảm bảo tính thực tế, AI bị giới hạn bởi các quy tắc khắt khe:
    1.  **Ràng buộc Tổng ngân sách:** Tổng số tiền giải ngân phải đúng bằng ngân sách khả dụng mà công ty cấp (Ví dụ: 10,000 USD).
    2.  **Ràng buộc Rủi ro (Diversification):** Không được đổ 100% tiền vào một kênh duy nhất để tránh bão hòa thị trường. Người dùng có thể thiết lập mức trần (Ví dụ: Một kênh không được chiếm quá 40% tổng ngân sách).
    3.  **Quy tắc Cắt lỗ (Stop-loss Rule):** AI được lập trình tư duy quản trị rủi ro. Nếu một kênh có $ROAS < 1$ (Chi 1 đồng thu về ít hơn 1 đồng), thuật toán sẽ ép ngân sách của kênh đó về mức $0.

* **Kết quả đầu ra (Output):**
    Sau khi xử lý phương trình ràng buộc, thuật toán xuất ra một bản Kế hoạch Rót vốn chi tiết tới từng đô la cho từng kênh, đi kèm với mức **Doanh thu Tối đa (Maximum Possible Revenue)** mà công ty có thể đạt được trong điều kiện giới hạn đó.