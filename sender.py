import argparse
import asyncio
import logging
import json
from asyncio import StreamReader, StreamWriter, coroutine
from distutils.log import INFO
from environs import Env

from tools import EMPTY_LINE, format_text, read_line, send_message

logger_sender = logging.getLogger("sender")

class TokenError(Exception):
    pass


def get_parser_args():
    parser = argparse.ArgumentParser(description='Text to the underground chat')
    parser.add_argument('--host', type=str, default=DEFAULT_HOST)
    parser.add_argument('--write_port', type=int, default=DEFAULT_WRITE_PORT)
    parser.add_argument('--token', type=str, default=DEFAULT_DEVMAN_TOKEN)
    parser.add_argument('--message', type=str)
    return parser.parse_args()

async def authorise(reader: StreamReader, writer: StreamWriter, token: str) -> coroutine:
    await read_line(reader, logger_sender)

    message_with_token = f'{token}{EMPTY_LINE}'
    await send_message(writer, logger_sender, message_with_token)

    server_check_token = await read_line(reader, logger_sender)
    if json.loads(server_check_token) is None:
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
    await send_message(writer, logger_sender, message)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    DEFAULT_HOST = env.str('HOST')
    DEFAULT_WRITE_PORT = env.int('WRITE_PORT')
    DEFAULT_DEVMAN_TOKEN = env.str('DEVMAN_TOKEN')
    parser_args = get_parser_args()
    logging.basicConfig(level = INFO)
    message = format_text(parser_args.message)
    asyncio.run(submit_message(parser_args.host, parser_args.write_port, parser_args.token, message))
