import os
import time
import scrapy
from scrapy import Request
from oriental_wealth.utils.build_url_para import join_url_para
from oriental_wealth.utils.tasks import get_tasks


class FundUnitsCumulativeEquitySpider(scrapy.Spider):
    name = "fund_units_cumulative_equity"
    allowed_domains = ["*"]

    def __init__(self, crawler_batch_id, **kwargs):
        super().__init__(**kwargs)
        self.crawler_batch_id = crawler_batch_id
        self.logger.info(f"当前批次ID：{crawler_batch_id:=^30}")
        self.sub_path = "/FundMApi/FundNetDiagram.ashx"

    def start_requests(self):
        db_host = self.settings.attributes.get("MYSQL_HOST").value
        table = self.settings.attributes.get("FUND_DATA_TABLE").value
        database = self.settings.attributes.get("MYSQL_DATABASE").value
        port = self.settings.attributes.get("MYSQL_POST").value
        user = os.environ.get('MYSQL_USERNAME', '')
        passwd = os.environ.get('MYSQL_PASSWORD', '')
        fund_code_infos = get_tasks(
            db_host, database, table, port, user, passwd)
        for code, fund_name in fund_code_infos:
            params = {
                "FCODE": code,
                "RANGE": "y",
                "deviceid": "embeb",
                "plat": "Wap",
                "product": "EFund",
                "version": "3.0",
                "_": str(int(time.time() * 1000)),
            }
            base_url = self.settings.attributes.get("BASE_URL").value
            full_url = join_url_para(base_url, self.sub_path, params)
            yield Request(full_url, meta={"fund_name": fund_name, "code": code}, callback=self.parse_units, dont_filter=True)

    def parse_units(self, response):
        fund_name = response.meta.get("fund_name")
        code = response.meta.get("code")
        try:
            data = response.json()
        except Exception as e:
            raise Exception(f"{self.name} =》 {e}")
        item = {
            "crawler_batch_id": self.crawler_batch_id,
            "fund_code": code,
            "fund_name": fund_name,
            "name": self.name,
            "crawl_ts": int(time.time() * 1000),
            "response_data": data
        }
        yield item
