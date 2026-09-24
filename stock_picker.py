import os, urllib.request, urllib.parse

send_key = os.environ.get('SCT_KEY')

# 1. 获取大盘指数（上证指数）
index_url = "http://qt.gtimg.cn/q=sh000001"
try:
    req = urllib.request.Request(index_url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read().decode('gbk')
    index_data = res.split('~')
    index_msg = f"大盘环境：上证指数 {index_data[3]}，涨跌幅 {index_data[32]}%"
except:
    index_msg = "大盘环境：获取失败"

# 2. 监控几只具备中线价值的龙头股（这里换成你关注的股票代码）
codes = "sh600519,sz000858,sh601318,sh600036,sz300750,sh601012,sh600900"
url = f"http://qt.gtimg.cn/q={codes}"

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    result = urllib.request.urlopen(req).read().decode('gbk')
    lines = result.strip().split(';')
    
    message = f"【{index_msg}】\n\n今日复盘与明日策略（仅供模拟参考）：\n"
    
    for line in lines:
        if '~' in line:
            data = line.split('~')
            if len(data) > 32:
                name, code, price, change = data[1], data[2], data[3], data[32]
                
                # 简单的均线策略占位（实际交易请人工判断）
                suggestion = "观望"
                if float(change) > 3:
                    suggestion = "涨势过猛，明天不建议追高"
                elif float(change) < -3:
                    suggestion = "跌幅较大，暂不接飞刀"
                else:
                    suggestion = "走势平稳，可加入自选观察"
                
                message += f"\n▶ {name} ({code})\n"
                message += f"现价: {price} | 涨跌幅: {change}%\n"
                message += f"明日建议: {suggestion}\n"
                message += f"严格止损位: 现价的 -5% (即 {round(float(price)*0.95, 2)})\n"
except Exception as e:
    message = f"获取数据失败：{e}"

# 3. 发送微信
send_url = f"https://sctapi.ftqq.com/{send_key}.send"
data = urllib.parse.urlencode({"title": "每日复盘与明日操作建议", "desp": message}).encode('utf-8')
send_req = urllib.request.Request(send_url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
urllib.request.urlopen(send_req)
