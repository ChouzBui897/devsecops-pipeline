# DevSecOps Web Application Pipeline

## 1. Giới thiệu dự án
Dự án này ứng dụng mô hình DevSecOps với triết lý "Shift-Left" vào vòng đời phát triển phần mềm (SDLC). Hệ thống tự động hóa quá trình rà soát mã nguồn, kiểm tra môi trường chạy và đánh giá ứng dụng trực tiếp trên đường ống (pipeline) CI/CD nhằm phát hiện và ngăn chặn sớm các lỗ hổng bảo mật.

Mục tiêu thử nghiệm là một ứng dụng Web được xây dựng bằng framework Flask (Python) và cơ sở dữ liệu SQLite, được thiết kế cố ý chứa các lỗ hổng bảo mật đặc trưng để đánh giá hiệu quả của pipeline.

## 2. Công cụ và Công nghệ sử dụng

- GitLab CI / GitLab Runner
- Docker / Docker Compose
- Flask / Python
- SonarQube
- Bandit
- Trivy
- OWASP ZAP

## 3. Kiến trúc DevSecOps Pipeline

Pipeline bao gồm:
1. Build
2. Test
3. SAST
4. Docker Build
5. Image Scan
6. Deploy
7. DAST

## 4. Kịch bản thử nghiệm

### Pipeline Failed
- SQL Injection
- Hardcoded Secrets
- XSS
- Vulnerable Docker Images

### Pipeline Passed
- Parameterized Queries
- Environment Variables
- XSS Protection
- Secure Container Configuration

## 5. Hướng dẫn triển khai

```bash
docker network create devsecops_net
docker compose up -d
```

## Access

- Web App: http://localhost:5000
- SonarQube: http://localhost:9000
