import os
import urllib.request
import urllib.parse
import json

# 获取环境变量中的 SendKey
send_key = os.environ.get('SCT_KEY')

# 获取 A 股实时行情（使用免费的东方财富接口）
url = "http://82.push2.eastmoney.com/api/qt/clist/get"
params = {
    "pn": "1", "pz": "10", "po": "1", "np": "1",
    "ut": "bd1d9ddb04089700cf9c27f6f7426281",
    "fltt": "2", "invt": "2", "fid": "f3",
    "fs": "m:0+t:6,m:0+t:80", # 筛选沪深A股
    "fields": "f12,f14,f2,f3,f4",
}
query_string = urllib.parse.urlencode(params)
req = urllib.request.Request(f"{url}?{query_string}")
try:
    response = urllib.request.urlopen(req)
    res_data = json.loads(response.read().decode('utf-8'))
    stocks = res_data['data']['diff'][:5] # 取前5只
    
    # 拼接消息内容
    message = "今日选股观察（按涨幅前5）：\n\n"
    for idx, s in enumerate(stocks):
        message += f"{idx+1}. {s['f14']} ({s['f12']}) 涨幅：{s['f3']}%\n"
        
except Exception as e:
    message = f"获取股票数据失败：{e}"

# 发送到微信
send_url = f"https://sctapi.ftqq.com/{send_key}.send"
data = urllib.parse.urlencode({"title": "每日选股结果", "desp": message}).encode('utf-8')
send_req = urllib.request.Request(send_url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
urllib.request.urlopen(send_req)
