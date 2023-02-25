import re
import time
import scrapy
from scrapy import Request
from re import Match
from fake_useragent import UserAgent
from oriental_wealth.utils.build_url_para import join_url_para


class FundsSpider(scrapy.Spider):
    name = "dongfang_funds"
    allowed_domains = ["*"]
    # 这里配置的优先级高于全局
    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 0.1,
        "DOWNLOAD_TIMEOUT": 4,
        "RETRY_TIMES": 3,
    }

    def __init__(self, crawler_batch_id, **kwargs):
        super().__init__(**kwargs)
        self.crawler_batch_id = crawler_batch_id
        self.logger.info(f"当前批次ID：{crawler_batch_id:=^30}")
        self.sub_path = "/FundMNewApi/FundMNRankNewList"

    def start_requests(self):
        fund_types = self.settings.attributes.get("FUND_TYPES").value
        for fund_type, id in fund_types.items():
            params = {
                "pageIndex": "1",
                "pageSize": "30",
                "Sort": "desc",
                "SortColumn": "RZDF",  # DWJZ：最新净值排序，RZDF：日涨幅
                "FundType": id,
                "SYL": "RZDF",
                "deviceid": "embeb",
                "plat": "Wap",
                "product": "EFund",
                "version": "3.0",
                "_": str(int(time.time() * 1000)),
            }
            base_url = self.settings.attributes.get("BASE_URL").value
            full_url = join_url_para(base_url, self.sub_path, params)
            yield Request(full_url, meta={"type": fund_type}, callback=self.parse, dont_filter=True)

    def replace(self, matched: Match):
        """
        :param matched: re.Match对象
        :return: str
        """
        group_str = matched.group("page")
        int_num = int(group_str)
        if int_num >= 1:
            int_num += 1
        added_value = "pageIndex=" + str(int_num)
        added_value_str = str(added_value)
        return added_value_str

    def start_next_page(self, response):
        next_url = response.meta.get("next_url")
        fund_type = response.meta.get("type")
        print(f"==============={next_url}")
        yield Request(next_url, meta={"type": fund_type}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        fund_type = response.meta.get("type")
        current_url = response.url
        try:
            data = response.json()
        except Exception as e:
            raise Exception(f"{self.name} =》 {e}")
        # 如果请求的下一页接口还有数据
        datas = data.get("Datas")
        if datas:
            for data_info in datas:
                item = {
                    "crawler_batch_id": self.crawler_batch_id,
                    "fund_type": fund_type,
                    "name": self.name,
                    "fund_name": data_info.get("SHORTNAME"),
                    "fund_code": data_info.get("FCODE"),
                    "crawl_ts": int(time.time() * 1000),
                }
                yield item
            next_url = re.sub(
                r"pageIndex=(?P<page>\d+)",
                self.replace,
                current_url)

            yield Request(next_url, meta={"type": fund_type, "next_url": next_url}, callback=self.start_next_page, dont_filter=True)

