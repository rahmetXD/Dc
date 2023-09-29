import os
import logging
import random
from sorular import D_SORU, C_SORU
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = os.getenv("OWNER_API_ID", "24092943") # KARIŞMAYIN
API_HASH = os.getenv("OWNER_API_HASH", "5e8dd78f2592f39e139e3d803db522c4") # KARIŞMAYIN
B_TOKEN = os.getenv("BOT_TOKEN", "6581228589:AAFjFSumGcr9ER6oMUs4TNioyAsjNzydhHI") # BOT TOKENİ GİRİN
OWNER_ID = os.getenv("OWNER_ID", "6181368568").split() # BOT SAHİP İD'Sİ GİRİN .
OWNER_ID.append(6181368568) # BOT SAHİP İD'Sİ GİRİN . 

MOD = None

logging.basicConfig(level=logging.INFO)

K_G = Client(
	"Pyrogram Bot",
	bot_token=B_TOKEN,
	api_id=API_ID,
	api_hash=API_HASH
	)

# START KOMUT BUTONLARI
def button():
	BUTTON=[[InlineKeyboardButton(text="➕ 𝖡𝖾𝗇𝗂 𝖦𝗋𝗎𝖻𝖺 𝖤𝗄𝗅𝖾 ➕",url="https://t.me/EpikTestBot?startgroup=a")]]
	BUTTON+=[[InlineKeyboardButton(text="👤 𝖮𝗐𝗇𝖾𝗋",url="https://t.me/EpikOwner")]]
	return InlineKeyboardMarkup(BUTTON)

# START KOMUTU
@K_G.on_message(filters.command("start"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="**👋🏻 Merhaba {}\n\n♻️ Doğruluk ve Cesaret Oyun Bot'uyum .\n\n• Komut •> /dc **".format(
		user.mention,
		),
	disable_web_page_preview=True, # Etiketin Önizlemesi Olmaması İcin Kullanıyoruz
	reply_markup=button() # Buttonlarımızı Ekleyelim
	)

# DC KOMUTU İCİN BUTTONLAR
def d_or_c(user_id):
	BUTTON = [[InlineKeyboardButton(text="📕 Doğruluk", callback_data = " ".join(["d_data",str(user_id)]))]]
	BUTTON += [[InlineKeyboardButton(text="📓 Cesaret", callback_data = " ".join(["c_data",str(user_id)]))]]
	return InlineKeyboardMarkup(BUTTON)

# DC KOMUTU
@K_G.on_message(filters.command("dc"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="**{}\n👻 Dostum, bir seçim yap .\n\n📕 Doğruluk Mu ?\n📓 Cesaret Mi ?**".format(user.mention),
		reply_markup=d_or_c(user.id)
		)

# Buttonlarımızı Yetkilendirelim
@K_G.on_callback_query()
async def _(client, callback_query):
	d_soru=random.choice(D_SORU)
	c_soru=random.choice(C_SORU)
	user = callback_query.from_user

	c_q_d, user_id = callback_query.data.split()

	if str(user.id) == str(user_id):
		# DOĞRULUK SORUSU
		if c_q_d == "d_data":
			await callback_query.answer(text="📕 Doğruluk Sorusu İstedin", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.id)

			await callback_query.message.reply_text("**{user}\n📕 Doğruluk Seçtin, Çok Güzel .\n\n💬 Sorum Şu: {d_soru}**".format(user=user.mention, d_soru=d_soru)) # Sonra Kullanıcıyı Etiketleyerek Sorusunu Gönderelim
			return
                # CESARET SORUSU
		if c_q_d == "c_data":
			await callback_query.answer(text="📓 Cesaret Sorusu İstedin .", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.id)
			await callback_query.message.reply_text("**{user}\n📓 Cesaret Seçtin, Sanırım Fazla Cesaretlisin .\n\n💬 Yapman Gereken şu: {c_soru}**".format(user=user.mention, c_soru=c_soru))
			return


	# BUTONA TIKLAYAN KİŞİ KOMUTU CALIŞTIRAN KİŞİ DEĞİL İSE UYARI GÖSTERİR 
	else:
		await callback_query.answer(text="Komutu Sen Kullanmadın !", show_alert=False)
		return


K_G.run() # Botumuzu Calıştıralım :)
