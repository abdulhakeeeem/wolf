import discord
import asyncio
import os, datetime
import time
from variables import bannedWords,alzgrt
from telegram.ext import Updater
from requests import get
from datetime import timedelta
import json
from discord.ext import commands, tasks
import openai as gpt
from dotenv import load_dotenv
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(intents=intents,command_prefix='$')

telegram_bot = Updater("5345322467:AAHxdqp9vzOUZU4CQCHFTfdnrgb0ucCb_Cs")



async def sendDm(id, message, delete=False):
    try:
        user = await client.fetch_user(id)

        if user is not None:
            if user.dm_channel is None:
                await user.create_dm()

            if not delete:
                await user.dm_channel.send(message)
            else:
                await user.dm_channel.send(message, delete_after=0.1)
            print(f"Private message sent")
    except:
        print("lh e]vj hvsg gi")

async def send_video(message, chatId):
    url = ''
    if message.attachments and (message.attachments[0].content_type.startswith('image') or message.attachments[0].content_type.startswith('video')):
        url = message.attachments[0].url

    elif message.content.lower().startswith("http"):
        url = message.content

    if not url:
        return False

    video = get(url)
    if video.ok:
        if url.lower()[-3:] == 'mp4':
            telegram_bot.bot.send_video(chat_id=chatId, video=video.content,  filename=url.split("/")[-1])
        else:
            telegram_bot.bot.send_document(chat_id=chatId, document=video.content, filename=url.split("/")[-1])
        print(f"Video sent")

    return True



async def add_roles(member, member_info):

    if member_info["name"]:
        await member.edit(nick=member_info["name"])
        print(member_info["name"])

    guild_roles = await member.guild.fetch_roles()

    for role in member_info["roles"]:
        for guild_role in guild_roles:
            if role == guild_role.id:
                try:
                    
                    await member.add_roles(guild_role)

                except:
                    pass



def isMeme(message):
    channels = [
        [712007174162874399, -1001765168485],
        [768887936514916363, -1001765168485],
        [745594435466690601, -1001556462610],
        [757161521477451806, -1001434343952],
        [745594467901243423, -1001750809271],
        [1064984991655792641, -1001765168485]
    ]

    for channel in channels:
        if message.channel.id == channel[0]:
            return channel[1]

    return False


# async def download_videos(message, id):
#     for m in await message.channel.history(limit=100000).flatten():
#         try:
#             await send_video(m, id)
#         except:
#             pass
#         time.sleep(3.2)
#     return True

async def steal(message):
    try:
        if message.author.id == 1001189121332617327:
            try:
                await message.channel.send(embed=message.embeds[0])
                await message.delete()
            except discord.errors.NotFound:
                # Message was already deleted, just continue
                pass
            except IndexError:
                # No embeds in the message
                pass
            return True

        if message.author.id == 282859044593598464:
            try:
                # Handle empty content (messages with only attachments/embeds)
                content = message.content or " "  # Fallback to space if empty

                # Re-upload attachments
                files = [await attachment.to_file() for attachment in message.attachments]

                # Send cloned message with content, files, and embeds
                await message.channel.send(
                    content=content,
                    files=files,
                    embeds=message.embeds
                )

                # Delete original message
                await message.delete()

            except discord.NotFound:
                pass  # Message already deleted
            except discord.Forbidden:
                print(f"Missing permissions to delete in {message.channel.name}")
            except Exception as e:
                print(f"Unexpected error: {type(e).__name__}: {e}")

            return  # Don't return True, just return

        if message.author.id == 672822334641537041:
            if message.channel.id == 853454311521386548:  # check if the message is from the source channel
                try:
                    target_channel = client.get_channel(1114150009106079756)  # get the target channel object
                    if target_channel:
                        files = [await attch.to_file() for attch in message.attachments]
                        embed = message.embeds[0] if message.embeds else None
                        await target_channel.send(
                            content=message.content,
                            tts=message.tts,
                            files=files,
                            embed=embed
                        )
                except Exception as e:
                    print(f"Error forwarding message: {e}")
                return True
    except Exception as e:
        print(f"Error in steal function: {e}")
    return False


#######################################
@tasks.loop(seconds=1000)  # Run every 10 seconds
async def check_new_messages():
    source_channel = client.get_channel(853454311521386548)
    target_channels = [client.get_channel(1114166935307964438), client.get_channel(1242111825193992204)]
    user_id = 956672052251721748

    if not source_channel:
        print(f'Source channel not found')
        return

    # Load processed message IDs
    try:
        with open("message_ids.txt", "r") as file:
            processed_messages = set(file.read().splitlines())
    except FileNotFoundError:
        processed_messages = set()

    # Get new messages
    async for message in source_channel.history(limit=50):  # Check last 50 messages
        if message.author.id == user_id and str(message.id) not in processed_messages:
            # Process message
            for target_channel in target_channels:
                if target_channel:
                    try:
                        files = [await attachment.to_file() for attachment in message.attachments]
                        for embed in message.embeds:
                            await target_channel.send(
                                content=message.content,
                                tts=message.tts,
                                files=files,
                                embed=embed
                            )
                    except Exception as e:
                        print(f"Error sending message to {target_channel.name}: {e}")

            # Mark message as processed
            processed_messages.add(str(message.id))
            with open("message_ids.txt", "a") as file:
                file.write(f"{message.id}\n")



@client.event
async def on_message(message):
    await client.process_commands(message)
    if await steal(message):
        return
    if message.author.id == 1001189121332617327:
        await message.channel.send(message.content)
        await message.delete()


    if message.channel.id == 1001195254025826366:
        if message.author.id == 375805687529209857:
            print(message.embeds[0].description)

            await client.fetch_channel(691164607749947436)
            #await message.channel.send(message.content)
            await client.get_channel(691164607749947436).send(embed=message.embeds[0],delete_after=3000)
            await client.get_channel(691164607749947436).send("لا يطوفكم بث دحيم",delete_after=3000)

            await client.fetch_channel(535473799005470740)
            # await message.channel.send(message.content)
            await client.get_channel(535473799005470740).send(embed=message.embeds[0], delete_after=3000)
            await client.get_channel(535473799005470740).send("لا يطوفكم بث الوالي",delete_after=3000)

            await client.fetch_channel(691164607749947436)
            # await message.channel.send(message.content)
            await client.get_channel(737789345653719124).send(embed=message.embeds[0], delete_after=3000)
            await client.get_channel(737789345653719124).send("لا يطوفكم بث ملك الليل", delete_after=3000)

            #await message.channel.send(embed=message.embeds[0])
    try:
        if message.author.id in alzgrt: #(message.author.id == 288660324842864642 or message.author.id == 288660324842864642 or message.author.id == 392331012727767060 or message.author.id == 542304547583033344 ) :#and (message.channel.id == 691164607749947436 or message.channel.id == 1016307203654815804):
            await message.add_reaction("🗑️")
            await message.add_reaction("👋")
            await message.add_reaction("👍")
    except:
        await message.delete()
        await message.author.timeout(timedelta(seconds=90000))
        await message.channel.send(f"<@{message.author.id}> فك البلك يالحقير",delete_after=100)




    if message.author.id == 976490404520288276:
        return
    channel = isMeme(message)

    if channel:
        if await send_video(message, channel):
            return

    print(f"{message.author}: {message.content}")

    if not message.guild:
        return

    # print(message.guild.roles[0].members)
    roles = [role.id for role in message.author.roles]

    if 1033163263535485018 in roles:
     if "نقلاب" in message.content:
         for role in message.guild.roles:
             if role.id == 1033163263535485018 :
                 print(role.members)
                 for member in role.members :
                     await member.kick(reason="قمع محاولة انقلاب")

                 await message.channel.send("تم قمع محاولة الانقلاب من الخونه")
    if "شقلبه" in message.content:
        for role in message.guild.roles:
            if role.id == 1033163263535485018:
                print(role.members)
                for member in role.members:
                    message.channel.send("تحاول تستذكي علي")
                    await member.kick(reason="قمع محاولة انقلاب")

                await message.channel.send("تم قمع محاولة الانقلاب من الخونه")

    
    for banned in bannedWords:
        if banned.isBanned(message):

            if banned.delete:
                await message.delete()
                print(f"Deleted {message.author} message")

            if banned.res:
                if banned.deleteAfter:
                    await message.channel.send(banned.response(message),delete_after=banned.deleteAfter)
                else:
                    await message.channel.send(banned.response(message))

            if banned.privMsg:
                if banned.privMsgUsers:
                    for user in banned.privMsgUsers:
                        await sendDm(user, banned.privMsg)
                else:
                    await sendDm(message.author.id, banned.privMsg)
            if banned.timeout:
                await message.author.timeout(timedelta(seconds=banned.timeout))

            if banned.reactions:
                for reaction in banned.reactions:
                    message.add_reaction(reaction)
            return









#chat gptai
    # if message.author.bot:
    #     return
    #
    # if client.user in message.mentions:
    #     await message.channel.typing()  # Appear as typing while processing.
    #
    #     # Save user message in the log
    #     chat_log = []
    #     chat_log.append({"role": "user", "content": message.content})
    #
    #     # Get response
    #     response = gpt.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=chat_log
    #     )
    #     gptResponse = response['choices'][0]['message']['content']
    #
    #     # Save Response message in the log
    #     chat_log.append({"role": "assistant", "content": gptResponse.strip("\n").strip()})
    #
    #     # Send Response to discord room.
    #     await message.channel.send("``` {} ```".format(gptResponse))
    #
    #     # Append to log file
    #     with open("log.txt", "a", encoding='utf-8') as file:
    #         now = datetime.datetime.now()
    #         file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
    #         file.write("\nUser:\n {}.\n".format(message.content))
    #         file.write("GPT:\n {}.\n\n".format(gptResponse))



@client.event
async def on_voice_state_update(member, before, after):
    user_roles = [role.id for role in member.roles]
    zgrts_role = 1033163263535485018 # حط رقم الرول
    if before.channel is None and zgrts_role in user_roles:
        try:
            await sendDm(member.id, "لاحظ", delete=True)
            print("مب مبلك")

        except:
            print('مبلك')
            await member.timeout(timedelta(seconds=3))
            channel = client.get_channel(691164607749947436)
            await channel.send('فك البلوك ولا منتب داخل ',delete_after=20)






async def check_all_kick_members():
    with open("users.json") as file:
        kicked_members = json.load(file)


    guild = client.get_guild(691164607749947432)
    edited = False
    for kicked_member in kicked_members:
        member = guild.get_member(kicked_member["user"])
        if member:
            await add_roles(member, kicked_member)
            edited = True
            kicked_members.remove(kicked_member)

    # طفيناها
    if edited and False:
        with open("users.json", "w") as file:
            json.dump(kicked_members, file)


ALLOWED_GUILD_ID = 691164607749947432  # Replace with your server ID

async def save_data(member):
    if member.guild.id != ALLOWED_GUILD_ID:
        return  # Exit if the member is not from the allowed server

    # await sendDm(member.id, "https://discord.gg/5z93XyFjBy")

    roles = [role.id for role in member.roles]
    member_id = member.id
    name = member.nick
    data = {
        "user":member_id,
        "name":name,
        "roles":roles,
    }
    try:
        with open("users.json", "r") as file:
            kicked_members = json.load(file)
    except Exception as e:
        kicked_members = []
    for member in kicked_members:
        if member["user"] == member_id:
            kicked_members.remove(member)
            break
    kicked_members.append(data)

    with open("users.json", "w") as file:
        json.dump(kicked_members, file)


async def add_roles(member, member_info):

    if member_info["name"]:
        await member.edit(nick=member_info["name"])
        print(member_info["name"])

    guild_roles = await member.guild.fetch_roles()
    users_role = []
    for role in member_info["roles"]:

        for guild_role in guild_roles:
            if role == guild_role.id and role != 691164607749947432:
                users_role.append(guild_role)

    if users_role:
        try:
            await member.add_roles(*users_role)
        except Exception as e:
            print(e)




@client.command()

async def foo(ctx):
    guild = client.get_guild(691164607749947432)
    members=guild.members

    with open("users.json") as file:
        kicked_user = json.load(file)

    for member in members:
        for index, user in enumerate(kicked_user):
            if user["user"] == member.id:
                await add_roles(member, user)
                #kicked_user.pop(index)
                # with open("users.json", "w") as file:
                #     json.dump(kicked_user, file)

@client.command()

async def save_all(ctx):
    print("DODN")
    guild = client.get_guild(691164607749947432)
    members = guild.members
    for member in members:
        await save_data(member)
        await asyncio.sleep(1)
        print("DODNnn")




@client.event
async def on_ready():

    # await client.change_presence(status=discord.Status.offline)

    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(691164607749947436)
    check_new_messages.start()  # Start the message checking loop
    #await channel.send('https://cdn.discordapp.com/attachments/976019318154342440/1062680976762880071/RPReplay_Final1656509018.mov ',delete_after=10)
    await check_all_kick_members()

    source_channel = client.get_channel(853454311521386548)  # get the source channel object
    target_channel = [client.get_channel(1114166935307964438), client.get_channel(1242111825193992204)]  # get the target channel object
    user_id = 956672052251721748  # get the user ID you want to filter
    file = open("message_ids.txt", "a+")  # open a file in append and read mode
    file.seek(0)  # move the cursor to the beginning of the file
    message_ids = file.read().splitlines()  # read the file and split it by lines
    if source_channel is not None:
        async for message in source_channel.history(limit=10):  # iterate over up to 100 messages from the source channel
            if message.author.id == user_id and str(message.id) not in message_ids:  # check if the message author's ID matches the user ID and the message ID is not in the file
                for embed in message.embeds:  # iterate over all embeds in the message
                    for channel in target_channel:
                        await channel.send(message.content, tts=message.tts,
                                           files=[await attch.to_file() for attch in message.attachments], embed=embed)
                file.write(str(message.id) + "\n")  # write the message ID to the file

    else:
        print(f'Channel with id {"سيرفر عمر"} not found')
    file.close()  # close the file

@client.event
async def on_member_remove(member):
    await save_data(member)
    await sendDm(member.id ,"https://discord.gg/5z93XyFjBy")
@client.event
async def on_member_join(member):
    with open("users.json") as file:
        kicked_user = json.load(file)

    for index, user in enumerate(kicked_user):
        if user["user"] == member.id:
            await add_roles(member, user)

            #kicked_user.pop(index)
            # with open("users.json", "w") as file:
            #     json.dump(kicked_user, file)



@client.event
async def on_raw_reaction_add(payload):

    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reactor = payload.user_id
    emoji = payload.emoji.name
    guild = await client.fetch_guild(payload.guild_id)
    user_reactor = await guild.fetch_member(reactor)

    if reactor == 976490404520288276:
        return
    print(emoji)

    if message.author.id in alzgrt: #(message.author.id == 968568452921061386 or message.author.id == 288660324842864642 or message.author.id == 392331012727767060 or message.author.id == 542304547583033344 or message.author.id == 1071729305274552433):
        #if reaction.message.channel.id == 691164607749947436 or reaction.message.channel.id == 1016307203654815804:
            if emoji == "🗑️":
                await message.delete()
                await message.channel.send(f"<@{reactor}> ما جاز له كلامك",delete_after=50)
            if emoji == "👋":

                await message.channel.send(f"<@{reactor}> يبيك تنطم",delete_after=50)
                await message.author.timeout(timedelta(seconds=15))
            if emoji == "👍":
                await message.author.timeout(timedelta(seconds=1))
                await message.channel.send(f"<@{reactor}> جاز له كلامك",delete_after=20)
                await sendDm(message.author.id,"https://cdn.discordapp.com/attachments/799620288684883979/954199701450817586/redditsave.com_ever_see_such_skill-egl9t3fyw0o81-360.mp4?ex=65b31438&is=65a09f38&hm=552d508b2dafd9d284dfdbfba74435df2f54bbcefe4715eed7ec9cc4dc179398&")
            if emoji == "☕":
                await message.author.timeout(timedelta(seconds=47))
                await message.channel.send("https://cdn.discordapp.com/attachments/417396224644087809/1074522951124258896/v12044gd0000cf2cnf3c77ufjm04q2ug.mov", delete_after=35)

            #if emoji == "🦵":
                #await message.author.kick()
                #await message.channel.send(f"<@{reactor}> ما يبيك في السيرفر")
            if emoji == "Anime":
                await message.author.kick()
                await message.channel.send(f"<@{reactor}> ما يبيك في السيرفر")
            if emoji == "coffe_anime":
                await message.author.kick()
                await message.channel.send(f"<@{reactor}> ما يبيك في السيرفر")

                #await reaction.message.author.timeout(timedelta(seconds=5))

    if emoji == "🦵":
        if user_reactor.id == 542304547583033344:
            await message.channel.send("ما اسمع كلام مصري  https://tenor.com/view/%D8%A7%D9%84%D9%83%D9%8A%D8%A7%D9%84-%D9%82%D9%88%D9%8A-%D8%A7%D9%84%D9%83%D9%8A%D8%A7%D9%84%D9%85%D8%B9%D8%B6%D9%84-%D8%A7%D9%84%D9%83%D9%8A%D8%A7%D9%84%D9%82%D9%88%D9%8A-%D8%A7%D8%AD%D9%85%D8%AF%D8%A7%D9%84%D9%83%D9%8A%D8%A7%D9%84-gif-25117516",delete_after=900)
            return
        else:
            if random.random() >=0.01 :

                try:
                    # if reactor.id == 542304547583033344:
                    #     await message.channel.send("ما اسمع كلام مصري  https://tenor.com/view/%D8%A7%D9%84%D9%83%D9%8A%D8%A7%D9%84-%D9%82%D9%88%D9%8A-%D8%A7%D9%84%D9%83%D9%8A%D8%A7%D9%84%D9%85%D8%B9%D8%B6%D9%84-%D8%A7%D9%84%D9%83%D9%8A%D8%A7%D9%84%D9%82%D9%88%D9%8A-%D8%A7%D8%AD%D9%85%D8%AF%D8%A7%D9%84%D9%83%D9%8A%D8%A7%D9%84-gif-25117516",delete_after=200)
                    #     return
                    # else:
                    await message.channel.send(f"<@{reactor}>  يقول ل <@{message.author.id}>  https://cdn.discordapp.com/attachments/758296682659184640/1126808434940063754/super_dpper_fucked.mov")
                    await asyncio.sleep(40)
                    await sendDm(message.author.id,"https://discord.gg/5z93XyFjBy")
                    await message.author.kick()
                except:
                    await message.channel.send(f"<@{reactor}> https://cdn.discordapp.com/attachments/758301217343537162/1080315882661756948/SPOILER_Screenshot_2023-01-25_9.png ")
                    await asyncio.sleep(20)
                    await sendDm(user_reactor.id,"https://discord.gg/5z93XyFjBy")
                    await user_reactor.kick()
            else:
                try:
                    await message.channel.send(f"<@{reactor}>  https://cdn.discordapp.com/attachments/847736808104263680/1082027777475219618/ja5f__1.mp4")
                    await asyncio.sleep(40)
                    await sendDm(user_reactor.id, "https://discord.gg/5z93XyFjBy")
                    await user_reactor.kick()
                except:
                    await message.channel.send(f"<@{reactor}> https://cdn.discordapp.com/attachments/758301217343537162/1080315882661756948/SPOILER_Screenshot_2023-01-25_9.png ")
                    await asyncio.sleep(20)
                    await sendDm(user_reactor.id,"https://discord.gg/5z93XyFjBy")
                    await user_reactor.kick()


    if emoji == "🦇":
        #await message.author.timeout(timedelta(seconds=47))
        await message.channel.send("https://cdn.discordapp.com/attachments/758296682659184640/1082495176276181062/basedBatman.mp4",delete_after=20)
    #if reactor == 288660324842864642:
        #if emoji == "🤣":
            #await message.channel.send("https://cdn.discordapp.com/attachments/1001195254025826366/1164899001494163477/My_Laugh_Is_Wrong_-_Jimmy_Carr___Jimmy_Carr_on_Laughing___Jimmy_Carr_1_online-video-cutter.com.mp4?ex=6544e3bc&is=65326ebc&hm=dcf1f20a6810d81dfcca62beb2ddf52fd02871f7c2dd6f461933a7a286b6bdf7&",delete_after=3000)
#================================================================================================

# Load Tokens
load_dotenv(".env")
DISCORD_TOKEN = os.getenv("OTc2NDkwNDA0NTIwMjg4Mjc2.Gqipb5.wNkNe_eZVNIkMCyircic0LdEbDqRICwu9IgNe4")
gpt.api_key = "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"










client.run('@@@')
