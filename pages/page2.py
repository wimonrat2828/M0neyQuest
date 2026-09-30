"""pages/page2.py — จัดการรายรับ-รายจ่าย (Tracker & History).

ผู้รับผิดชอบ: นายสิรภพ เหนี่ยวพันธ์
รูปแบบ: form + list ผสมกัน
มีฟอร์มบันทึกรายรับ-รายจ่าย พร้อมการตรวจสอบความถูกต้อง (Validation),
ระบบลบรายการ และตารางแสดงประวัติรายการพร้อมตัวกรอง
"""
import datetime
import storage

TITLE = "Income & Expense"

CATEGORY_OPTIONS = [
    ("food", "อาหารและเครื่องดื่ม"),
    ("shopping", "ช้อปปิ้ง / ของใช้"),
    ("housing", "ที่พัก / ค่าน้ำค่าไฟ"),
    ("game", "เกมและความบันเทิง"),
    ("travel", "การเดินทาง"),
    ("salary", "เงินเดือน / รายได้ประจำ"),
    ("freelance", "งานเสริม / ฟรีแลนซ์"),
    ("other", "อื่นๆ"),
]

CATEGORY_DICT = dict(CATEGORY_OPTIONS)


def read_number(text):
    """แปลงข้อความเป็นตัวเลขทศนิยมอย่างปลอดภัย"""
    try:
        val = float(text)
    except (ValueError, TypeError):
        return None
    if val != val or val in (float("inf"), float("-inf")):
        return None
    return val


def build(query):
    items = storage.load()
    type_filter = query.get("type", "").strip()
    search_q = query.get("q", "").strip().lower()

    filtered = []
    total_income = 0.0
    total_expense = 0.0

    for item in items:
        itype = item.get("type", "")
        # กรองเฉพาะรายรับและรายจ่าย (ไม่รวมเป้าหมาย goal ในหน้านี้)
        if itype not in ("income", "expense"):
            continue

        amount = float(item.get("amount", 0))
        if itype == "income":
            total_income = total_income + amount
        elif itype == "expense":
            total_expense = total_expense + amount

        # ตัวกรองตามประเภท
        if type_filter and itype != type_filter:
            continue

        # ตัวกรองตามคำค้นหา
        if search_q and search_q not in item.get("title", "").lower():
            continue

        filtered.append(item)

    # เรียงลำดับจากวันที่ล่าสุด
    display_rows = list(reversed(filtered))

    today_str = datetime.date.today().strftime("%Y-%m-%d")

    return {
        "items": display_rows,
        "count": len(display_rows),
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense,
        "type_filter": type_filter,
        "search_q": search_q,
        "categories": CATEGORY_OPTIONS,
        "category_dict": CATEGORY_DICT,
        "today_str": today_str,
    }


def handle(form):
    """ประมวลผลฟอร์ม: ลบรายการ หรือ บันทึกรายการใหม่"""
    if not form:
        return "กรุณากรอกข้อมูลในแบบฟอร์ม"

    items = storage.load()

    # กรณีลบรายการ
    if "delete" in form:
        del_target = str(form.get("delete", "")).strip()
        idx_to_remove = -1
        target_name = ""
        for i, it in enumerate(items):
            if str(it.get("id")) == del_target:
                idx_to_remove = i
                target_name = it.get("title", "")
                break
        if idx_to_remove >= 0:
            items.pop(idx_to_remove)
            storage.save(items)
            return f"🗑️ ลบรายการ '{target_name}' เรียบร้อยแล้ว"
        return "✗ ไม่พบรายการที่ต้องการลบ"

    # ตรวจสอบความถูกต้องของข้อมูล (Validation)
    title = form.get("title", "").strip()
    if not title:
        return "⚠️ กรุณาระบุชื่อรายการ"

    amount = read_number(form.get("amount", ""))
    if amount is None:
        return "⚠️ กรุณาระบุจำนวนเงินเป็นตัวเลข"
    if amount <= 0:
        return "⚠️ จำนวนเงินต้องมากกว่า 0 บาท"

    item_type = form.get("type", "").strip()
    if item_type not in ("income", "expense"):
        return "⚠️ กรุณาเลือกประเภทรายการ (รายรับ หรือ รายจ่าย)"

    category = form.get("category", "").strip()
    if not category:
        return "⚠️ กรุณาเลือกหมวดหมู่รายการ"

    date_str = form.get("date", "").strip()
    if not date_str:
        date_str = datetime.date.today().strftime("%Y-%m-%d")

    # กำหนด ID ใหม่
    max_id = 100
    for it in items:
        if isinstance(it.get("id"), int) and it["id"] > max_id:
            max_id = it["id"]
    new_id = max_id + 1

    new_record = {
        "id": new_id,
        "title": title,
        "amount": round(amount, 2),
        "type": item_type,
        "category": category,
        "date": date_str,
        "is_selected": False,
    }

    items.append(new_record)
    storage.save(items)

    type_text = "รายรับ" if item_type == "income" else "รายจ่าย"
    return f"✓ บันทึก{type_text} '{title}' จำนวน {amount:,.2f} บาท สำเร็จแล้ว"

