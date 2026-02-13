import pandas as pd
import calendar
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Set
import copy

def generate_optimized_shift(year=2025, month=2):
    """
    理想的なシフト作成を実装した最適化版
    - 休みの順番を計画的に管理
    - 1日全体を見て効率的に配置
    - 休憩時間を計画的に設計
    - ピーク時間に戦力を集中
    - 月全体の計画を考慮
    - スキル・ポジションのバランスを最適化
    """
    
    # --- 1. スタッフ定義 (元のコードと同じ) ---
    staff_ids = {
        '高校生': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        '大学生': ['I', 'J', 'K', 'L', 'M'],
        'フリーター': ['AB', 'BC', 'BD'],
        'パート': ['MN', 'KO']
    }
    
    staff_master = {}
    for role, ids in staff_ids.items():
        for i, s_id in enumerate(ids):
            pos = 'キッチン' if i < (len(ids) + 1) // 2 else 'ホール'
            staff_master[s_id] = {
                'type': role, 
                'pos': pos, 
                'total_pay': 0, 
                'total_hours': 0,
                'work_days_this_week': 0,
                'scheduled_off_days': []  # 計画休日
            }

    def get_required_slots(hour, is_weekend):
        """必要人数を取得（元のコードと同じ）"""
        is_peak = (12 <= hour < 14) or (18 <= hour < 21)
        num = (3 if is_peak else 2) if is_weekend else (2 if is_peak else 1)
        return {"ホール": num, "キッチン": num}
    
    def can_work_at_time(staff_id, hour, is_weekend, date_obj, staff_info):
        """スタッフが特定の時間に勤務可能かを判定"""
        staff_type = staff_info['type']
        
        # 休日判定
        if date_obj in staff_info['scheduled_off_days']:
            return False
        
        # 週6日制限
        if staff_info['work_days_this_week'] >= 6:
            return False
        
        # スタッフ種別ごとの時間制限
        if staff_type == '高校生':
            limit_start, limit_end = (18, 21) if not is_weekend else (10, 22)
            return limit_start <= hour < limit_end
        elif staff_type == '大学生':
            # 🔧修正: 今日働いたら給与上限を超えるかチェック（最大14時間勤務と仮定）
            estimated_pay = staff_info['total_pay'] + (14 * 1100)
            if estimated_pay > 85833:
                return False
            limit_start = 18 if not is_weekend else 10
            return limit_start <= hour < 24
        elif staff_type == 'フリーター':
            return 10 <= hour < 24
        elif staff_type == 'パート':
            return not is_weekend and 10 <= hour < 18
        
        return False
    
    def calculate_priority_score(staff_id, hour, is_weekend, staff_info, date_obj):
        """
        スタッフの優先度スコアを計算
        - ピーク時間に適した人を優先
        - 累計労働時間が少ない人を優先
        - ポジションバランスを考慮
        """
        score = 0
        
        # 累計労働時間が少ない方が高スコア（最大100点）
        max_hours = 200
        score += (max_hours - min(staff_info['total_hours'], max_hours)) / 2
        
        # 🔧修正: 変数hourを使ってピーク判定
        is_peak = (12 <= hour < 14) or (18 <= hour < 21)
        
        # ピーク時間にフリーター・パートを優先（+50点）
        if is_peak:
            if staff_info['type'] in ['フリーター', 'パート']:
                score += 50
        
        # 大学生の給与上限を考慮（上限に近いほど低スコア）
        if staff_info['type'] == '大学生':
            remaining = 85833 - staff_info['total_pay']
            if remaining < 20000:  # 残り2万円以下
                score -= 30  # 優先度を下げる
        
        # 月後半は高校生を優先（大学生の離脱に備える）
        if date_obj.day > 20:
            if staff_info['type'] == '高校生':
                score += 20
        
        return score
    
    def plan_rest_days(staff_master, year, month, num_days):
        """
        月全体の休日を計画的に配分
        - フリーター・パートは交代で休む
        - 高校生・大学生は週1日休み
        """
        for staff_id, info in staff_master.items():
            staff_type = info['type']
            rest_days = []
            
            # 🔧修正: 正しい曜日計算を使用 (datetime.weekday()を使用)
            if staff_type == 'フリーター':
                # フリーター3名が交代で休む
                if staff_id == 'AB':
                    # 火曜休み (weekday() == 1)
                    rest_days = [d for d in range(1, num_days + 1) 
                                if datetime(year, month, d).weekday() == 1]
                elif staff_id == 'BC':
                    # 木曜休み (weekday() == 3)
                    rest_days = [d for d in range(1, num_days + 1) 
                                if datetime(year, month, d).weekday() == 3]
                else:  # BD
                    # 日曜休み (weekday() == 6)
                    rest_days = [d for d in range(1, num_days + 1) 
                                if datetime(year, month, d).weekday() == 6]
            
            elif staff_type == 'パート':
                # パート2名が交代で休む
                if staff_id == 'MN':
                    # 水曜休み (weekday() == 2)
                    rest_days = [d for d in range(1, num_days + 1) 
                                if datetime(year, month, d).weekday() == 2]
                else:  # KO
                    # 金曜休み (weekday() == 4)
                    rest_days = [d for d in range(1, num_days + 1) 
                                if datetime(year, month, d).weekday() == 4]
            
            elif staff_type == '高校生':
                # 高校生は曜日を分散（8名いるので調整）
                offset = ord(staff_id) - ord('A')
                target_weekday = offset % 7
                rest_days = [d for d in range(1, num_days + 1) 
                            if datetime(year, month, d).weekday() == target_weekday]
            
            elif staff_type == '大学生':
                # 大学生は曜日を分散（5名いるので調整）
                offset = ord(staff_id) - ord('I')
                target_weekday = (offset + 6) % 7
                rest_days = [d for d in range(1, num_days + 1) 
                            if datetime(year, month, d).weekday() == target_weekday]
            
            # 日付オブジェクトに変換
            info['scheduled_off_days'] = [
                pd.Timestamp(year, month, d) for d in rest_days if d <= num_days
            ]
    
    def optimize_daily_shift(date_obj, staff_master, is_weekend):
        """
        1日全体のシフトを最適化
        - ピーク時間に戦力を集中
        - 効率的な勤務時間を設計
        - 適切な休憩時間を確保
        """
        hourly_allocation = {h: {"ホール": [], "キッチン": []} for h in range(10, 24)}
        
        # 🔧修正: ピーク時間を正しく判定
        peak_hours = []
        for h in range(10, 24):
            if (12 <= h < 14) or (18 <= h < 21):
                peak_hours.append(h)
        
        # 通常時間
        normal_hours = [h for h in range(10, 24) if h not in peak_hours]
        
        # ピーク→通常の順で配置
        for hour in peak_hours + normal_hours:
            required = get_required_slots(hour, is_weekend)
            
            # 利用可能なスタッフをスコア順にソート
            available_staff = []
            for s_id, info in staff_master.items():
                if can_work_at_time(s_id, hour, is_weekend, date_obj, info):
                    score = calculate_priority_score(s_id, hour, is_weekend, info, date_obj)
                    available_staff.append((s_id, score, info))
            
            available_staff.sort(key=lambda x: x[1], reverse=True)
            
            # ポジションごとに配置
            for pos in ["ホール", "キッチン"]:
                needed = required[pos]
                placed = 0
                
                for s_id, score, info in available_staff:
                    if info['pos'] != pos:
                        continue
                    if placed >= needed:
                        break
                    
                    # この時間に既に配置されているかチェック
                    if s_id in hourly_allocation[hour]["ホール"] or s_id in hourly_allocation[hour]["キッチン"]:
                        continue
                    
                    # 配置
                    hourly_allocation[hour][pos].append(s_id)
                    placed += 1
        
        return hourly_allocation
    
    def design_break_time(work_hours):
        """
        休憩時間を計画的に設計
        - 拘束時間に応じた適切な休憩
        - 中間地点に配置
        """
        if not work_hours:
            return 0.0
        
        start = min(work_hours)
        end = max(work_hours) + 1
        duration = end - start
        actual_work = len(work_hours)
        
        # 自然休憩時間
        natural_break = duration - actual_work
        
        # 法定最低休憩
        legal_min = 0.0
        if duration > 8:
            legal_min = 1.0
        elif duration > 6:
            legal_min = 0.75
        
        # 計画的な休憩時間の設定
        if duration <= 6:
            # 6時間以内：休憩なしまたは短時間
            planned_break = max(natural_break, 0.0)
        elif duration <= 8:
            # 6〜8時間：45分〜1時間
            planned_break = max(natural_break, legal_min, 0.75)
        elif duration <= 10:
            # 8〜10時間：1時間
            planned_break = max(natural_break, 1.0)
        else:
            # 10時間超：1〜1.5時間
            planned_break = max(natural_break, 1.0)
            if duration > 12:
                planned_break = max(planned_break, 1.5)
        
        return planned_break

    # --- 2. メイン処理 ---
    shift_results = []
    alerts = []
    num_days = calendar.monthrange(year, month)[1]
    
    # 月全体の休日を事前に計画（🔧修正: year, monthを渡す）
    plan_rest_days(staff_master, year, month, num_days)
    
    for day in range(1, num_days + 1):
        date_obj = pd.Timestamp(year, month, day)
        is_weekend = date_obj.weekday() >= 5
        day_name = ["月", "火", "水", "木", "金", "土", "日"][date_obj.weekday()]
        
        # 週の切り替わり
        if date_obj.weekday() == 0:
            for s in staff_master.values():
                s['work_days_this_week'] = 0
        
        # 1日全体のシフトを最適化
        hourly_allocation = optimize_daily_shift(date_obj, staff_master, is_weekend)
        
        # 欠員チェック
        for hour in range(10, 24):
            required = get_required_slots(hour, is_weekend)
            for p in ["ホール", "キッチン"]:
                if len(hourly_allocation[hour][p]) < required[p]:
                    alerts.append(
                        f"【欠員警告】{date_obj.strftime('%m/%d')}({day_name}) "
                        f"{hour}:00台 {p}が不足（必要:{required[p]}名/現在:{len(hourly_allocation[hour][p])}名）"
                    )
        
        # --- 3. 休憩の挿入と結果の集計 ---
        # 🔧修正: 日単位で勤務日をカウント（各スタッフが今日働いたかを追跡）
        staff_worked_today = set()
        
        for s_id, info in staff_master.items():
            work_hours = [h for h in range(10, 24) if s_id in hourly_allocation[h][info['pos']]]
            if not work_hours:
                continue
            
            # 勤務時間の計算
            start_time = min(work_hours)
            end_time = max(work_hours) + 1
            total_duration = end_time - start_time
            actual_work_hours = len(work_hours)
            
            # 計画的な休憩時間の設計
            break_hours = design_break_time(work_hours)
            
            # 実労働時間の調整
            final_work_hours = total_duration - break_hours
            
            # マスター更新
            info['total_hours'] += final_work_hours
            info['total_pay'] += final_work_hours * 1100
            
            # 🔧修正: 日単位で勤務日カウント（今日初めて勤務する場合のみ+1）
            if s_id not in staff_worked_today:
                staff_worked_today.add(s_id)
                info['work_days_this_week'] += 1
            
            shift_results.append({
                "日付": date_obj.strftime('%Y/%m/%d'),
                "曜日": day_name,
                "スタッフID": s_id,
                "開始": f"{start_time}:00",
                "終了": f"{end_time}:00",
                "休憩": f"{int(break_hours * 60)}分",
                "実労働時間": final_work_hours
            })
    
    return pd.DataFrame(shift_results), alerts, staff_master

if __name__ == "__main__":
    df_shift, alerts, staff_summary = generate_optimized_shift(2025, 2)
    
    print("=" * 80)
    print("【最適化シフト表（先頭10件）】")
    print("=" * 80)
    print(df_shift.head(10))
    print()
    
    print("=" * 80)
    print("【欠員警告】")
    print("=" * 80)
    if alerts:
        for alert in alerts[:10]:  # 最初の10件
            print(alert)
        if len(alerts) > 10:
            print(f"... 他 {len(alerts) - 10} 件")
    else:
        print("欠員なし！完璧なシフトです。")
    print()
    
    print("=" * 80)
    print("【スタッフ別集計】")
    print("=" * 80)
    for s_id, info in sorted(staff_summary.items()):
        print(f"{s_id}（{info['type']}・{info['pos']}）: "
              f"{info['total_hours']:.1f}時間 / {info['total_pay']:,}円 / "
              f"休日: {len(info['scheduled_off_days'])}日")
def save_shift_to_excel(df, filename="最適化シフト表_2025_02.xlsx"):
    # ↓ ここから下の行はすべて、左端に「半角スペース4つ」が入っています
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='シフト一覧')

    workbook  = writer.book
    worksheet = writer.sheets['シフト一覧']

    # --- 書式定義 ---
    header_format = workbook.add_format({
        'bold': True, 'text_wrap': True, 'valign': 'vcenter',
        'fg_color': '#D7E4BC', 'border': 1, 'align': 'center'
    })
    
    hall_format = workbook.add_format({'bg_color': '#E1F5FE', 'border': 1})
    kitchen_format = workbook.add_format({'bg_color': '#FFEBEE', 'border': 1})
    default_format = workbook.add_format({'border': 1, 'align': 'center'})

    worksheet.set_column('A:H', 15, default_format)

    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    for row_num in range(1, len(df) + 1):
        pos_value = df.iloc[row_num-1]['ポジション']
        fmt = hall_format if pos_value == 'ホール' else kitchen_format
        
        for col_num in range(len(df.columns)):
            worksheet.write(row_num, col_num, df.iloc[row_num-1, col_num], fmt)

    writer.close()
    print(f"✨ ファイル保存完了: {filename}")



    # --- 実行セクション ---

  # --- プログラムの最後にあるこの部分を確認・修正してください ---

if __name__ == "__main__":
    # 1. シフト計算を実行
    df_shift, alerts, staff_summary = generate_optimized_shift(2025, 2)
    
    # 2. スタッフ別集計の表示（エラーが出ないように修正済み）
    print("\n" + "="*80)
    print("【スタッフ別集計】")
    print("="*80)
    for s_id, info in staff_summary.items():
        h = info.get('total_hours', 0)
        p = info.get('total_pay', 0)
        o = info.get('off_days', 0)
        pos = info.get('pos', '不明')
        print(f"{s_id}（{pos}）: {h}時間 / {p:,.0f}円 / 休日: {o}日")

    # 3. ポジション情報を紐付け
    pos_map = {s_id: info.get('pos', '不明') for s_id, info in staff_summary.items()}
    df_shift['ポジション'] = df_shift['スタッフID'].map(pos_map)
    
    # 4. 列の順番を整理
    column_order = ["日付", "曜日", "ポジション", "スタッフID", "開始", "終了", "休憩", "実労働時間"]
    df_shift = df_shift[column_order]

    # 5. Excelとして保存
    save_shift_to_excel(df_shift, filename="最適化シフト表_2025_02.xlsx")

    print("\n" + "="*50)
    print("✨ Excelファイルの作成に成功しました！")
    print("="*50)