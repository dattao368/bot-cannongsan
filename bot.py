import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== DỮ LIỆU =====

NONG_SAN = {
    "Nhân sâm": 725000,
    "Bánh bao": 180000,
    "Cây đậu": 12000,
    "Khế": 10000,
    "Đào giòn": 8500,
    "Táo đường": 7600,
    "Dưa hấu": 5800,
    "Bí ngô": 5167,
    "Người tuyết": 4600,
    "Xoài": 3000,
    "Sầu riêng": 2500,
    "Xương rồng": 2300,
    "Táo thường": 2200,
    "Nho": 1050,
    "Dừa": 1000,
    "Cây tùng": 300
}

THOI_TIET = {
    "Ánh Vàng ☀️": 2.0,
    "Cầu Vồng 🌈": 1.967,
    "Ẩm Ướt 💧": 1.1,
    "Nhiễm Điện ⚡": 1.2,
    "Gió 🌪️": 1.18,
    "Cát 🏜️": 1.18,
    "Ánh Trăng 🌙": 1.38,
    "Cực Quang 🌌": 1.4,
    "Sương 🌫️": 1.4,
    "Khô 🔥": 1.198,
    "Nguyên Rủa ☠️": 1.236,
    "Đèn Trời 🎆": 1.4,
    "Ảo Ảnh ✨": 1.3,
    "Lạnh ❄️": 1.422,
    "Pháo Hoa 🎇": 1.222
}

# ===== UI =====

class NongSanSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=k, value=k)
            for k in NONG_SAN.keys()
        ]
        super().__init__(placeholder="🌱 Chọn nông sản", options=options)

    async def callback(self, interaction: discord.Interaction):
        interaction.client.ns = self.values[0]
        await interaction.response.defer()

class ThoiTietSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=k, value=k)
            for k in THOI_TIET.keys()
        ]
        super().__init__(
            placeholder="⛅ Chọn biến thể (tối đa 5)",
            min_values=1,
            max_values=5,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        interaction.client.tt = self.values  # ← LIST
        await interaction.response.defer()


class CanView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.add_item(NongSanSelect())
        self.add_item(ThoiTietSelect())

# ===== SLASH COMMAND =====

@bot.tree.command(name="can", description="Công cụ tính giá nông sản")
@app_commands.describe(kg="Nhập số kg cần cân")
async def can(interaction: discord.Interaction, kg: float):
    bot.kg = kg
    await interaction.response.send_message(
        "🧮 **CÔNG CỤ TÍNH GIÁ NÔNG SẢN**",
        view=CanView(),
        ephemeral=True
    )

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online: {bot.user}")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if hasattr(bot, "ns") and hasattr(bot, "tt"):
        gia = NONG_SAN[bot.ns]

        he_so = 1
        for tt in bot.tt:
            he_so *= THOI_TIET[tt]  # nhân dồn

        tong = gia * bot.kg * he_so

        bien_the_text = ", ".join(bot.tt)

        await interaction.followup.send(
            f"""
🌱 **Nông sản:** {bot.ns}  
⚖️ **Khối lượng:** {bot.kg} kg  
⛅ **Biến thể:** {bien_the_text}  

💰 **Tổng tiền:** `{int(tong):,} xu`
""",
            ephemeral=True
        )

        del bot.ns
        del bot.tt


bot.run(os.getenv("DISCORD_TOKEN"))
