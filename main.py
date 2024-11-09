import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from gemini_chat import generate_reply
from keep_alive import keep_alive

# Botの初期設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# プリセンス(ステータス)表示
@tasks.loop(seconds=20)
async def presence_loop():
    game = discord.Game("/chatをプレイ中")
    await bot.change_presence(activity=game)

# Bot起動時の処理
@bot.event
async def on_ready():
    presence_loop.start()
    await bot.tree.sync()  # コマンドを同期
    print(f"Logged in as {bot.user.name}")

# 会話機能 (スラッシュコマンド)
@bot.tree.command(
    name="chat",
    description="Google Gemini APIを使って会話します",
)
@app_commands.describe(message="送信したいメッセージ")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer()  # 応答を一旦保留にして、タイムアウト回避
    try:
        # Gemini APIからの応答を非同期で取得
        reply = await asyncio.to_thread(generate_reply, message)  
        await interaction.followup.send(reply)  # 返答を送信
    except Exception as e:
        await interaction.followup.send(f"エラーが発生しました: {str(e)}")  # エラーが発生した場合にメッセージ送信

# 履歴クリア機能 (スラッシュコマンド)
@bot.tree.command(
    name="chat_clear",
    description="会話履歴をクリアします",
)
async def chat_clear(interaction: discord.Interaction):
    await interaction.response.send_message("会話履歴をクリアしました。")

# サポートサーバリンク表示機能 (スラッシュコマンド)
@bot.tree.command(
    name="support",
    description="サポートサーバーのリンクを表示します",
)
async def support(interaction: discord.Interaction):
    embed = discord.Embed(
        title="サポートサーバー",
        description="[こちらからサポートサーバーに参加できます。](https://discord.gg/r594PHeNNp)",
        color=0xFF0000,
    )
    await interaction.response.send_message(embed=embed)

# ヘルプ機能 (スラッシュコマンド)
@bot.tree.command(
    name="help",
    description="ボットの使い方を表示します",
)
async def bot_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ボットの使い方", color=discord.Colour.blurple()
    ).add_field(name="/chat", value="Google Geminiと会話することができます") \
     .add_field(name="/chat_clear", value="会話履歴をクリアします") \
     .add_field(name="/support", value="サポートサーバーのリンクを表示します") \
     .add_field(name="/help", value="ボットの使い方を表示します")
    
    await interaction.response.send_message(embed=embed)

# 重複コマンド登録防止
@bot.event
async def on_ready():
    # コマンドの同期
    await bot.tree.sync()
    print(f"Logged in as {bot.user.name}")
    presence_loop.start()

# Botを実行
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
