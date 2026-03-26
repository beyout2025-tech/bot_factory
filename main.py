import os
import sys
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from sheets import save_user, save_bot

# إعدادات البوت والتحقق
TOKEN = "7173112564:AAGrLaXGViCRyDM4YGGCqxbXlu6pnfkGdFA"
ADMIN_ID = 873158772 # معرفك الذي زودتنا به

menu = [["➕ إنشاء بوت"]]

# وظيفة التعامل مع الملفات المرفوعة (تحديث موديولات البوت)
async def handle_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تحديث أو إضافة ملفات .py إلى مجلد modules مباشرة من تليجرام"""
    if update.effective_user.id != ADMIN_ID:
        return

    doc = update.message.document
    if doc.file_name.endswith(".py"):
        file = await doc.get_file()
        # التأكد من وجود مجلد modules
        if not os.path.exists("modules"):
            os.makedirs("modules")
            
        file_path = f"modules/{doc.file_name}"
        await file.download_to_drive(file_path)
        
        await update.message.reply_text(
            f"✅ تم استلام الموديول: {doc.file_name}\n🚀 جاري إعادة تشغيل المصنع لتطبيق التعديلات..."
        )
        
        # إعادة تشغيل السكريبت ليعتمد الملفات الجديدة
        os.execv(sys.executable, ['python'] + sys.argv)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username)
    
    await update.message.reply_text(
        "أهلاً بك في مصنع البوتات 🤖",
        reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "➕ إنشاء بوت":
        keyboard = [
            ["📩 تواصل"],
            ["🛡 حماية"],
            ["🎓 منصة تعليمية"],
            ["🛒 متجر"]
        ]
        
        await update.message.reply_text(
            "اختر نوع البوت:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    
    elif text in ["📩 تواصل", "🛡 حماية", "🎓 منصة تعليمية", "🛒 متجر"]:
        context.user_data["type"] = text
        await update.message.reply_text("أرسل اسم البوت:")
    
    else:
        bot_type = context.user_data.get("type")
        
        if bot_type:
            save_bot(update.effective_user.id, bot_type, text)
            
            await update.message.reply_text(
                f"✅ تم إنشاء بوت ({bot_type}) باسم: {text}"
            )
            
            context.user_data.clear()

# بناء التطبيق
app = ApplicationBuilder().token(TOKEN).build()

# إضافة المعالجات (Handlers)
app.add_handler(CommandHandler("start", start))
# معالج الملفات للأدمن فقط لتحديث الأكواد
app.add_handler(MessageHandler(filters.Document.FileExtension("py"), handle_docs))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
