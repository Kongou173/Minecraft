# main.py

import discord
from discord.ext import commands
import os
from gemini_chat import generate_reply
from keep_alive import keep_alive

# Intents設定
intents = discord.Intents.default()
intents.message_content = True

# Botの初期設定（`discord.Bot`を使用）
bot = discord.Bot(intents=intents)

# Bot起動時の処理
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="/helpをプレイ中"))
    print(f"Logged in as {bot.user}")

# 会話機能
@bot.command(name="chat")
async def chat(ctx, *, message):
    try:
        reply = generate_reply(message)  # Gemini APIからの応答を取得
        await ctx.send(reply)
    except Exception as e:
        await ctx.send("エラーが発生しました: " + str(e))

# 履歴クリア機能
@bot.slash_command(name="chat_clear", description="会話履歴をクリアします")
async def chat_clear(ctx):
    await ctx.respond("会話履歴をクリアしました。")

# ヘルプ機能
@bot.slash_command(name="help", description="使い方を表示します")
async def help(ctx):
    help_text = "/chat [メッセージ] - Google Geminiとの会話\n" \
                "/chat_clear - 会話履歴をクリア\n" \
                "/support - サポートサーバーへのリンクを表示"
    await ctx.respond(help_text)

# Discordサーバリンク表示機能
@bot.slash_command(name="support", description="サポートサーバーのリンクを表示します")
async def support(ctx):
    embed = discord.Embed(title="サポートサーバー", description="こちらからサポートサーバーに参加できます。", color=0x00ff00)
    embed.add_field(name="リンク", value="https://discord.gg/r594PHeNNp")  # サポートサーバのリンクを設定
    await ctx.respond(embed=embed)

# Botを実行
keep_alive()  # サーバを継続稼働させるためのkeep_aliveモジュールの呼び出し
bot.run(os.getenv("DISCORD_TOKEN"))
