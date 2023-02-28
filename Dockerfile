# 指定创建的基础镜像
FROM python:3.8-bullseye

# 替换pip源
RUN pip3 config set global.index-url https://pypi.douban.com/simple/

# 复制本地代码到容器内
ADD . /home/code/

# 安装python环境
RUN pip3 install --upgrade pip && \
    cd /home/code/ && \
    pip3 install -r requirements.txt

# 启动程序
WORKDIR /home/code/oriental_wealth/
CMD ["python3", "run_spider.py"]