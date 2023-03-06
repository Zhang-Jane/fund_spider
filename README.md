## 需求：
1. 抓取东方财富app中所有基金的相关信息内容
   - 费率 √
   - 原费率 √
   - 单位净值走势 √
   - 累计净值走势 √
2. 爬取的数据保存至本地服务器的mysql数据库
3. 将该爬虫项目在docker中部署并运行并输出docker部署文档。

## 调研
1. 基金的分类，排行以及搜索功能
2. 基金的详情

## 遇到的问题
1. Android证书ssl校验，导致无法直接进行抓包（解决思路，通过hook校验的底层库，直接绕过）
2. Windows系统下Scrapy2.8版本
## 抓取的思路
1. 根据需求`所有的基金`意味着要尽可能地多和广，不用在乎细致地分类区别
2. 根据基金开始和结束时间，意味着任务不用一直持续的进行。任务可以分为频繁地更新和不频繁地更新
3. 根据时间设定一个批次id，便于数据的检验以及计算。

## 说明
scrapy的配置的优先级
```python
SETTINGS_PRIORITIES = {
    'default': 0,
    'command': 10,
    'project': 20,
    'spider': 30,
    'cmdline': 40,
}
```
配置环境：
1. local_settings.py(开发环境)
2. settings.py(部署环境)
## 创建表的sql
```sql
CREATE TABLE IF NOT EXISTS `funds`(
   `fund_id` INT UNSIGNED AUTO_INCREMENT,
   `fund_title` VARCHAR(100),
   `info` Text,
   PRIMARY KEY ( `fund_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `fund_rate_info`(
   `fund_id` INT UNSIGNED AUTO_INCREMENT,
   `fund_title` VARCHAR(100),
   `info` Text,
   PRIMARY KEY ( `fund_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `fund_units_cumulative_equity`(
   `fund_id` INT UNSIGNED AUTO_INCREMENT,
   `fund_title` VARCHAR(100),
   `info` Text,
   PRIMARY KEY ( `fund_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
## Docker

### 第一步：构建开发环境的镜像

```bash
docker build -f Dockerfile文件的目录 -t 名称：标签
docker build -f --no-cache . -t oriental_wealth:v1

docker run  -it  --name  oriental_wealth  oriental_wealth:v1  /bin/bash
```

### 第二部：制作docker-compose

