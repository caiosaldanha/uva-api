FROM nginx:alpine

# Copy custom configuration
COPY default.conf /etc/nginx/conf.d/default.conf

# Uncomment the lines below if you have SSL certificate/key files to copy
COPY cert.crt /etc/nginx/certs/cert.crt
COPY cert.key /etc/nginx/certs/cert.key
