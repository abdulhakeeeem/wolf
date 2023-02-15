import discord
import time
from variables import bannedWords,alzgrt
from telegram.ext import Updater
from requests import get
from datetime import timedelta


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

telegram_bot = Updater("5345322467:AAHxdqp9vzOUZU4CQCHFTfdnrgb0ucCb_Cs")


async def sendDm(id, message, delete=False):
    user = await client.fetch_user(id)

    if user is not None:
        if user.dm_channel is None:
            await user.create_dm()

        if not delete:
            await user.dm_channel.send(message)
        else:
            await user.dm_channel.send(message, delete_after=0.1)
        print(f"Private message sent")


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
     
     if message.author.id == 1001189121332617327:

         #print(message.embeds[0].description)

         await message.channel.send(embed=message.embeds[0])
         await message.delete()
         return True
     if message.author.id == 282859044593598464:
         # print(message.embeds[0].description)

         await message.channel.send(message.content)
         await message.delete()
         return True

     return False




@client.event
async def on_message(message):


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
            await client.get_channel(691164607749947436).send(embed=message.embeds[0])
            await message.channel.send("لا يطوفكم بث دحيم")

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

# @client.event
# async def on_reaction_add(reaction, user):
#     if user.id == 976490404520288276:
#         return
#
#     if (reaction.message.author.id == 968568452921061386 or reaction.message.author.id == 288660324842864642 or reaction.message.author.id == 392331012727767060 or reaction.message.author.id == 542304547583033344):
#         #if reaction.message.channel.id == 691164607749947436 or reaction.message.channel.id == 1016307203654815804:
#             if reaction.emoji == "🗑️":
#
#                 await reaction.message.delete()
#                 await reaction.message.channel.send(f"<@{user.id}> ما جاز له كلامك",delete_after=50)
#             if reaction.emoji == "👋":
#
#                 await reaction.message.channel.send(f"<@{user.id}> يبيك تنطم",delete_after=50)
#                 await reaction.message.author.timeout(timedelta(seconds=15))
#             if reaction.emoji == "👍":
#                 await reaction.message.author.timeout(timedelta(seconds=1))
#                 await reaction.message.channel.send("عفان جاز له كلامك",delete_after=20)
#                 await sendDm(reaction.message.author.id,"يا حظك https://cdn.discordapp.com/attachments/799603925085847573/1062815358316183654/shakira.mov ")
#             if reaction.emoji == "☕":
#                 await reaction.message.author.timeout(timedelta(seconds=47))
#                 await reaction.message.channel.send("https://cdn.discordapp.com/attachments/417396224644087809/1064686107918352444/monkey_banana_boat.mp4", delete_after=47)
#             if reaction.emoji == "🦵":
#                 await reaction.message.author.kick()
#                 await reaction.message.channel.send(f"<@{user.id}> ما يبيك في السيرفر")
#
#                 #await reaction.message.author.timeout(timedelta(seconds=5))
#
#     if reaction.emoji == "🦵":
#         await reaction.message.author.kick()
#         await reaction.message.channel.send(f"<@{user.id}> ما يبيك في السيرفر")
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


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(691164607749947436)
    #await channel.send('https://cdn.discordapp.com/attachments/976019318154342440/1062680976762880071/RPReplay_Final1656509018.mov ',delete_after=10)


@client.event
async def on_raw_reaction_add(payload):

    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reactor = payload.user_id
    emoji = payload.emoji.name
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
                await sendDm(message.author.id,"يا حظك https://cdn.discordapp.com/attachments/799603925085847573/1062815358316183654/shakira.mov ")
            if emoji == "☕":
                await message.author.timeout(timedelta(seconds=47))
                await message.channel.send("https://cdn.discordapp.com/attachments/417396224644087809/1074522951124258896/v12044gd0000cf2cnf3c77ufjm04q2ug.mov", delete_after=35)

            if emoji == "🦵":
                await message.author.kick()
                await message.channel.send(f"<@{reactor}> ما يبيك في السيرفر")
            if emoji == "Anime":
                await message.author.kick()
                await message.channel.send(f"<@{reactor}> ما يبيك في السيرفر")
            if emoji == "coffe_anime":
                await message.author.kick()
                await message.channel.send(f"<@{reactor}> ما يبيك في السيرفر")

                #await reaction.message.author.timeout(timedelta(seconds=5))

    if emoji == "🦵":
        try:
            await message.author.kick()
            await message.channel.send(f"<@{reactor}> ما يبيك في السيرفر")
        except:
            await reactor.kick()
            await message.channel.send(f"<@{reactor}> https://cdn.discordapp.com/attachments/758296682659184640/1069692160858927194/nope.mov ")
    if emoji == "🦇":
        #await message.author.timeout(timedelta(seconds=47))
        await message.channel.send("https://cdn.discordapp.com/attachments/627445959793704971/796994158223949844/VID-20180914-WA0008.mp4",delete_after=20)



client.run('OTc2NDkwNDA0NTIwMjg4Mjc2.Gqipb5.wNkNe_eZVNIkMCyircic0LdEbDqRICwu9IgNe4')
