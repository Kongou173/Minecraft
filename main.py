import asyncio
import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from gemini_chat import generate_reply
from keep_alive import keep_alive

# Botの初期設定（discord.Clientを使用）
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents)


# プリセンス(ステータス)表示
@tasks.loop(seconds=20)
async def presence_loop():
    game = discord.Game("/chatをプレイ中")
    await bot.change_presence(activity=game)


# Bot起動時の処理
@bot.event
async def on_ready():
    presence_loop.start()
    print(f"Logged in as {bot.me.name}")


# 会話機能
@app_commands.command(
    name="chat",
    description="Google Gemini APIを使って会話します",
)
@app_commands.describe(message="送信したいメッセージ")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer()  # 応答を一旦保留にして、タイムアウト回避
    try:
        reply = await asyncio.to_thread(
            generate_reply, message
        )  # Gemini APIからの応答を取得
        await ctx.send(reply)
    except Exception as e:
        await ctx.send(f"エラーが発生しました: {str(e)}")


# 履歴クリア機能
@bot.command(
    name="chat_clear",
    description="会話履歴をクリアします",
)
async def chat_clear(interaction: discord.Interaction):
    await interaction.response.send_message("会話履歴をクリアしました。")


# ヘルプ機能
@bot.command(
    name="help",
    description="使い方を表示します",
)
async def help(interaction: discord.Interaction):
    embed = (
        discord.Embed(title="ボットの使い方", colour=discord.Colour.blurple())
        .add_field(name="/chat", value="Google Geminiと会話することができます")
        .add_field(name="/chat_clear", value="会話履歴をクリアします")
        .add_field(
            name="/support",
            value="サポートサーバーへのリンクを確認することができます。",
        )
    )
    await interaction.response.send_message(embed=embed)


# Discordサーバリンク表示機能
@bot.command(
    name="support",
    description="サポートサーバーのリンクを表示します",
)
async def support(interaction: discord.Interaction):
    embed = interactions.Embed(
        title="サポートサーバー",
        description="[こちらからサポートサーバーに参加できます。](https://discord.gg/r594PHeNNp)",
        color=0xFF0000,
    )
    await interaction.response.send_message(embed=embed)


# Botを実行
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
