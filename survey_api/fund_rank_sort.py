import requests

headers = {
    'Host': 'fundmobapi.eastmoney.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 8 Lite Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.65 Mobile Safari/537.36;eastmoney_android;color=w;pkg=com.eastmoney.android.berlin;appver=9.0;tag=91116051;statusBarHeight=29.818182;titleBarHeight=45.090908;density=2.75;androidsdkversion=28;fontsize=2',
    'Accept': '*/*',
    'X-Requested-With': 'com.eastmoney.android.berlin',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://trademob2.1234567.com.cn/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

params = {
    # 'callback': 'jQuery311006633481466357316_1677153614990',
    'pageIndex': '1000',
    'pageSize': '30',
    'Sort': 'desc',
    'SortColumn': 'RZDF', # DWJZ：最新净值排序，RZDF：日涨幅
    'FundType': '31', # 基金的类型，0-全部，31-债券，35-货币，6-QDII，3-ETF场内，3-ETF联接，15-FOF，4-LOF，2949-理财
    'SYL': 'RZDF',
    'deviceid': 'embeb',
    'plat': 'Wap',
    'product': 'EFund',
    'version': '3.0',
    '_': '1677153614992',
}

response = requests.get('https://fundmobapi.eastmoney.com/FundMNewApi/FundMNRankNewList', params=params, headers=headers)
print(response.url)
print(response.text)