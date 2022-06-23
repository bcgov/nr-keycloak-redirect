FROM python:alpine3.15

COPY . .
RUN apk add bash && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT [ "/bin/bash", "./entrypoint.sh" ]
