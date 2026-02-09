import pulp

# スタッフと条件の設定
staff = ["田中", "佐藤", "鈴木", "高橋"]
days = ["月", "火", "水", "木", "金", "土", "日"]
shifts = ["早番", "遅番"]

# 最適化パズルを解く準備
prob = pulp.LpProblem("ShiftOptimization", pulp.LpMinimize)
x = pulp.LpVariable.dicts("x", (staff, days, shifts), cat="Binary")

# 全員が1日1回、週4〜5回入るように計算
for j in days:
    for k in shifts:
        prob += pulp.lpSum([x[i][j][k] for i in staff]) == 2 # 各枠2名

for i in staff:
    for j in days:
        prob += pulp.lpSum([x[i][j][k] for k in shifts]) <= 1 # 1日1回
    prob += pulp.lpSum([x[i][j][k] for j in days for k in shifts]) >= 3 # 週3回以上

# 実行（パズルを解く）
prob.solve(pulp.PULP_CBC_CMD(msg=0))

# 結果を表示
print("--- 最適化されたシフト表 ---")
for j in days:
    print(f"【{j}曜日】")
    for k in shifts:
        assigned = [i for i in staff if pulp.value(x[i][j][k]) == 1]
        print(f"  {k}: {', '.join(assigned)}")


