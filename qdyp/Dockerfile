FROM python:3.8
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Scrapy==2.4.1 requests==2.25.1 Twisted==20.3.0 PyMySQL==1.0.2 scrapy-redis==0.6.8 fake-useragent==0.1.11
COPY . /qdyp
WORKDIR /qdyp
#VOLUME ["/scrapydemo/scrapydemo/log"]
CMD scrapy crawl qdyp

#不会每次修改代码重新build时都要pip

# FROM python:3.8
# COPY . /scrapydemo
# WORKDIR /scrapydemo
# VOLUME ["/scrapydemo/scrapydemo/log"]
# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt && chmod 777 run.py
# CMD ./run.py yousuubooklist