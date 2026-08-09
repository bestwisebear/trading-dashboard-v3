# 数据完整性规则 v1.0

> 本文件是所有数据写入日程的强制规范。每个写数据的 Agent 启动后第一件事读此文件。

## 1. 状态连续性（state.json）

**每次执行前必读：**
```
读取 data/state.json → 获取昨日的 total_assets / total_pnl / positions
```
- `prev_close_assets` = 昨日 state.json 的 `total_assets`
- `net_today` = `total_assets` - `prev_close_assets`
- `total_pnl_amount` = `total_assets` - `initial_capital`（固定200000）
- 更新后回写 state.json，同步更新 cumulative 和 today_so_far

## 2. 价格来源（强制）

| 时段 | 价格类型 | 说明 |
|------|---------|------|
| 盘后 16:15 | **收盘价** | 15:00 后的收盘价，用于日PnL计算 |
| 午间 11:35 | 盘中价 | 仅用于盘中展示，标注 session="intraday" |
| 盘前 08:25 | 昨收/竞价 | 不可用于日PnL计算 |

**铁律：日 PnL 只能用收盘价算，绝不能用盘中价。**

## 3. PnL 计算公式

```
日浮动盈亏 = Σ(持仓股收盘价 × 持仓数量) - Σ(持仓股成本价 × 持仓数量)
日已实现盈亏 = Σ(当日卖出交易的 realized_pnl)
日总盈亏 net_today = 日浮动盈亏 + 日已实现盈亏
累计盈亏 total_pnl = total_assets - initial_capital
```

**交叉验证（必须通过）：**
- ✅ `net_today == total_assets - prev_close_assets`
- ✅ `total_pnl_amount == total_assets - 200000`
- ✅ `Σ(所有日 net_today) == 最终 total_pnl`

## 4. 交易记录唯一源（trades_all.json）

- **trades_all.json** 是唯一的交易真相源
- 每日新增交易追加到 trades_all.json 的 trades 数组
- trades_today.json 的 trades 必须与 trades_all.json 中当日记录完全一致
- trade_count 必须与交易记录条数匹配，禁止手动填写

## 5. 字段名规范（HTML前端绑定，禁止改名）

### positions.json summary 必填：
`net_today`, `today_return`(=net_today), `total_pnl_amount`, `monthly_pnl`(=total_pnl_amount),
`total_assets`, `available_cash`, `position_ratio`, `prev_close_assets`, `initial_capital`,
`monthly_return_rate`, `today_return_rate`

### reviews_daily.json：
- 顶层键名必须是 `records`（不是 reviews/data）
- 每条记录必填：`date`, `pnl_amount`, `pnl_percent`, `trade_count`, `violation_count`,
  `execution_score`, `key_decisions`, `operation_analysis`,
  `planned_executed`, `planned_not_executed`, `unplanned_actions`,
  `market_review`, `emotion_state`, `tomorrow_focus`

### reviews_weekly.json：
- 顶层键名必须是 `records`
- 每条必填：`week`, `date_range`, `pnl_amount`, `pnl_percent`, `trade_count`,
  `win_rate`, `violation_count`, `execution_score_avg`,
  `best_trade`, `worst_trade`, `weekly_reflection`, `key_lessons`

### 其他：
- plans.json 必须同时有 `core_plan` + `key_stats` + `plans`
- risk_assessment.json 必须有 `rule_checks` 数组
- discipline_log.json 必须同时有 `stats` + `statistics`（内容相同）+ `today_assessment`
- bottom_signals.json 必须有 `aggregate`(含 ratio/recommendation) + `history_7d`

## 6. 写后校验（强制执行）

**每次写数据后，必须执行：**
```bash
cd /tmp/trading-dashboard && python3 scripts/validate_schema.py data/
```
- 校验不通过 → 修复后重新校验，直到通过
- 校验通过后 → 才能 git commit + push + 上传项目空间

## 7. 历史快照规范

- 路径：`data/history/YYYY-MM-DD/`
- 保留最近 7 个交易日
- 快照必须包含 positions.json（收盘价版本）+ trades_today.json + reviews_daily.json
- 快照中的收盘价必须与当日 positions.json 一致
