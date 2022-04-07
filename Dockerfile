FROM eoxa/eoxserver:latest

RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev python-dev

ADD requirements.txt .

RUN pip3 install -r requirements.txt

RUN sed -i "s/geos_version().decode()/geos_version().decode().split(' ')[0]/g" /usr/local/lib/python3.8/dist-packages/django/contrib/gis/geos/libgeos.py

WORKDIR /home/ogc

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP edc_ogc/app.py
COPY edc_ogc/. edc_ogc/.

ENTRYPOINT []
CMD ["flask", "run", "--host=0.0.0.0"]