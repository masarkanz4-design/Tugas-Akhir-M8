import discord
from discord.ext import commands
import sqlite3
# Memanggil data FAQ dari file faq_data.py yang kita buat di atas
from faq_data import FAQ_DATABASE

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Setup Database SQLite langsung di sini
db = sqlite3.connect("laporan_error.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tiket (nama TEXT, masalah TEXT)")
db.commit()

@bot.event
async def on_ready():
    print(f"Bot {bot.user.name} online dengan file terpisah!")

@bot.command()
async def mulai(ctx):
    embed = discord.Embed(
        title="🛠️ Pusat Bantuan - Semua Bisa Kamu Beli",
        description="Ketik kata kunci langsung di chat (seperti `pembayaran`, `error`, atau `bug`) atau pilih perintah di bawah:",
        color=discord.Color.blue()
    )
    embed.add_field(name="📚 Lihat Semua FAQ", value="Ketik `!faq`", inline=False)
    embed.add_field(name="🚨 Lapor Masalah", value="Ketik `!lapor [pesan]`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def faq(ctx):
    embed = discord.Embed(title="📚 Daftar FAQ Programmer", color=discord.Color.green())
    for keyword, answer in FAQ_DATABASE.items():
        embed.add_field(name=f"Topik: {keyword.capitalize()}", value=answer, inline=False)
    await ctx.send(embed=embed)

# Fitur otomatis mencocokkan FAQ dari file faq_data.py
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    pesan_teks = message.content.lower()

    for keyword, answer in FAQ_DATABASE.items():
        if keyword in pesan_teks:
            embed = discord.Embed(title=f"🤖 Jawaban Otomatis ({keyword.capitalize()})", description=answer, color=discord.Color.orange())
            await message.channel.send(embed=embed)
            break 

    await bot.process_commands(message)

@bot.command()
async def lapor(ctx, *, masalah):
    nama_user = ctx.author.name
    
    cursor.execute("INSERT INTO tiket (nama, masalah) VALUES (?, ?)", (nama_user, masalah))
    db.commit()
    
    await ctx.send(f"✅ Terima kasih **{nama_user}**, laporanmu berhasil disimpan ke database!")

@bot.command()
@commands.has_permissions(administrator=True)
async def cek_laporan(ctx):
    cursor.execute("SELECT * FROM tiket")
    semua_tiket = cursor.fetchall()
    
    if not semua_tiket:
        await ctx.send("📭 Belum ada laporan error.")
        return
        
    pesan = "📋 **Daftar Laporan Masalah:**\n"
    for row in semua_tiket:
        pesan += f"- **{row[0]}**: {row[1]}\n"
        
    await ctx.send(pesan)

# Jalankan bot
bot.run("TOKEN_DISINI")
