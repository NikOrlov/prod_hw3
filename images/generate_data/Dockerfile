#FROM python
#
#
#COPY main.py /main.py
#COPY requirements.txt /requirements.txt
#RUN pip install -r requirements.txt
#
##CMD ["python", "main.py", "/data/raw/345"]
#ENTRYPOINT ["python", "main.py"]

FROM my_ml_base_image

COPY main.py /main.py

ENTRYPOINT ["python", "main.py"]