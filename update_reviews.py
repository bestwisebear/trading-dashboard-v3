import json, os

DATA_DIR = '/tmp/trading-dashboard/data'
TODAY = '2026-08-18'
NOW_ISO = '2026-08-18T16:55:00+08:00'

# Read existing reviews_daily
with open(os.path.join(DATA_DIR, 'reviews_daily.json')) as f:
    reviews = json.load(f)

# Calculate from state
with open(os.path.join(DATA_DIR, 'state.json')) as f:
    state = json.load(f)

net_today = state['today_so_far']['net_today']
total_assets = state['current']['total_assets']
total_pnl = state['current']['monthly_pnl']

# New review record for today
today_review = {
    "date": TODAY,
    "pnl_amount": net_today,
    "pnl_percent": round(net_today / 207076.77 * 100, 2),
    "trade_count": 6,
    "violation_count": 1,
    "execution_score": 65,
    "discipline_score": 7,
    "net_today": net_today,
    "today_return": round(net_today / 207076.77 * 100, 2),
    "total_pnl_amount": total_pnl,
    "key_decisions": [
        "09:30协创数据减仓100股@266.40(+727),保留100股轻仓",
        "09:48-09:50国瓷材料分两笔清仓600股(+1946.64),MLCC链去重保留风华出国产瓷",
        "10:45风华高科清仓500股@64.36(+925.54),PE207x偏高换仓机器人",
        "13:42昊志机电建仓500@80.18(violation:non_watchlist),机器人大会概念博弈",
        "13:45三环集团建仓300@126.21,MLCC涨价30%催化。挂单126成交126.21",
        "换仓逻辑:MLCC三股去重→机器人(昊志)+MLCC龙头(三环)"
    ],
    "operation_analysis": {
        "good": "1)MLCC去重逻辑清晰:国瓷+风华清仓+1946+925=+2872,锁定利润;2)换仓方向聚焦:机器人概念(昊志+6.80%验证判断正确)+MLCC龙头(三环虽亏但逻辑正确);3)买入在13:30-14:30窗口内执行",
        "bad": "1)昊志机电为非关注池标的(violation:non_watchlist),虽结果+6.80%但不能鼓励;2)三环集团首日即-4.73%大亏,挂单126成交126.21滑点0.21元;3)3笔卖出在早盘窗口外执行",
        "improvement": "明日核心:①三环集团123.99距止损122仅1.6%,跌破即止损!②昊志+6.80%关注80元(成本线)支撑③宇树8/19上市观察是否利好兑现④非关注池开仓需提前加入观察池"
    },
    "planned_executed": [
        {"stock":"三环集团","code":"300408","plan":"MLCC涨价催化建仓","actual":"13:45买入300股@126.21","result":"建仓完成,首日-4.73%","deviation":"滑点0.21元"}
    ],
    "planned_not_executed": [],
    "unplanned_actions": [
        {"stock":"昊志机电","code":"300503","action":"买入500股@80.18","reason":"机器人大会概念博弈,替代长盛轴承(涨太多)","result":"首日+6.80%","deviation":"非关注池标的(violation)"}
    ],
    "market_review": "分化日。沪指探底回升+0.19%收3990,创业板-0.93%。农业+9.54%全线爆发(厄尔尼诺+粮食危机)。科技高低切换:半导体休整,CPO/算力获利回吐。涨跌2121:3292,赚钱效应仅38%。北证50+2.67%资金未离场。成交2.42万亿平量高位。",
    "emotion_state": "换仓日心态相对平稳。MLCC去重果断(+2872锁利),机器人方向选择正确(昊志+6.80%)。但三环首日-4.73%有一定压力,需关注明日是否触发止损。整体纪律评分7分(昊志non_watchlist扣1分)",
    "tomorrow_focus": "①三环集团止损线122!跌破果断执行!②昊志80元支撑能否守住③宇树8/19上市→机器人概念是否利好兑现④鹏辉横盘关注65支撑⑤农业主线是否延续"
}

# Check if today already exists, if so replace
records = reviews.get('records', [])
existing_idx = None
for i, r in enumerate(records):
    if r.get('date') == TODAY:
        existing_idx = i
        break
if existing_idx is not None:
    records[existing_idx] = today_review
else:
    records.append(today_review)

reviews['records'] = records
reviews['meta']['last_updated'] = NOW_ISO
reviews['meta']['total_records'] = len(records)

with open(os.path.join(DATA_DIR, 'reviews_daily.json'), 'w') as f:
    json.dump(reviews, f, ensure_ascii=False, indent=2)
print(f"✅ reviews_daily.json ({len(records)} records)")
