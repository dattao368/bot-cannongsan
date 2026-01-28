import os
import discord
from discord.ext import commands

# ==========================
# 🔑 TOKEN Railway Variables
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
    "bí ngô kêu la": 153120,
    "cây tùng": 320,
    "nhân sâm": 705000,
    "bánh bao hấp": 1040000,
    "người tuyết": 5060,
}

# ==========================
# 🌱 EMOJI NÔNG SẢN (emoji của bạn)
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
    "bí ngô kêu la": "<:bi_ngo_keu_la:1465971922494820514>",
    "cây tùng": "<:cay_tung:1465977949869179047>",
    "nhân sâm": "<:nhan_sam:1465971726469828688>",
    "người tuyết": "<:nguoi_tuyet:1465971855558053992>",
    "bánh bao hấp": "<:nguoi_tuyet:1465971790357729487>",
}

# ==========================
# 🌦 BIẾN THỂ (hệ số nhân)
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

# ==========================
# 🌦 EMOJI BIẾN THỂ (emoji của bạn)
# ==========================
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
# 📌 MODAL NHẬP KG
# ==========================
class KgModal(discord.ui.Modal, title="⚖️ Nhập số kg"):
    kg = discord.ui.TextInput(
        label="Cân nặng (kg)",
        placeholder="Ví dụ: 20"
    )

    def __init__(self, nong_san, bien_the):
        super().__init__()
        self.nong_san = nong_san
        self.bien_the = bien_the

    async def on_submit(self, interaction: discord.Interaction):
        try:
            kg = float(self.kg.value)
        except:
            return await interaction.response.send_message(
                "❌ Kg phải là số!",
                ephemeral=True
            )

        gia = GIA_GOC[self.nong_san]

        # nhân hệ số biến thể
        he_so = 1.0
        for bt in self.bien_the:
            he_so *= BIEN_THE[bt]

        tong = int(gia * kg * he_so)

        role = interaction.guild.get_role(ROLE_NONG_DAN_ID)

        embed = discord.Embed(
            title="⚖️ KẾT QUẢ CÂN NÔNG SẢN",
            color=0x00ff99
        )

        embed.add_field(
            name="🌱 Nông sản",
            value=f"{EMOJI_NS[self.nong_san]} **{self.nong_san.title()}**",
            inline=False
        )

        embed.add_field(
            name="⚖️ Số kg",
            value=f"**{kg} kg**",
            inline=False
        )

        if self.bien_the:
            ds = "\n".join(
                f"{EMOJI_TT[x]} {x.title()}" for x in self.bien_the
            )
        else:
            ds = "Không có"

        embed.add_field(
            name="🌦 Biến thể",
            value=ds,
            inline=False
        )

        embed.add_field(
            name="💰 Tổng xu",
            value=f"**{tong:,} xu**",
            inline=False
        )

        await interaction.response.send_message(
            content=role.mention if role else "",
            embed=embed
        )

# ==========================
# 📌 VIEW DROPDOWN UI
# ==========================
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
    async def chon_nong_san(self, interaction, select):
        self.nong_san = select.values[0]
        await interaction.response.defer()

    # Dropdown biến thể
    @discord.ui.select(
        placeholder="🌦 Chọn biến thể (tối đa 5)",
        min_values=0,
        max_values=5,
        options=[
            discord.SelectOption(
                label=bt.title(),
                value=bt,
                emoji=EMOJI_TT[bt]
            )
            for bt in BIEN_THE
        ]
    )
    async def chon_bien_the(self, interaction, select):
        self.bien_the = select.values
        await interaction.response.defer()

    # Button nhập kg
    @discord.ui.button(label="⚖️ Nhập kg & Tính", style=discord.ButtonStyle.success)
    async def tinh(self, interaction, button):

        if not self.nong_san:
            return await interaction.response.send_message(
                "❌ Bạn chưa chọn nông sản!",
                ephemeral=True
            )

        await interaction.response.send_modal(
            KgModal(self.nong_san, self.bien_the)
        )

# ==========================
# SLASH COMMAND /can
# ==========================
@bot.tree.command(name="can", description="Cân nông sản Play Together")
async def can(interaction: discord.Interaction):
    await interaction.response.send_message(
        "📌 Chọn nông sản + biến thể, sau đó nhập kg:",
        view=CanView()
    )

# ==========================
# READY SYNC
# ==========================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("✅ Bot online:", bot.user)

# ==========================
# RUN BOT
# ==========================
bot.run(TOKEN)
