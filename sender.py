import argparse
import asyncio
import json
import logging
from asyncio import StreamReader, StreamWriter, coroutine
from distutils.log import INFO
from environs import Env

from tools import (
    EMPTY_LINE,
    format_text,
    open_connection,
    read_line,
    send_message,
)

logger_sender = logging.getLogger("sender")


class TokenError(Exception):
    pass


def get_parser_args():
    parser = argparse.ArgumentParser(description='Text to the underground chat')
    parser.add_argument('--host', type=str, default=default_host)
    parser.add_argument('--write_port', type=int, default=default_write_port)
    parser.add_argument('--token', type=str, default=default_devman_token)
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


async def submit_message(
    host: str,
    port: int,
    token: str,
    message: str,
) -> coroutine:
    async with open_connection(host, port) as connection:
        reader, writer = connection
        try:
            await authorise(reader, writer, token)
        except TokenError:
            return
        message = f'{message}{EMPTY_LINE}{EMPTY_LINE}'
        await send_message(writer, logger_sender, message)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    default_host = env.str('HOST', 'minechat.dvmn.org')
    default_write_port = env.int('WRITE_PORT', 5050)
    default_devman_token = env.str('DEVMAN_TOKEN')
    parser_args = get_parser_args()
    logging.basicConfig(level=INFO)
    message = format_text(parser_args.message)
    asyncio.run(
        submit_message(
            parser_args.host,
            parser_args.write_port,
            parser_args.token,
            message,
        )
    )
