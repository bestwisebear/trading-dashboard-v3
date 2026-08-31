import json
import os
from datetime import datetime

# Read existing news_impact.json
news_path = "/tmp/trading-dashboard/data/news_impact.json"
with open(news_path, 'r') as f:
    old_data = json.load(f)

# Midday news items (2026-08-18)
midday_items = [
    {
        "id": 13,
        "time": "12:00",
        "title": "A股午间收盘：三大指数齐跌，涨跌家数仅1221:3875",
        "category": "market",
        "impact": "negative",
        "impact_level": 4,
        "detail": "沪指-0.39%报3966.99，深成指-1.09%报14543.45，创业板指-1.30%报3691.69。半日成交1.64万亿。全市场仅1221家上涨(23.48%)，3875家下跌(74.50%)。昨日4335家普涨后今日严重分化。",
        "affected_stocks": [],
        "source": "新华财经/新浪财经/财联社"
    },
    {
        "id": 14,
        "time": "12:00",
        "title": "科技板块全面回调：CPO净流出170亿，储能135亿，机器人150亿",
        "category": "sector",
        "impact": "negative",
        "impact_level": 5,
        "detail": "60日线成科技逆鳞，冲关遇阻后资金集体兑现。CPO净流出170亿，储能135亿，存储芯片103亿，半导体94亿，机器人150亿。电子板块全天净流出超117亿，算力概念20:206。新易盛净卖出超13亿，中际旭创/工业富联净流出居前。",
        "affected_stocks": ["300502", "300308", "300857"],
        "source": "财联社/东方财富"
    },
    {
        "id": 15,
        "time": "10:00",
        "title": "农业板块逆势爆发：JPM预警粮食危机，种业10余股涨停",
        "category": "sector",
        "impact": "positive",
        "impact_level": 3,
        "detail": "JPMorgan预警厄尔尼诺影响下明年可能出现粮食危机，叠加商务部县域消费政策。种业(+8.60%)、转基因(+7.93%)、饲料(+2.66%)、猪肉(+2.57%)领涨。金健米业/农发种业2连板，万向德农/登海种业/亚盛集团涨停，罗牛山2连板。",
        "affected_stocks": [],
        "source": "AASTOCKS/财联社"
    },
    {
        "id": 16,
        "time": "13:06",
        "title": "午后算力租赁概念继续下挫，鸿博股份逼近跌停",
        "category": "sector",
        "impact": "negative",
        "impact_level": 4,
        "detail": "午后开盘算力租赁概念震荡下挫，鸿博股份逼近跌停，城地香江、行云科技、宏景科技、金开新能、美利云、群兴玩具均跌超5%。协创数据午后继续走弱。",
        "affected_stocks": ["300857"],
        "source": "财联社13:06"
    },
    {
        "id": 17,
        "time": "08:00",
        "title": "美股隔夜三大指数全跌：道指-0.51%，标普-0.52%，纳指-0.32%",
        "category": "macro",
        "impact": "negative",
        "impact_level": 3,
        "detail": "美伊谈判动摇，30年期美债收益率升至2007年来新高(5.311%)。但费城半导体指数此前涨超2.5%，存储芯片领涨(闪迪+10%，美光+6%)。10年期收益率4.725%。美元指数99.59(-0.08%)。",
        "affected_stocks": [],
        "source": "CNBC/Kapitales"
    },
    {
        "id": 18,
        "time": "09:30",
        "title": "宇树科技8/19科创板上市+世界机器人大会8/19开幕，机器人概念异动",
        "category": "sector",
        "impact": "positive",
        "impact_level": 4,
        "detail": "宇树科技发行价150.80元/股，中签率0.0181%为科创板史上最难。发布超人机器人：跳高2米、速度12.66m/s超越人类极限。正裕工业3连板，南方精工/日丰股份涨停，万达轴承+12.13%，长盛轴承+5.81%。但机器人板块整体净流出150亿，资金分歧大。",
        "affected_stocks": ["300718"],
        "source": "财联社/科创板日报"
    },
    {
        "id": 19,
        "time": "10:00",
        "title": "发改委能源局印发石油天然气十五五规划：CCUS+储能+氢能",
        "category": "macro",
        "impact": "positive",
        "impact_level": 3,
        "detail": "2030年国内油气供应量4.4亿吨油当量，新增长输管道2万公里。CCS/CCUS年注入1000万吨，加快重型燃气轮机国产化。储能/绿氢/低碳板块受政策催化。",
        "affected_stocks": ["300438"],
        "source": "国家发改委/国家能源局"
    },
    {
        "id": 20,
        "time": "11:00",
        "title": "玻璃基板概念走强：中信证券看好先进封装路径",
        "category": "sector",
        "impact": "positive",
        "impact_level": 2,
        "detail": "中信证券研报称玻璃基板有望成为先进封装大尺寸化、高密高速升级瓶颈的重要工艺。红星发展、彩虹股份双双涨停，沃格光电触及涨停。",
        "affected_stocks": [],
        "source": "财联社/中信证券"
    },
    {
        "id": 21,
        "time": "11:30",
        "title": "鹏辉能源：上半年扭亏为盈盈利8亿，登顶全球户储电芯TOP1",
        "category": "stock",
        "impact": "positive",
        "impact_level": 3,
        "detail": "鹏辉能源(300438)午间64.97(-0.82%)。上半年扭亏盈利约8亿，登顶全球户储电芯出货TOP1。12位分析师一致看好(75%强推+25%买入)，目标价均值88.58元。储能板块整体-1.15%。新获实用新型专利(8/18)。港交所IPO申报中。",
        "affected_stocks": ["300438"],
        "source": "大湾区经济网/富途牛牛/查股网"
    },
    {
        "id": 22,
        "time": "08:30",
        "title": "协创数据H1净利18.63亿(+331%)，负债率85.89%，算力板块集体调整",
        "category": "stock",
        "impact": "negative",
        "impact_level": 3,
        "detail": "协创数据(300857)午间261.21(-2.95%)。上半年营收126.41亿(+155.69%)，净利18.63亿(+331.11%)。但负债率85.89%偏高。拟用70亿自有资金委托理财。算力租赁板块午后继续下挫，鸿博股份逼近跌停。变更保荐机构重新签三方监管协议。",
        "affected_stocks": ["300857"],
        "source": "人民财讯/巨潮资讯网/企查查"
    },
    {
        "id": 23,
        "time": "15:00",
        "title": "国新办下午3时发布会：激发下沉市场活力活跃县域消费",
        "category": "macro",
        "impact": "positive",
        "impact_level": 2,
        "detail": "商务部部长助理袁晓明和农业农村部、文旅部、市场监管总局负责人介绍下沉市场消费政策。商务部等9部门支持农村集体经营性建设用地入市发展县域商业。关注消费板块下午反应。",
        "affected_stocks": [],
        "source": "国新办"
    },
    {
        "id": 24,
        "time": "11:00",
        "title": "SK海力士7200亿美元全球扩产，存储荒逻辑强化",
        "category": "sector",
        "impact": "positive",
        "impact_level": 3,
        "detail": "SK海力士董事长强调存储需求爆发式增长，明年或现最严重存储荒。7200亿美元扩产计划，目标五年产能翻倍。龙仁Y2+清州M17两新厂，生产HBM及NAND。半导体设备ETF(159558)规模创新高216.81亿，近5日4日净流入合计6.19亿。",
        "affected_stocks": [],
        "source": "每日经济新闻/SK海力士"
    }
]

# Merge: keep old items, update meta, add new items
old_data['meta']['date'] = '2026-08-18'
old_data['meta']['last_updated'] = '2026-08-18T13:16:00+08:00'
old_data['meta']['merged_note'] = 'merged: 8/14 early items + 8/18 midday scan'
old_data['overall_sentiment'] = '分化日偏空'
old_data['sentiment_summary'] = '昨日4335家普涨后今日严重分化,仅1221家上涨.科技全面回调(CPO-170亿/储能-135亿/半导体-94亿),农业/油气逆势走强.美股隔夜三大指数齐跌,30年美债收益率19年新高.午后算力租赁继续下挫.'

# Add midday items
existing_ids = {item['id'] for item in old_data['items']}
for item in midday_items:
    if item['id'] not in existing_ids:
        old_data['items'].append(item)

old_data['items_count'] = len(old_data['items'])

# Write
with open(news_path, 'w') as f:
    json.dump(old_data, f, ensure_ascii=False, indent=2)

print(f"✅ news_impact.json: {len(old_data['items'])}条 (新增{len(midday_items)}条)")
