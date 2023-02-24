import requests
# 累计净值
headers = {
    'Host': 'fundmobapi.eastmoney.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 8 Lite Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.65 Mobile Safari/537.36;eastmoney_android;color=w;pkg=com.eastmoney.android.berlin;appver=9.0;tag=5929205;statusBarHeight=29.818182;titleBarHeight=45.090908;density=2.75;androidsdkversion=28;fontsize=2',
    'Accept': '*/*',
    'X-Requested-With': 'com.eastmoney.android.berlin',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://trademob2.1234567.com.cn/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

params = {
    'callback': 'jQuery31107218797606334098_1677151981714',
    'FCODE': '014238',
    'RANGE': 'y',
    'deviceid': 'embeb',
    'plat': 'Wap',
    'product': 'EFund',
    'version': '3.0',
    '_': '1677151981736',
}

response = requests.get('https://fundmobapi.eastmoney.com/FundMApi/FundNetDiagram.ashx', params=params, headers=headers)
print(response.text)