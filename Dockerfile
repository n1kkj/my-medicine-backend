FROM python:3.12

ENV PYTHONUNBUFFERED=1


WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN pip install gunicorn


CMD ["gunicorn", "backend.wsgi:application", "-b", "0.0.0.0:8001"]