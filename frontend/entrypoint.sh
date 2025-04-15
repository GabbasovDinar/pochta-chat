#!/bin/sh
# Substitute environment variables in the config template and generate config.js
envsubst '${BASE_URL}' < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js
# Start nginx in the foreground
exec nginx -g "daemon off;"
