FROM python:3.10.4-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD streamlit run 0_🏠_Home.py