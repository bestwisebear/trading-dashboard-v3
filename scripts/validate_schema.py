#!/usr/bin/env python3
"""
看板V3 JSON Schema 校验脚本
用途：在数据刷新后验证 JSON 字段名是否与 index.html 期望一致
用法：python3 scripts/validate_schema.py [data_dir]
"""

import json, sys, os, glob

DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else 'data'
errors = []
warnings = []

def check(condition, msg):
    if not condition:
        errors.append(f"❌ {msg}")
        return False
    return True

def warn(condition, msg):
    if not condition:
        warnings.append(f"⚠️  {msg}")

def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        errors.append(f"❌ 无法加载 {path}: {e}")
        return None

# ============================================================
# 1. positions.json — 总览页和持仓页的核心数据源
# ============================================================
pos = load_json(os.path.join(DATA_DIR, 'positions.json'))
if pos:
    s = pos.get('summary', {})
    
    # HTML 通过 summary.net_today 读取今日收益
    check('net_today' in s, "positions.json: summary 缺少 'net_today'（HTML读取今日收益的字段）")
    # HTML 通过 summary.monthly_pnl 读取本月收益
    check('monthly_pnl' in s, "positions.json: summary 缺少 'monthly_pnl'（HTML读取本月收益的字段）")
    
    # 以下字段也必需
    for field in ['total_assets', 'monthly_return_rate', 'position_ratio', 'available_cash', 'prev_close_assets']:
        check(field in s, f"positions.json: summary 缺少 '{field}'")
    
    # 检查 positions 数组中每个持仓的必需字段
    for i, p in enumerate(pos.get('positions', [])):
        for field in ['code', 'name', 'quantity', 'cost_price', 'current_price', 'stop_loss', 'pnl_percent', 'pnl_amount']:
            check(field in p, f"positions.json: positions[{i}]({p.get('name','?')}) 缺少 '{field}'")
    
    # 兼容字段：保留 today_return/total_pnl_amount 作为别名，但 net_today/monthly_pnl 是主字段
    if 'today_return' in s and 'net_today' not in s:
        s['net_today'] = s['today_return']
        warnings.append("⚠️  positions.json: 用 today_return 自动补充了 net_today（下次请直接用 net_today）")
    if 'total_pnl_amount' in s and 'monthly_pnl' not in s:
        s['monthly_pnl'] = s['total_pnl_amount']
        warnings.append("⚠️  positions.json: 用 total_pnl_amount 自动补充了 monthly_pnl（下次请直接用 monthly_pnl）")

# ============================================================
# 2. reviews_daily/weekly/monthly.json — 复盘页数据源
# ============================================================
for freq in ['daily', 'weekly', 'monthly']:
    fname = f'reviews_{freq}.json'
    rev = load_json(os.path.join(DATA_DIR, fname))
    if rev:
        # HTML 通过 records 数组读取复盘记录，不是 reviews
        check('records' in rev, f"{fname}: 顶层键必须是 'records'（不是 'reviews'）")
        
        # 检查每条记录的必需字段
        for i, r in enumerate(rev.get('records', [])):
            for field in ['date', 'market_summary', 'portfolio', 'plan_vs_actual', 'key_observations', 'discipline']:
                check(field in r, f"{fname}: records[{i}] 缺少 '{field}'")
            
            # 检查嵌套字段
            portfolio = r.get('portfolio', {})
            for field in ['total_assets', 'daily_pnl', 'daily_return', 'positions']:
                check(field in portfolio, f"{fname}: records[{i}].portfolio 缺少 '{field}'")
            
            discipline = r.get('discipline', {})
            for field in ['score', 'trades', 'violations']:
                check(field in discipline, f"{fname}: records[{i}].discipline 缺少 '{field}'")

# ============================================================
# 3. trades_today.json — 交易记录页
# ============================================================
trades = load_json(os.path.join(DATA_DIR, 'trades_today.json'))
if trades:
    for i, t in enumerate(trades.get('trades', [])):
        for field in ['time', 'code', 'action', 'quantity', 'price']:
            check(field in t, f"trades_today.json: trades[{i}] 缺少 '{field}'")

# ============================================================
# 4. market_signals.json — 七道闸
# ============================================================
signals = load_json(os.path.join(DATA_DIR, 'market_signals.json'))
if signals:
    check('signals' in signals, "market_signals.json: 缺少 'signals' 数组")
    check('aggregate' in signals, "market_signals.json: 缺少 'aggregate' 对象")
    agg = signals.get('aggregate', {})
    for field in ['green_count', 'yellow_count', 'red_count', 'total_score', 'max_score']:
        check(field in agg, f"market_signals.json: aggregate 缺少 '{field}'")

# ============================================================
# 5. watchlist.json — 关注池
# ============================================================
watch = load_json(os.path.join(DATA_DIR, 'watchlist.json'))
if watch:
    check('watchlist' in watch, "watchlist.json: 缺少 'watchlist' 数组")
    check('summary' in watch, "watchlist.json: 缺少 'summary' 对象")

# ============================================================
# 6. market_environment.json — 市场环境
# ============================================================
env = load_json(os.path.join(DATA_DIR, 'market_environment.json'))
if env:
    for field in ['indices', 'market_stats', 'hot_sectors_up', 'hot_sectors_down']:
        check(field in env, f"market_environment.json: 缺少 '{field}'")

# ============================================================
# 7. risk_assessment.json — 风险评估
# ============================================================
risk = load_json(os.path.join(DATA_DIR, 'risk_assessment.json'))
if risk:
    for field in ['level', 'score', 'factors', 'suggestion']:
        check(field in risk, f"risk_assessment.json: 缺少 '{field}'")

# ============================================================
# 8. 历史快照同步检查
# ============================================================
for date_dir in sorted(glob.glob(os.path.join(DATA_DIR, 'history/20*'))):
    date = os.path.basename(date_dir)
    
    hist_pos = load_json(os.path.join(date_dir, 'positions.json'))
    if hist_pos:
        s = hist_pos.get('summary', {})
        check('net_today' in s, f"history/{date}/positions.json: summary 缺少 'net_today'")
        check('monthly_pnl' in s, f"history/{date}/positions.json: summary 缺少 'monthly_pnl'")
    
    hist_rev = load_json(os.path.join(date_dir, 'reviews_daily.json'))
    if hist_rev:
        check('records' in hist_rev, f"history/{date}/reviews_daily.json: 必须是 'records' 不是 'reviews'")

# ============================================================
# 输出结果
# ============================================================
print(f"\n{'='*60}")
print(f"看板V3 Schema 校验报告")
print(f"{'='*60}")

if warnings:
    print(f"\n⚠️  警告 ({len(warnings)}):")
    for w in warnings:
        print(f"  {w}")

if errors:
    print(f"\n❌ 错误 ({len(errors)}):")
    for e in errors:
        print(f"  {e}")
    print(f"\n🔴 校验失败：{len(errors)} 个字段错误需要修复")
    sys.exit(1)
else:
    print(f"\n✅ 校验通过：所有JSON文件字段正确")
    sys.exit(0)
