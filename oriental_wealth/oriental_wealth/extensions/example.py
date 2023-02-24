from scrapy import signals


class SelfExtensions(object):
    """
    engine_started = object()               # 引擎启动时
    engine_stopped = object()               # 引擎停止时
    spider_opened = object()                # 爬虫启动时
    spider_idle = object()                  # 爬虫闲置时
    spider_closed = object()                # 爬虫停止时
    spider_error = object()                 # 爬虫错误时
    request_scheduled = object()            # 请求放入调度器
    request_dropped = object()              # 丢弃请求
    request_reached_downloader = object()   # response下载时
    response_received = object()            # 响应被接收
    response_downloaded = object()          # 响应被下载
    item_scraped = object()                 # 获得item
    item_dropped = object()                 # 丢弃item
    item_error = object()                   # 异常item
    """

    def __init__(self, crawler):
        self.crawler = crawler
        self.crawler.signals.connect(self.start, signals.engine_started)
        self.crawler.signals.connect(self.stop, signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def start(self):
        print("signals.engine_started --- start")

    def stop(self):
        print("signals.engine_stopped --- stopped")
