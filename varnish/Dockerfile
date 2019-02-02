FROM alpine

RUN apk add varnish

ENV VARNISH_PORT 8080
ENV VARNISH_CACHE_SIZE "64m"

WORKDIR /varnish
COPY ./config.vcl ./ 

CMD ["sh", "-c", "varnishd -F -f /varnish/config.vcl -s malloc,$VARNISH_CACHE_SIZE -a :$VARNISH_PORT"]
