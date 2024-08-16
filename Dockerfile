FROM ubuntu:22.04

LABEL maintainer "Roman Dodin <dodin.roman@gmail.com>"
LABEL description "Lang chain Service with Flask"

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Set timezone to avoid tzdata prompt
ENV TZ=Etc/UTC


# Install necessary packages and build dependencies
RUN apt-get update && apt-get install -y \
    tzdata \
    bash \
    nginx \
    uwsgi \
    uwsgi-plugin-python3 \
    supervisor \
    libffi-dev \
    gcc \
    make \
    python3-dev \
    python3-pip \
    openssl \
    build-essential \
    cmake \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*



# Upgrade pip and install necessary Python packages
RUN pip3 install --upgrade pip setuptools wheel

# Copy python requirements file
COPY requirements.txt /tmp/requirements.txt

RUN apt-get install -y uwsgi-plugin-python3


# Install Python packages
RUN pip3 install numpy opencv-python && \
    pip3 install -r /tmp/requirements.txt

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



# Add nginx group
RUN groupadd --system nginx && \
    adduser --system --no-create-home --shell /bin/false --ingroup nginx nginx

RUN groupadd --system uwsgi && \
useradd --system --gid uwsgi --no-create-home --shell /bin/false uwsgi

RUN chown -R uwsgi:uwsgi /app


WORKDIR /app

EXPOSE 8989

CMD ["/usr/bin/supervisord"]
