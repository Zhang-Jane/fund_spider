import datetime
import logging
from scrapy.exceptions import NotConfigured
from twisted.internet import task
from scrapy import signals

logger = logging.getLogger(__name__)


class MonitorStat(object):
    """
    An extension monitor spider rate
    """

    @classmethod
    def from_crawler(cls, crawler):
        interval = crawler.settings.getfloat('LOGSTATS_INTERVAL')  # 日志间隔时间
        ding_channel = crawler.settings.get('DING_CHANNEL')  # 通知的对象
        if not interval:
            raise NotConfigured
        o = cls(crawler.stats, interval, ding_channel)
        crawler.signals.connect(o._spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o._spider_closed, signal=signals.spider_closed)
        return o

    def __init__(self, stats, interval, ding_channel):
        self.last_success_count = 0  # 上一次成功200数量统计
        self.last_received_count = 0  # 上一次请求成功的数量统计
        self.last_item_count = 0  # 上一次成功入库的数量统计
        self.stats = stats
        self.interval = interval
        self.ding_channel = ding_channel

    def get_current_time(self):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    def _spider_opened(self, spider):
        self.task = task.LoopingCall(self._log, spider)
        self.task.start(self.interval)

    def _spider_closed(self, spider, reason):
        if self.task.running:
            self.task.stop()

    def _log(self, spider):
        current_time = self.get_current_time()
        current_success_count = self.stats.get_value('downloader/response_status_count/200', 0)
        current_received_count = self.stats.get_value('response_received_count', 0)
        received_count = current_received_count - self.last_received_count
        success_count = current_success_count - self.last_success_count

        # 统计成功每xx间隔时间，成功入库的速度
        item_count = self.stats.get_value('shop_goods_count', 0)
        add_items = item_count - self.last_item_count
        try:
            success_item_rate = round((add_items / received_count) * 100, 2)
        except ZeroDivisionError:
            success_item_rate = 0
        item_message = f"-- {current_time} scraped item success count: {add_items} , success rate is {success_item_rate}% --"
        spider.logger.info(item_message)

        # 统计成功每xx间隔时间，http code为200的速度，成功为200不一定成功返回数据
        try:
            success_200_rate = round((success_count / received_count) * 100, 2)
        except ZeroDivisionError:
            success_200_rate = 0
        success_message = f"-- {current_time} scraped code 200 success count: {success_count} , success rate is {success_200_rate}% --"
        spider.logger.info(success_message)
        if success_item_rate < 0.5 and success_200_rate < 0.5:
            pass

        self.last_success_count = current_success_count
        self.last_received_count = current_received_count
        self.last_item_count = item_count
