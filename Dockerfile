# pull official base image
FROM python:3.8.0-alpine
# set work directory
WORKDIR /usr/src/app
#add google secrets
ENV SECRETS_INIT_VERSION=v0.2.12
ENV SECRETS_INIT_URL=https://github.com/doitintl/secrets-init/releases/download/$SECRETS_INIT_VERSION/secrets-init_Linux_amd64.tar.gz
ENV SECRETS_INIT_SHA256=3abc42a40600fcb914ae7f7ec2d6029724bc59a3129b78d756194838572bc615
RUN mkdir -p /opt/secrets-init && cd /opt/secrets-init \
    && wget -qO secrets-init.tar.gz "$SECRETS_INIT_URL" \
    && echo "$SECRETS_INIT_SHA256  secrets-init.tar.gz" | sha256sum -c - \
    && tar -xzvf secrets-init.tar.gz \
    && mv secrets-init /usr/local/bin \
    && rm secrets-init.tar.gz


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip install -r requirements.txt
# copy project
COPY . /usr/src/app/
RUN chmod +x docker-entrypoint.sh
EXPOSE 5000
RUN ls -la app/
CMD ["/usr/local/bin/secrets-init", "--provider=google", "/usr/src/app/docker-entrypoint.sh"]
