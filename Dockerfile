FROM python:3.13
RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED=1
WORKDIR /pythonproject
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
