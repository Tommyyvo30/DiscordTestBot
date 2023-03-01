import discord
import requests
import responses
import asyncio


async def send_message(message, user_message, is_private, image_url=None):
    try:
        # Get a response based on the user's message
        response = responses.handle_response(user_message)
        if image_url is not None:
            # Download image and save to local file
            response = requests.get(image_url)
            with open("image.jpg", "wb") as f:
                f.write(response.content)

            file = discord.File("image.jpg")
            if is_private:
                await message.author.send(file=file, content=response)
            else:
                await message.channel.send(file=file, content=response)
        else:
            if is_private:
                await message.author.send(response)
            else:
                await message.channel.send(response)
    except Exception as e:
        print(e)


async def send_image_every_minute(channel, message, image_url):
    while True:
        # Download image and save to local file
        response = requests.get(image_url)
        with open("image.jpg", "wb") as f:
            f.write(response.content)

        # Send message and image as file
        with open("image.jpg", "rb") as f:
            await channel.send(content=message, file=discord.File(f))

        # Wait for one minute
        await asyncio.sleep(60)


def run_discord_bot():
    # Replace "Your bot Token" with your bot's token
    TOKEN = 'Your bot Token'

    # Set up the client with default intents and enable message content
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    # Event handler for when the bot is ready
    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        channel = client.get_channel("Your channel ID")
        message = "Here's an image for you!"

        # Replace "Your image url" with the URL of the image you want to send
        image_url = 'Your image url'

        # Start the coroutine to send an image every minute
        asyncio.create_task(send_image_every_minute(channel, message, image_url))

    # Start the bot with the provided token
    client.run(TOKEN)


run_discord_bot()
