import discord
from mistralai import Mistral
from dotenv import load_dotenv
import json
import os
import logging
from datetime import datetime

load_dotenv()

BOT_TOKEN = os.getenv('DISCORD_TOKEN')
MISTRAL_TOKEN = os.getenv('MISTRAL_API_KEY')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an instance of the bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

model = "mistral-large-latest"
client = Mistral(api_key=MISTRAL_TOKEN)

@bot.event
async def on_ready():
    logger.info(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == bot.user:
        return

    async def detect_inappropriate_content(content):
        prompt_text = """
            You are a content moderator for Infobrains computer science club Discord server.
            Analyze the following message and respond with true if it violates our rules, or false if it's acceptable.

            Rules to check for:
            1. Business Exploitation:
                - Attempting to exploit students for free work
                - Offering unfair payment/compensation
                - Pressuring students into commercial projects without clear terms
                - Anyone that mentions business and wants someone to do it for them

            2. Negative Behavior:
                - Hate speech or discriminatory language
                - Insults towards programmers or their work
                - Dismissive attitudes towards open source
                - Toxic or hostile comments about others' contributions
                - Anyone that decreases the morale and ability of the group
                - Anyone that says "DM me" or refers to anyone to DM them

            3. Community Guidelines:
                - Respect for collaborative work
                - Support for open source culture
                - Professional communication
                - Constructive criticism only

            4. Academic Integrity:
                - No cheating or academic dishonesty
                - Proper credit for others' work

            Analyze this message: {message_content}

            Respond only with true if rules are violated and provide a strict and fair reason in english, or false if the message is acceptable. You must respond strictly in this structure without using ```json or any other markdown, give me a pure JSON response:
            {{
                "if_violated": true or false,
                "reason": "Reason for the violation make the reason as strict and fair as possible and make him feel threated about what he said."
            }}
        """.format(message_content=content)

        response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": prompt_text}]
        )
        return response.choices[0].message.content

    try:
        result = await detect_inappropriate_content(message.content)
        logger.info(f"API Response: {result}")

        if not result.strip():
            logger.error("Empty response from the API")
            return

        response_json = json.loads(result)

        if response_json["if_violated"]:
            # Create a better warning embed
            warning_embed = discord.Embed(
                title="⚠️ Message Removed: Rule Violation",
                description=(
                    f"**User:** {message.author.mention}\n"
                    f"**Channel:** {message.channel.mention}\n"
                    f"**Time:** {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    "**Note:** Further violations may result in stronger actions."
                ),
                color=0xFF0000  # Red color
            )
            
            # Set the thumbnail to user's avatar
            warning_embed.set_thumbnail(
                url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url
            )

            # Add footer
            warning_embed.set_footer(
                text=f"Community Safety Bot | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            try:
                await message.delete()
                await message.channel.send(embed=warning_embed)
                
                # Send a detailed DM to the user
                dm_embed = discord.Embed(
                    title="🚫 SEVERE WARNING: RULE VIOLATION DETECTED",
                    description=(
                        f"**IMMEDIATE ACTION REQUIRED**\n\n"
                        f"Your message in **{message.guild.name}** ({message.channel.mention}) has been removed for a serious rule violation.\n\n"
                        f"**Offending Content:**\n```\n{message.content[:1000]}```\n\n"
                        f"**Violation Details:**\n{response_json['reason']}\n\n"
                        "**Consequences:**\n"
                        "⚠️ Message permanently deleted\n"
                        "⚠️ 10-minute timeout enforced\n"
                        "⚠️ Violation logged\n\n"
                        "**WARNING:** Further violations will result in:\n"
                        "• Extended timeouts\n"
                        "• Role restrictions\n"
                        "• Permanent ban\n\n"
                        "This is your formal warning. Review server rules immediately."
                    ),
                    color=0xDC143C  # Crimson red
                )
                
                await message.author.send(embed=dm_embed)
                
                # Log the incident
                logger.warning(f"Rule violation by {message.author.display_name} | Content: {message.content}")
                
            except discord.Forbidden:
                logger.warning(f"Could not delete message or send DM to {message.author.display_name}")
                await message.channel.send(embed=warning_embed)
                
        else:
            logger.info(f"Message from {message.author.display_name} is acceptable.")
            
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON response: {result}")
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")

# Run the bot
bot.run(BOT_TOKEN)
