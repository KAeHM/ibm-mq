FROM ubuntu

COPY ./downloads/ /tmp/
COPY ./setup.sh /tmp/
COPY ./venv.sh /tmp/

RUN sed -i -e 's/\r$//' /tmp/setup.sh
RUN sed -i -e 's/\r$//' /tmp/venv.sh

CMD ["/tmp/setup.sh"]
RUN [ "/bin/bash" ]