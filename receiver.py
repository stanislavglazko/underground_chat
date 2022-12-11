import aiofiles
import argparse
import asyncio
from asyncio import coroutine
import datetime
from environs import Env


def get_parser_args():
    parser = argparse.ArgumentParser(description='Connect to underground chat')
    parser.add_argument('--host', type=str, default=DEFAULT_HOST)
    parser.add_argument('--port', type=int, default=DEFAULT_READ_PORT)
    parser.add_argument('--history', type=str, default=DEFAULT_HISTORY_FILE)

    return parser.parse_args()


async def read_chat(host: str, port: int, history: str) -> coroutine:
    reader, _ = await asyncio.open_connection(
        host, port)
    
    while True:
        try:
            data = await reader.readline()
            current_datetime = datetime.datetime.now()
            current_datetime_in_correct_format = current_datetime.strftime("%d.%m.%y %H:%M")
            chat_message = f'[{current_datetime_in_correct_format}] {data.decode()}'
            async with aiofiles.open(history, mode="a") as f:
                await f.write(chat_message)
            print(chat_message)
        except Exception as exc:
            print(str(exc))
            raise


if __name__ == '__main__':
    env = Env()
    env.read_env()
    DEFAULT_HOST = env.str('HOST')
    DEFAULT_READ_PORT = env.int('READ_PORT')
    DEFAULT_HISTORY_FILE = env.str('HISTORY_FILE')
    parser_args = get_parser_args()
    asyncio.run(read_chat(parser_args.host, parser_args.port, parser_args.history))
