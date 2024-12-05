import discord
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import threading
import datetime

try:
	load_dotenv()
except:
	pass

# DISCORD_TOKEN, PROVIDER_URL, API_KEY, CHAT_MODEL, MAX_TOKENS, TEMPERATURE

m = " Please set a valid value in your .env file or as an environment variable."

if not os.getenv("DISCORD_TOKEN"):
	raise Exception("DISCORD_TOKEN is not set!" + m)

if not os.getenv("PROVIDER_URL"):
	raise Exception("PROVIDER_URL is not set!" + m)

if not os.getenv("API_KEY"):
	raise Exception("API_KEY is not set!" + m)

if not os.getenv("MAX_TOKENS").isdigit():
	print("MAX_TOKENS is not a valid integer, defaulting to 1024.")
	os.environ["MAX_TOKENS"] = 1024

try:
	os.environ["TEMPERATURE"] = str(float(os.getenv("TEMPERATURE")))
except ValueError:
	print("TEMPERATURE is not a valid number, defaulting to 0.")
	os.environ["TEMPERATURE"] = "0"

provider = OpenAI(
	base_url = os.getenv("PROVIDER_URL"),
	api_key = os.getenv("API_KEY")
)

try:
	provider.models.retrieve(os.getenv("CHAT_MODEL"))
except:
	raise Exception(os.getenv("CHAT_MODEL") + "is not a valid CHAT_MODEL!")

if os.getenv("VISION_MODEL"):
	raise Exception("Vision is not supported.")

client = discord.Client(intents=discord.Intents.all())

blacklist = []

if os.path.isfile("blacklist.json"):
	with open("blacklist.json", "r") as f:
		blacklist = json.load(f)

		# TO-DO: watch it

def is_blacklisted(id):
	return id in blacklist

def make_specials_LLM_friendly (content, guild):
	# replace <@12345678> with <@username>
	# replace <@!12345678> with <@username>
	# replace <#12345678> with <#channel>
	if guild:
		pass # replace <@&12345678> with <@&role>

	return content

def make_specials_LLM_unfriendly (content, guild):
	# replace <@username> with <@12345678>
	# replace <@!username> with <@!12345678>
	# replace <#channel> with <#12345678>
	if guild:
		pass # // replace <@&role> with <@&12345678>

	return content

@client.event
async def on_message(msg):
	if msg.author.id == client.user.id:
		return

	if is_blacklisted(msg.author.id) or is_blacklisted(msg.channel.id) or is_blacklisted(msg.guild.id):
		return

	if client.user.id not in [user.id for user in msg.mentions]:
		return

	try:
		# await msg.channel.sendTyping()
		await msg.channel.typing()
	except:
		return # an error here means we can't send messages, so don't even bother.

	# TO-DO: setInterval(msg.channel.sendTyping, 5000)

	channel_messages = None

	try:
		channel_messages = [msg async for msg in msg.channel.history(limit=100)]
	except e:
		return

	messages = [
		{ "role": "system", "content":
f"""- You are an AI assistant, based on the "{os.environ["CHAT_MODEL"]}" model, named {client.user.name}.
- You are in the "{msg.channel.name}" channel (<#{msg.channel.id}>) of the "{msg.guild.name}" Discord server.
- Use informal language with all-lowercase and only 1-2 sentences.
- You are a buggy mess due to being coded in the Python toy language.
- Engage in role-playing actions only when requested.
- Avoid using "UwU" or "OwO" as they are deprecated, instead using ":3".""" }
	]

	for message in channel_messages:
		if message.author.id == client.user.id:
			if message.type == 7:
				messages.append({ "role": "assistant", "content": f"<@{message.author.id}> joined the server." })
			else:
				messages.append({ "role": "assistant", "content": make_specials_LLM_friendly(message.content, message.guild) })
		else:
			content = ""

			if message.type == 7:
				messages.append({ "role": "user", "content": f"<@{message.author.id}> joined the server." })
				continue

			content += message.created_at.isoformat() + "\n"
			content += f"<@{message.author.name}#{message.author.discriminator}>"
			if message.author.nick:
				content += f" ({message.author.nick})"
			if message.author.bot:
				content += " (BOT)"
			if message.edited_at:
				content += " (edited)"
			if message.type == 19:
				content += f" (replying to <@{message.reference.message_id or 'unknown'}>)"

			content += ":\n" + make_specials_LLM_friendly(message.content, message.guild)

			messages.append({ "role": "user", "content": content })

	reply = { "content": "", "files": [], "embeds": [] }

	try:
		response = provider.chat.completions.create(
			model=os.environ["CHAT_MODEL"],
			messages=messages,
			temperature=float(os.getenv("TEMPERATURE")),
			max_tokens=int(os.getenv("MAX_TOKENS"))
		)

		reply["content"] = response.choices[0].message.content
	except Exception as e:
		reply["content"] = '⚠️ ' + str(e)

	if reply["content"] == "":
		return # :(

	reply["content"] = make_specials_LLM_unfriendly(reply["content"], message.guild)

	# if the contnet is over 2000
	if len(reply["content"]) > 2000:
		reply["content"] = reply["content"][:2000]

	try:
		await msg.reply(**reply)
	except:
		try:
			await msg.channel.send(**reply)
		except:
			pass # ¯\_(ツ)_/¯

@client.event
async def on_ready():
	print(f"ready on {client.user.name}#{client.user.discriminator}")

client.run(os.getenv("DISCORD_TOKEN"))