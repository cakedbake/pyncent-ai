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

if not os.getenv("CHAT_MODEL"):
	raise Exception("CHAT_MODEL is not set!" + m)

if not os.getenv("MAX_TOKENS").isdigit():
	print("MAX_TOKENS is not a valid integer, defaulting to 1024.")
	os.environ["MAX_TOKENS"] = 1024

try:
	temperature = float(os.getenv("TEMPERATURE"))
except ValueError:
	print("TEMPERATURE is not a valid number, defaulting to 0.")
	temperature = 0

provider = OpenAI(
	base_url = os.getenv("PROVIDER_URL"),
	api_key = os.getenv("API_KEY")
)

# check that CHAT_MODEL and VISION_MODEL exist
try:
	provider.models.retrieve(os.getenv("CHAT_MODEL"))
except:
	raise Exception(os.getenv("CHAT_MODEL") + "is not a valid CHAT_MODEL!")

try:
	provider.models.retrieve(os.getenv("VISION_MODEL"))
except:
	print(os.getenv("VISION_MODEL") + "is not a valid VISION_MODEL, vision will be disabled.")
	os.environ["VISION_MODEL"] = False

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
async def on_message(message):
	if message.author.id == client.user.id:
		return

	if is_blacklisted(message.author.id) or is_blacklisted(message.channel.id) or is_blacklisted(message.guild.id):
		return

	if client.user.id not in [user.id for user in message.mentions]:
		return

	try:
		# await msg.channel.sendTyping()
		await message.channel.typing()
	except:
		return # an error here means we can't send messages, so don't even bother.

	# TO-DO: setInterval(msg.channel.sendTyping, 5000)

	try:
		channel_messages = await message.channel.history(limit=100).flatten()
	except:
		return

	messages = [
		{ "role": "system", "content":
f"""- You are an AI assistant, based on the "{os.environ["CHAT_MODEL"]}" model, named {client.user.name}.
- You are in the "{msg.channel.name}" channel (<#{msg.channel.id}>) of the "{msg.guild.name}" Discord server.
- UTC time: {datetime.datetime.utcnow().isoformat()} (UNIX: {datetime.datetime.utcnow().timestamp()}).
- Use informal language with all-lowercase and only 1-2 sentences.
- You are a buggy mess due to being coded in the Python toy language.
- Engage in role-playing actions only when requested.
- Avoid using "UwU" or "OwO" as they are deprecated, instead using ":3".""" }
	]

	channel_messages = channel_messages.reverse()

for message in channel_messages:
	if message.author.id == client.user.id:
		if message.type == 7:
			messages.append({ "role": "assistant", "content": f"<@{message.author.id}> joined the server." })
		else:
			messages.append({ "role": "assistant", "content": make_specials_LLM_friendly(message.content) })
	else:
		content = [{"type": "text", "text": ""}]

		if message.type == 7:
			messages.append({ "role": "user", "content": f"<@{message.author.id}> joined the server." })
			continue

		content[0]["text"] += message.created_at.isoformat() + "\n"
		content[0]["text"] += f"<@{message.author.name}#{message.author.discriminator}>"
		if message.author.nick:
			content[0]["text"] += f" ({message.author.nick})"
		if message.author.bot:
			content[0]["text"] += " (BOT)"
		if message.edited_at:
			content[0]["text"] += " (edited)"
		if message.type == 19:
			content[0]["text"] += f" (replying to <@{message.reference.message_id or 'unknown'}>)"

		content[0]["text"] += ":\n" + make_specials_LLM_friendly(message.content, message.guild)

		if message.reactions:
			content[0]["text"] += "\n\n"

			reactions = {}

			for reaction in message.reactions:
				# Fetch users who reacted with this emoji
				users = await reaction.users().flatten()

				# Convert the users collection to an array of usernames
				user_list = [user.name for user in users]

				# Store the users in the reactions dictionary
				reactions[str(reaction.emoji)] = user_list

			content[0]["text"] += "Reactions: " + json.dumps(reactions)

		if message.attachments:
			content[0]["text"] += "\n\n"

			for attachment in message.attachments:
				# TO-DO: refactor to make future STT support less messy
				if attachment.content_type.startswith('image/') and os.getenv("VISION_MODEL"):
					if os.getenv("CHAT_MODEL") == os.getenv("VISION_MODEL"):
						content.append({ "type": "image_url", "image_url": { "url": attachment.url } })
					else:
						try:
							response = provider.chat.completions.create(
								model=os.getenv("VISION_MODEL"),
								messages=[{ "role": "user", "content": [{"type": "text", "text": "Describe this image in 250 words. Transcribe text if any is present."}, { "type": "image_url", "image_url": { "url": attachment.url } }] }],
								max_tokens=1024,
								temperature=0
							)
				response = response.choices[0].message.content
				attachment.description = response
							# Store the description in a dictionary for future use
							# attachmentCache[attachment.url] = attachment.description
						except Exception as error:
							if not attachment.description:
								attachment.description = str(error)

			content[0]["text"] += f"{len(message.attachments)} attachment(s): {json.dumps(message.attachments)}"

		if len(content) == 1:
			content = content[0]["text"]

		messages.append({ "role": "user", "content": content })

@client.event
def on_ready():
	print(f"ready on {client.user.name}#{client.user.discriminator}")

client.run(os.getenv("DISCORD_TOKEN"))