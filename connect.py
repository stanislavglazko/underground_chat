import aiofiles
import asyncio
import datetime


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        "minechat.dvmn.org", 5000)
    
    while True:
        try:
            data = await reader.readline()
            current_datetime = datetime.datetime.now()
            current_datetime_in_correct_format = current_datetime.strftime("%d.%m.%y %H:%M")
            chat_message = f'[{current_datetime_in_correct_format}] {data.decode()}'
            async with aiofiles.open("history", mode="a") as f:
                await f.write(chat_message)
            print(chat_message)
        except Exception as exc:
            print(str(exc))
            raise


asyncio.run(tcp_echo_client())
