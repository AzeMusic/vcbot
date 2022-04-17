from pyrogram import Client
from pyrogram import filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from TamilVc.helpers.decorators import authorized_users_only
from TamilVc.helpers.decorators import errors
from TamilVc.services.callsmusic import client as USER
from TamilVc.config import SUDO_USERS

@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Əvvəlcə məni öz qrupuna admin kimi əlavə et</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "TamilVc"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "Sizin xahiş etdiyiniz kimi bura qoşuldum")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Assistant artıq söhbətinizdədir</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Daşqın Gözləmə Xətası 🛑 \n İstifadəçi {user.first_name} Assistant üçün çoxlu qoşulma sorğuları səbəbindən qrupunuza qoşula bilmədi! Assistantın qrupda qadağan edilmədiyinə əmin olun."
            f"\n\nvəya özünüz **@{ASSISTANT_NAME}** Qrupa əlavə edin və təkrar cəhd edin</b>",
        )
        return
    await message.reply_text(
        "<b>Assistant söhbətinizə qoşuldu</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>Assistant qrupunuzu tərk edə bilmədi! Floodwaits ola bilər."
            "\n\nveya Özünüz çıxarın</b>",
        )
        return
    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("Assistant Leaving all chats")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")
    
    
@Client.on_message(filters.command(["userbotjoinchannel","ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Is chat even linked")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Add me as admin of yor channel first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "TamilVc"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "I joined here as you requested")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>helper already in your channel</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n User {user.first_name} couldn't join your channel due to heavy join requests for userbot! Make sure user is not banned in channel."
            f"\n\nOr manually add **@{ASSISTANT_NAME}** to your Group and try again</b>",
        )
        return
    await message.reply_text(
        "<b>helper userbot joined your channel</b>",
    )
    
