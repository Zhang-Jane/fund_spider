from urllib.parse import urlencode
from urllib.parse import urljoin


def join_url_para(base_url: str, sub_path: str, para: dict):
    url = urljoin(base_url, sub_path)
    return url + "?" + urlencode(para)
