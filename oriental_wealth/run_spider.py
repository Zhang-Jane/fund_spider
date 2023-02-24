import logging
import os
import platform
import time
import subprocess
import datetime


def get_current_project_settings():
    """
    判断当前系统，选用不同的scrapy settings配置文件,区分生产,本地环境
    :return:
    """
    system_current = platform.system()
    current_env = os.environ['SCRAPY_PROJECT']
    if current_env:
        logging.warning(
            f'##*current_scrapy.cfg，CurrentDev：{os.getenv("SCRAPY_PROJECT")}')
    elif system_current == 'Windows':
        os.environ['SCRAPY_PROJECT'] = "dev"
        logging.warning(
            f'##*current_scrapy.cfg，WindowsDev：{os.getenv("SCRAPY_PROJECT")}')
    else:
        os.environ['SCRAPY_PROJECT'] = "default"
        logging.warning(
            f'##*current_scrapy.cfg，CompanyLinux：{os.getenv("SCRAPY_PROJECT")}')


def run_spider(spider_name, pools=1):
    """
    注意：使用多进程的启动
    使用subprocess启动scrapy
    2>&1：表示错误返回值传递给1输出通道，1表示标准输出，2表示标准错误输出
    Args:
        spider_name: 启动的爬虫名称
        pools: 启动的进程数, 默认1
    """
    get_current_project_settings()
    subpros = []
    # s1 = 'scrapy crawl {} >/dev/null 2>&1'.format(spider_name)
    crawler_batch_id = datetime.datetime.now().strftime('%Y-%m-%d')
    for num in range(pools):
        cmd = f"scrapy crawl {spider_name} -a crawler_batch_id='{crawler_batch_id}'"
        subpro = subprocess.Popen(cmd, shell=True, stdout=None)
        subpros.append(subpro)
        time.sleep(0.1)
    for por in subpros:
        por.wait()


if __name__ == '__main__':
    spider_list = [
        # "dongfang_funds",
        # "fund_rate_info",
        "fund_units_cumulative_equity"
    ]
    for spider_name in spider_list:
        run_spider(spider_name, 1)
