import aiofiles
import argparse
import asyncio
import logging
import json
from asyncio import coroutine
from distutils.log import INFO
from environs import Env

EMPTY_LINE = '\n'

logger_registration = logging.getLogger("registration")


def get_parser_args():
    parser = argparse.ArgumentParser(description='Registrate in the underground chat')
    parser.add_argument('--host', type=str, default=DEFAULT_HOST)
    parser.add_argument('--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('--name', type=str, default=DEFAULT_NAME)
    return parser.parse_args()


async def register(host: str, port: int, name: str):
    reader, writer = await asyncio.open_connection(
        host, port)

    hello_answer = await reader.readline()
    logger_registration.debug(hello_answer.decode())

    message = f'{EMPTY_LINE}'
    writer.write(message.encode())
    await writer.drain()

    answer_with_name = await reader.readline()
    logger_registration.debug(answer_with_name.decode())

    message = f'{name}{EMPTY_LINE}'
    writer.write(message.encode())
    logger_registration.debug(message)
    await writer.drain()

    answer_with_token = await reader.readline()
    decoded_answer_with_token = json.loads(answer_with_token.decode())
    logger_registration.debug(answer_with_token)
    token = decoded_answer_with_token["account_hash"]
    logger_registration.debug(token)
    async with aiofiles.open(".env", mode="a") as f:
        await f.write(f"DEVMAN_TOKEN='{token}'")
    return


if __name__ == '__main__':
    env = Env()
    env.read_env()
    DEFAULT_HOST = env.str('HOST')
    DEFAULT_PORT = env.int('WRITE_PORT')
    DEFAULT_NAME = env.str('NAME')
    logging.basicConfig(level = INFO)
    parser_args = get_parser_args()
    correct_name = parser_args.name.replace('\n', '')
    asyncio.run(register(parser_args.host, parser_args.port, correct_name))
