# Direct port of [cakedbake/vincent-ai](https://github.com/cakedbake/vincent-ai/) to Python.

# Not implemented:
- Re-loading the blacklist when the file is changed
- Typing interval; bot will only send channel typing event once.
- Temporary fix for Mistral not taking more than 8 images from [cakedbake/vincent-ai](https://github.com/cakedbake/vincent-ai/).
- Any form of vision.
- Error logging.
- Reactions.
- Mention convertion (<@123456789012345678> -> <@user>).
- The bot will not dump error messages or regular messages with length > 2000 to attachment.

## How to run
### Prerequisites: only God knows
1. Clone this repository like this:
```bash
git clone https://github.com/cakedbake/pyncent-ai.git
```
2. `cd` into the repository:
```bash
cd pyncent-ai
```
3. Install the dependencies:
```bash
pip install -r requirements.txt --break-system-packages
```
4. Run it:
```bash
python3 main.py
```

# Environment variables
- `DISCORD_TOKEN`: your [Discord bot](https://discord.com/developers/applications/) token.
- `PROVIDER_URL`: the URL of your OpenAI-API-compatible provider. Leave undefined to default to https://api.openai.com/v1/.
- `API_KEY`: the API key of your provider.
- `CHAT_MODEL`: the model to use for chat.
- `MAX_TOKENS`: maximum amount of tokens the `CHAT_MODEL` can generate. Leave undefined to default to 4096.
- `TEMPERATURE`: the temperature to use for the `CHAT_MODEL`. Leave undefined to default to 0°C.
- `VISION_MODEL`: if set, will throw an exception. See [Not implemented](#not-implemented).

# Temperature
- A temperature of 0°C will make the bot's responses deterministic and repetitive.
- A temperature of 0.5°C will make the bot's responses more balanced between creativity and coherence.
- A temperature of 0.7°C is recommended for most use cases.
- A temperature of 1°C will make the bot's responses more creative.
- A temperature of 1.5°C will make the bot borderline incoherent.
- A temperature of 2°C or above will make the bot generate total nonsense.

# [cakedbake](https://github.com/cakedbake)'s recommended settings:
- Set `PROVIDER_URL` to `https://api.mistral.ai/v1/` ([Mistral](https://mistral.ai/)).
- Set `CHAT_MODEL` to `pixtral-large-latest`.
- Set `MAX_TOKENS` to `8000`.
- Set `TEMPERATURE` to `0.0`. (optional: see [Temperature](#temperature)).

# Blacklisting
- You can blacklist a user, a channel, or a guild by adding its ID to the `blacklist.json` file, like this:
```json
[
	"123456789012345678",
	"123456789012345678",
	...
]
```
- The bot will completely ignore messages from blacklisted contexts.
- Note: You need to enable Developer Mode in your Discord client to be able to copy the IDs:
1. Go into User Settings by clicking the cog next to your profile.
2. Go into App Settings > Advanced and enable Developer Mode.
- Due to the way the blacklist is checked, junk can be specified that is not a valid ID. This can help keep track of blacklisted IDs, like this:
```json
[
	"123456789012345678", "#spam",
	"123456789012345678", "@bad-person",
	...
]
```

# Plans
- Ollama support
- Add tool usage, Memory
- Custom system prompts
- Speech-to-text
- Sentience
- Respond with TTS to voice messages
- Web searching (with Google)
- DM support may come in the future, disabled by default, but enableable manually
