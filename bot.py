import discord
from discord.ext import commands

# ================== CONFIG ==================
TOKEN = "MTQ2NTcxNjQ0ODg3MjYzMjQ1Mw.GfbV5C.slpMZ3P88z-hKzeceG2nkh_YLkZgRAsH9bdioU"

ROLE_NONG_DAN_ID = 123456789012345678  # thay ID role Nông Dân

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================== GIÁ GỐC (xu/kg) ==================
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

# ================== EMOJI NÔNG SẢN ==================
EMOJI_NS = {
    "bí ngô": "<:bi_ngo:1465929149561704521>",
    "nho": "<:nho:1465929423147761859>",
    "dưa hấu": "<:duahau:1465929236660490436>",
    "dừa": "<:dua:1465929313051349035>",
    "xoài": "<:xoai:1465929367031910514>",
    "trái cổ đại": "<:traicoidai:1465929696498684181>",
    "đậu thần": "<:dauthan:1465929579775656069>",
    "khế": "<:khe:1465929502533095475>",
    "táo đường": "<:taoduong:1465929638365761571>",
}

# ================== BIẾN THỂ THỜI TIẾT ==================
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
    "bão tuyết": "<:baotuyet:1465929805064306922>",
    "tuyết": "<:tuyet:1465930053039689810>",
    "mưa": "<:mua:1465930166654996490>",
    "mưa bão": "<:muabao:1465930483555635210>",
    "sương mù": "<:suongmu:1465930208195510415>",
    "sương sớm": "<:suongsom:1465930409648066581>",
    "ánh trăng": "<:anhtrang:1465930353968677004>",
    "cực quang": "<:cucquang:1465929983074762948>",
    "nắng nóng": "<:nangnong:1465929883216777227>",
    "gió": "<:gio:1465930114390032384>",
    "gió cát": "<:giocat:1465930264340599080>",
}

# ================== VIEW UI ==================
class CanView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.nong_san = None
        self.bien_the = []

    @discord.ui.select(
        placeholder="🌱 Chọn nông sản",
        options=[
            discord.SelectOption(label=name.title(), value=name, emoji=EMOJI_NS[name])
            for name in GIA_GOC
        ],
    )
    async def chon_nong_san(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.nong_san = select.values[0]
        await interaction.response.defer()

    @discord.ui.select(
        placeholder="🌈 Chọn biến thể (tối đa 5)",
        min_values=0,
        max_values=5,
        options=[
            discord.SelectOption(label=bt.title(), value=bt, emoji=EMOJI_TT[bt])
            for bt in BIEN_THE
        ],
    )
    async def chon_bien_the(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.bien_the = select.values
        await interaction.response.defer()

    @discord.ui.button(label="⚖️ Tính Giá", style=discord.ButtonStyle.success)
    async def tinh_gia(self, interaction: discord.Interaction, button: discord.ui.Button):

        if not self.nong_san:
            return await interaction.response.send_message(
                "❌ Bạn chưa chọn nông sản!", ephemeral=True
            )

        await interaction.response.send_modal(KgModal(self.nong_san, self.bien_the))


# ================== MODAL NHẬP KG ==================
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

        embed = discord.Embed(title="⚖️ CÔNG CỤ CÂN NÔNG SẢN", color=0x00ff99)

        embed.add_field(
            name="🌱 Nông sản",
            value=f"{EMOJI_NS[self.nong_san]} **{self.nong_san.title()}**",
            inline=False,
        )

        embed.add_field(name="⚖️ Cân nặng", value=f"**{kg} kg**", inline=False)

        ds = (
            "\n".join(f"{EMOJI_TT[x]} {x.title()}" for x in self.bien_the)
            if self.bien_the
            else "Không có"
        )

        embed.add_field(name="🌈 Biến thể", value=ds, inline=False)

        embed.add_field(name="💰 Kết quả", value=f"**{tong:,} xu**", inline=False)

        await interaction.response.send_message(content=f"{role.mention}", embed=embed)


# ================== SLASH COMMAND ==================
@bot.tree.command(name="can", description="Cân nông sản Play Together")
async def can(interaction: discord.Interaction):
    await interaction.response.send_message(
        "📌 **Chọn nông sản và biến thể để tính giá:**",
        view=CanView(),
    )


# ================== READY ==================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("✅ Bot online:", bot.user)


bot.run(TOKEN)
