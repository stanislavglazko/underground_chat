import asyncio

async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        "minechat.dvmn.org", 5000)
    
    while True:
        data = await reader.readline()
        print(data.decode())


asyncio.run(tcp_echo_client())
