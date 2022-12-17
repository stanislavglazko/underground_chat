import aiofiles
import argparse
import asyncio
import logging
import json
from asyncio import coroutine
from distutils.log import INFO
from environs import Env

from tools import EMPTY_LINE, ENV_FILE, format_text, send_message, read_line

logger_registration = logging.getLogger("registration")


def get_parser_args():
    parser = argparse.ArgumentParser(description='Register in the underground chat')
    parser.add_argument('--host', type=str, default=DEFAULT_HOST)
    parser.add_argument('--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('--name', type=str, default=DEFAULT_NAME)
    return parser.parse_args()


async def register(host: str, port: int, name: str) -> coroutine:
    reader, writer = await asyncio.open_connection(
        host, port)

    greetings = await read_line(reader)
    logger_registration.debug(greetings)

    empty_message = f'{EMPTY_LINE}'
    await send_message(writer, logger_registration, empty_message)

    name_request = await read_line(reader)
    logger_registration.debug(name_request)

    username = f'{name}{EMPTY_LINE}'
    await send_message(writer, logger_registration, username)

    data_with_token = await read_line(reader)
    decoded_data_with_token = json.loads(data_with_token)
    logger_registration.debug(decoded_data_with_token)
    token = decoded_data_with_token["account_hash"]
    logger_registration.debug(token)

    async with aiofiles.open(ENV_FILE, mode="a") as f:
        await f.write(f"{EMPTY_LINE}DEVMAN_TOKEN='{token}'")
    return


if __name__ == '__main__':
    env = Env()
    env.read_env()
    DEFAULT_HOST = env.str('HOST')
    DEFAULT_PORT = env.int('WRITE_PORT')
    DEFAULT_NAME = env.str('NAME')
    logging.basicConfig(level = INFO)
    parser_args = get_parser_args()
    username = format_text(parser_args.name)
    asyncio.run(register(parser_args.host, parser_args.port, username))
