# Direct port of [cakedbake/vincent-ai](https://github.com/cakedbake/vincent-ai/) to Python.

# Not implemented:
## Due to Python being a toy language made by kids for kids, these will most likely never be fixed.
- Re-loading the blacklist when the file is changed
- Typing interval; bot will only send channel typing event once.
- Temporary fix for Mistral not taking more than 8 images from [cakedbake/vincent-ai](https://github.com/cakedbake/vincent-ai/).

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
- `VISION_MODEL`: the model to use to provide image descriptions for the `CHAT_MODEL`. Leave undefined to default to disabled. See [Vision](#vision).

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
- Set `VISION_MODEL` to `pixtral-large-latest` to enable multimodality mode (see [Vision](#vision)).
- Warning: The Mistral API only allows providing a maximum of 8 images to Pixtral Large. See [Not implemented](#not-implemented).

# Vision
### If your `CHAT_MODEL` and `VISION_MODEL` are different:
- Vision uses your chosen `VISION_MODEL` with a very simple prompt: `Describe this image in 250 words. Transcribe text if any is present.`
- It allows using a much smarter chat model than the vision model. It also allows caching, which saves money.
### If your `CHAT_MODEL` and `VISION_MODEL` are the same:
- The images will be passed directly to the `CHAT_MODEL`. This is much faster as another model does not have to interfere and generate a description.
- Only use with models that are both multimodal, and can handle more than one image unless you can absolutely guarantee that the bot will not see more than one image at a time.
- Llama 3.2 11B & 90B can only support one image per context, so are not good for this.

# Error logging
- Create a directory named `errors` for the bot to store errors within it.
- If it encounters an error during inference, it will log the error to `errors` as `./errors/X.json` where X is the UNIX timestamp at time of error with milliseconds.

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
