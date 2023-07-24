FROM ubuntu

COPY ./downloads/ /tmp/
COPY ./script.sh /tmp/

RUN sed -i -e 's/\r$//' /tmp/script.sh

CMD ["/tmp/script.sh"]
RUN [ "/bin/bash" ]
