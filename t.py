# server {
#     listen 80;
#     server_name hit-travel.org;

#     location = /favicon.ico { access_log off; log_not_found off; }

#     location /static/ {
#         root /home/chyngyz/hit-travel;
#     }

#     location  /media/ {
#         root /home/chyngyz/hit-travel;
#     }

#     location / {
#         add_header 'Access-Control-Allow-Origin' '*';
#         add_header 'Access-Control-Allow-Credentials' 'true';
#         add_header 'Access-Coptrol-Allow-Methods' 'GET, HEAD, OPTIONS, POST, PUT, PATCH, DELETE';
#         add_header 'Access-Control-Allow-Headers' 'Access-Control-Allow-Headers, Access-Control-Request-Method, Access-Control-Request-Header, Origin, Content-Type, Accept, Authorization, X-Requested-With, Set-cookie';
#         add_header 'Allow' 'GET, HEAD, OPTIONS, POST, PUT, PATCH, DELETE';

#         include proxy_params;
#         proxy_pass http://unix:/home/chyngyz/hit-travel/config.sock;
#     }
# }