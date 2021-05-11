from todo_app.data.item import Item
import requests
import os

def custom_sort(t):
    return t['status']

def get_lists():
    """
    Gets all lists on a board 
    """
    params = {
        'key': os.environ['ACCOUNT_KEY'],
        'token': os.environ['SECRET_KEY']
    }
    response = requests.request('GET', 'https://api.trello.com/1/boards/607f1ee7c99b117ea947851a/lists', params=params)
    listMap = {}
    for r in response.json():
        listMap[r['id']] = r
    return listMap

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    #return sorted(session.get('items', _DEFAULT_ITEMS), key = custom_sort, reverse=True)
    params = {
        'key': os.environ['ACCOUNT_KEY'],
        'token': os.environ['SECRET_KEY']
    }
    response = requests.request('GET', 'https://api.trello.com/1/boards/9u4MeVfa/cards', params=params)
    objList = []
    for r in response.json():
        objList.append(Item(r['id'], r['name'], r['desc'], r['idList']))
    return objList

def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    params = {
        'key': os.environ['ACCOUNT_KEY'],
        'token': os.environ['SECRET_KEY']
    }
    response = requests.get('https://api.trello.com/1/cards/' + id, params=params)
    r = response.json()
    return Item(r['id'], r['name'], r['desc'], r['idList'])


def add_item(title, description):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    params = {
        'key': os.environ['ACCOUNT_KEY'],
        'token': os.environ['SECRET_KEY'],
        'idList': '607f1ee7c99b117ea947851b',
        'name': title,
        'desc': description
    }
    response = requests.post('https://api.trello.com/1/cards', params=params)



def save_item(id, list):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    params = {
        'key': os.environ['ACCOUNT_KEY'],
        'token': os.environ['SECRET_KEY'],
        'idList': list
    }
    response = requests.put('https://api.trello.com/1/cards/' + id, params=params)
    r = response.json()
    return Item(r['id'], r['name'], r['desc'], r['idList'])

def delete_item(id):
    """
    Deletes an existing item in the session. If no existing item matches the ID of the specified item, nothing is deleted.

    Args:
        item: The id of the item to delete.
    """
    params = {
        'key': os.environ['ACCOUNT_KEY'],
        'token': os.environ['SECRET_KEY']
    }
    requests.delete('https://api.trello.com/1/cards/' + id, params=params)
