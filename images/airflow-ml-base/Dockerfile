FROM python:3.6
RUN mkdir /build/
COPY requirements.txt /build/requirements.txt

RUN pip install --proxy http://squid.lvsi.loc:3128 -r /build/requirements.txt