from urlshort import create_app

def test_shorten(client):
    response=client.get('/')
    assert b'Shorten URL' in response.data
