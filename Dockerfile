FROM python:latest

WORKDIR /app

COPY app.py /app/
COPY compare /app/compare/
COPY static /app/static/
COPY templates /app/templates/
COPY uploads /app/uploads/
COPY requirements.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

CMD [ "python" ,"./app.py" ]