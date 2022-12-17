import argparse
import asyncio
import logging
from asyncio import coroutine
from distutils.log import INFO
from environs import Env

EMPTY_LINE = '\n'

logger_sender = logging.getLogger("sender")


def get_parser_args():
    parser = argparse.ArgumentParser(description='Connect to underground chat')
    parser.add_argument('--host', type=str, default=DEFAULT_HOST)
    parser.add_argument('--write_port', type=int, default=DEFAULT_WRITE_PORT)
    parser.add_argument('--token', type=str, default=DEFAULT_DEVMAN_TOKEN)
    parser.add_argument('--message', type=str)

    return parser.parse_args()


async def write_to_chat(host: str, port: int, token: str, message: str) -> coroutine:
    reader, writer = await asyncio.open_connection(
        host, port)
    server_answer = await reader.readline()
    logger_sender.debug(server_answer.decode())
    token = '284f12ae-793c-11ed-8c47-0242ac110002'
    message_with_token = f'{token}{EMPTY_LINE}'
    print(message_with_token)
    writer.write(message_with_token.encode())
    await writer.drain()
    new_message = f'{message}{EMPTY_LINE}{EMPTY_LINE}'
    print(new_message)
    writer.write(new_message.encode())
    await writer.drain()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    DEFAULT_HOST = env.str('HOST')
    DEFAULT_WRITE_PORT = env.int('WRITE_PORT')
    DEFAULT_DEVMAN_TOKEN = env.str('DEVMAN_TOKEN')
    parser_args = get_parser_args()
    logging.basicConfig(level = INFO)
    asyncio.run(write_to_chat(parser_args.host, parser_args.write_port, parser_args.token, parser_args.message))
