FROM python:3.8

# Install dependencies
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN playwright install-deps
RUN playwright install

# copy code
COPY ./ /app
WORKDIR /app

# run
CMD ["python3", "main.py", "--broadcast" ]
