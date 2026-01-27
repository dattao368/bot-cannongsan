import discord
from discord import app_commands
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ===== DỮ LIỆU =====

GIA_GOC = {
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

BIEN_THE = {
    "Ánh Vàng": 2.0,
    "Cầu Vồng": 1.967,
    "Ẩm Ướt": 1.10,
    "Nhiễm Điện": 1.20,
    "Gió": 1.18,
    "Cát": 1.18,
    "Ánh Trăng": 1.38,
    "Cực Quang": 1.40,
    "Sương": 1.40,
    "Khô": 1.198,
    "Nguyền Rủa": 1.236,
    "Đèn Trời": 1.40,
    "Ảo Ảnh": 1.30,
    "Lạnh": 1.422,
    "Pháo Hoa": 1.222
}

# ===== MODAL NHẬP KG =====
class KgModal(discord.ui.Modal, title="Nhập số kg"):
    kg = discord.ui.TextInput(label="Số kg", placeholder="VD: 17.58")

    def __init__(self, nong_san, bien_the):
        super().__init__()
        self.nong_san = nong_san
        self.bien_the = bien_the

    async def on_submit(self, interaction: discord.Interaction):
        try:
            kg = float(self.kg.value)
        except:
            await interaction.response.send_message("❌ Số kg không hợp lệ", ephemeral=True)
            return

        gia = GIA_GOC[self.nong_san] * kg * BIEN_THE[self.bien_the]

        embed = discord.Embed(
            title="🚨 CÂN NÔNG SẢN",
            color=0xFFD966
        )
        embed.add_field(name="Vật phẩm", value=self.nong_san, inline=False)
        embed.add_field(name="Cân nặng", value=f"{kg} kg", inline=True)
        embed.add_field(name="Biến thể", value=self.bien_the, inline=True)
        embed.add_field(name="💰 KẾT QUẢ", value=f"{int(gia):,} xu", inline=False)

        await interaction.response.send_message(embed=embed)

# ===== DROPDOWN BIẾN THỂ =====
class BienTheSelect(discord.ui.Select):
    def __init__(self, nong_san):
        options = [
            discord.SelectOption(label=name)
            for name in BIEN_THE.keys()
        ]
        super().__init__(placeholder="Chọn biến thể", options=options)
        self.nong_san = nong_san

    async def callback(self, interaction: discord.Interaction):
        bien_the = self.values[0]
        await interaction.response.send_modal(KgModal(self.nong_san, bien_the))

# ===== DROPDOWN NÔNG SẢN =====
class NongSanSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=name)
            for name in GIA_GOC.keys()
        ]
        super().__init__(placeholder="Chọn nông sản", options=options)

    async def callback(self, interaction: discord.Interaction):
        nong_san = self.values[0]
        view = discord.ui.View()
        view.add_item(BienTheSelect(nong_san))
        await interaction.response.send_message("🔽 Chọn biến thể", view=view, ephemeral=True)

# ===== VIEW =====
class NongSanView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(NongSanSelect())

# ===== SLASH COMMAND =====
@tree.command(name="can", description="Cân giá nông sản Play Together")
async def can(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🔽 Chọn nông sản cần cân",
        view=NongSanView(),
        ephemeral=True
    )

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot online: {client.user}")

client.run(os.getenv("DISCORD_TOKEN"))
