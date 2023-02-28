import datetime
import logging
import json
from scrapy.exceptions import NotConfigured
from twisted.internet import task
from scrapy import signals

logger = logging.getLogger(__name__)


class MonitorStat(object):
    """
    An extension monitor spider status
    """
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats, crawler)

    def __init__(self, stats, crawler):
        self.stats = stats
        self.crawler = crawler
        self.interval = crawler.settings.getfloat(
            'LOGSTATS_INTERVAL')  # 日志打印间隔的时间
        self.ding_channel = crawler.settings.get(
            'DING_CHANNEL')  # 消息通知的对象
        if not self.interval:
            raise NotConfigured
        cs = crawler.signals
        cs.connect(self._spider_opened, signal=signals.spider_opened)
        cs.connect(self._spider_closed, signal=signals.spider_closed)

    def get_current_time(self):
        """
        获取当前的时间
        :return:
        """
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    def handle_stat(self):
        """
        获取当前的实时的状态
        :return:
        """
        stats = self.crawler.stats.get_stats()
        d = {
            'current_time': self.get_current_time(),
            'dequeued': stats.get('scheduler/dequeued/redis', 0),
            'log_warning': stats.get('log_count/WARNING', 0),
            'requested': stats.get('downloader/request_count', 0),
            'request_bytes': stats.get('downloader/request_bytes', 0),
            'response': stats.get('downloader/response_count', 0),
            'response_bytes': stats.get('downloader/response_bytes', 0),
            'response_200': stats.get('downloader/response_status_count/200', 0),
            'response_301': stats.get('downloader/response_status_count/301', 0),
            'response_404': stats.get('downloader/response_status_count/404', 0),
            'responsed': stats.get('response_received_count', 0),
            'item': stats.get('item_scraped_count', 0),
            'depth': stats.get('request_depth_max', 0),
            'filtered': stats.get('bloomfilter/filtered', 0),
            'enqueued': stats.get('scheduler/enqueued/redis', 0),
            'spider_name': self.crawler.spider.name
        }
        return json.dumps(d)

    def _spider_opened(self, spider):
        """
        spider开启的时候调用
        :param spider:
        :return:
        """
        self.task = task.LoopingCall(self._log, spider)
        self.task.start(self.interval)

    def _spider_closed(self, spider, reason):
        """
        spider关闭的时候调用
        :param spider:
        :param reason:
        :return:
        """
        if self.task.running:
            self.task.stop()
        stats = self.handle_stat()

    def _log(self, spider):
        """
        爬虫的日志打印
        :param spider:
        :return:
        """
        stats = self.handle_stat()
        spider.logger.info(stats)
