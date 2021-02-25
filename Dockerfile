FROM nginx:1.19.6

#RUN ufw allow 'Nginx Full' && ufw allow OpenSSH && ufw enable && ufw status && systemctl start nginx

#RUN rm /etc/nginx/sites-enabled/default

COPY nginx_default/default /etc/nginx/sites-enabled/

#RUN sudo systemctl start nginx
