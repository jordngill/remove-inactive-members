from pyrogram import Client, filters
from pyrogram.enums import UserStatus, ChatMemberStatus
import uvloop
import datetime
import asyncio

# Edit your credentials here

api_id = 0
api_hash = ''
bot_token = ''

uvloop.install()

app = Client('app', api_id, api_hash, bot_token=bot_token)

@app.on_message(filters.channel | filters.group & filters.command(['remove_inactive']))
async def remove(_, message):

    members = await app.get_chat_members_count(message.chat.id)
    scanned, removed, failed = 0, 0, 0

    async for member in app.get_chat_members(message.chat.id):
        remove = False

        if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            if member.user.is_deleted:
                remove = True
            elif not member.user.is_bot:
                if member.user.status in (UserStatus.LAST_MONTH, UserStatus.LONG_AGO):
                    remove = True

        if remove:
            try:
                await app.ban_chat_member(message.chat.id, member.user.id, datetime.datetime.now() + datetime.timedelta(minutes=1))
                removed += 1
            except Exception:
                failed += 1
            finally:
                await asyncio.sleep(2)

        scanned += 1
        print(f'Scanned : {scanned}/{members} | Removed : {removed} | Failed : {failed}', end='\r' if scanned != members else '\n')

app.run()
