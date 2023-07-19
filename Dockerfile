FROM python:3.9-alpine
COPY . .
RUN pip install -r requirements.txt && \
    apk add --no-cache tzdata
CMD ["python", "main.py"]