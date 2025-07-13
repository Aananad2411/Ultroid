Anu - UserBot

Modified from Ultroid - UserBot

Original License: GNU AGPL v3.0

import inspect import re from traceback import format_exc

from telethon import Button from telethon.errors import QueryIdInvalidError from telethon.events import CallbackQuery, InlineQuery, NewMessage from telethon.tl.types import InputWebDocument

from .. import LOGS, asst, udB, ultroid_bot from ..fns.admins import admin_check from . import append_or_update, owner_and_sudos

OWNER = ultroid_bot.full_name

MSG = f""" Anu - UserBot ➖➖➖➖➖➖➖➖➖➖ Owner: {OWNER} ➖➖➖➖➖➖➖➖➖➖ """

IN_BTTS = [ [Button.url("🌐 Support", "https://t.me/SarkarTerminal")], [Button.inline("✨ Help", data=b"help")], ]

decorator for assistant

def asst_cmd(pattern=None, load=None, owner=False, **kwargs): """Decorator for assistant's command""" name = inspect.stack()[1].filename.split("/")[-1].replace(".py", "") kwargs["forwards"] = False

def ult(func):
    if pattern:
        kwargs["pattern"] = re.compile(f"^/{pattern}")

    async def handler(event):
        if owner and event.sender_id not in owner_and_sudos():
            return
        try:
            await func(event)
        except Exception as er:
            LOGS.exception(er)

    asst.add_event_handler(handler, NewMessage(**kwargs))
    if load is not None:
        append_or_update(load, func, name, kwargs)

return ult

def callback(data=None, from_users=None, admins=False, owner=False, **kwargs): """Assistant's callback decorator""" if from_users is None: from_users = [] if "me" in from_users: from_users.remove("me") from_users.append(ultroid_bot.uid)

def ultr(func):
    async def wrapper(event):
        if admins and not await admin_check(event):
            return
        if from_users and event.sender_id not in from_users:
            return await event.answer("Not for You!", alert=True)
        if owner and event.sender_id not in owner_and_sudos():
            return await event.answer(f"This is {OWNER}'s bot!!")
        try:
            await func(event)
        except Exception as er:
            LOGS.exception(er)

    asst.add_event_handler(wrapper, CallbackQuery(data=data, **kwargs))

return ultr

def in_pattern(pattern=None, owner=False, **kwargs): """Assistant's inline decorator."""

def don(func):
    async def wrapper(event):
        if owner and event.sender_id not in owner_and_sudos():
            res = [
                await event.builder.article(
                    title=" Anu Userbot",
                    text=MSG,
                    thumb=InputWebDocument(
                        "https://graph.org/file/04fbe1479fa10209c0664-6feb1a7ffe75d4673f.jpg",
                        0,
                        "image/jpeg",
                        [],
                    ),
                    buttons=IN_BTTS,
                )
            ]
            return await event.answer(
                res,
                switch_pm=f"🤖: Assistant of {OWNER}",
                switch_pm_param="start",
            )
        try:
            await func(event)
        except QueryIdInvalidError:
            pass
        except Exception as er:
            err = format_exc()
            LOGS.exception(er)

            me = await asst.get_me()

            def error_text():
                return f"**#ERROR #INLINE**\n\nQuery: `{me.username} {pattern}`\n\n**Traceback:**\n`{err}`"

            try:
                await event.answer(
                    [
                        await event.builder.article(
                            title="Unhandled Exception has Occured!",
                            text=error_text(),
                            buttons=Button.url(
                                "Report", "https://t.me/SarkarTerminal"
                            ),
                        )
                    ]
                )
            except QueryIdInvalidError:
                LOGS.exception(err)
            except Exception as er:
                LOGS.exception(er)
                await asst.send_message(udB.get_key("LOG_CHANNEL"), error_text())

    asst.add_event_handler(wrapper, InlineQuery(pattern=pattern, **kwargs))

return don

