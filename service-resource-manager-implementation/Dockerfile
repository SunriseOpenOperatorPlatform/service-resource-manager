FROM python:3.9-alpine

#RUN apk add git

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

#RUN apk add --no-cache --virtual .build-deps gcc musl-dev

#RUN apk update && apk add python3-dev \
#                        gcc \
#                        libc-dev


#THIS SOLVED THE ISSUE WITH CFFI: building wheel for cffi (setup.py) finished with status 'error'!
RUN apk add --no-cache libffi-dev build-base
#
COPY requirements.txt /usr/src/app/
#RUN pip3 install connexion

#ENV EMP_STORAGE_DRIVER mongo
#ENV EMP_STORAGE_URI mongodb://203.0.113.8:27017
#
#ENV PIP_ROOT_USER_ACTION=ignore
#
ENV PYTHONUNBUFFERED=1
#RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
#RUN python3 -m ensurepip

#RUN pip3 install --no-cache --upgrade pip setuptools

RUN pip3 install --upgrade pip

RUN pip3 install wheel

#RUN pip3 install --no-cache --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]

