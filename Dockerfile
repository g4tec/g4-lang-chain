FROM python:3.11-alpine

LABEL maintainer "Roman Dodin <dodin.roman@gmail.com>"
LABEL description "Lang chain Service with Flask"

# Copy python requirements file
COPY requirements.txt /tmp/requirements.txt

# Install necessary packages and build dependencies
RUN apk add --no-cache \
    bash \
    nginx \
    uwsgi \
    uwsgi-python3 \
    supervisor \
    libffi-dev \
    gcc \
    musl-dev \
    make \
    python3-dev \
    openssl-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools wheel
    # rm /etc/nginx/conf.d/default.conf && \
    # rm -r /root/.cache

# Install specific version of opencv-python
RUN pip3 install numpy
RUN pip3 install opencv-python==4.8.0.74
RUN pip3 install -r /tmp/requirements.txt 

# Copy the Nginx global conf
COPY nginx.conf /etc/nginx/
# Copy the Flask Nginx site conf
COPY flask-site-nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY supervisord.conf /etc/supervisord.conf

# Add demo app
COPY ./app /app
WORKDIR /app

CMD ["/usr/bin/supervisord"]
