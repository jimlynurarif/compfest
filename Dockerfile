# Gunakan image Python sebagai base
FROM python:3.9

# Set work directory
WORKDIR /app

# Salin requirements.txt ke dalam container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke dalam container
COPY . /app

# Tentukan port yang digunakan oleh aplikasi Flask
EXPOSE 5000

# Tentukan command untuk menjalankan aplikasi
CMD ["python", "app.py"]
