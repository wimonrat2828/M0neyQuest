"""models.py — Data models for MoneyQuest.

ผู้รับผิดชอบ: นางสาววิมลรัตน์ ประเสริฐสิน
Class Goal represents a financial savings target / quest,
providing methods to calculate progress, remaining amount,
monthly savings required, and status messages.
"""


class Goal:
    def __init__(self, title, target_amount, current_savings=0.0, target_date=""):
        self.title = title
        self.target_amount = float(target_amount)
        self.current_savings = float(current_savings)
        self.target_date = target_date

    def progress_percent(self):
        """Calculate the percentage of target reached (0 to 100)."""
        if self.target_amount <= 0:
            return 100
        percent = int((self.current_savings / self.target_amount) * 100)
        if percent > 100:
            return 100
        return max(0, percent)

    def remaining_amount(self):
        """Calculate the remaining amount needed to complete the quest."""
        diff = self.target_amount - self.current_savings
        return max(0.0, diff)

    def monthly_target(self, months_left):
        """Calculate required monthly savings given remaining months."""
        if months_left <= 0:
            return self.remaining_amount()
        return round(self.remaining_amount() / months_left, 2)

    def status_message(self):
        """Return a descriptive message about quest status."""
        if self.current_savings >= self.target_amount:
            return f"เควส '{self.title}' สำเร็จแล้ว! (Mission Complete!)"
        percent = self.progress_percent()
        remaining = self.remaining_amount()
        return f"เควส '{self.title}' สำเร็จแล้ว {percent}% (ขาดอีก {remaining:,.2f} บาท)"


class Pet:
    """MoneyPet Companion — สัตว์เลี้ยงคู่หูนักออมเงิน."""

    SPECIES_MAP = {
        "cat": ("🐱", "น้องแมว"),
        "dog": ("🐶", "น้องหมา"),
        "rabbit": ("🐰", "น้องกระต่าย"),
        "frog": ("🐸", "น้องกบ"),
    }

    HATS_MAP = {
        "crown": ("👑", "มงกุฎราชา"),
        "grad_cap": ("🎓", "หมวกบัณฑิต"),
        "wizard": ("🎩", "หมวกจอมเวท"),
        "cap": ("🧢", "หมวกแก๊ป"),
        "flower": ("🌸", "ดอกไม้หวาน"),
        "none": ("", "ไม่ใส่หมวก"),
    }

    ACC_MAP = {
        "sunglasses": ("🕶️", "แว่นกันแดด"),
        "bow": ("🎀", "โบว์แดง"),
        "scarf": ("🧣", "ผ้าพันคอ"),
        "shield": ("🛡️", "โล่อัศวิน"),
        "none": ("", "ไม่ใส่ไอเทม"),
    }

    def __init__(self, name="น้องนำโชค", species="cat", hat="crown", accessory="sunglasses"):
        self.name = name or "น้องนำโชค"
        self.species = species if species in self.SPECIES_MAP else "cat"
        self.hat = hat if hat in self.HATS_MAP else "crown"
        self.accessory = accessory if accessory in self.ACC_MAP else "sunglasses"

    def get_base_emoji(self):
        """คืนค่าอีโมจิตัวสัตว์เลี้ยง"""
        return self.SPECIES_MAP.get(self.species, ("🐱", ""))[0]

    def get_hat_emoji(self):
        """คืนค่าอีโมจิหมวก"""
        return self.HATS_MAP.get(self.hat, ("", ""))[0]

    def get_acc_emoji(self):
        """คืนค่าอีโมจิเครื่องประดับ"""
        return self.ACC_MAP.get(self.accessory, ("", ""))[0]

    def get_stage_info(self, net_balance):
        """คำนวณขั้นการพัฒนาและประโยคคำพูดตามยอดเงินเก็บ"""
        if net_balance < 2000:
            stage_name = "เบบี้ฝึกออม"
            dialogue = f"สวัสดีฮับ! {self.name} รอเจ้านายออมเงินอยู่น้า~ 💖"
        elif net_balance < 5000:
            stage_name = "คู่หูนักออม"
            dialogue = f"ว้าวว! เงินเก็บเริ่มเยอะขึ้นแล้ว {self.name} แข็งแกร่งขึ้น! ✨"
        elif net_balance < 10000:
            stage_name = "ผู้พิทักษ์คลัง"
            dialogue = f"ชุดนี้เท่สุดๆ! เจ้านายบริหารเงินเก่งมากเลยฮะ! ⚔️"
        else:
            stage_name = "จอมราชันย์ทองคำ"
            dialogue = f"ออร่าสีทองเปล่งประกาย! ยอดเศรษฐีตัวจริงอยู่นี่แล้ว! 👑"

        return {
            "stage_name": stage_name,
            "dialogue": dialogue,
        }


def load_pet(items):
    """ดึงข้อมูลสัตว์เลี้ยงจากรายการใน storage"""
    for it in items:
        if it.get("type") == "pet":
            return Pet(
                name=it.get("name", "น้องนำโชค"),
                species=it.get("species", "cat"),
                hat=it.get("hat", "crown"),
                accessory=it.get("accessory", "sunglasses"),
            )
    return Pet()


def update_pet(items, name, species, hat, accessory):
    """อัปเดตข้อมูลการแต่งตัวสัตว์เลี้ยงลงใน items"""
    found = False
    for it in items:
        if it.get("type") == "pet":
            it["name"] = name
            it["species"] = species
            it["hat"] = hat
            it["accessory"] = accessory
            found = True
            break
    if not found:
        items.append({
            "id": 999,
            "title": "MoneyPet",
            "amount": 0.0,
            "type": "pet",
            "species": species,
            "name": name,
            "hat": hat,
            "accessory": accessory,
            "date": "2026-09-24",
            "is_selected": True,
        })
    return items



