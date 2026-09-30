"""pages/page3.py — เควสเก็บเงิน (MoneyQuest Planner & Simulator).

ผู้รับผิดชอบ: นายสิรภพ เหนี่ยวพันธ์
รูปแบบ: form + calculator ผสมกัน
มีระบบตั้งเป้าหมายทางการเงิน (Quests), ระบบคำนวณเงินออมต่อวัน/สัปดาห์/เดือน,
การจำลองแผนการออมทีละเดือน (Milestone Simulator) ผ่าน class models.Goal
"""
import models
import storage

TITLE = "Quest Planner"


def read_number(text, default=0.0):
    """แปลงข้อความเป็นตัวเลขทศนิยมอย่างปลอดภัย"""
    try:
        val = float(text)
    except (ValueError, TypeError):
        return default
    if val != val or val in (float("inf"), float("-inf")):
        return default
    return val


def build(query):
    items = storage.load()

    # คำนวณเงินเก็บปัจจุบันจากรายรับ–รายจ่าย
    total_income = 0.0
    total_expense = 0.0
    goals = []

    for item in items:
        itype = item.get("type", "")
        amount = float(item.get("amount", 0))
        if itype == "income":
            total_income = total_income + amount
        elif itype == "expense":
            total_expense = total_expense + amount
        elif itype == "goal":
            goals.append(item)

    current_savings = total_income - total_expense

    # เลือกเป้าหมายที่จะนำมาคำนวณ
    selected_id = query.get("goal_id", "")
    active_goal = None
    for g in goals:
        if str(g.get("id")) == selected_id:
            active_goal = g
            break
    if active_goal is None:
        for g in goals:
            if g.get("is_selected", False):
                active_goal = g
                break
    if active_goal is None and len(goals) > 0:
        active_goal = goals[0]

    # กำหนดจำนวนเดือนในการจำลอง
    months_req = int(read_number(query.get("months", 6), 6))
    if months_req < 1:
        months_req = 1
    elif months_req > 36:
        months_req = 36

    goal_obj = None
    monthly_saving = 0.0
    daily_saving = 0.0
    weekly_saving = 0.0
    remaining = 0.0
    is_completed = False
    sim_rows = []
    advice = ""

    if active_goal is not None:
        goal_obj = models.Goal(
            active_goal.get("title", "เป้าหมาย"),
            active_goal.get("amount", 0),
            current_savings,
            active_goal.get("date", ""),
        )

        remaining = goal_obj.remaining_amount()
        monthly_saving = goal_obj.monthly_target(months_req)
        daily_saving = round(monthly_saving / 30.0, 2)
        weekly_saving = round(monthly_saving / 4.0, 2)

        if current_savings >= goal_obj.target_amount:
            is_completed = True
            advice = "🎉 ยอดเยี่ยมมาก! คุณมีเงินเก็บเพียงพอสำหรับเควสนี้แล้ว (Mission Complete!)"
        else:
            if monthly_saving > 15000:
                advice = f"⚠️ แผนนี้ต้องเก็บเงินเดือนละ {monthly_saving:,.2f} บาท ซึ่งค่อนข้างสูง ลองเพิ่มจำนวนเดือนเพื่อผ่อนคลายแผนการออม"
            elif months_req <= 2 and remaining > 5000:
                advice = "⚠️ เวลากระชั้นชิด ต้องมีวินัยในการออมเงินอย่างเคร่งครัด"
            else:
                advice = f"💡 แนะนำให้ออมสม่ำเสมอเดือนละ {monthly_saving:,.2f} บาท (หรือวันละ {daily_saving:,.2f} บาท) คุณจะพิชิตเป้าหมายได้ตามกำหนด!"

        # จำลองการออมสะสมทีละเดือน (Milestone Loop)
        accumulated = current_savings
        m = 1
        while m <= months_req:
            accumulated = accumulated + monthly_saving
            pct = int((accumulated / goal_obj.target_amount) * 100) if goal_obj.target_amount > 0 else 100
            if pct > 100:
                pct = 100
            sim_rows.append({
                "month": m,
                "monthly_deposit": monthly_saving,
                "accumulated": accumulated,
                "percent": pct,
            })
            m = m + 1

    return {
        "goals": goals,
        "active_goal": active_goal,
        "goal_obj": goal_obj,
        "current_savings": current_savings,
        "months": months_req,
        "monthly_saving": monthly_saving,
        "daily_saving": daily_saving,
        "weekly_saving": weekly_saving,
        "remaining": remaining,
        "is_completed": is_completed,
        "sim_rows": sim_rows,
        "advice": advice,
    }


def handle(form):
    """ประมวลผลฟอร์ม: ลบเควส, สลับเควสหลัก, หรือสร้างเควสใหม่"""
    if not form:
        return "กรุณากรอกข้อมูลในแบบฟอร์ม"

    items = storage.load()

    # ลบเควส
    if "delete_goal" in form:
        del_target = str(form.get("delete_goal", "")).strip()
        idx_to_remove = -1
        target_name = ""
        for i, it in enumerate(items):
            if str(it.get("id")) == del_target and it.get("type") == "goal":
                idx_to_remove = i
                target_name = it.get("title", "")
                break
        if idx_to_remove >= 0:
            items.pop(idx_to_remove)
            storage.save(items)
            return f"🗑️ ลบเควส '{target_name}' เรียบร้อยแล้ว"
        return "✗ ไม่พบเควสที่ต้องการลบ"

    # ตั้งเป็นเควสหลัก
    if "select_goal" in form:
        sel_id = str(form.get("select_goal", "")).strip()
        selected_name = ""
        for it in items:
            if it.get("type") == "goal":
                if str(it.get("id")) == sel_id:
                    it["is_selected"] = True
                    selected_name = it.get("title", "")
                else:
                    it["is_selected"] = False
        storage.save(items)
        if selected_name:
            return f"⭐ ตั้งเควส '{selected_name}' เป็นเควสหลักเรียบร้อยแล้ว"
        return "✗ ไม่พบเควส"

    # เพิ่มเควสใหม่
    title = form.get("title", "").strip()
    if not title:
        return "⚠️ กรุณาระบุชื่อเควสเป้าหมาย"

    amount = read_number(form.get("amount", ""), -1)
    if amount <= 0:
        return "⚠️ จำนวนเงินเป้าหมายต้องเป็นตัวเลขที่มากกว่า 0"

    target_date = form.get("target_date", "").strip()
    if not target_date:
        target_date = "2026-12-31"

    category = form.get("category", "shopping").strip()

    max_id = 100
    for it in items:
        if isinstance(it.get("id"), int) and it["id"] > max_id:
            max_id = it["id"]
    new_id = max_id + 1

    new_goal = {
        "id": new_id,
        "title": title,
        "amount": round(amount, 2),
        "type": "goal",
        "category": category,
        "date": target_date,
        "is_selected": False,
    }

    items.append(new_goal)
    storage.save(items)
    return f"🎉 เพิ่มเควสใหม่ '{title}' เป้าหมาย {amount:,.2f} บาท สำเร็จแล้ว!"

