ARG ARCH="amd64"
ARG OS="linux"
LABEL maintainer="Justinas Balinskas <justinas.balinskas@gmail.com>"

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9118
CMD [ "python", "./your-daemon-or-script.py" ]
