FROM python:3.11
EXPOSE 8888
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY . .

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]