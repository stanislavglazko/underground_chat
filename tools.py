from asyncio import StreamReader, StreamWriter, coroutine
import logging

EMPTY_LINE = '\n'
ENV_FILE = '.env'


async def send_message(writer: StreamWriter, logger: logging.Logger, message: str) -> coroutine:
    message = message.encode()
    logger.debug(message)
    writer.write(message)
    await writer.drain()


async def read_line(reader: StreamReader) -> str:
    line = await reader.readline()
    decoded_line = line.decode()
    return decoded_line


def format_text(text: str) -> str:
    return text.replace(EMPTY_LINE, '')
