FROM python:3.7.3

RUN pip install --upgrade pip

ENV GEOS http://download.osgeo.org/geos/geos-3.5.1.tar.bz2

ENV PROCESSOR_COUNT 1

WORKDIR /install-postgis

WORKDIR /install-postgis/geos
ADD $GEOS /install-postgis/geos.tar.bz2
RUN tar xf /install-postgis/geos.tar.bz2 -C /install-postgis/geos --strip-components=1
RUN ./configure && make -j $PROCESSOR_COUNT && make install
RUN ldconfig
WORKDIR /install-postgis

COPY requirements.txt .

RUN pip install -U pip \
    && pip install --user -r requirements.txt

WORKDIR /app

COPY app .

EXPOSE 5002
CMD [ "python", "app.py" ]