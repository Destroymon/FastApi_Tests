from fastapi.testclient import TestClient
from main import app


def test_ping() -> None:
    client = TestClient(app)
    response = client.get("/ping_page/ping")
    assert response.status_code == 200
    assert response.json() == {
        "ping": "pong!",
        "environment": "Test task",
        "testing": "testing",
    }


def test_get_genres():
    client = TestClient(app)
    response = client.get("/ping_page/get_genres")
    assert response.text == '{"1":"Rock","2":"Jazz","3":"Metal","4":"Alternative & Punk","5":"Rock And Roll","6":"Blues","7":"Latin","8":"Reggae","9":"Pop","10":"Soundtrack","11":"Bossa Nova","12":"Easy Listening","13":"Heavy Metal","14":"R&B/Soul","15":"Electronica/Dance","16":"World","17":"Hip Hop/Rap","18":"Science Fiction","19":"TV Shows","20":"Sci Fi & Fantasy","21":"Drama","22":"Comedy","23":"Alternative","24":"Classical","25":"Opera"}'
    

def test_get_data():
    client = TestClient(app)
    response = client.get("/ping_page/get_data/25")
    assert response.text == '{"Wolfgang Amadeus Mozart":"Die Zauberflöte, K.620: \\"Der Hölle Rache Kocht in Meinem Herze\\"","count":1}'
    