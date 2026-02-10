import pandas as pd
import calendar
import random

def generate_professional_shift(year=2025, month=2):
    # --- 1. スタッフ定義とポジション割り振り ---
    staff_ids = {
        '高校生': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
        '大学生': ['I', 'J', 'K', 'L', 'M'],
        'フリーター': ['AB', 'BC', 'BD'],
        'パート': ['MN', 'KO']
    }
    
    staff_master = {}
    for role, ids in staff_ids.items():
        # 半分をキッチン、残りをホール（奇数はキッチン優先）
        for i, s_id in enumerate(ids):
            pos = 'キッチン' if i < (len(ids) + 1) // 2 else 'ホール'
            staff_master[s_id] = {'type': role, 'pos': pos, 'monthly_pay': 0}

    # --- 2. 1時間ごとの必要人数の定義 ---
    def get_required_slots(hour, is_weekend):
        is_peak = (12 <= hour < 14) or (18 <= hour < 21)
        if is_weekend:
            num = 3 if is_peak else 2
        else:
            num = 2 if is_peak else 1
        return {"ホール": num, "キッチン": num}

    # --- 3. メイン処理 ---
    shift_results = []
    num_days = calendar.monthrange(year, month)[1]

    for day in range(1, num_days + 1):
        date_obj = pd.Timestamp(year, month, day)
        is_weekend = date_obj.weekday() >= 5
        day_name = ["月", "火", "水", "木", "金", "土", "日"][date_obj.weekday()]
        
        # 1日の勤務状況を記録
        daily_work = {s_id: {'start': None, 'end': None} for s_id in staff_master}

        # 10時から24時まで、1時間ごとに枠を埋める
        for hour in range(10, 24):
            required = get_required_slots(hour, is_weekend)
            current_on_duty = {"ホール": 0, "キッチン": 0}
            
            # スタッフをシャッフルして公平に割り当て
            shuffled_staff = list(staff_master.keys())
            random.shuffle(shuffled_staff)

            for s_id in shuffled_staff:
                info = staff_master[s_id]
                pos = info['pos']
                
                # すでにこの時間の必要人数を満たしているならパス
                if current_on_duty[pos] >= required[pos]:
                    continue
                
                # --- 勤務可能判定 (店長さんの厳しい条件) ---
                can_work = False
                if info['type'] == '高校生':
                    if not is_weekend and 18 <= hour < 21: can_work = True
                    if is_weekend and 10 <= hour < 22: can_work = True
                elif info['type'] == '大学生':
                    if not is_weekend and 18 <= hour < 24: can_work = True
                    if is_weekend and 10 <= hour < 24: can_work = True
                elif info['type'] == 'フリーター':
                    can_work = True # 全日フリー
                elif info['type'] == 'パート':
                    if not is_weekend and 10 <= hour < 18: can_work = True

                # 大学生の103万制限チェック
                if info['type'] == '大学生' and info['monthly_pay'] >= 85000:
                    can_work = False

                if can_work:
                    # 1日8時間制限のチェック
                    worked_hours = 0
                    if daily_work[s_id]['start'] is not None:
                        worked_hours = hour - daily_work[s_id]['start']
                    
                    if worked_hours < 8:
                        if daily_work[s_id]['start'] is None:
                            daily_work[s_id]['start'] = hour
                        daily_work[s_id]['end'] = hour + 1
                        current_on_duty[pos] += 1

        # 1日の終わりにデータを集計
        for s_id, period in daily_work.items():
            if period['start'] is not None:
                start, end = period['start'], period['end']
                duration = end - start
                # 休憩計算
                break_m = 60 if duration > 8 else (45 if duration > 6 else 0)
                actual_h = duration - (break_m / 60)
                pay = int(actual_h * 1100)
                
                staff_master[s_id]['monthly_pay'] += pay
                shift_results.append({
                    "日付": date_obj.strftime('%Y-%m-%d'), "曜日": day_name,
                    "スタッフID": s_id, "職種": staff_master[s_id]['type'],
                    "役割": staff_master[s_id]['pos'], "開始": f"{start:02d}:00",
                    "終了": f"{end:02d}:00", "実働": round(actual_h, 2), "給与": pay
                })

    # CSV出力
    df = pd.DataFrame(shift_results)
    df.to_csv(f'{month}月店舗最適化シフト.csv', index=False, encoding='utf-8-sig')
    print(f"{month}月のシフトを生成しました。")

generate_professional_shift(2025, 2)
