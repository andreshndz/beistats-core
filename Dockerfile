FROM python:3.10

ADD Makefile requirements.txt /beistats_core/
WORKDIR /beistats_core

RUN apt-get update -y
RUN pip install --quiet --upgrade pip
RUN make install
RUN pip install --quiet uvicorn

EXPOSE 80

COPY . /beistats_core

CMD uvicorn beistats_core.app:app --host 0.0.0.0 --workers=5  --port 80