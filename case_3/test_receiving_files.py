import main 
import asyncio
from aioresponses import aioresponses
import aiohttp
import builtins


def test_get_flag():
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession()
    with aioresponses() as m:
        m.get('http://flupy.org/data/flags/ru/ru.gif', body=b"test")
        data = loop.run_until_complete(main.get_flag("RU"))
        assert b"test" == data


def test_download_one(mocker):
    mocker.patch("main.save_flag")
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession()
    with aioresponses() as m:
        m.get('http://flupy.org/data/flags/ru/ru.gif', body=b"test")
        data = loop.run_until_complete(main.download_one("RU"))
        assert "RU" == data
        main.save_flag.assert_called_once_with(b"test", 'ru.gif')


def test_download_many(mocker):
    async def download_one(cc):
        return cc
    mocker.patch('main.download_one', return_value=download_one)
    count = main.download_many(main.POP20_C)
    assert count == 11


def test_main(mocker):
    mocker.patch('builtins.print')
    mocker.patch('time.time', return_value=1)
    main.main(len)
    builtins.print.assert_called_once_with("11 flags downloaded in 0s")