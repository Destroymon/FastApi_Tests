from fastapi.testclient import TestClient
from main import app, html


def test_read_main() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == html


def test_websocket_1() -> None:
    client = TestClient(app)
    with client.websocket_connect("/ws/1") as websocket:
        data = websocket.receive_text()
        assert data == 'Client #1 joined the chat'


def test_websocket_2() -> None:
    client = TestClient(app)
    with client.websocket_connect("/ws/2") as websocket:
        data = websocket.receive_text()
        assert data == 'Client #2 joined the chat'


def module_test_ws():
    client = TestClient(app)
    with client.websocket_connect("/ws/2") as websocket_2:
        mes_con2_c2 = websocket_2.receive_text()
        assert mes_con2_c2 == 'Client #2 joined the chat'

        with client.websocket_connect("/ws/3") as websocket_3:
            mes_con3_c3 = websocket_3.receive_text()
            assert mes_con3_c3 == 'Client #3 joined the chat'
            mes_con3_c2 = websocket_2.receive_text()
            assert mes_con3_c2 == 'Client #3 joined the chat'

            websocket_2.send_text("mes test 2")
            mes_per2_c3 = websocket_2.receive_text()
            mes_test2_c2 = websocket_2.receive_text()
            mes_test2_c3 = websocket_3.receive_text()
            assert mes_per2_c3 == 'You wrote: mes test 2'
            assert mes_test2_c2 == 'Client #2 says: mes test 2'
            assert mes_test2_c3 == 'Client #2 says: mes test 2'

            websocket_3.send_text("mes test 3")
            mes_test2_c2 = websocket_2.receive_text()
            mes_per3_c3 = websocket_3.receive_text()
            mes_test2_c3 = websocket_3.receive_text()
            assert mes_test2_c2 == 'Client #3 says: mes test 3'
            assert mes_per3_c3 == 'You wrote: mes test 3'
            assert mes_test2_c3 == 'Client #3 says: mes test 3'

        mes_end3_c2 = websocket_2.receive_text()
        assert mes_end3_c2 == 'Client #3 left the chat'
