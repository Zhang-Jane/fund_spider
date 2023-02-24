import requests
# 基金热搜榜
cookies = {
    'st_si': '92917763303098',
    'st_pvi': '32193501818915',
    'st_sp': '2023-02-23%2000%3A23%3A12',
    'st_inirUrl': 'https%3A%2F%2Ftrademob2.1234567.com.cn%2Findex.html',
    'st_sn': '13',
    'st_psi': '20230223005015605-119147306933-9663966372',
    'st_asi': 'delete',
}

headers = {
    'Host': 'appsuggest.1234567.com.cn',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 8 Lite Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.65 Mobile Safari/537.36;eastmoney_android;color=w;pkg=com.eastmoney.android.berlin;appver=9.0;tag=91116051;statusBarHeight=29.818182;titleBarHeight=45.090908;density=2.75;androidsdkversion=28;fontsize=2',
    'Accept': '*/*',
    'X-Requested-With': 'com.eastmoney.android.berlin',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Dest': 'script',
    'Referer': 'https://trademob2.1234567.com.cn/',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    # 'Cookie': 'st_si=92917763303098; st_pvi=32193501818915; st_sp=2023-02-23%2000%3A23%3A12; st_inirUrl=https%3A%2F%2Ftrademob2.1234567.com.cn%2Findex.html; st_sn=13; st_psi=20230223005015605-119147306933-9663966372; st_asi=delete',
}

params = {
    # 'callback': 'jQuery311039499459068316556_1677153015530',
    'deviceid': 'embeb',
    'plat': 'Wap',
    'product': 'EFund',
    'version': '3.0',
    '_': '1677153015531',
}

response = requests.get(
    'https://appsuggest.1234567.com.cn/FundMobileSearchApi/FundHotSearchList.ashx',
    params=params,
    # cookies=cookies,
    headers=headers,
)
print(response.text)