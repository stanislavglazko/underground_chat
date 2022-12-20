import aiofiles
import argparse
import asyncio
import datetime
import logging
from asyncio import coroutine
from distutils.log import INFO
from environs import Env

from tools import EMPTY_LINE, open_connection, read_line

logger_receiver = logging.getLogger("receiver")


def get_parser_args():
    parser = argparse.ArgumentParser(description='Read the underground chat')
    parser.add_argument('--host', type=str, default=default_host)
    parser.add_argument('--port', type=int, default=default_read_port)
    parser.add_argument('--history', type=str, default=default_history_file)
    return parser.parse_args()


async def read_chat(host: str, port: int, history: str) -> coroutine:
    async with aiofiles.open(history, mode="a") as f:
        async with open_connection(host, port) as connection:
            reader, _ = connection
            while True:
                try:
                    chat_line = await read_line(reader, logger_receiver)
                    current_datetime = datetime.datetime.now()
                    current_datetime_in_correct_format = (
                        current_datetime.strftime("%d.%m.%y %H:%M")
                    )
                    chat_message = (
                        f'[{current_datetime_in_correct_format}] {chat_line}'
                    )
                    await f.write(f'{chat_message}{EMPTY_LINE}')
                except asyncio.IncompleteReadError as exc:
                    logger_receiver.error(str(exc))
                    return


if __name__ == '__main__':
    env = Env()
    env.read_env()
    default_host = env.str('HOST', 'minechat.dvmn.org')
    default_read_port = env.int('READ_PORT', 5000)
    default_history_file = env.str('HISTORY_FILE', 'history')
    parser_args = get_parser_args()
    logging.basicConfig(level=INFO)
    asyncio.run(
        read_chat(
            parser_args.host, parser_args.port, parser_args.history
        )
    )
