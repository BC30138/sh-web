FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
COPY .ssl/stanethuzhe.ru.crt /etc/ssl/stanethuzhe.ru.crt
COPY .ssl/stanethuzhe.ru.key /etc/ssl/stanethuzhe.ru.key
COPY docker/nginx/app.conf /etc/nginx/conf.d