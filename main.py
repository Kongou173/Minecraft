import os
import interactions
from gemini_chat import generate_reply
from keep_alive import keep_alive

# Botの初期設定（interactions.Clientを使用）
bot = interactions.Client(token=os.getenv("DISCORD_TOKEN"))

# Bot起動時の処理
@bot.event
async def on_ready():
    await bot.change_presence(activities=[interactions.PresenceActivity(name="/helpをプレイ中", type=interactions.PresenceActivityType.GAME)])
    print(f"Logged in as {bot.me.name}")

# 会話機能
@bot.command(
    name="chat",
    description="Google Gemini APIを使って会話します",
    options=[
        interactions.Option(
            name="message",
            description="送信したいメッセージ",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def chat(ctx, message: str):
    try:
        # 応答を一旦保留
        await ctx.defer()
        
        # Gemini APIからの応答を取得
        reply = generate_reply(message)  
        
        # 応答が正常であれば、返信
        await ctx.send(reply)
    except Exception as e:
        # エラーが発生した場合
        if not ctx._responded:
            await ctx.send(f"エラーが発生しました: {str(e)}")

# 履歴クリア機能
@bot.command(
    name="chat_clear",
    description="会話履歴をクリアします",
)
async def chat_clear(ctx):
    await ctx.send("会話履歴をクリアしました。")

# ヘルプ機能
@bot.command(
    name="help",
    description="使い方を表示します",
)
async def help(ctx):
    help_text = "/chat [メッセージ] - Google Geminiとの会話\n" \
                "/chat_clear - 会話履歴をクリア\n" \
                "/support - サポートサーバーへのリンクを表示"
    await ctx.send(help_text)

# Discordサーバリンク表示機能
@bot.command(
    name="support",
    description="サポートサーバーのリンクを表示します",
)
async def support(ctx):
    embed = interactions.Embed(
        title="サポートサーバー",
        description="こちらからサポートサーバーに参加できます。",
        color=0x00ff00,
    )
    embed.add_field(name="リンク", value="https://discord.gg/r594PHeNNp")  # サポートサーバのリンクを設定
    await ctx.send(embeds=[embed])

# Botを実行
keep_alive()  # サーバを継続稼働させるためのkeep_aliveモジュールの呼び出し
bot.start()  # discord-py-interactionsのスタート方法
