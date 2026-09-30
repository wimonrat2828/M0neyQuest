# PAGES · แดชบอร์ดความคืบหน้า

กรอกสัปดาห์ที่ 1 แล้วอัปเดตทุกครั้งที่ commit — อาจารย์ดูไฟล์นี้ + `git log` แทนการถาม

**หัวข้อ:** MoneyQuest — เว็บแอปช่วยวางแผนการเก็บเงินและจัดการรายรับ–รายจ่าย
**data.json เก็บอะไร (field):** id, title, amount, type, category, date, is_selected
**คัดลอก data.json → data.sample.json แล้ว:** [x]

## team — หน้าทีม (สัปดาห์ 0)
- [x] กรอก `team.json` ครบทุกคน (ชื่อ, รหัส, บทบาท, งานที่รับผิดชอบ)
- [x] เปิด /team เห็นชื่อทุกคน
- [ ] commit `team: members filled` + push

## page1 — ผู้รับผิดชอบ: นายวชิรวิทย์ บุญรินทร์ · TITLE: Dashboard · แบบจาก catalog: stats + detail
- [x] คัดลอกจาก catalog แล้วเปลี่ยน TITLE
- [x] ใช้ field ของ data.json ของกลุ่ม
- [x] เปิด /page1 ได้ ไม่มี TODO
- [x] `check.bat` → /page1 ✓ ไม่มี warning
- [ ] commit `page1: Dashboard สรุปภาพรวมและสถิติการเงิน`

## page2 — ผู้รับผิดชอบ: นายสิรภพ เหนี่ยวพันธ์ · TITLE: Income & Expense · แบบจาก catalog: form + list
- [x] คัดลอกจาก catalog แล้วเปลี่ยน TITLE
- [x] ใช้ field ของ data.json ของกลุ่ม
- [x] เปิด /page2 ได้ ไม่มี TODO
- [x] `check.bat` → /page2 ✓ ไม่มี warning
- [ ] commit `page2: Income & Expense จัดการรายรับ-รายจ่าย`

## page3 — ผู้รับผิดชอบ: นายสิรภพ เหนี่ยวพันธ์ · TITLE: Quest Planner · แบบจาก catalog: form + calculator
- [x] คัดลอกจาก catalog แล้วเปลี่ยน TITLE
- [x] ใช้ field ของ data.json ของกลุ่ม
- [x] เปิด /page3 ได้ ไม่มี TODO
- [x] `check.bat` → /page3 ✓ ไม่มี warning
- [ ] commit `page3: Quest Planner วางแผนเควสการออม`

## page4 (โบนัส +5) — ผู้รับผิดชอบ: นางสาววิมลรัตน์ ประเสริฐสิน · TITLE: Daily Quest · สุ่มเควสออมเงินรายวัน
- [x] สร้างหน้า page4.py และ templates/page4.html
- [x] ใช้ random สุ่มเควสออมเงินประจำวัน และมีปุ่มบันทึกเงินออมเข้า data.json
- [x] เปิด /page4 ได้ ไม่มี TODO
- [x] `check.bat` → /page4 ✓ extra page bonus
- [ ] commit `page4: Daily Quest สุ่มภารกิจออมเงินรายวัน`

## models.py — ผู้รับผิดชอบ: นางสาววิมลรัตน์ ประเสริฐสิน
- [x] เปลี่ยนชื่อ class ให้ตรงหัวข้อ, field ตรง data.json (class Goal)
- [x] method 1 ตัวที่มีประโยชน์ (ไม่เหลือ TODO: progress_percent, remaining_amount, monthly_target, status_message)
- [x] มีหน้าใดหน้าหนึ่งใช้ class นี้ (ใช้ใน page1 และ page3)
- [x] `python check_project.py` → class ✓ 9/9
- [ ] commit `models: class Goal คำนวณเป้าหมายการเงิน`

## ส่งงาน
- [ ] `check.bat` → 60/60, pytest 4 passed, ไม่มี warning
- [ ] ทุกคนอยู่ใน `git log`
- [ ] นำเสนอ: ทุกคนอธิบายหน้าของตัวเอง 1 นาที

