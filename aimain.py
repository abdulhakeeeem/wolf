import discord
import speech_recognition as sr

# Define the intents your bot will use
intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)
r = sr.Recognizer()

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!listen'):
        await message.channel.send('Listening...')

        with sr.Microphone() as source:
            print('Listening...')
            audio = r.listen(source)

            try:
                recognized_text = r.recognize_google(audio)
                await message.channel.send(f'You said: {recognized_text}')
            except sr.UnknownValueError:
                await message.channel.send('Sorry, I did not understand what you said.')
            except sr.RequestError as e:
                await message.channel.send(f'Sorry, there was an error processing your request: {e}')

client.run('OTc2NDkwNDA0NTIwMjg4Mjc2.Gqipb5.wNkNe_eZVNIkMCyircic0LdEbDqRICwu9IgNe4')