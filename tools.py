import logging
from asyncio import StreamReader, StreamWriter, coroutine

EMPTY_LINE = '\n'
ENV_FILE = '.env'


async def send_message(writer: StreamWriter, logger: logging.Logger, message: str) -> coroutine:
    logger.debug(message)
    message = message.encode()
    writer.write(message)
    await writer.drain()


async def read_line(reader: StreamReader, logger: logging.Logger) -> str:
    line = await reader.readline()
    decoded_line = line.decode()
    formatted_line = format_text(decoded_line)
    logger.debug(formatted_line)
    return formatted_line


def format_text(text: str) -> str:
    return text.replace(EMPTY_LINE, '')
