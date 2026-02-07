FROM python:3.11-slim
WORKDIR /app
COPY app.py .
COPY static ./static
RUN pip install flask requests
EXPOSE 5000
CMD ["python","app.py"]
