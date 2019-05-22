import json
import requests
from somemart.models import Item, Review


class TestViews(object):

    def test_post_item(self, client, db=None):
        """/api/v1/goods/ (POST) сохраняет товар в базе."""
        url = 'http://127.0.0.1:8000/api/v1/goods/'
        data = json.dumps({
            'title': 'Сыр "Российский"',
            'description': 'Очень вкусный сыр, да еще и российский.',
            'price': 100
        })
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == 201
        document = response.json()
        # Объект был сохранен в базу
        item = Item.objects.get(pk=document['id'])
        assert item.title == 'Сыр "Российский"'
        assert item.description == 'Очень вкусный сыр, да еще и российский.'
        assert item.price == 100


if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/api/v1/goods/'
    data = json.dumps({
        'title': 'Сыр "Российский"',
        'description': 'Очень вкусный сыр, да еще и российский.',
        'price': 100
    })
    response = requests.post(url, data=data, content_type='application/json')
    print(response.status_code)