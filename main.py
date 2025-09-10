import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# --- KONFIGURASI ---
import os
TOKEN_BOT = os.environ.get("TELEGRAM_TOKEN")
ADMIN_USER_ID = int(os.environ.get("ADMIN_USER_ID"))
MONGO_URI = os.environ.get("MONGO_URI")

# State untuk ConversationHandler
QUESTION, ANSWER = range(2)

# Atur logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- FUNGSI-FUNGSI BIASA (UNTUK USER) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Halo, {user_name}! Selamat datang. Ketik /help untuk melihat daftar perintah."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
    Perintah yang tersedia:
    /start - Memulai percakapan
    /help - Menampilkan pesan bantuan ini
    /faq - Menampilkan daftar pertanyaan interaktif
    """
    # Tambahkan menu admin jika pengguna adalah admin
    if update.effective_user.id == ADMIN_USER_ID:
        text += """
        \n*Perintah Admin:*
        /tambah_faq - Menambah FAQ baru
        /hapus_faq - Menghapus FAQ yang ada
        """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')

async def faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # (Fungsi ini sama seperti sebelumnya, tidak ada perubahan)
    try:
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COLLECTION]
        faqs = list(collection.find({}, {"_id": 1, "question": 1}))
        client.close()
        if not faqs:
            await update.message.reply_text("Maaf, belum ada data FAQ.")
            return
        keyboard = [[InlineKeyboardButton(faq['question'], callback_data=f"view_{faq['_id']}")] for faq in faqs]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Silakan pilih pertanyaan di bawah ini:", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error di faq_command: {e}")
        await update.message.reply_text("Maaf, terjadi kesalahan.")

# --- FUNGSI-FUNGSI ADMIN ---

# --- Bagian Tambah FAQ (ConversationHandler) ---
async def tambah_faq_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("Maaf, perintah ini hanya untuk admin.")
        return ConversationHandler.END
    await update.message.reply_text("Oke, mari kita tambahkan FAQ baru.\nSilakan kirim *pertanyaannya*. Kirim /batal untuk berhenti.", parse_mode='Markdown')
    return QUESTION

async def terima_pertanyaan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['question'] = update.message.text
    await update.message.reply_text("Pertanyaan disimpan. Sekarang, silakan kirim *jawabannya*. Kirim /batal untuk berhenti.", parse_mode='Markdown')
    return ANSWER

async def terima_jawaban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = context.user_data['question']
    answer = update.message.text
    try:
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COLLECTION]
        collection.insert_one({"question": question, "answer": answer})
        client.close()
        await update.message.reply_text("✅ FAQ baru berhasil ditambahkan!")
    except Exception as e:
        print(f"Error saat insert DB: {e}")
        await update.message.reply_text("❌ Terjadi kesalahan saat menyimpan ke database.")
    context.user_data.clear()
    return ConversationHandler.END

async def batal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Proses dibatalkan.")
    context.user_data.clear()
    return ConversationHandler.END

# --- Bagian Hapus FAQ ---
async def hapus_faq_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("Maaf, perintah ini hanya untuk admin.")
        return
    try:
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COLLECTION]
        faqs = list(collection.find({}, {"_id": 1, "question": 1}))
        client.close()
        if not faqs:
            await update.message.reply_text("Tidak ada FAQ untuk dihapus.")
            return
        keyboard = [[InlineKeyboardButton(f"❌ {faq['question']}", callback_data=f"delete_{faq['_id']}")] for faq in faqs]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Pilih FAQ yang ingin dihapus:", reply_markup=reply_markup)
    except Exception as e:
        print(f"Error di hapus_faq_start: {e}")
        await update.message.reply_text("Maaf, terjadi kesalahan.")

# --- FUNGSI HANDLER TOMBOL (di-upgrade) ---
async def button_click_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    action, doc_id = query.data.split('_', 1)

    try:
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COLLECTION]
        
        if action == "view":
            result = collection.find_one({"_id": ObjectId(doc_id)})
            if result:
                response_text = f"*{result['question']}*\n\n{result['answer']}"
                await query.edit_message_text(text=response_text, parse_mode='Markdown')
        
        elif action == "delete":
            # Cek lagi apakah yang menekan tombol adalah admin
            if query.from_user.id != ADMIN_USER_ID:
                await context.bot.send_message(chat_id=query.from_user.id, text="Aksi ini hanya untuk admin.")
                return
            
            result = collection.delete_one({"_id": ObjectId(doc_id)})
            if result.deleted_count > 0:
                await query.edit_message_text(text="✅ FAQ berhasil dihapus.")
            else:
                await query.edit_message_text(text="Gagal menghapus, FAQ tidak ditemukan.")
        
        client.close()

    except Exception as e:
        print(f"Error di button_click_handler: {e}")

# --- FUNGSI UTAMA ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN_BOT).build()

    # Conversation handler untuk tambah FAQ
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('tambah_faq', tambah_faq_start)],
        states={
            QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, terima_pertanyaan)],
            ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, terima_jawaban)],
        },
        fallbacks=[CommandHandler('batal', batal)],
    )

    # Daftarkan semua handler
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('faq', faq_command))
    application.add_handler(CommandHandler('hapus_faq', hapus_faq_start))
    application.add_handler(CallbackQueryHandler(button_click_handler))

    print("Bot Admin dengan Database MongoDB sedang berjalan...")
    application.run_polling()