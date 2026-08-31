import json, datetime

DATA_DIR = '/tmp/trading-dashboard/data'

news = {
    "meta": {
        "date": "2026-08-18",
        "last_updated": "2026-08-18T16:55:00+08:00",
        "source": "web_search_close"
    },
    "overall_sentiment": "中性偏空",
    "sentiment_summary": "分化日：农业爆发+科技休整，赚钱效应仅38%，散户难度高。三环-4.73%需警惕",
    "items": [
        {
            "id": 1,
            "time": "09:30",
            "title": "农业板块全线爆发，种植业+9.54%领涨",
            "category": "sector",
            "impact": "positive",
            "impact_level": 4,
            "detail": "厄尔尼诺+粮食危机催化。秋乐种业30%涨停，神农种业/华绿生物/天山生物20%涨停，敦煌种业/隆平高科等涨停。17只农业股涨停。ETF粮食ETF南方涨停创新高",
            "affected_stocks": [],
            "source": "新华财经/东方财富"
        },
        {
            "id": 2,
            "time": "06:00",
            "title": "联合国粮农组织预警：全球谷物产量预计降2%",
            "category": "macro",
            "impact": "positive",
            "impact_level": 4,
            "detail": "2026-2027年度全球谷物产量预计较上一年度下降2%至29.82亿吨，消费量增长0.6%。强厄尔尼诺概率升至81%，多国减少小麦种植。粮食涨价预期强烈",
            "affected_stocks": [],
            "source": "证券时报"
        },
        {
            "id": 3,
            "time": "08:30",
            "title": "九部门发文激发下沉市场活力，活跃县域消费",
            "category": "macro",
            "impact": "positive",
            "impact_level": 3,
            "detail": "商务部等9部门发布意见：支持县域消费渠道升级、大力支持新能源汽车/绿色智能产品下乡、扩大农村充电设施覆盖。国新办下午3时举行发布会",
            "affected_stocks": [],
            "source": "财联社"
        },
        {
            "id": 4,
            "time": "09:00",
            "title": "宇树科技8/19科创板上市，机器人大会本周召开",
            "category": "sector",
            "impact": "positive",
            "impact_level": 4,
            "detail": "宇树科技8/19上市，发行价150.80元。机器人大会本周召开，正裕工业3连板，南方精工/日丰股份等多股涨停。机器人概念获23亿主力净流入",
            "affected_stocks": ["300503","300718"],
            "source": "东方财富"
        },
        {
            "id": 5,
            "time": "15:00",
            "title": "三环集团收盘-4.73%，高位回调需警惕止损",
            "category": "stock",
            "impact": "negative",
            "impact_level": 4,
            "detail": "MLCC龙头三环集团首日建仓即遭重挫-4.73%，收于123.99。距止损122仅1.6%。盘中最高133.15后跳水，成交量放大。MLCC概念分化严重",
            "affected_stocks": ["300408"],
            "source": "腾讯行情"
        },
        {
            "id": 6,
            "time": "10:00",
            "title": "MLCC涨价30%催化，但板块严重分化",
            "category": "sector",
            "impact": "neutral",
            "impact_level": 3,
            "detail": "MLCC涨价消息催化三环集团建仓逻辑。但板块严重分化：三环-4.73%，元件板块整体-2.03%。风华高科清仓后继续走高+0.77%。涨价受益逻辑需验证",
            "affected_stocks": ["300408","000636"],
            "source": "财联社"
        },
        {
            "id": 7,
            "time": "14:00",
            "title": "央行净回笼958亿，逆回购精准调控",
            "category": "macro",
            "impact": "neutral",
            "impact_level": 2,
            "detail": "央行7天期逆回购连续第6日归零，开展4697亿隔夜逆回购。当日净回笼958亿。市场对缩量操作反应温和，指数探底回升",
            "affected_stocks": [],
            "source": "东方财富"
        },
        {
            "id": 8,
            "time": "15:00",
            "title": "北向资金净流出36亿，电子/通信大出血",
            "category": "market",
            "impact": "negative",
            "impact_level": 3,
            "detail": "沪股通-29.12亿+深股通-7.27亿=合计-36亿。昨日+31亿后获利兑现。主力净流出669亿，电子-130亿、通信-124亿、计算机-63亿大幅流出",
            "affected_stocks": [],
            "source": "Wind/东方财富"
        },
        {
            "id": 9,
            "time": "12:00",
            "title": "磷化铟基板Q4涨幅或超10%，创历史最大涨幅",
            "category": "sector",
            "impact": "positive",
            "impact_level": 3,
            "detail": "AI算力需求爆发将磷化铟(InP)推向供应极限。Q4价格涨幅或超10%，已经历三度调涨即将四连涨。光模块厂与AI数据中心竞相抢购",
            "affected_stocks": ["688012"],
            "source": "中证报"
        },
        {
            "id": 10,
            "time": "13:00",
            "title": "PCB产业链半年报亮眼，高端供需偏紧或延至2028",
            "category": "sector",
            "impact": "positive",
            "impact_level": 3,
            "detail": "多家PCB企业2026H1营收净利较快增长。AI服务器迭代+ASIC放量支撑高端需求。高阶HDI/高多层PCB持续供需偏紧，涨价趋势明确",
            "affected_stocks": [],
            "source": "上证报"
        },
        {
            "id": 11,
            "time": "10:00",
            "title": "创新药板块领跌，贝达药业20cm跌停",
            "category": "sector",
            "impact": "negative",
            "impact_level": 3,
            "detail": "创新药板块延续调整，贝达药业20cm跌停领跌。医药板块资金持续流出",
            "affected_stocks": [],
            "source": "东方财富"
        },
        {
            "id": 12,
            "time": "15:00",
            "title": "全市场成交2.42万亿平量高位，4000点关前蓄势",
            "category": "market",
            "impact": "neutral",
            "impact_level": 2,
            "detail": "沪深京合计24199亿较昨日放量173亿。沪指盘中3994距4000仅6点未破，尾盘回升收3990。下影线确认3955支撑有效。北证50暴涨+2.67%说明资金未离场",
            "affected_stocks": [],
            "source": "新华财经"
        }
    ]
}

with open(f'{DATA_DIR}/news_impact.json', 'w') as f:
    json.dump(news, f, ensure_ascii=False, indent=2)
print("✅ news_impact.json written")
