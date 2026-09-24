import os, urllib.request, urllib.parse, json

send_key = os.environ.get('SCT_KEY')

# 预设的测试股票池（你可以随时增减，格式必须是 sh 或 sz 开头）
stock_pool = ["sh600519", "sz000858", "sh601318", "sh600036", "sz300750", 
              "sh601012", "sh600900", "sz000333", "sh601166", "sz000651"]

message = "【今日均线回踩策略扫描】\n\n"
found = False

for code in stock_pool:
    url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={code},day,,,5,qfq"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        
        # 提取近5天收盘价
        klines = data['data'][code]['qfqday']
        closes = [float(k[2]) for k in klines]
        
        ma5 = sum(closes) / len(closes)           # 5日均线
        today_close = closes[-1]                  # 今天收盘价
        yesterday_close = closes[-2]              # 昨天收盘价
        change = (today_close - yesterday_close) / yesterday_close * 100  # 今天涨跌幅
        
        # 策略核心：收盘价在5日线之上，且今天微跌（-3%到0%之间）
        if today_close > ma5 and -3 <= change <= 0:
            found = True
            message += f"✅ {code}\n"
            message += f"  现价: {today_close} | 5日均线: {round(ma5, 2)}\n"
            message += f"  今日涨跌: {round(change, 2)}%\n"
            message += f"  👉 关注点：若明日开盘不破5日线，可分批轻仓；跌破则放弃。\n\n"
            
    except Exception as e:
        # 个别股票网络波动获取失败，跳过即可
        pass 

if not found:
    message += "今日无符合“均线回踩”形态的股票，建议保持观望，耐心等待。"

message += "💡 警告：此为技术指标辅助工具，非投资建议。股市有风险，入市需谨慎！"

# 发送微信
send_url = f"https://sctapi.ftqq.com/{send_key}.send"
data = urllib.parse.urlencode({"title": "均线回踩策略扫描", "desp": message}).encode('utf-8')
send_req = urllib.request.Request(send_url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
urllib.request.urlopen(send_req)
