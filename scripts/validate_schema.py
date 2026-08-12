#!/usr/bin/env python3
"""
看板数据 Schema 校验脚本
验证所有 JSON 数据文件的字段与 HTML 期望完全一致。
每次数据刷新后必须运行此脚本，通过才能 git commit。

用法: python3 scripts/validate_schema.py data/
"""
import json, sys, os, glob

DATA_DIR = sys.argv[1] if len(sys.argv) > 1 else 'data'
errors = []

def check(condition, msg):
    if not condition:
        errors.append(msg)

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        errors.append(f"无法加载 {path}: {e}")
        return None

# ============================================================
# 1. positions.json
# ============================================================
pos = load_json(os.path.join(DATA_DIR, 'positions.json'))
if pos:
    # summary 必须包含 HTML 用到的所有字段
    s = pos.get('summary', {})
    for field in ['net_today', 'monthly_pnl', 'today_return', 'today_return_rate',
                  'position_ratio', 'available_cash', 'total_assets',
                  'total_pnl_amount', 'monthly_return_rate', 'prev_close_assets', 'initial_capital']:
        check(field in s, f"positions.json: summary 缺少 '{field}'")
    for p in pos.get('positions', []):
        for field in ['code', 'name', 'quantity', 'cost_price', 'current_price', 'stop_loss', 'pnl_percent', 'pnl_amount']:
            check(field in p, f"positions.json: positions[] 缺少 '{field}'")

# ============================================================
# 2. market_signals.json
# ============================================================
ms = load_json(os.path.join(DATA_DIR, 'market_signals.json'))
if ms:
    check('signals' in ms, "market_signals.json: 缺少 'signals'")
    agg = ms.get('aggregate', {})
    for field in ['green_count', 'yellow_count', 'red_count', 'total_score', 'max_score', 'no_open_position', 'market_comment']:
        check(field in agg, f"market_signals.json: aggregate 缺少 '{field}'")

# ============================================================
# 3. watchlist.json
# ============================================================
wl = load_json(os.path.join(DATA_DIR, 'watchlist.json'))
if wl:
    check('watchlist' in wl, "watchlist.json: 缺少 'watchlist'")
    for w in wl.get('watchlist', []):
        for field in ['code', 'name', 'key_price', 'status', 'sector', 'today_close', 'today_change_pct']:
            check(field in w, f"watchlist.json: watchlist[] 缺少 '{field}'")
    # transit_pool
    for t in wl.get('transit_pool', []):
        for field in ['name', 'code', 'score', 'gates', 'key_price', 'sector']:
            check(field in t, f"watchlist.json: transit_pool[] 缺少 '{field}'")

# ============================================================
# 4. oversold_sectors.json
# ============================================================
os_data = load_json(os.path.join(DATA_DIR, 'oversold_sectors.json'))
if os_data:
    check('sectors' in os_data, "oversold_sectors.json: 缺少 'sectors'")

# ============================================================
# 5. bottom_signals.json
# ============================================================
bs = load_json(os.path.join(DATA_DIR, 'bottom_signals.json'))
if bs:
    check('signals' in bs, "bottom_signals.json: 缺少 'signals'")
    check('aggregate' in bs, "bottom_signals.json: 缺少 'aggregate'")
    if 'aggregate' in bs:
        for field in ['ratio', 'recommendation', 'recommendation_detail']:
            check(field in bs['aggregate'], f"bottom_signals.json: aggregate 缺少 '{field}'")
    check('history_7d' in bs, "bottom_signals.json: 缺少 'history_7d'")
    if 'history_7d' in bs:
        for h in bs['history_7d']:
            for field in ['date', 'satisfied_count', 'count']:
                check(field in h, f"bottom_signals.json: history_7d[] 缺少 '{field}'")

# ============================================================
# 6. market_environment.json
# ============================================================
me = load_json(os.path.join(DATA_DIR, 'market_environment.json'))
if me:
    check('indices' in me, "market_environment.json: 缺少 'indices'")
    check('hot_sectors_up' in me, "market_environment.json: 缺少 'hot_sectors_up'")
    check('hot_sectors_down' in me, "market_environment.json: 缺少 'hot_sectors_down'")
    stats = me.get('market_stats', {})
    for field in ['rise_count', 'fall_count', 'turnover_comment']:
        check(field in stats, f"market_environment.json: market_stats 缺少 '{field}'")

# ============================================================
# 7. plans.json
# ============================================================
pl = load_json(os.path.join(DATA_DIR, 'plans.json'))
if pl:
    check('plans' in pl, "plans.json: 缺少 'plans'")
    check('core_plan' in pl, "plans.json: 缺少 'core_plan'")
    if 'core_plan' in pl:
        for field in ['action', 'detail', 'conditions']:
            check(field in pl['core_plan'], f"plans.json: core_plan 缺少 '{field}'")
        if 'conditions' in pl['core_plan']:
            check(isinstance(pl['core_plan']['conditions'], list), "plans.json: core_plan.conditions 必须是数组")
    check('key_stats' in pl, "plans.json: 缺少 'key_stats'")
    if 'key_stats' in pl:
        for field in ['win_rate_30d', 'monthly_pnl_percent', 'execution_score']:
            check(field in pl['key_stats'], f"plans.json: key_stats 缺少 '{field}'")

# ============================================================
# 8. risk_assessment.json
# ============================================================
risk = load_json(os.path.join(DATA_DIR, 'risk_assessment.json'))
if risk:
    for field in ['level', 'score', 'factors', 'suggestion', 'rule_checks']:
        check(field in risk, f"risk_assessment.json: 缺少 '{field}'")
    if 'rule_checks' in risk:
        for i, rc in enumerate(risk['rule_checks']):
            for f in ['rule', 'passed', 'current_value']:
                check(f in rc, f"risk_assessment.json: rule_checks[{i}] 缺少 '{f}'")

# ============================================================
# 9. discipline_log.json
# ============================================================
dl = load_json(os.path.join(DATA_DIR, 'discipline_log.json'))
if dl:
    check('logs' in dl, "discipline_log.json: 缺少 'logs'")
    check('stats' in dl, "discipline_log.json: 缺少 'stats'")
    check('statistics' in dl, "discipline_log.json: 缺少 'statistics' (HTML使用此字段)")
    check('today_assessment' in dl, "discipline_log.json: 缺少 'today_assessment'")

# ============================================================
# 10. trades_today.json
# ============================================================
tt = load_json(os.path.join(DATA_DIR, 'trades_today.json'))
if tt:
    check('trades' in tt, "trades_today.json: 缺少 'trades'")
    s = tt.get('summary', {})
    for field in ['total_trades', 'buy_count', 'sell_count', 'realized_pnl']:
        check(field in s, f"trades_today.json: summary 缺少 '{field}'")

# ============================================================
# 11. reviews_daily.json
# ============================================================
rd = load_json(os.path.join(DATA_DIR, 'reviews_daily.json'))
if rd:
    check('records' in rd, "reviews_daily.json: 必须用 'records' 不是 'reviews'")
    if 'records' in rd:
        for i, r in enumerate(rd['records']):
            for field in ['date', 'pnl_amount', 'pnl_percent', 'trade_count', 'violation_count',
                          'execution_score', 'key_decisions', 'operation_analysis',
                          'planned_executed', 'planned_not_executed', 'unplanned_actions',
                          'market_review', 'emotion_state', 'tomorrow_focus']:
                check(field in r, f"reviews_daily.json: records[{i}] 缺少 '{field}'")

# ============================================================
# 12. reviews_weekly.json
# ============================================================
rw = load_json(os.path.join(DATA_DIR, 'reviews_weekly.json'))
if rw:
    check('records' in rw, "reviews_weekly.json: 必须用 'records'")
    if 'records' in rw:
        for i, r in enumerate(rw['records']):
            for field in ['week', 'date_range', 'pnl_amount', 'pnl_percent', 'trade_count',
                          'win_rate', 'violation_count', 'execution_score_avg',
                          'best_trade', 'worst_trade', 'weekly_reflection', 'key_lessons']:
                check(field in r, f"reviews_weekly.json: records[{i}] 缺少 '{field}'")

# ============================================================
# 13. reviews_monthly.json
# ============================================================
rm = load_json(os.path.join(DATA_DIR, 'reviews_monthly.json'))
if rm:
    check('records' in rm, "reviews_monthly.json: 必须用 'records'")
    if 'records' in rm:
        for i, r in enumerate(rm['records']):
            for field in ['month', 'pnl_amount', 'pnl_percent', 'trade_count', 'win_rate',
                          'max_drawdown_percent', 'sharpe_ratio', 'strategy_review',
                          'monthly_reflection', 'next_month_goals']:
                check(field in r, f"reviews_monthly.json: records[{i}] 缺少 '{field}'")

# ============================================================
# 14. fundamentals.json
# ============================================================
fu = load_json(os.path.join(DATA_DIR, 'fundamentals.json'))
if fu:
    check('stocks' in fu, "fundamentals.json: 缺少 'stocks'")

# ============================================================
# 15. news_impact.json
# ============================================================
ni = load_json(os.path.join(DATA_DIR, 'news_impact.json'))
if ni:
    check('messages' in ni, "news_impact.json: 缺少 'messages'")
    check('overall_sentiment' in ni, "news_impact.json: 缺少 'overall_sentiment'")
    for i, m in enumerate(ni.get('messages', [])[:5]):
        check('title' in m, f"news_impact.json: messages[{i}] 缺少 'title'")
        check('type' in m, f"news_impact.json: messages[{i}] 缺少 'type'")
        check(m.get('type') in ['利好', '利空', '中性'], f"news_impact.json: messages[{i}].type 必须是 利好/利空/中性")
        check('impact_level' in m, f"news_impact.json: messages[{i}] 缺少 'impact_level'")
        check(isinstance(m.get('impact_level'), (int, float)), f"news_impact.json: messages[{i}].impact_level 必须是数值")

# ============================================================
# 16. quick_eval.json
# ============================================================
qe = load_json(os.path.join(DATA_DIR, 'quick_eval.json'))
if qe:
    check('stocks' in qe, "quick_eval.json: 缺少 'stocks'")

# ============================================================
# 17. daily_review.json
# ============================================================
dr = load_json(os.path.join(DATA_DIR, 'daily_review.json'))
if dr:
    check('date' in dr, "daily_review.json: 缺少 'date'")
    check('score' in dr, "daily_review.json: 缺少 'score'")
    check('daily_metrics' in dr, "daily_review.json: 缺少 'daily_metrics'")

# ============================================================
# 18. 历史快照同步检查
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
        if 'records' in hist_rev:
            for i, r in enumerate(hist_rev['records']):
                for field in ['date', 'pnl_amount', 'pnl_percent']:
                    check(field in r, f"history/{date}/reviews_daily.json: records[{i}] 缺少 '{field}'")

# ============================================================
# 输出结果
# ============================================================
if errors:
    print(f"❌ 发现 {len(errors)} 个问题：")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print("✅ Schema 校验全部通过！所有 17 个 JSON 文件字段完整匹配 HTML。")
    sys.exit(0)

# ============================================================
# 19. state.json（状态连续性）
# ============================================================
st = load_json(os.path.join(DATA_DIR, 'state.json'))
if st:
    for field in ['meta', 'cumulative', 'current', 'today_so_far', 'positions', 'validation']:
        check(field in st, f"state.json: 缺少 '{field}'")
    if 'cumulative' in st:
        check('total_pnl_amount' in st['cumulative'], "state.json: cumulative 缺少 total_pnl_amount")
    if 'current' in st:
        for field in ['total_assets', 'prev_close_assets', 'initial_capital']:
            check(field in st['current'], f"state.json: current 缺少 '{field}'")
    # 交叉验证
    if 'current' in st and 'validation' in st:
        c = st['current']
        if 'total_assets' in c and 'initial_capital' in c:
            expected_pnl = c['total_assets'] - c['initial_capital']
            if 'cumulative' in st:
                actual_pnl = st['cumulative'].get('total_pnl_amount')
                if actual_pnl is not None:
                    check(abs(expected_pnl - actual_pnl) < 10,
                          f"state.json: total_pnl({actual_pnl}) != total_assets({c['total_assets']}) - initial({c['initial_capital']}) = {expected_pnl}")

# ============================================================
# 20. trades_all.json（交易总账）
# ============================================================
ta = load_json(os.path.join(DATA_DIR, 'trades_all.json'))
if ta:
    check('meta' in ta, "trades_all.json: 缺少 'meta'")
    check('trades' in ta, "trades_all.json: 缺少 'trades'")
    check('daily_summary' in ta, "trades_all.json: 缺少 'daily_summary'")
    if 'trades' in ta:
        for i, t in enumerate(ta['trades']):
            for field in ['seq', 'date', 'time', 'code', 'name', 'action', 'quantity', 'price', 'realized_pnl']:
                check(field in t, f"trades_all.json: trades[{i}] 缺少 '{field}'")
    if 'daily_summary' in ta:
        for i, ds in enumerate(ta['daily_summary']):
            for field in ['date', 'trade_count', 'realized_pnl']:
                check(field in ds, f"trades_all.json: daily_summary[{i}] 缺少 '{field}'")
        # 验证 trade_count 总和 == trades 数组长度
        summary_total = sum(ds['trade_count'] for ds in ta['daily_summary'])
        trades_count = len(ta['trades'])
        check(summary_total == trades_count,
              f"trades_all.json: daily_summary trade_count总和({summary_total}) != trades数组长度({trades_count})")
