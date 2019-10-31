FROM ubuntu:18.04

# install OS dependency packages
RUN apt-get update && \
  apt-get install -y \
    python3 \
    python3-pip \
    python3-gdal \
    gdal-bin && \
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/partial/* /tmp/* /var/tmp/*

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD eoxserver eoxserver
RUN cd eoxserver && \
  pip3 install .

WORKDIR /home/ogc

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP edc_ogc/app.py
COPY edc_ogc/. edc_ogc/.

CMD ["flask", "run", "--host=0.0.0.0"]