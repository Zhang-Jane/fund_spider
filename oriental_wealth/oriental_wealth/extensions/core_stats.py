"""
Extension for collecting core stats like items scraped and start/finish times
"""
import time
from scrapy import signals


class CoreStats:

    def __init__(self, stats):
        self.stats = stats
        self.start_time = None

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(o.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(o.response_received, signal=signals.response_received)
        return o

    # def spider_opened(self, spider):
    #     self.start_time = datetime.utcnow()
    #     self.stats.set_value('start_time', self.start_time, spider=spider)
    #
    # def spider_closed(self, spider, reason):
    #     finish_time = datetime.utcnow()
    #     elapsed_time = finish_time - self.start_time
    #     elapsed_time_seconds = elapsed_time.total_seconds()
    #     self.stats.set_value('elapsed_time_seconds', elapsed_time_seconds, spider=spider)
    #     self.stats.set_value('finish_time', finish_time, spider=spider)
    #     self.stats.set_value('finish_reason', reason, spider=spider)

    def spider_opened(self, spider):
        # 源码
        # self.stats.set_value('start_time', datetime.datetime.utcnow(), spider=spider)
        self.start = time.time()
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start))  # 转化格式
        self.stats.set_value('start_time', '开始时间  --  {}'.format(start_time), spider=spider)

    def spider_closed(self, spider, reason):
        # 源码
        # self.stats.set_value('finish_time', datetime.datetime.utcnow(), spider=spider)
        # self.stats.set_value('finish_reason', reason, spider=spider)
        self.end = time.time()
        finish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.end))  # 转化格式
        self.stats.set_value('finish_time', '结束时间  --  {}'.format(finish_time), spider=spider)
        self.stats.set_value('finish_reason', reason, spider=spider)

        # 运行总耗时，时:分:秒
        Total_time = self.end - self.start
        m, s = divmod(Total_time, 60)
        h, m = divmod(m, 60)
        self.stats.set_value('Total_time', "总耗时  --  %d时:%02d分:%02d秒" % (h, m, s), spider=spider)
        
    def item_scraped(self, item, spider):
        self.stats.inc_value('item_scraped_count', spider=spider)

    def response_received(self, spider):
        self.stats.inc_value('response_received_count', spider=spider)

    def item_dropped(self, item, spider, exception):
        reason = exception.__class__.__name__
        self.stats.inc_value('item_dropped_count', spider=spider)
        self.stats.inc_value(f'item_dropped_reasons_count/{reason}', spider=spider)
