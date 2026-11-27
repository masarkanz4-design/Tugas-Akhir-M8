import discord
from discord.ext import commands
# Memanggil fungsi dari file database.py yang kita buat barusan
import database

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Menyiapkan database saat bot pertama kali nyala
    database.setup_database()
    print(f"Bot {bot.user.name} online dan siap menggunakan file database terpisah!")

@bot.command()
async def mulai(ctx):
    embed = discord.Embed(
        title="🛠️ Pusat Bantuan - Semua Bisa Kamu Beli",
        description="Halo! Pilih perintah di bawah ini:",
        color=discord.Color.blue()
    )
    embed.add_field(name="📚 Lihat FAQ", value="Ketik `!faq`", inline=False)
    embed.add_field(name="🚨 Lapor Masalah", value="Ketik `!lapor [pesan]`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def faq(ctx):
    embed = discord.Embed(title="📚 FAQ Programmer", color=discord.Color.green())
    embed.add_field(name="1. Tugas Programmer", value="Memperbaiki website yang error.", inline=False)
    embed.add_field(name="2. Gagal Bayar", value="Tunggu 10-15 menit.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def lapor(ctx, *, masalah):
    nama_user = ctx.author.name
    
    # Menyimpan data menggunakan fungsi dari file database.py
    database.simpan_tiket(nama_user, masalah)
    
    await ctx.send(f"✅ Terima kasih **{nama_user}**, laporanmu berhasil disimpan ke database!")

@bot.command()
@commands.has_permissions(administrator=True)
async def cek_laporan(ctx):
    # Mengambil data menggunakan fungsi dari file database.py
    semua_tiket = database.ambil_semua_tiket()
    
    if not semua_tiket:
        await ctx.send("📭 Belum ada laporan error.")
        return
        
    pesan = "📋 **Daftar Laporan Masalah:**\n"
    for row in semua_tiket:
        pesan += f"- **{row[0]}**: {row[1]}\n"
        
    await ctx.send(pesan)

# Jalankan bot
bot.run("TOKEN_DISINI")
