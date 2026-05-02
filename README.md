# Đồ án: Xây dựng mô hình DevSecOps cho ứng dụng Web

## 1. Giới thiệu dự án
Dự án này ứng dụng mô hình DevSecOps với triết lý "Shift-Left" vào vòng đời phát triển phần mềm (SDLC)[cite: 1]. Hệ thống tự động hóa quá trình rà soát mã nguồn, kiểm tra môi trường chạy và đánh giá ứng dụng trực tiếp trên đường ống (pipeline) CI/CD nhằm phát hiện và ngăn chặn sớm các lỗ hổng bảo mật[cite: 1].

Mục tiêu thử nghiệm là một ứng dụng Web được xây dựng bằng framework Flask (Python) và cơ sở dữ liệu SQLite, được thiết kế cố ý chứa các lỗ hổng bảo mật đặc trưng để đánh giá hiệu quả của pipeline[cite: 1].

## 2. Công cụ và Công nghệ sử dụng
* **Mã nguồn & CI/CD:** GitLab CI / GitLab Runner[cite: 1].
* **Môi trường triển khai:** Docker, Docker Compose (Môi trường Local/Self-hosted)[cite: 1].
* **Ứng dụng mục tiêu:** Python 3.10, Flask, SQLite[cite: 1].
* **Bảo mật tĩnh (SAST):** 
  * **SonarQube (Community):** Đánh giá chất lượng mã nguồn, phát hiện code smell và điểm nóng cấu hình (Security Hotspots)[cite: 1].
  * **Bandit:** Phân tích luồng dữ liệu chuyên sâu cho Python để phát hiện SQLi, XSS, Hardcoded Secrets[cite: 1].
* **Bảo mật thành phần (SCA):** **Trivy** (Quét lỗ hổng CVE từ Docker Image)[cite: 1].
* **Bảo mật động (DAST):** **OWASP ZAP** (Giả lập tấn công hộp đen vào container đang chạy)[cite: 1].

## 3. Kiến trúc DevSecOps Pipeline
Đường ống CI/CD được cấu hình trong tệp `.gitlab-ci.yml` bao gồm 7 giai đoạn (stages) tự động nối tiếp nhau[cite: 1]:

1. **`build`**: Biên dịch thử mã nguồn bằng `py_compile` để bắt các lỗi cú pháp cơ bản[cite: 1].
2. **`test`**: Khởi chạy ứng dụng ở chế độ nền và kiểm tra sức khỏe (Health check) thông qua API `/health` trên cổng 5000[cite: 1].
3. **`sast`**: Thực thi song song SonarScanner CLI kết nối với SonarQube Local và công cụ Bandit để quét chuyên sâu thư mục `src/app`[cite: 1].
4. **`docker-build`**: Áp dụng Docker-in-Docker (DinD) để đóng gói ứng dụng thành Docker Image và đẩy lên GitLab Container Registry[cite: 1].
5. **`image-scan`**: Sử dụng AquaSec Trivy để quét image vừa tạo, cấu hình chặn (fail) nếu phát hiện lỗ hổng mức độ HIGH và CRITICAL[cite: 1].
6. **`deploy`**: Giao tiếp qua shell thực thi `docker compose up -d web` để tự động triển khai ứng dụng dưới dạng Container[cite: 1].
7. **`security_scan_dynamic`**: Chạy ZAP Baseline Scan tấn công trực tiếp vào địa chỉ IP nội bộ của ứng dụng để tìm lỗ hổng cấp độ Web và xuất báo cáo HTML[cite: 1].

## 4. Các kịch bản thử nghiệm
Dự án được đánh giá qua 2 kịch bản chính[cite: 1]:

### Kịch bản 1: Ứng dụng tồn tại lỗ hổng (Pipeline Failed)
* **SQL Injection (CWE-89):** Tính năng đăng nhập `/login` cộng chuỗi SQL trực tiếp, bị Bandit phát hiện (Mã B608)[cite: 1].
* **Hardcoded Secrets (CWE-259):** Khóa bí mật (Secret Key) đặt trực tiếp trong mã nguồn, bị Bandit phát hiện (Mã B105)[cite: 1].
* **Cross-Site Scripting (XSS):** Dữ liệu tính năng `/search` không được làm sạch, bị OWASP ZAP phát hiện lúc runtime qua cơ chế Reflected XSS[cite: 1].
* **Lỗ hổng Image:** Trivy phát hiện các CVE mức độ High/Critical từ base image của hệ điều hành Linux[cite: 1].

### Kịch bản 2: Khắc phục và Vận hành an toàn (Pipeline Passed)
* **Khắc phục code:** Sử dụng truy vấn có tham số (Parameterized Queries) cho SQL, lấy khóa bảo mật qua biến môi trường `os.environ`, và sử dụng hàm `escape()` để chặn XSS[cite: 1].
* **Tối ưu Vận hành (Ops):** Cấu hình Volume Persistence cho SQLite để tránh mất dữ liệu, tích hợp Auto-Restart, và giới hạn dung lượng log container ở mức tối đa 10MB/file để tránh tràn bộ nhớ[cite: 1].
* **Kết quả:** Pipeline chạy thành công (Passed) qua toàn bộ 7 giai đoạn, ZAP báo cáo 0 lỗi nghiêm trọng mới (FAIL-NEW: 0)[cite: 1].

## 5. Hướng dẫn Triển khai (Local Development)
1. Yêu cầu hệ thống: Cài đặt sẵn Docker Engine v24+ và Docker Compose v2[cite: 1].
2. Clone kho lưu trữ này về máy.
3. Thiết lập mạng nội bộ cho các công cụ bảo mật giao tiếp:
   ```bash
   docker network create devsecops_net
Khởi chạy hệ thống thông qua Docker Compose:

Bash
docker compose up -d
Truy cập ứng dụng Flask tại http://localhost:5000 và bảng điều khiển SonarQube tại http://localhost:9000[cite: 1].