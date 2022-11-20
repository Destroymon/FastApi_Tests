import asyncio
import aiohttp
import os
import time

POP20_C = "CN IN US ID BR PK NG BD RU EN GE".split()
BASE_URL = "http://flupy.org/data/flags"
DEST_DIR = "downloads"


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    # time.sleep(2)
    with open(path, "wb") as f:
        f.write(img)


async def get_flag(cc):
    url = f"{BASE_URL}/{cc.lower()}/{cc.lower()}.gif"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            image = await resp.read()
    return image


async def download_one(cc):
    image = await get_flag(cc)
    save_flag(image, f"{cc.lower()}.gif")
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)


def main(func):
    t0 = time.time()
    count = func(POP20_C)
    elapsed = time.time() - t0
    msg = "{} flags downloaded in {}s".format(count, elapsed)
    print(msg)


if __name__ == '__main__':
    main(download_many)