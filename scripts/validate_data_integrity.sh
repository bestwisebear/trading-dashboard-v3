#!/bin/bash
# 数据完整性验证角色 — 所有日程任务同步后必须运行
# 用法: bash scripts/validate_data_integrity.sh

DATA_DIR="/tmp/trading-dashboard/data"
ERRORS=0

red(){ echo -e "\033[31m$1\033[0m"; }
green(){ echo -e "\033[32m$1\033[0m"; }

echo "========== 数据完整性验证 =========="

# 1. 检查关键文件存在且非空
for f in state.json positions.json trades_all.json news_impact.json market_environment.json; do
  if [ ! -s "$DATA_DIR/$f" ]; then
    red "❌ $f 不存在或为空！"
    ERRORS=$((ERRORS+1))
  else
    green "✅ $f ($(wc -c < $DATA_DIR/$f) bytes)"
  fi
done

# 2. news_impact.json 必须有实质性内容
item_count=$(python3 -c "import json; d=json.load(open('$DATA_DIR/news_impact.json')); print(len(d.get('items',[])))" 2>/dev/null)
if [ "$item_count" -lt 3 ]; then
  red "❌ news_impact.json 只有 ${item_count} 条消息（需要≥3）！"
  ERRORS=$((ERRORS+1))
else
  green "✅ news_impact.json: ${item_count} 条消息"
fi

# 3. 交叉一致性：总资产 = 持仓市值 + 现金
python3 -c "
import json
s=json.load(open('$DATA_DIR/state.json'))
assets=s['current']['total_assets']
cash=s['current']['available_cash']
p_total=sum(p.get('market_value',0) for p in s.get('positions',[]))
diff=abs(assets - (p_total + cash))
if diff > 2:
    print(f'❌ 资产不匹配: 总资产{assets} ≠ 持仓{p_total} + 现金{cash} (差{diff})')
    exit(1)
else:
    print(f'✅ 资产交叉一致: {assets} = {p_total} + {cash} (差{diff:.2f})')
" 2>/dev/null || ERRORS=$((ERRORS+1))

# 4. GitHub Pages 可访问
http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://bestwisebear.github.io/trading-dashboard-v3/" 2>/dev/null)
if [ "$http_code" = "200" ]; then
  green "✅ GitHub Pages 可访问 (HTTP 200)"
else
  red "❌ GitHub Pages 访问失败 (HTTP ${http_code})"
  ERRORS=$((ERRORS+1))
fi

# 5. Canonical路径同步检查
if [ -s "/app/data/所有对话/主对话/看板V3/data/news_impact.json" ]; then
  canon_items=$(python3 -c "import json; print(len(json.load(open('/app/data/所有对话/主对话/看板V3/data/news_impact.json')).get('items',[])))" 2>/dev/null)
  if [ "$canon_items" -lt 1 ]; then
    red "❌ Canonical news_impact.json 为空！"
    ERRORS=$((ERRORS+1))
  else
    green "✅ Canonical同步正常: ${canon_items} 条"
  fi
else
  red "❌ Canonical news_impact.json 不存在！"
  ERRORS=$((ERRORS+1))
fi

echo "========== 结果: ${ERRORS} 个错误 =========="
exit $ERRORS
