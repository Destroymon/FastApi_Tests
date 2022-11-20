import sqlite3

from fastapi import APIRouter

router = APIRouter()
db_name = "test.db"
con = sqlite3.connect(db_name, check_same_thread=False)

"""
Поля таблицы и типы полей
tracks:
    TrackId: INTEGER 
    Name: NVARCHAR(200)
    AlbumId:INTEGER
    MediaTypeId:INTEGER
    GenreId:INTEGER
    Composer: NVARCHAR(200)
    Milliseconds:INTEGER
    Bytes:INTEGER
    UnitPrice: NUMERIC
    
genres:
    GenreId: INTEGER
    Name: NVARCHAR(120)
"""


@router.get("/ping")
async def pong():
    return {
        "ping": "pong!",
        "environment": "Test task",
        "testing": "testing",
    }


# TODO: получить список жанров в виде словаря формата "id: name"
@router.get("/get_genres")
async def get_genres():
    cur = con.cursor()
    res = cur.execute("SELECT * FROM genres")
    return res


# TODO: вывести уникальные записей по полю "композитор" в требуемом жанре
#  в формате словаря в виде "композитор: название трека",
#  отсортированного по композитору,
#  а также количество таких записей в тот же словарь
#  !!!Все операции за исключением формирования результата делать с помощью SQL!!!
@router.get("/get_data/{genre_id}")
async def get_data(genre_id: int = 0):
    cur = con.cursor()
    string = f"SELECT DISTINCT Name, Composer, GenreId FROM tracks WHERE GenreId = {genre_id} AND Composer <> 'None' ORDER BY Composer"
    res = cur.execute(string)
    res = res.fetchall()
    result = {row[1]: row[0] for row in res}
    result["count"] = len(res)
    return result
