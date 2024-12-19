from hub import SocHub

def test_server(host, port):
    hub = SocHub(host, port)
    hub.close()
    assert True

if __name__ == '__main__':
    test_server('localhost', 12345)