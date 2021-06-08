FROM python

COPY requirements.txt /requirements.txt

RUN pip install --proxy http://squid.lvsi.loc:3128 -r requirements.txt
