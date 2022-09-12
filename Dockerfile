FROM python:3.10.4
LABEL org.opencontainers.image.authors="amir.rahwane@gmail.com"


ADD requirements.txt /
RUN pip install -r requirements.txt

ADD main.py /

EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1
CMD [ "python3" , "./main.py", "-l", "0.0.0.0" ]
