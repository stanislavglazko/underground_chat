import aiofiles
import argparse
import asyncio
import json
import logging
from asyncio import coroutine
from distutils.log import INFO
from environs import Env

from tools import (
    ENV_FILE,
    EMPTY_LINE,
    format_text,
    open_connection,
    read_line,
    send_message,
)

logger_registration = logging.getLogger("registration")


def get_parser_args():
    parser = argparse.ArgumentParser(description='Register in the underground chat')
    parser.add_argument('--host', type=str, default=default_host)
    parser.add_argument('--port', type=int, default=default_port)
    parser.add_argument('--name', type=str, default=default_username)
    return parser.parse_args()


async def register(host: str, port: int, name: str) -> coroutine:
    async with open_connection(host, port) as connection:
        reader, writer = connection

        await read_line(reader, logger_registration)

        empty_message = f'{EMPTY_LINE}'
        await send_message(writer, logger_registration, empty_message)

        await read_line(reader, logger_registration)

        username = f'{name}{EMPTY_LINE}'
        await send_message(writer, logger_registration, username)

        data_with_token = await read_line(reader, logger_registration)
        parsed_data_with_token = json.loads(data_with_token)
        token = parsed_data_with_token["account_hash"]
        async with aiofiles.open(ENV_FILE, mode="a") as f:
            await f.write(f"{EMPTY_LINE}DEVMAN_TOKEN='{token}'")


if __name__ == '__main__':
    env = Env()
    env.read_env()
    default_host = env.str('HOST', 'minechat.dvmn.org')
    default_port = env.int('WRITE_PORT', 5050)
    default_username = env.str('NAME', 'Guest')
    logging.basicConfig(level=INFO)
    parser_args = get_parser_args()
    username = format_text(parser_args.name)
    asyncio.run(register(parser_args.host, parser_args.port, username))
