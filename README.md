# BÁO CÁO NỘP BÀI TẬP LỚN
# I. Thông tin Repository
GitHub Repository (Private):
https://github.com/quybuithanh/Mushroom-Classification

# II. Link video demo: 
https://drive.google.com/file/d/11leD89pzBbjEUeofhycSEgUfFm5-CjOo/view?usp=drive_link

# III. Phân công công việc

| Họ và tên     | MSSV       | Công việc                                               | Đóng góp |
| ------------- | ---------- | ------------------------------------------------------- | -------: |
| Vũ Tiến Đạt   | 2451012024 | - Xây dựng và hoàn thiện giao diện Streamlit            |     100% |
                             | - Đóng gói toàn bộ hệ thống bằng Docker                 |          |
                             | - Chỉnh cấu hình môi trường chạy cho FastAPI, MySQL và  |          |
                             |Streamlit                                                |          |
                             | - Kiểm thử, sửa lỗi                                     |          |
                             | - Viết README, hướng dẫn chạy dự án                     |          |
|----------------------------|---------------------------------------------------------|          |
| Bùi Thanh Quý | 2451012083 | - Khởi tạo dự án và cấu trúc ban đầu                    |    100%  |
                             | - Tiền xử lý dữ liệu                                    |          |
                             | - Feature Engineering                                   |          |
                             | - Train model                                           |          |
                             | - Viết README                                           |          |
|----------------------------|---------------------------------------------------------|----------|
| Đỗ Ngọc Tuấn  | 2451012126 | - Xây dựng FastAPI và các API                           |     100% |
                             | - Kết nối API với cơ sở dữ liệu và mô hình              |          |
                             | - Kiểm thử API, sửa lỗi và tích hợp mô hình vào hệ thống|          |
                             | - Hoàn thiện các chức năng trước khi bàn giao           |          |
|----------------------------|---------------------------------------------------------|----------|

# IV. Khai báo sử dụng AI
Nhóm có sử dụng công cụ AI trong quá trình thực hiện bài tập.

| Công cụ | Mục đích sử dụng                                                            |
| ------- | --------------------------------------------------------------------------- |
| ChatGPT | Giải thích lỗi, tối ưu code, viết README, hỗ trợ Docker, FastAPI, Streamlit |
| Gemini  | Kiểm tra, sửa lỗi, tối ưu code                                              | 
| Claude  | Kiểm tra, sửa lỗi, tối ưu code                                              |


# V. Model Artifact
File model được lưu trong project:

models/
|- best_model.pkl
|- encoders.pkl

## Cách load model
import joblib

model = joblib.load("models/best*model.pkl")
print("Loại model:", type(model))
print("Thông số:")
print(model.get_params())
encoders = joblib.load("models/encoders.pkl")
print("\nCác encoder:")
print(encoders.keys())
print("\nGiá trị của cap_shape:")
print(encoders["cap_shape"].classes*)


# Mushroom-Classification
* Mô tả bài toán: Phân loại nấm là ăn được hay độc từ 22 đặc trưng hình thái phân loại (màu mũ, mùi, hình thái phiến nấm…). Dữ liệu thuần phân loại, lý tưởng để thực hành mã hóa biến và cây quyết định; có thể đạt độ chính xác gần như tuyệt đối.

1. Quy trình hoạt động
- MySQL: lưu lịch sử mỗi lần dự đoán
- API (FastAPI): nhận dữ liệu về cây nấm, dùng model đã train để dự đoán ăn được hay có độc và lưu kết quả vào MySQL 
- Giao diện web (Streamlit): cho người dùng nhập dữ liệu, gửi yêu cầu cho API và hiển thị kết quả dự đoán
- Docker: đóng gói toàn bộ hệ thống, chỉ cần một lệnh để khởi động mà không cần cài đặt thủ công MySQL hay thư viện python

2. Cấu trúc dự án
Mushroom-Classification/
|- api/                  # Chứa các phần xử lý chính của API
|- data/                 # Lưu bộ dữ liệu dùng để huấn luyện model
|- models/               # Lưu model đã huấn luyện và các file hỗ trợ
|- notebooks/            # Các notebook dùng để phân tích dữ liệu, tiền xử lý và train model
|- src/                  # Chứa các hàm xử lý dữ liệu dùng chung
|- .dockerignore         # Bỏ qua các file không cần thiết khi docker tạo image
|- docker-compose.yml    # Khởi động toàn bộ hệ thống bằng docker
|- Dockerfile            # Cấu hình tạo image cho API
|- Dockerfile.streamlit  # Cấu hình tạo image cho giao diện streamlit
|- mushroom_db.sql       # File tạo cơ sở dữ liệu mySQL
|- README.md             # Hướng dẫn chạy dự án
|- requirements.txt      # Danh sách các thư viện cần cài
|- streamlit_app.py      # File chạy giao diện web

3. Cách chạy dự án
a) Chạy bằng docker
B1. Cài đặt và mở Docker Desktop
B2. Mở terminal trong thư mục dự án và gõ "docker compose up --build", lệnh này sẽ khởi động và kết nối MySQL, API và giao diện web với nhau
B3. Truy cập giao diện web bằng đường link: http://localhost:8501 và tài liệu API bằng http://localhost:8000/docs
B4. Thực hiện các tác vụ
B5. Gõ "docker compose down" tại terminal để dừng hệ thống

b) Chạy thủ công
B1. Cài đặt Python và MySQL
B2. Tạo cơ sở dữ liệu để lưu lịch sử dự đoán
B3. Cài các thư viện trong python 
B4. Mở terminal và gõ "python -m uvicorn api.app:app --reload" để chạy API
B5. Mở cửa sổ terminal khác và gõ "streamlit run streamlit_app.py" để chạy giao diện

4. Mô hình đã huấn luyện
- Model đã được huấn luyện và lưu trong thư mục models/, có thể sử dụng ngay mà không cần train lại
- File model_metadata.json lưu thông tin về loại model, độ chính xác và thời điểm huấn luyện

5. Các API hỗ trợ
- GET/ : Kiểm tra xem API có đang chạy không
- GET/health: Cũng để kiểm tra xem API có đang chạy không
- GET/model-info: Xem thông tin về model coi nó thuộc loại nào, quan tâm nhiều nhất tới đặc điểm nào của cây nấm
- POST/predict: Gửi lên đặc điểm của 1 cây nấm và nhận lại kết quả ăn được hay có độc
- POST/predict/batch: Giống POST/predict nhưng gửi nhiều cây nấm cùng lúc để xử lý và lưu tất cả trong 1 lần, nên nhanh hơn nhiều so với gửi từng cây một
- GET/history: Giúp lại lịch sử các lần dữ đoán trước đó
- DELETE/history: Xóa lịch sử các lần dự đoán đã lưu
- GET/stats: Giúp xem tổng cộng đã đoán bao nhiêu lần, bao nhiêu lần ra "ăn được", bao nhiêu lần ra "có độc"

6. Chức năng của giao diện web
- Trang chủ/Dashboard: Giúp xem tổng cộng đã đoán bao nhiêu lần, bao nhiêu lần ra "ăn được", bao nhiêu lần ra "có độc" và có nút để xóa tất cả lịch sử dự đoán nếu muốn làm lại từ đầu
- Dự đoán: Chọn từng đặc điểm của 1 cây nấm qua các ô lựa chọn, sau đó bấm nút để hiện kết quả 
- Thông tin model: Hiển thị thông tin về mô hình đã huấn luyện như tên thuật toán, độ chính xác và các đặc trưng quan trọng mà model sử dụng để đưa ra dự đoán.
- Lịch sử: Hiển thị danh sách các lần dự đoán và có thể tải lịch sử dự đoán về dưới dạng CSV hoặc Excel
- Dự đoán hàng loạt: Thay vì nhập từng cây một thì có thể nhập nhiều dòng cùng lúc hoặc tải lên 1 file danh sách (.csv), hệ thống sẽ dự đoán toàn bộ trong 1 lượt rồi rồi trả danh sách kết quả dự đoán

7. Các tệp Docker
- Dockerfile: Dùng để tạo docker image cho API FastAPI, cài đặt môi trường và các thư viện cần thiết để API có thể chạy
- Dockerfile.streamlit: Dùng để tạo docker image cho giao diện streamlit, cài đặt các thư viện và cấu hình để chạy giao diện web
- docker-compose.yml: Dùng để khởi động và kết nối các container MySQL, FastAPI và Streamlit, chỉ cần gõ "docker compose up --build" ở terminal trong thư mục dự án là toàn bộ hệ thống sẽ hoạt động
