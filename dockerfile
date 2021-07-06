FROM python:3.9
RUN apt-get update \
    &&apt-get -y install freetds-dev \
    &&apt-get -y install unixodbc-dev 
COPY . .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

CMD supervisord -c supervisord.conf -n