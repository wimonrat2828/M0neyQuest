"""pages/page1.py — สรุปการเงิน (Dashboard & Stats).

ผู้รับผิดชอบ: นายวชิรวิทย์ บุญรินทร์
รูปแบบ: stats + detail ผสมกัน
แสดงยอดเงินเก็บปัจจุบัน, สถิติรายรับ/รายจ่าย, สัดส่วนค่าใช้จ่ายตามหมวดหมู่,
และ % ความคืบหน้าของเควสเป้าหมายผ่าน class models.Goal
"""
import models
import storage

TITLE = "Dashboard"

CATEGORY_NAMES = {
    "food": "อาหารและเครื่องดื่ม",
    "shopping": "ช้อปปิ้ง / ของใช้",
    "housing": "ที่พัก / ค่าน้ำค่าไฟ",
    "game": "เกมและความบันเทิง",
    "travel": "การเดินทาง",
    "salary": "เงินเดือน / รายได้ประจำ",
    "freelance": "งานเสริม / ฟรีแลนซ์",
    "other": "อื่นๆ",
}


def build(query):
    items = storage.load()

    total_income = 0.0
    total_expense = 0.0
    per_category = {}
    goals = []
    transactions = []

    for item in items:
        item_type = item.get("type", "")
        amount = float(item.get("amount", 0))

        if item_type == "income":
            total_income = total_income + amount
            transactions.append(item)
        elif item_type == "expense":
            total_expense = total_expense + amount
            transactions.append(item)
            cat = item.get("category", "other")
            if cat in per_category:
                per_category[cat] = per_category[cat] + amount
            else:
                per_category[cat] = amount
        elif item_type == "goal":
            goals.append(item)

    net_balance = total_income - total_expense

    top_category = "-"
    max_expense = 0.0
    for cat in per_category:
        if per_category[cat] > max_expense:
            max_expense = per_category[cat]
            top_category = CATEGORY_NAMES.get(cat, cat)

    bars = []
    for cat in per_category:
        percent = 0
        if max_expense > 0:
            percent = int((per_category[cat] / max_expense) * 100)
        bars.append({
            "code": cat,
            "label": CATEGORY_NAMES.get(cat, cat),
            "amount": per_category[cat],
            "percent": percent,
        })

    selected_goal = None
    goal_obj = None
    if len(goals) > 0:
        goal_id = query.get("goal_id", "")
        for g in goals:
            if str(g.get("id")) == goal_id:
                selected_goal = g
                break
        if selected_goal is None:
            for g in goals:
                if g.get("is_selected", False):
                    selected_goal = g
                    break
        if selected_goal is None:
            selected_goal = goals[0]

        goal_obj = models.Goal(
            selected_goal.get("title", "เป้าหมาย"),
            selected_goal.get("amount", 0),
            net_balance,
            selected_goal.get("date", ""),
        )

    recent_items = list(reversed(transactions))[:5]

    # ---------- Gamification: Level & EXP ----------
    exp_from_savings = int(max(0.0, net_balance) / 500.0) * 100
    exp_from_records = len(transactions) * 50
    completed_goals = 0
    for g in goals:
        g_target = float(g.get("amount", 0))
        if g_target > 0 and net_balance >= g_target:
            completed_goals = completed_goals + 1
    exp_from_goals = completed_goals * 300

    total_exp = exp_from_savings + exp_from_records + exp_from_goals

    if total_exp < 500:
        level = 1
        rank_title = "Novice Adventurer"
        rank_badge = "🥉 นักออมฝึกหัด"
        current_level_min = 0
        next_level_exp = 500
    elif total_exp < 1500:
        level = 2
        rank_title = "Silver Keeper"
        rank_badge = "🥈 นักสะสมเงินเหรียญ"
        current_level_min = 500
        next_level_exp = 1500
    elif total_exp < 3000:
        level = 3
        rank_title = "Gold Crusader"
        rank_badge = "🥇 อัศวินคลังสมบัติ"
        current_level_min = 1500
        next_level_exp = 3000
    elif total_exp < 5000:
        level = 4
        rank_title = "Treasure Master"
        rank_badge = "💎 จอมเวทคลังหลวง"
        current_level_min = 3000
        next_level_exp = 5000
    else:
        level = 5
        rank_title = "Dragon Slayer"
        rank_badge = "👑 ราชาผู้พิชิตเป้าหมาย"
        current_level_min = 5000
        next_level_exp = 5000

    if level >= 5:
        exp_percent = 100
        exp_progress_text = "MAX LEVEL"
    else:
        level_exp_range = next_level_exp - current_level_min
        exp_in_level = total_exp - current_level_min
        exp_percent = int((exp_in_level / level_exp_range) * 100) if level_exp_range > 0 else 100
        exp_progress_text = f"{exp_in_level} / {level_exp_range} EXP"

    # ---------- Gamification: Badges / Achievements ----------
    unlocked_first_blood = len(transactions) >= 1
    unlocked_goal_crusher = completed_goals >= 1 or (goal_obj is not None and goal_obj.progress_percent() >= 100)
    unlocked_wealth_builder = net_balance >= 10000.0
    fun_expense = per_category.get("shopping", 0.0) + per_category.get("game", 0.0)
    unlocked_budget_saver = total_expense > 0 and (fun_expense <= (total_expense * 0.20))

    badges = [
        {
            "id": "first_blood",
            "icon": "🛡️",
            "name": "First Blood",
            "desc": "บันทึกรายการเงินเข้า/ออกครั้งแรกในระบบ",
            "unlocked": unlocked_first_blood,
            "req": "บันทึกอย่างน้อย 1 รายการ",
        },
        {
            "id": "goal_crusher",
            "icon": "🎯",
            "name": "Goal Crusher",
            "desc": "พิชิตเควสเป้าหมายการออมสำเร็จ 100%",
            "unlocked": unlocked_goal_crusher,
            "req": "สะสมเงินจนครบเป้าหมายเควส",
        },
        {
            "id": "wealth_builder",
            "icon": "💰",
            "name": "Wealth Builder",
            "desc": "มียอดเงินเก็บคงเหลือสุทธิสะสมแตะ 10,000 บาท",
            "unlocked": unlocked_wealth_builder,
            "req": "มีเงินคงเหลือ >= 10,000 ฿",
        },
        {
            "id": "budget_saver",
            "icon": "🧘",
            "name": "Budget Saver",
            "desc": "ควบคุมค่าใช้จ่ายช้อปปิ้งและเกมไม่เกิน 20% ของรายจ่าย",
            "unlocked": unlocked_budget_saver,
            "req": "ช้อปปิ้ง+เกม <= 20% ของรายจ่ายรวม",
        },
    ]

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance,
        "transaction_count": len(transactions),
        "top_category": top_category,
        "bars": bars,
        "goals": goals,
        "selected_goal": selected_goal,
        "goal_obj": goal_obj,
        "recent_items": recent_items,
        "category_names": CATEGORY_NAMES,
        "total_exp": total_exp,
        "level": level,
        "rank_title": rank_title,
        "rank_badge": rank_badge,
        "exp_percent": exp_percent,
        "exp_progress_text": exp_progress_text,
        "badges": badges,
    }

