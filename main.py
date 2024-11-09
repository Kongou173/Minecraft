import os
import discord  # discord.pyを使用します
from gemini_chat import generate_reply
from keep_alive import keep_alive

# Botの設定
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Bot起動時の処理
@client.event
async def on_ready():
    print("Botは正常に起動しました！")
    print(client.user.name)  # Botの名前
    print(client.user.id)  # BotのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')
    # ステータスメッセージを「TEST」に設定
    await client.change_presence(activity=discord.Game(name="TEST"))

# チャット機能
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # /chat コマンド
    if message.content.startswith("/chat "):
        try:
            user_message = message.content[len("/chat "):].strip()
            reply = generate_reply(user_message)  # Gemini APIからの応答を取得
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send("エラーが発生しました: " + str(e))

    # /chat_clear コマンド
    elif message.content == "/chat_clear":
        await message.channel.send("会話履歴をクリアしました。")

    # /help コマンド
    elif message.content == "/help":
        help_text = "/chat [メッセージ] - Google Geminiとの会話\n" \
                    "/chat_clear - 会話履歴をクリア\n" \
                    "/support - サポートサーバーへのリンクを表示"
        await message.channel.send(help_text)

    # /support コマンド
    elif message.content == "/support":
        embed = discord.Embed(
            title="サポートサーバー",
            description="こちらからサポートサーバーに参加できます。",
            color=0x00ff00
        )
        embed.add_field(name="リンク", value="https://discord.gg/r594PHeNNp")  # サポートサーバのリンクを設定
        await message.channel.send(embed=embed)

# サーバを維持するためのkeep_aliveの呼び出し
keep_alive()

# Botを起動（トークンを環境変数から取得）
client.run(os.getenv("DISCORD_TOKEN"))
