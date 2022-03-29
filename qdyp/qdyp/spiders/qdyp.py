import scrapy
from scrapy import Request
import json
from qdyp.items import QdypItem

class QdypSpider(scrapy.Spider):
    name = 'qdyp'
    allowed_domains = ['qidian.com']
    #起点M.qidian.com反爬：每个cookies只能爬16个页面，需设置禁止dont_merge_cookies
    start_urls = ' https://m.qidian.com/majax/rank/yuepiaolist?_csrfToken=IpoVuIEkJw8kIImg60tAuc3c5MO0NBdahkHTFglG&gender=male&pageNum={pageNum}&catId=-1'
    start_page = 1
    end_page = 200
    #cookies = {'___rl__test__cookies': '1623236772391', ' newstatisticUUID': '1588910339_889360335', ' qdrs': '0%7C3%7C0%7C0%7C1', ' showSectionCommentGuide': '1', ' qdgd': '1', ' _csrfToken': 'OSEDHyZKH6C89IXTApimdbSiQAC0wZUIAnOLnW7N', ' lrbc': '1019845744%7C524743171%7C0%2C1028045047%7C654454986%7C0%2C1011452759%7C406124178%7C0', ' rcr': '1019845744%2C1028045047%2C1025230752%2C1013218690%2C1445033%2C1027582783%2C1027073436%2C1018216002%2C1021800771%2C1023422452%2C1023338233%2C1022069596%2C1023501483%2C1023715291%2C1017597974%2C1015890279%2C1022576776%2C1023873138%2C1024544333%2C1023562168%2C1012026774%2C1013290743%2C1015042011%2C1015179225%2C1012390525%2C1015102783%2C1015106587%2C1013861765%2C1436555%2C1013026063%2C1014265314%2C1011121310%2C1011718497%2C3119617%2C1011816096%2C1012208137%2C1012490256%2C1011452759', ' hiijack': '0', ' _yep_uuid': '1136bad6-ab1d-cea6-a311-7f18749916a5', ' OUTFOX_SEARCH_USER_ID_NCOO': '309780546.3640947', ' gender': 'male', ' ywkey': 'ywP4QMfOomX6', ' ywguid': '800124720485', ' ywopenid': 'C7E73E7FBBD57802272AA2FB3DB04724', ' ___rl__test__cookies': '1623237094664', ' e1': '%7B%22pid%22%3A%22mqd_P_qidianm%22%2C%22eid%22%3A%22mqd_A12%22%2C%22l1%22%3A3%7D', ' e2': '%7B%22pid%22%3A%22mqd_P_user%22%2C%22eid%22%3A%22mqd_G14%22%2C%22l1%22%3A41%7D'}



    def start_requests(self):
        for i in range(self.start_page, self.end_page + 1):
            print('正在爬取月票榜第{}页'.format(i))
            yield Request(self.start_urls.format(pageNum=str(i)), callback=self.parse_yp,meta = {'dont_merge_cookies': True})

    def parse_yp(self,response):
        #print(response.text.encode('latin-1').decode('unicode_escape'))
        try:
            ypbooks = json.loads(response.text.encode('latin-1').decode('unicode_escape'))['data']['records']
        except KeyError:
            print('爬取失败，原因未知')
            print(json.loads(response.text.encode('latin-1').decode('unicode_escape')))
        
        #print(ypbooks)
        for book in ypbooks:
            qdypItem = QdypItem()
            for field in book:
                qdypItem[field] = book[field]

                if field == 'rankCnt':
                    value = book['rankCnt'][:-2]
                    if value[-1] == '万':
                        tmp = int(float(value[:-1]) * 10000)
                        value = str(tmp)
                    qdypItem['rankCnt'] = value

                if field == 'cnt':
                    value = book['cnt'][:-1]
                    if value[-1] == '万':
                        tmp = int(float(value[:-1])*10000)
                        value = str(tmp)
                    qdypItem['cnt'] = value
            yield qdypItem