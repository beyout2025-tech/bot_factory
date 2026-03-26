import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# إعداد الاتصال
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# فتح الملف باستخدام ID الذي وضعته في الكود الخاص بك
SPREADSHEET_ID = "1UxpWI4Bzv8OvU2Y7b64kC-oev96TkCzuu5-0CmAkYRg"
ss = client.open_by_key(SPREADSHEET_ID)

# تعريف الأوراق للوصول السريع
users_sheet = ss.worksheet("المستخدمين")
bots_sheet = ss.worksheet("البوتات_المصنوعة")
settings_sheet = ss.worksheet("إعدادات_المحتوى")
logs_sheet = ss.worksheet("السجلات")

def register_new_user(user_id, username):
    """تسجيل مستخدم جديد في ورقة المستخدمين مع الإعدادات الافتراضية"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # الترتيب: ID المستخدم، اسم المستخدم، تاريخ التسجيل، الحالة، نوع الاشتراك، رصيد... إلخ
    user_data = [str(user_id), username, now, "نشط", "مجاني", 0, now, "ar", "Bot", "", 0]
    users_sheet.append_row(user_data)

def save_created_bot(owner_id, bot_type, bot_name, token):
    """حفظ بيانات البوت الجديد في ورقة البوتات_المصنوعة"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # الترتيب حسب أعمدة المصفوفة التي صممتها
    bot_data = [str(owner_id), bot_type, bot_name, token, "متوقف", "", "", now, "", 0, 0, "جيد", "", "polling", "free", "", "true", ""]
    bots_sheet.append_row(bot_data)

def get_content_settings(bot_id):
    """جلب إعدادات المحتوى لبوت معين"""
    try:
        cell = settings_sheet.find(str(bot_id))
        return settings_sheet.row_values(cell.row)
    except:
        return None

def add_log(bot_id, log_type, message):
    """إضافة سجل جديد في ورقة السجلات"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs_sheet.append_row([str(bot_id), log_type, message, now])
