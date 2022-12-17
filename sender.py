import aiofiles
import argparse
import asyncio
import logging
import json
from asyncio import coroutine
from distutils.log import INFO
from environs import Env

EMPTY_LINE = '\n'

logger_sender = logging.getLogger("sender")

class TokenError(Exception):
    pass


def get_parser_args():
    parser = argparse.ArgumentParser(description='Connect to underground chat')
    parser.add_argument('--host', type=str, default=DEFAULT_HOST)
    parser.add_argument('--write_port', type=int, default=DEFAULT_WRITE_PORT)
    parser.add_argument('--token', type=str, default=DEFAULT_DEVMAN_TOKEN)
    parser.add_argument('--message', type=str)

    return parser.parse_args()

async def authorise(reader, writer, token: str) -> coroutine:
    server_answer = await reader.readline()
    logger_sender.debug(server_answer.decode())
    message_with_token = f'{token}{EMPTY_LINE}'
    writer.write(message_with_token.encode())
    await writer.drain()
    server_answer_about_token = await reader.readline()
    if json.loads(server_answer_about_token.decode()) is None:
        logger_sender.error('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        raise TokenError()


async def submit_message(host: str, port: int, token: str, message: str) -> coroutine:
    reader, writer = await asyncio.open_connection(
        host, port)
    try:
        await authorise(reader, writer, token)
    except TokenError:
        return
    message = f'{message}{EMPTY_LINE}{EMPTY_LINE}'
    logger_sender.debug(message)
    writer.write(message.encode())
    await writer.drain()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    DEFAULT_HOST = env.str('HOST')
    DEFAULT_WRITE_PORT = env.int('WRITE_PORT')
    DEFAULT_DEVMAN_TOKEN = env.str('DEVMAN_TOKEN')
    parser_args = get_parser_args()
    logging.basicConfig(level = INFO)
    message = parser_args.message.replace(EMPTY_LINE,'')
    asyncio.run(submit_message(parser_args.host, parser_args.write_port, parser_args.token, message))
