#!/bin/sh

# Replace $PORT in nginx configuration with the actual value from the environment
sed -i "s/\$PORT/${PORT}/g" /etc/nginx/conf.d/nginx.conf

# Start Nginx in the foreground
nginx -g 'daemon off;'