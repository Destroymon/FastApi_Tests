import numpy as np
import sqlite3

if __name__ == '__main__':
    db_name = "test.db"
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    res = cur.execute("SELECT DISTINCT Name, Composer "
                      "FROM tracks "
                      "WHERE GenreId = 3 AND Composer <> 'None' "
                      "ORDER BY Composer")
    # res_genres = cur.execute("SELECT * FROM genres")
    a = res.fetchall()
    a = np.array(a)
    a = np.unique(a, axis=5)
    pass
