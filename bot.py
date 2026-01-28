import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ==============================
# 🌐 WEB SERVER GIỮ BOT ONLINE (Railway)
# ==============================

app = Flask("railway_bot")

@app.route("/")
def home():
    return "Bot đang chạy OK!"

def run_web():
    app.run(host="0.0.0.0", port=3000)

Thread(target=run_web).start()

# ==============================
# 🔑 TOKEN (Railway Variables)
# ==============================

TOKEN = os.getenv("TOKEN")  # Railway sẽ lấy token ở Variables

if TOKEN is None:
    print("❌ TOKEN chưa được đặt trong Railway Variables!")
    exit()

# ==============================
# ⚙️ CONFIG ROLE
# ==============================

ROLE_NONG_DAN_ID = 123456789012345678  # thay ID role nông dân

# ==============================
# 🤖 BOT SETUP
# ==============================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==============================
# 💰 GIÁ GỐC
# ==============================

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

# ==============================
# 🌱 EMOJI NÔNG SẢN
# ==============================

EMOJI_NS = {
    "bí ngô": "🎃",
    "nho": "🍇",
    "dưa hấu": "🍉",
    "dừa": "🥥",
    "xoài": "🥭",
    "trái cổ đại": "🌟",
    "đậu thần": "🫘",
    "khế": "🍈",
    "táo đường": "🍎",
}

# ==============================
# 🌈 BIẾN THỂ THỜI TIẾT
# ==============================

BIEN_THE = {
    "bão tuyết": 1.4,
    "tuyết": 1.3,
    "mưa": 1.2,
    "mưa bão": 1.5,
    "sương mù": 1.4,
    "ánh trăng": 1.6,
    "cực quang": 2.0,
    "nắng nóng": 1.5,
}

EMOJI_TT = {
    "bão tuyết": "❄️",
    "tuyết": "🌨️",
    "mưa": "🌧️",
    "mưa bão": "⛈️",
    "sương mù": "🌫️",
    "ánh trăng": "🌙",
    "cực quang": "🌌",
    "nắng nóng": "☀️",
}

# ==============================
# 📌 VIEW UI
# ==============================

class CanView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.nong_san = None
        self.bien_the = []

    # Dropdown nông sản
    @discord.ui.select(
        placeholder="🌱 Chọn nông sản",
        options=[
            discord.SelectOption(
                label=name.title(),
                value=name,
                emoji=EMOJI_NS[name]
            )
            for name in GIA_GOC
        ]
    )
    async def chon_nong_san(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.nong_san = select.values[0]
        await interaction.response.defer()

    # Dropdown biến thể
    @discord.ui.select(
        placeholder="🌈 Chọn biến thể (tối đa 3)",
        min_values=0,
        max_values=3,
        options=[
            discord.SelectOption(
                label=bt.title(),
                value=bt,
                emoji=EMOJI_TT[bt]
            )
            for bt in BIEN_THE
        ]
    )
    async def chon_bien_the(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.bien_the = select.values
        await interaction.response.defer()

    # Button tính
    @discord.ui.button(label="⚖️ Tính Giá", style=discord.ButtonStyle.success)
    async def tinh_gia(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.nong_san:
            return await interaction.response.send_message(
                "❌ Bạn chưa chọn nông sản!",
                ephemeral=True
            )

        await interaction.response.send_modal(KgModal(self.nong_san, self.bien_the))


# ==============================
# 📝 MODAL NHẬP KG
# ==============================

class KgModal(discord.ui.Modal, title="Nhập số kg"):
    kg = discord.ui.TextInput(label="Cân nặng (kg)", placeholder="Ví dụ: 20")

    def __init__(self, nong_san, bien_the):
        super().__init__()
        self.nong_san = nong_san
        self.bien_the = bien_the

    async def on_submit(self, interaction: discord.Interaction):

        kg = float(self.kg.value)
        gia = GIA_GOC[self.nong_san]

        he_so = 1.0
        for bt in self.bien_the:
            he_so *= BIEN_THE[bt]

        tong = int(gia * kg * he_so)

        role = interaction.guild.get_role(ROLE_NONG_DAN_ID)

        embed = discord.Embed(
            title="⚖️ CÂN NÔNG SẢN PLAY TOGETHER",
            color=0x00ff99
        )

        embed.add_field(
            name="🌱 Nông sản",
            value=f"{EMOJI_NS[self.nong_san]} {self.nong_san.title()}",
            inline=False
        )

        embed.add_field(
            name="⚖️ Cân nặng",
            value=f"{kg} kg",
            inline=False
        )

        embed.add_field(
            name="🌈 Biến thể",
            value="Không có" if not self.bien_the else "\n".join(
                f"{EMOJI_TT[x]} {x.title()}" for x in self.bien_the
            ),
            inline=False
        )

        embed.add_field(
            name="💰 Tổng tiền",
