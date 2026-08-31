#!/usr/bin/env python3
"""Generate 14 JSON data files for the trading dashboard V3"""
import json, os, datetime

OUT_DIR = "/app/data/所有对话/主对话/看板V3_data"
os.makedirs(OUT_DIR, exist_ok=True)

NOW = "2026-08-03T16:15:00+08:00"
TODAY = "2026-08-03"

# ===== 1. positions.json =====
positions = {
    "meta": {"last_updated": NOW, "version": "3.0"},
    "positions": [
        {
            "code": "300136", "name": "信维通信", "quantity": 1200, "cost_price": 60.70,
            "cost_source": "dialog_sync", "current_price": 56.50, "price_updated_at": NOW,
            "buy_date": "2026-07-28", "holding_days": 6, "stop_loss": 55.75, "stop_profit": 75.00,
            "pnl_percent": round((56.50 - 60.70) / 60.70 * 100, 2),
            "pnl_amount": round((56.50 - 60.70) * 1200, 2),
            "sector": "消费电子", "status": "holding",
            "notes": "⚠️ 今日最低55.75触及止损线！收盘56.50略高于止损"
        },
        {
            "code": "300408", "name": "三环集团", "quantity": 500, "cost_price": 114.00,
            "cost_source": "dialog_sync", "current_price": 114.00, "price_updated_at": NOW,
            "buy_date": "2026-07-31", "holding_days": 3, "stop_loss": 110.00, "stop_profit": 135.00,
            "pnl_percent": 0.0, "pnl_amount": 0.0,
            "sector": "电子元器件", "status": "holding",
            "notes": "今日+2.08%，表现良好"
        }
    ],
    "summary": {
        "total_positions": 2,
        "total_pnl_percent": round((-5040 + 0) / (60.70*1200 + 114.00*500) * 100, 2),
        "total_pnl_amount": -5040.0,
        "position_ratio": round((56.50*1200 + 114.00*500) / 200000 * 100, 2),
        "available_cash": round(200000 - (56.50*1200 + 114.00*500), 2),
        "total_assets": 200000
    }
}
with open(f"{OUT_DIR}/positions.json", "w") as f:
    json.dump(positions, f, ensure_ascii=False, indent=2)

# ===== 2. market_signals.json =====
market_signals = {
    "meta": {"date": TODAY, "last_updated": NOW},
    "signals": [
        {"id": "rise_fall_count", "name": "涨跌家数", "description": "全市场涨跌家数对比",
         "value": None, "threshold": 2000, "status": "yellow",
         "detail": "市场整体下跌，涨跌家数约1:1偏弱", "updated_at": NOW},
        {"id": "sector_strength", "name": "板块真假强", "description": "持仓板块涨跌比判定",
         "value": None, "status": "yellow",
         "detail": "消费电子板块-2.48%，电子元器件板块分化，三环集团逆势上涨", "updated_at": NOW},
        {"id": "main_capital_flow", "name": "主力资金方向", "description": "全市场主力资金净流入(亿)",
         "value": -150.0, "threshold": 0, "status": "red",
         "detail": "主力资金大幅净流出，市场承压", "updated_at": NOW},
        {"id": "northbound_flow", "name": "北向资金流入", "description": "北向资金净流入(亿)",
         "value": None, "threshold": 0, "status": "yellow",
         "detail": "北向资金数据待更新", "updated_at": NOW},
        {"id": "limit_up_count", "name": "涨停家数", "description": "涨停板数量",
         "value": 45, "threshold": 30, "status": "green",
         "detail": "涨停45家，跌停12家，局部热度尚可", "updated_at": NOW},
        {"id": "volume_ratio", "name": "量比指标", "description": "全市场量比",
         "value": 1.15, "threshold": 1.2, "status": "yellow",
         "detail": "量比1.15，接近放量阈值", "updated_at": NOW},
        {"id": "market_breadth", "name": "市场宽度", "description": "站上5日线个股占比",
         "value": 45.0, "threshold": 60, "status": "yellow",
         "detail": "站上5日线占比约45%，低于健康线", "updated_at": NOW}
    ],
    "aggregate": {
        "green_count": 1, "yellow_count": 5, "red_count": 1,
        "total_score": 7, "max_score": 14,
        "no_open_position": True,
        "no_open_reason": "主力资金大幅流出+市场宽度偏弱，建议谨慎开仓"
    }
}
with open(f"{OUT_DIR}/market_signals.json", "w") as f:
    json.dump(market_signals, f, ensure_ascii=False, indent=2)

# ===== 3. watchlist.json =====
watchlist_stocks = [
    {"code": "300857", "name": "协创数据", "close": 204.80, "change_pct": -5.12, "sector": "AI服务器", "support": 195.0, "resistance": 225.0, "buy_range": [195.0, 205.0], "status": "tracking", "tags": ["AI服务器"]},
    {"code": "002156", "name": "通富微电", "close": 51.34, "change_pct": -9.50, "sector": "半导体封测", "support": 48.0, "resistance": 58.0, "buy_range": [48.0, 52.0], "status": "tracking", "tags": ["封测"]},
    {"code": "300502", "name": "新易盛", "close": 394.08, "change_pct": -0.49, "sector": "光模块", "support": 370.0, "resistance": 420.0, "buy_range": [370.0, 395.0], "status": "tracking", "tags": ["光模块"]},
    {"code": "300308", "name": "中际旭创", "close": 902.50, "change_pct": 0.05, "sector": "光模块", "support": 850.0, "resistance": 950.0, "buy_range": [850.0, 910.0], "status": "tracking", "tags": ["光模块龙头"]},
    {"code": "300394", "name": "天孚通信", "close": 180.50, "change_pct": 5.55, "sector": "光模块", "support": 165.0, "resistance": 190.0, "buy_range": [165.0, 180.0], "status": "tracking", "tags": ["光模块", "强势"]},
    {"code": "300223", "name": "北京君正", "close": 119.00, "change_pct": -6.16, "sector": "存储芯片", "support": 115.0, "resistance": 130.0, "buy_range": [115.0, 122.0], "status": "tracking", "tags": ["存储"]},
    {"code": "301308", "name": "江波龙", "close": 319.80, "change_pct": -7.84, "sector": "存储芯片", "support": 310.0, "resistance": 350.0, "buy_range": [310.0, 325.0], "status": "tracking", "tags": ["存储"]},
    {"code": "300408", "name": "三环集团", "close": 114.00, "change_pct": 2.08, "sector": "电子元器件", "support": 108.0, "resistance": 120.0, "buy_range": [108.0, 115.0], "status": "holding", "tags": ["持仓"]},
    {"code": "300438", "name": "鹏辉能源", "close": 59.36, "change_pct": -0.82, "sector": "电池", "support": 55.0, "resistance": 65.0, "buy_range": [55.0, 60.0], "status": "tracking", "tags": ["电池"]},
    {"code": "300395", "name": "菲利华", "close": 70.89, "change_pct": -2.58, "sector": "半导体材料", "support": 68.0, "resistance": 78.0, "buy_range": [68.0, 72.0], "status": "tracking", "tags": ["半导体材料"]},
    {"code": "300442", "name": "润泽科技", "close": 62.97, "change_pct": -0.44, "sector": "IDC", "support": 58.0, "resistance": 68.0, "buy_range": [58.0, 64.0], "status": "tracking", "tags": ["IDC"]},
    {"code": "300604", "name": "长川科技", "close": 227.42, "change_pct": -12.41, "sector": "半导体设备", "support": 220.0, "resistance": 260.0, "buy_range": [220.0, 235.0], "status": "tracking", "tags": ["半导体设备"]},
    {"code": "000988", "name": "华工科技", "close": 93.17, "change_pct": -2.31, "sector": "激光设备", "support": 88.0, "resistance": 100.0, "buy_range": [88.0, 95.0], "status": "tracking", "tags": ["激光"]},
    {"code": "002384", "name": "东山精密", "close": 162.81, "change_pct": -5.06, "sector": "PCB/FPC", "support": 155.0, "resistance": 175.0, "buy_range": [155.0, 165.0], "status": "tracking", "tags": ["PCB"]},
    {"code": "000977", "name": "浪潮信息", "close": 71.66, "change_pct": -0.21, "sector": "AI服务器", "support": 68.0, "resistance": 76.0, "buy_range": [68.0, 72.0], "status": "tracking", "tags": ["AI服务器", "等右侧信号"]},
    # 观察池
    {"code": "603026", "name": "石大胜华", "close": 63.95, "change_pct": 0.19, "sector": "锂电材料", "support": 60.0, "resistance": 68.0, "buy_range": [60.0, 65.0], "status": "observing", "tags": ["观察"]},
    {"code": "300769", "name": "德方纳米", "close": 42.96, "change_pct": 0.51, "sector": "锂电材料", "support": 40.0, "resistance": 48.0, "buy_range": [40.0, 44.0], "status": "observing", "tags": ["观察"]}
]

watchlist = {
    "meta": {"last_updated": NOW},
    "watchlist": [
        {
            "code": s["code"], "name": s["name"],
            "key_price": {"support": s["support"], "resistance": s["resistance"], "buy_range": s["buy_range"]},
            "status": s["status"], "sector": s["sector"],
            "today_close": s["close"], "today_change_pct": s["change_pct"],
            "tags": s["tags"], "added_date": "2026-08-03"
        } for s in watchlist_stocks
    ],
    "oversold_scan": []
}
with open(f"{OUT_DIR}/watchlist.json", "w") as f:
    json.dump(watchlist, f, ensure_ascii=False, indent=2)

# ===== 4. oversold_sectors.json =====
# Based on board data: 半导体-5.84%, 玻璃玻纤-7.17%, 电子-4.18%
oversold = {
    "meta": {"date": TODAY, "last_updated": NOW},
    "sectors": [
        {"sector_name": "半导体", "change_20d": -5.84, "top3_resistant": [
            {"code": "300408", "name": "三环集团", "change_20d": 2.08},
            {"code": "300308", "name": "中际旭创", "change_20d": 0.05},
            {"code": "300394", "name": "天孚通信", "change_20d": 5.55}
        ], "can_add_watchlist": True, "note": "半导体板块今日重挫，但部分光模块个股逆势走强"},
        {"sector_name": "玻璃玻纤", "change_20d": -7.17, "top3_resistant": [], "can_add_watchlist": False, "note": "板块跌幅较大，暂观察"},
        {"sector_name": "消费电子", "change_20d": -2.48, "top3_resistant": [
            {"code": "300136", "name": "信维通信", "change_20d": -1.70}
        ], "can_add_watchlist": False, "note": "信维通信触及止损位"}
    ]
}
with open(f"{OUT_DIR}/oversold_sectors.json", "w") as f:
    json.dump(oversold, f, ensure_ascii=False, indent=2)

# ===== 5. bottom_signals.json =====
bottom = {
    "meta": {"date": TODAY, "last_updated": NOW},
    "signals": [
        {"id": "volume_shrink", "name": "缩量企稳", "status": "yellow", "detail": "关注池多数个股换手率较高，未见明显缩量"},
        {"id": "key_support", "name": "关键支撑位测试", "status": "yellow", "detail": "信维通信触及止损位55.75，长川科技接近支撑220"},
        {"id": "sector_rotation", "name": "板块轮动信号", "status": "green", "detail": "电力/电网/风电等低位板块今日领涨，资金有切换迹象"},
        {"id": "northbound", "name": "北向资金转向", "status": "yellow", "detail": "待更新"},
        {"id": "sentiment_extreme", "name": "情绪极端值", "status": "yellow", "detail": "涨跌家数偏弱但未到极端"}
    ],
    "triggered_count": 0, "threshold": 3
}
with open(f"{OUT_DIR}/bottom_signals.json", "w") as f:
    json.dump(bottom, f, ensure_ascii=False, indent=2)

# ===== 6. market_environment.json =====
market_env = {
    "meta": {"date": TODAY, "last_updated": NOW},
    "indices": [
        {"name": "上证指数", "code": "sh000001", "close": 3809.66, "change_pct": -0.59},
        {"name": "深证成指", "code": "sz399001", "close": 13448.29, "change_pct": -0.96},
        {"name": "创业板指", "code": "sz399006", "close": 3302.55, "change_pct": -1.24}
    ],
    "hot_sectors_up": [
        {"name": "电机Ⅱ", "change_pct": 4.63},
        {"name": "风电设备", "change_pct": 3.73},
        {"name": "航天装备Ⅱ", "change_pct": 3.59},
        {"name": "电网设备", "change_pct": 2.68},
        {"name": "核电概念", "change_pct": 2.80}
    ],
    "hot_sectors_down": [
        {"name": "玻璃玻纤", "change_pct": -7.17},
        {"name": "半导体", "change_pct": -5.84},
        {"name": "电子", "change_pct": -4.18}
    ],
    "overall_assessment": "市场分化明显，科技板块回调，电力/风电等低位板块补涨。整体偏弱，涨跌家数约1:1。"
}
with open(f"{OUT_DIR}/market_environment.json", "w") as f:
    json.dump(market_env, f, ensure_ascii=False, indent=2)

# ===== 7. plans.json =====
plans = {
    "meta": {"date": TODAY, "last_updated": NOW},
    "plans": [
        {
            "id": 1, "stock": "信维通信", "code": "300136",
            "action": "观察/止损", "condition": "若跌破55.75止损线则清仓",
            "target": "反弹至58-60区间考虑减仓", "priority": "high",
            "notes": "今日最低55.75精确触及止损，需高度警惕"
        },
        {
            "id": 2, "stock": "三环集团", "code": "300408",
            "action": "持有", "condition": "站稳110上方继续持有",
            "target": "目标120-125区间", "priority": "medium",
            "notes": "今日+2.08%表现强势，电子元器件板块相对抗跌"
        },
        {
            "id": 3, "stock": "浪潮信息", "code": "000977",
            "action": "等待右侧信号", "condition": "放量突破76可考虑建仓",
            "target": "目标80+", "priority": "low",
            "notes": "当前价格71.66在买入区间内，但未出现右侧信号"
        }
    ]
}
with open(f"{OUT_DIR}/plans.json", "w") as f:
    json.dump(plans, f, ensure_ascii=False, indent=2)

# ===== 8. risk_assessment.json =====
risk = {
    "meta": {"date": TODAY, "last_updated": NOW},
    "level": "medium_high",
    "score": 65,
    "factors": [
        {"factor": "持仓集中度", "score": 60, "detail": "2只持仓，集中度中等"},
        {"factor": "止损风险", "score": 80, "detail": "信维通信距止损仅1.3%，风险较高"},
        {"factor": "市场环境", "score": 55, "detail": "指数普跌，科技板块重挫"},
        {"factor": "资金面", "score": 65, "detail": "主力资金净流出"},
        {"factor": "板块强度", "score": 60, "detail": "持仓板块分化，消费电子弱、电子元器件强"}
    ],
    "suggestion": "当前风险等级中高。信维通信逼近止损线是最大风险点，建议明日密切关注。三环集团表现相对健康。"
}
with open(f"{OUT_DIR}/risk_assessment.json", "w") as f:
    json.dump(risk, f, ensure_ascii=False, indent=2)

# ===== 9. discipline_log.json =====
discipline = {
    "meta": {"last_updated": NOW},
    "logs": [],
    "stats": {
        "total_violations": 0,
        "by_type": {},
        "this_week": 0,
        "this_month": 0
    }
}
with open(f"{OUT_DIR}/discipline_log.json", "w") as f:
    json.dump(discipline, f, ensure_ascii=False, indent=2)

# ===== 10. avoid_list.json =====
avoid = {
    "meta": {"last_updated": NOW},
    "items": [],
    "auto_check_enabled": True
}
with open(f"{OUT_DIR}/avoid_list.json", "w") as f:
    json.dump(avoid, f, ensure_ascii=False, indent=2)

# ===== 11. trades_today.json =====
trades = {
    "meta": {"date": TODAY, "last_updated": NOW},
    "trades": [],
    "summary": {
        "total_trades": 0,
        "buy_count": 0,
        "sell_count": 0,
        "net_pnl": 0
    }
}
with open(f"{OUT_DIR}/trades_today.json", "w") as f:
    json.dump(trades, f, ensure_ascii=False, indent=2)

# ===== 12-14. Reviews =====
review_daily = {
    "meta": {"last_updated": NOW},
    "reviews": [
        {
            "date": TODAY,
            "market_summary": "三大指数集体下跌，上证-0.59%，创业板-1.24%。半导体板块重挫-5.84%，电力/风电板块补涨。",
            "portfolio_summary": "信维通信-1.70%（最低触及止损55.75），三环集团+2.08%表现良好。",
            "key_observations": "市场风格切换，科技股承压，低位板块轮动补涨。",
            "score": 60
        }
    ]
}
with open(f"{OUT_DIR}/reviews_daily.json", "w") as f:
    json.dump(review_daily, f, ensure_ascii=False, indent=2)

review_weekly = {"meta": {"last_updated": NOW}, "reviews": []}
with open(f"{OUT_DIR}/reviews_weekly.json", "w") as f:
    json.dump(review_weekly, f, ensure_ascii=False, indent=2)

review_monthly = {"meta": {"last_updated": NOW}, "reviews": []}
with open(f"{OUT_DIR}/reviews_monthly.json", "w") as f:
    json.dump(review_monthly, f, ensure_ascii=False, indent=2)

print(f"✅ Generated 14 JSON files in {OUT_DIR}")
for f in sorted(os.listdir(OUT_DIR)):
    print(f"  - {f}")
