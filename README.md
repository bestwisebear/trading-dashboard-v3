# 交易看板 V3

A股交易决策看板，实时数据驱动。

## 数据源

看板从以下 JSON 文件实时拉取数据：
- positions.json - 持仓数据
- market_signals.json - 市场信号
- watchlist.json - 观察池
- trades_today.json - 今日交易
- discipline_log.json - 纪律日志
- risk_assessment.json - 风险评估
- news_impact.json - 消息面
- fundamentals.json - 基本面
- quick_eval.json - 快速检测（7道闸扫描）

数据每日自动刷新（06:00/09:00/11:35/15:15/20:00/23:00）。
