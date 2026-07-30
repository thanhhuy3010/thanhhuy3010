#!/bin/bash

# Di chuyển vào thư mục chứa script
cd "$(dirname "$0")"

# Kích hoạt môi trường ảo nếu tồn tại
if [ -d ".venv" ]; then
    echo "Đang kích hoạt môi trường ảo (.venv)..."
    source .venv/bin/activate
else
    echo "Cảnh báo: Không tìm thấy thư mục .venv. Sẽ chạy bằng python mặc định của hệ thống."
fi

# Chạy script gen hình
echo "Đang chạy local_gen.py..."
python3 local_gen.py

echo "Hoàn tất!"
