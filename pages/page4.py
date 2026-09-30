"""pages/page4.py — Daily Quest (ระบบสุ่มภารกิจออมเงินรายวัน).

ผู้รับผิดชอบ: นางสาววิมลรัตน์ ประเสริฐสิน
รูปแบบ: form + calculator / ranking ผสมกัน
มีระบบสุ่มเควสออมเงินรายวันด้วย random, ปุ่มสุ่มใหม่ (Reroll),
และปุ่มยอมรับเควสเพื่อบันทึกเงินออมเข้าสู่ระบบ
"""
import datetime
import random
import storage

TITLE = "Daily Quest"

QUEST_POOL = [
    {
        "id": "q1",
        "icon": "☕",
        "title": "งดหวาน ชื่นใจกระเป๋า",
        "desc": "งดซื้อชานมไข่มุก กาแฟพิเศษ หรือน้ำหวาน 1 วัน",
        "reward": 45.0,
        "difficulty": "ง่าย",
    },
    {
        "id": "q2",
        "icon": "🍱",
        "title": "เชฟกระทะเหล็ก",
        "desc": "ทำอาหารทานเอง หรือทานที่โรงอาหาร งดสั่งเดลิเวอรี่ 1 มื้อ",
        "reward": 80.0,
        "difficulty": "ปานกลาง",
    },
    {
        "id": "q3",
        "icon": "🪙",
        "title": "กระปุกเศษเหรียญ",
        "desc": "หยอดกระปุกด้วยเศษเหรียญทอนทั้งหมดที่ได้รับในวันนี้",
        "reward": 30.0,
        "difficulty": "ง่าย",
    },
    {
        "id": "q4",
        "icon": "🚶",
        "title": "สองเท้าก้าวประหยัด",
        "desc": "เดินออกกำลังกายแทนการนั่งวินมอเตอร์ไซค์ในระยะใกล้",
        "reward": 25.0,
        "difficulty": "ง่าย",
    },
    {
        "id": "q5",
        "icon": "🎮",
        "title": "ดองเกมพิชิตตลับ",
        "desc": "เคลียร์เกมเก่าที่มีอยู่ให้จบ งดซื้อเกมลดราคาใน Steam ชั่วคราว",
        "reward": 150.0,
        "difficulty": "ท้าทาย",
    },
    {
        "id": "q6",
        "icon": "🧴",
        "title": "นักสืบของใช้",
        "desc": "สำรวจของในห้อง ใช้ของที่มีให้หมดก่อนเปิดซื้อขวดใหม่",
        "reward": 60.0,
        "difficulty": "ปานกลาง",
    },
    {
        "id": "q7",
        "icon": "🥤",
        "title": "พกกระบอกน้ำคู่ใจ",
        "desc": "พกกระบอกน้ำส่วนตัวแทนการซื้อน้ำขวดพลาสติก",
        "reward": 20.0,
        "difficulty": "ง่าย",
    },
]


def build(query):
    items = storage.load()

    # นับสถิติเควสประจำวันที่พิชิตไปแล้ว
    completed_quests = []
    total_saved_from_quests = 0.0

    for it in items:
        title = it.get("title", "")
        if title.startswith("ภารกิจ:"):
            completed_quests.append(it)
            total_saved_from_quests = total_saved_from_quests + float(it.get("amount", 0))

    # สุ่มเควสประจำวัน 3 รายการ
    reroll = query.get("reroll", "")
    seed = int(query.get("seed", 0)) if query.get("seed", "").isdigit() else 0

    if reroll != "":
        seed = random.randint(1, 99999)

    rng = random.Random(seed if seed > 0 else 1309102)
    daily_quests = rng.sample(QUEST_POOL, 3)

    # ลูกเล่นทอยลูกเต๋าเสี่ยงทายออมเงิน (Dice Roll Challenge)
    dice_num = random.randint(1, 6)
    dice_reward = dice_num * 10

    next_seed = random.randint(1, 99999)

    return {
        "daily_quests": daily_quests,
        "dice_num": dice_num,
        "dice_reward": dice_reward,
        "completed_count": len(completed_quests),
        "total_saved_from_quests": total_saved_from_quests,
        "recent_completed": list(reversed(completed_quests))[:4],
        "next_seed": next_seed,
    }


def handle(form):
    """บันทึกการพิชิตเควสลงใน data.json"""
    if not form:
        return "กรุณาเลือกเควสที่ต้องการพิชิต"

    quest_title = form.get("quest_title", "").strip()
    reward_text = form.get("reward", "0").strip()

    try:
        reward = float(reward_text)
    except (ValueError, TypeError):
        reward = 0.0

    if not quest_title or reward <= 0:
        return "⚠️ ข้อมูลเควสไม่ถูกต้อง"

    items = storage.load()

    # สร้าง ID รายการใหม่
    max_id = 100
    for it in items:
        if isinstance(it.get("id"), int) and it["id"] > max_id:
            max_id = it["id"]
    new_id = max_id + 1

    today_str = datetime.date.today().strftime("%Y-%m-%d")

    new_record = {
        "id": new_id,
        "title": f"ภารกิจ: {quest_title}",
        "amount": round(reward, 2),
        "type": "income",
        "category": "freelance",
        "date": today_str,
        "is_selected": False,
    }

    items.append(new_record)
    storage.save(items)

    return f"🎉 ยอดเยี่ยมมาก! คุณพิชิตเควส '{quest_title}' และออมเงินเพิ่ม +{reward:,.2f} บาท สำเร็จแล้ว!"
