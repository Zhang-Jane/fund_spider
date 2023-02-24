from urllib.parse import urlparse, unquote


def show_query(url):
    """
    查看url的各个参数
    :param url:
    :return:
    """
    query = urlparse(url).query
    query_list = query.split("&")
    for para in query_list:
        print("-" + para)
        k, v = para.split("=")
        print("+" + k + ":" + unquote(v, "utf-8"))


def build_query(url):
    query = urlparse(url).query
    query_list = query.split("&")
    print("{")
    for para in query_list:
        k, v = para.split("=")
        print("    " + repr(k).replace('\'', '"') + ":" + " " +
              repr(unquote(v, "utf-8")).replace('\'', '"'), end=",\n")
    print("}")


if __name__ == '__main__':
    url = "https://daojia.jd.com/client?channel=wx_xcx&platform=5.0.0&platCode=mini&appVersion=5.0.0&xcxVersion=5.5.1&appName=paidaojia&functionId=station%2FgetRecommendList&isForbiddenDialog=true&isNeedDealError=true&isNeedDealLogin=false&body=%7B%22lgt%22%3A+%22100.99475%22%2C+%22lat%22%3A+%2236.9005%22%2C+%22cityId%22%3A+1%2C+%22currentPage%22%3A+1%2C+%22dataSize%22%3A+20%2C+%22storeId%22%3A+%22%22%7D&afsImg=&lat_pos=36.9005&lng_pos=100.99475&lat=36.9005&lng=100.99475&city_id=1&deviceToken=e52ca79c-5954-4b13-89c0-300f202d30f6&deviceId=e52ca79c-5954-4b13-89c0-300f202d30f6&deviceModel=appmodel&business=&traceId=e52ca79c-5954-4b13-89c0-300f202d30f61604545287909"
    build_query(url)
