import datetime

import discord
from discord.ext import tasks

import gaw_modules.exception as gaw_expt
import gaw_modules.function as gaw_func
import gaw_modules.util as gaw_util

client = discord.Client()


@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))
    # asyncio.ensure_future()


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    try:
        if msg.content.upper().startswith("//TODO") and msg.channel.name in [
            "宣言",
            "bot試験場",
        ]:
            new_schedule = gaw_util.create_schedule(msg)
            await msg.channel.send(new_schedule.get_accepted_message(msg))
            gaw_util.schedule_list.append(new_schedule)

        if msg.content.startswith("heygaw "):
            command_and_args = msg.content[len("heygaw"):].strip().split(" ")
            command = command_and_args[0]
            args = command_and_args[1:] if len(command_and_args) > 1 else None
            await gaw_func.exec_gaw_func(msg, command, args)
    except gaw_expt.UserNotifyException as e:
        await msg.channel.send(e.post_msg)


@tasks.loop(seconds=1)
async def loop():
    now = datetime.datetime.now()
    tmp = []
    for s in gaw_util.schedule_list:
        if s.end_time - now < datetime.timedelta(seconds=1):
            channel = client.get_channel(698746373402525696)
            # channel = client.get_channel(701841878739451924)
            res = ""

            res += str(s.author.mention) + " 時間です！\n"
            res += "> " + "\n> ".join(s.task.split("\n"))

            await channel.send(res)
        else:
            tmp.append(s)

    gaw_util.schedule_list = tmp


if __name__ == "__main__":
    with open("access_token.txt") as fin:
        token = fin.read()
    gaw_func.init()
    loop.start()
    client.run(token)
