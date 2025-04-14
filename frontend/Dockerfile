# Use an official nginx image based on Alpine
FROM nginx:alpine

# Install gettext to use envsubst
RUN apk add --no-cache gettext

# Remove default nginx config if needed
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files including config.template.js
COPY . /usr/share/nginx/html

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

CMD ["/entrypoint.sh"]
