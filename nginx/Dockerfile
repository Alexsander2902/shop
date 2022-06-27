#FROM nginx
FROM owasp/modsecurity:nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY /crs/rules /etc/modsecurity/crs/rules
COPY crs-setup.conf /etc/modsecurity/crs
RUN echo '# OWASP CRS v3 rules' >> /etc/modsecurity.d/setup.conf
RUN echo 'Include /etc/modsecurity/crs/crs-setup.conf' >> /etc/modsecurity.d/setup.conf
RUN echo 'Include /etc/modsecurity/crs/rules/*.conf' >> /etc/modsecurity.d/setup.conf
