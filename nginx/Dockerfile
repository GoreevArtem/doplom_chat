# Use an official Ubuntu base image
FROM ubuntu:latest

ENV NGINX_VERSION nginx-1.26.1

# Install required packages for building Nginx and ModSecurity
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpcre3 \
    libpcre3-dev \
    zlib1g \
    zlib1g-dev \
    libssl-dev \
    wget \
    git \
    libtool \
    automake \
    autoconf \
    pkg-config \
    libbrotli-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create nginx user and group
RUN groupadd -r nginx && useradd -r -g nginx nginx

# Create necessary directories for Nginx
RUN mkdir -p /var/log/nginx && \
    mkdir -p /usr/share/nginx/html && \
    mkdir -p /var/run/nginx && \
    chown -R nginx:nginx /var/log/nginx /usr/share/nginx/html /var/run/nginx

# Install ModSecurity
RUN git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity /opt/ModSecurity && \
    cd /opt/ModSecurity && \
    git submodule init && \
    git submodule update && \
    ./build.sh && \
    ./configure && \
    make && \
    make install

# Install ModSecurity Nginx connector
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git /opt/ModSecurity-nginx

# Download and build Nginx with Brotli and ModSecurity modules
RUN wget http://nginx.org/download/${NGINX_VERSION}.tar.gz && \
    tar -xzvf ${NGINX_VERSION}.tar.gz && \
    cd ${NGINX_VERSION} && \
    git clone --depth 1 https://github.com/google/ngx_brotli.git && \
    cd ngx_brotli && \
    git submodule update --init && \
    cd .. && \
    ./configure --with-compat --add-dynamic-module=./ngx_brotli --add-dynamic-module=/opt/ModSecurity-nginx --with-http_ssl_module && \
    make && \
    make install

# Copy custom Nginx configuration file
COPY nginx.conf /usr/local/nginx/conf/nginx.conf

# Copy ModSecurity configuration files
COPY modsecurity.conf /usr/local/nginx/conf/modsecurity.conf

# Copy OWASP CRS
RUN mkdir -p /usr/local/nginx/conf/crs
COPY crs /usr/local/nginx/conf/crs

EXPOSE 80

# Start Nginx server
CMD ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;"]
