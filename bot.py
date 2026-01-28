import os
import discord
from discord.ext import commands

# ==========================
# 🔑 TOKEN (Railway Variables)
# ==========================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise Exception("❌ TOKEN chưa có! Railway → Variables → Add TOKEN")

# ==========================
# 🌾 ROLE NÔNG DÂN ID
# ==========================
ROLE_NONG_DAN_ID = 1465291719087100059  # đổi đúng role server bạn

# ==========================
# INTENTS
# ==========================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# 🌱 GIÁ GỐC (xu/kg)
# ==========================
GIA_GOC = {
    "bí ngô": 5167,
    "nho": 1050,
    "dưa hấu": 5800,
    "dừa": 1000,
    "xoài": 3000,
    "trái cổ đại": 99999,
    "đậu thần": 12000,
    "khế": 10000,
    "táo đường": 7600,
}

# ==========================
# 🌱 EMOJI NÔNG SẢN (GIỐNG BOT BẠN)
# ==========================
EMOJI_NS = {
    "bí ngô": "<:bi_ngo:1465929149561704521>",
    "nho": "<:nho:1465929423147761859>",
    "dưa hấu": "<:dua_hau:1465929236660490436>",
    "dừa": "<:dua:1465929313051349035>",
    "xoài": "<:xoai:1465929367031910514>",
    "trái cổ đại": "<:trai_co_dai:1465929696498684181>",
    "đậu thần": "<:dau_than:1465929579775656069>",
    "khế": "<:khe:1465929502533095475>",
    "táo đường": "<:tao_duong:1465929638365761571>",
}

# ==========================
# 🌦 THỜI TIẾT + HỆ SỐ
# ==========================
BIEN_THE = {
    "bão tuyết": 1.4,
    "tuyết": 1.3,
    "mưa": 1.2,
    "mưa bão": 1.5,
    "sương mù": 1.4,
    "sương sớm": 1.3,
    "ánh trăng": 1.6,
    "cực quang": 2.0,
    "nắng nóng": 1.5,
    "gió": 1.2,
    "gió cát": 1.4,
}

EMOJI_TT = {
    "bão tuyết": "<:bao_tuyet:1465929805064306922>",
    "tuyết": "<:tuyet:1465930053039689810>",
    "mưa": "<:mua:1465930166654996490>",
    "mưa bão": "<:mua_bao:1465930483555635210>",
    "sương mù": "<:suong_mu:1465930208195510415>",
    "sương sớm": "<:suong_som:1465930409648066581>",
    "ánh trăng": "<:anh_trang:1465930353968677004>",
    "cực quang": "<:cuc_quang:1465929983074762948>",
    "nắng nóng": "<:nang_nong:1465929883216777227>",
    "gió": "<:gio:1465930114390032384>",
    "gió cát": "<:gio_cat:1465930264340599080>",
}

# ==========================
# 📌 BOT READY
# ==========================
@bot.event
async def on_ready():
    print("===================================")
    print("✅ Bot đã online:", bot.user)
    print("===================================")

# ==========================
# 📌 LỆNH CÂN: !can bí ngô 20 mưa cực quang
# ==========================
@bot.command()
async def can(ctx, nong_san=None, kg=None, *bien_the):

    if not nong_san or not kg:
        return await ctx.send(
            "❌ Sai cú pháp!\n"
            "Ví dụ: `!can bí ngô 20 mưa cực quang`"
        )

    nong_san = nong_san.lower()

    if nong_san not in GIA_GOC:
        return await ctx.send("❌ Nông sản không đúng!")

    try:
        kg = float(kg)
    except:
        return await ctx.send("❌ Kg phải là số!")

    # Giá gốc
    gia = GIA_GOC[nong_san]

    # Nhân biến thể
    he_so = 1.0
    ds_bt = []

    for bt in bien_the:
        bt = bt.lower()
        if bt in BIEN_THE:
            he_so *= BIEN_THE[bt]
            ds_bt.append(f"{EMOJI_TT[bt]} {bt.title()}")

    tong = int(gia * kg * he_so)

    role = ctx.guild.get_role(ROLE_NONG_DAN_ID)

    embed = discord.Embed(
        title="⚖️ CÔNG CỤ CÂN NÔNG SẢN",
        color=0x00ff99
    )

    embed.add_field(
        name="🌱 Nông sản",
        value=f"{EMOJI_NS[nong_san]} **{nong_san.title()}**",
        inline=False
    )

    embed.add_field(
        name="⚖️ Cân nặng",
        value=f"**{kg} kg**",
        inline=False
    )

    embed.add_field(
        name="🌈 Biến thể",
        value="\n".join(ds_bt) if ds_bt else "Không có",
        inline=False
    )

    embed.add_field(
        name="💰 Tổng xu",
        value=f"**{tong:,} xu**",
        inline=False
    )

    await ctx.send(
        content=role.mention if role else "",
        embed=embed
    )

# ==========================
# 🚀 RUN BOT
# ==========================
bot.run(TOKEN)
