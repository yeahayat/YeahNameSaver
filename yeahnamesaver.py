import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8142907845:AAGA-EDMpLCr44QwVgB6SR9rm9ITjMrrzMo"
DATA_FILE = "movies.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data,f,indent=2,ensure_ascii=False)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/add чтобы что-то добавить")

async def add_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    movie_name = " ".join(context.args)

    if not movie_name:
        await update.message.reply_text("/add название")
        return
    
    data = load_data()
    if user_id not in data:
        data[user_id] = []
    
    data[user_id].append(movie_name)
    save_data(data)
    await update.message.reply_text(f"Найс добавил: {movie_name}")

async def list_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    movies = data.get(user_id, [])

    if not movies:
        await update.message.reply_text("Тут пустовато ^_^")
        return
    
    text = "\n".join(f"{i+1}. {name}" for i, name in enumerate(movies))
    await update.message.reply_text(f"Списочек:\n{text}")


async def clear_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    if user_id in data:
        del data[user_id]
        save_data(data)
        await update.message.reply_text("тут чисто!!!!!!")
    else:
        await update.message.reply_text("Пустенько")
    
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_movie))
app.add_handler(CommandHandler("list", list_movies))
app.add_handler(CommandHandler("clear", clear_movies))

print("Запуск....")
app.run_polling()
