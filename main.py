from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from sheets import save_user, save_bot

TOKEN = "7173112564:AAGrLaXGViCRyDM4YGGCqxbXlu6pnfkGdFA"

menu = [["➕ إنشاء بوت"]]

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

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
