# 小说爬虫

git clone https://github.com/MonkeyOnFire/scrapydemo.git
docker build -t yousuu:v1 ./scrapydemo/
docker run -itd -v /root/tmp:/scrapydemo/scrapydemo/log -v /etc/localtime:/etc/localtime:ro --name yousuulist --net proxypool_default --restart=always yousuu:v1
docker run -itd -v /root/tmp:/scrapydemo/scrapydemo/log -v /etc/localtime:/etc/localtime:ro --name yousuubook --net proxypool_default --restart=always yousuu:v1 sh -c "chmod 777 run.py && ./run.py"