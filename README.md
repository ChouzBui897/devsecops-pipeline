# 🛡️ DevSecOps Web Application Pipeline

## 📖 1. Giới thiệu dự án
Dự án này ứng dụng mô hình DevSecOps với triết lý "Shift-Left" vào vòng đời phát triển phần mềm (SDLC). Hệ thống tự động hóa quá trình rà soát mã nguồn, kiểm tra môi trường chạy và đánh giá ứng dụng trực tiếp trên đường ống (pipeline) CI/CD nhằm phát hiện và ngăn chặn sớm các lỗ hổng bảo mật.

Mục tiêu thử nghiệm là một ứng dụng Web được xây dựng bằng framework Flask (Python) và cơ sở dữ liệu SQLite, được thiết kế cố ý chứa các lỗ hổng bảo mật đặc trưng để đánh giá hiệu quả của pipeline.

## 🛠️ 2. Công cụ và Công nghệ sử dụng
* **Mã nguồn & CI/CD:** GitLab CI / GitLab Runner
* **Môi trường triển khai:** Docker, Docker Compose (Local/Self-hosted)
* **Ứng dụng mục tiêu:** Python 3.10, Flask, SQLite
* **Bảo mật tĩnh (SAST):** * **SonarQube (Community):** Đánh giá chất lượng mã nguồn, phát hiện code smell và điểm nóng cấu hình.
  * **Bandit:** Phân tích luồng dữ liệu chuyên sâu cho Python (SQLi, XSS, Hardcoded Secrets).
* **Bảo mật thành phần (SCA):** **Trivy** (Quét lỗ hổng CVE từ Docker Image).
* **Bảo mật động (DAST):** **OWASP ZAP** (Giả lập tấn công hộp đen vào container đang chạy).

## ⚙️ 3. Kiến trúc DevSecOps Pipeline
Đường ống CI/CD được cấu hình trong tệp `.gitlab-ci.yml` bao gồm 7 giai đoạn (stages) tự động nối tiếp nhau:

1. **`build`**: Biên dịch thử mã nguồn bằng `py_compile` để bắt các lỗi cú pháp cơ bản.
2. **`test`**: Khởi chạy ứng dụng ở chế độ nền và kiểm tra sức khỏe (Health check) thông qua API `/health` trên cổng 5000.
3. **`sast`**: Thực thi song song SonarScanner CLI (kết nối SonarQube Local) và công cụ Bandit để quét chuyên sâu.
4. **`docker-build`**: Áp dụng Docker-in-Docker (DinD) để đóng gói ứng dụng thành Docker Image và đẩy lên GitLab Registry.
5. **`image-scan`**: Sử dụng AquaSec Trivy để quét image, cấu hình đánh trượt (fail) pipeline nếu phát hiện lỗ hổng mức độ HIGH hoặc CRITICAL.
6. **`deploy`**: Thực thi `docker compose up -d web` qua shell để tự động triển khai ứng dụng dưới dạng Container.
7. **`security_scan_dynamic`**: Chạy ZAP Baseline Scan. Quá trình giao tiếp được thực hiện thông qua **tên container (container name)** trong mạng Docker nội bộ để đảm bảo kết nối luôn ổn định và chính xác trong quá trình rà quét Web.

## 🧪 4. Kịch bản thử nghiệm

### ❌ Kịch bản 1: Ứng dụng tồn tại lỗ hổng (Pipeline Failed)
* **SQL Injection (CWE-89):** Tính năng đăng nhập bị Bandit phát hiện do cộng chuỗi SQL trực tiếp.
* **Hardcoded Secrets (CWE-259):** Khóa bí mật (Secret Key) bị Bandit phát hiện lộ lọt trong mã nguồn.
* **Cross-Site Scripting (XSS):** OWASP ZAP phát hiện lỗ hổng Reflected XSS lúc runtime do dữ liệu không được làm sạch.
* **Lỗ hổng Image:** Trivy phát hiện các CVE mức độ High/Critical từ base image của hệ điều hành.

### ✅ Kịch bản 2: Khắc phục và Vận hành an toàn (Pipeline Passed)
* **Khắc phục code:** Sử dụng truy vấn có tham số (Parameterized Queries) cho SQL, nạp khóa bảo mật động qua biến môi trường `os.environ`, và sử dụng hàm `escape()` để vô hiệu hóa XSS.
* **Tối ưu Vận hành (Ops):** Cấu hình Volume Persistence cho SQLite để tránh mất dữ liệu, tích hợp Auto-Restart, và giới hạn dung lượng log container ở mức 10MB/file.
* **Kết quả:** Pipeline chạy thành công (Passed) qua toàn bộ 7 giai đoạn. Hệ thống ghi nhận 0 lỗi nghiêm trọng mới từ ZAP (FAIL-NEW: 0). *(Lưu ý: Các cảnh báo warning còn tồn đọng sau khi vá lỗi XSS chỉ là rủi ro thụ động do thiếu cấu hình Security Headers, không ảnh hưởng đến an toàn ứng dụng).*

## 🚀 5. Hướng dẫn Triển khai (Local Development)

**Yêu cầu hệ thống:** Cài đặt sẵn Docker Engine v24+ và Docker Compose v2.

1. Clone kho lưu trữ này về máy.
2. Thiết lập mạng ảo cho các công cụ bảo mật giao tiếp:
   ```bash
   docker network create devsecops_net

  Khởi chạy hệ thống thông qua Docker Compose:

3. Khởi chạy hệ thống thông qua Docker Compose:
    ```bash
    docker compose up -d
4. Truy cập ứng dụng:

    Web App: http://localhost:5000

    SonarQube Dashboard: http://localhost:9000

👨‍💻 Tác giả
Bùi Minh Châu - Đồ án chuyên ngành 2025-2026