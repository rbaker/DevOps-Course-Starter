from todo_app.app import create_app
from dotenv import find_dotenv, load_dotenv
from unittest.mock import Mock, patch
import pytest
import os
import sys

@pytest.fixture
def client():
    if os.environ.get('FLASK_APP') == None:
        file_path = find_dotenv('.env.test')
        load_dotenv(file_path, override=True)
    
    test_app = create_app()
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')
    assert response.status_code == 200
    assert b'first item in to-do' in response.data
    assert b'in the middle...' in response.data
    assert b'description right here.....' in response.data

@patch('requests.post')
def test_add_item(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.post('/addItem', content_type='multipart/form-data', data = dict(name = 'test name', description = 'test description'))
    assert response.status_code == 302
    params = {
        'key': os.environ['TRELLO_ACCOUNT_KEY'],
        'token': os.environ['TRELLO_SECRET_KEY'],
        'idList': os.environ['TODO_LIST_ID'],
        'name': 'test name',
        'desc': 'test description'
    }
    mock_get_requests.assert_called_once_with('https://api.trello.com/1/cards', params=params)

@patch('requests.put')
def test_move_to_doing(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.post('/start/123')
    assert response.status_code == 302
    params = {
        'key': os.environ['TRELLO_ACCOUNT_KEY'],
        'token': os.environ['TRELLO_SECRET_KEY'],
        'idList': os.environ['IN_PROGRESS_LIST_ID']
    }
    mock_get_requests.assert_called_once_with('https://api.trello.com/1/cards/123', params=params)

@patch('requests.put')
def test_move_to_done(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.post('/complete/123')
    assert response.status_code == 302
    params = {
        'key': os.environ['TRELLO_ACCOUNT_KEY'],
        'token': os.environ['TRELLO_SECRET_KEY'],
        'idList': os.environ['DONE_LIST_ID']
    }
    mock_get_requests.assert_called_once_with('https://api.trello.com/1/cards/123', params=params)

@patch('requests.put')
def test_move_to_todo(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.post('/reset/123')
    assert response.status_code == 302
    params = {
        'key': os.environ['TRELLO_ACCOUNT_KEY'],
        'token': os.environ['TRELLO_SECRET_KEY'],
        'idList': os.environ['TODO_LIST_ID']
    }
    mock_get_requests.assert_called_once_with('https://api.trello.com/1/cards/123', params=params)

@patch('requests.delete')
def test_delete(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.delete('/delete/123')
    assert response.status_code == 200
    params = {
        'key': os.environ['TRELLO_ACCOUNT_KEY'],
        'token': os.environ['TRELLO_SECRET_KEY'],
    }
    mock_get_requests.assert_called_once_with('https://api.trello.com/1/cards/123', params=params)
    

def mock_get_lists(url, params):
    response = None

    if url == f'https://api.trello.com/1/boards/boardId/lists':
        response = Mock()
        response.json.return_value = [{"id":"607f1ee7c99b117ea947851b","name":"To Do","closed":False,"pos":16384,"softLimit":None,"idBoard":"607f1ee7c99b117ea947851a","subscribed":False},{"id":"607f1ee7c99b117ea947851c","name":"Doing","closed":False,"pos":32768,"softLimit":None,"idBoard":"607f1ee7c99b117ea947851a","subscribed":False},{"id":"607f1ee7c99b117ea947851d","name":"Done","closed":False,"pos":49152,"softLimit":None,"idBoard":"607f1ee7c99b117ea947851a","subscribed":False}]
        
    if url == f'https://api.trello.com/1/boards/boardId/cards':
        response = Mock()
        response.json.return_value = [{"id":"607f1effc75bf07772e3d825","checkItemStates":None,"closed":False,"dateLastActivity":"2021-05-25T19:30:32.923Z","desc":"","descData":None,"dueReminder":None,"idBoard":"607f1ee7c99b117ea947851a","idList":"607f1ee7c99b117ea947851b","idMembersVoted":[],"idShort":1,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"first item in to-do","pos":65535,"shortLink":"rkSfwrYU","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":False,"due":None,"dueComplete":False,"start":None},"dueComplete":False,"due":None,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/rkSfwrYU","start":None,"subscribed":False,"url":"https://trello.com/c/rkSfwrYU/1-first-item-in-to-do","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}},{"id":"60ad4868211a87658c0ab2e6","checkItemStates":None,"closed":False,"dateLastActivity":"2021-05-25T18:56:49.654Z","desc":"        centrer","descData":None,"dueReminder":None,"idBoard":"607f1ee7c99b117ea947851a","idList":"607f1ee7c99b117ea947851c","idMembersVoted":[],"idShort":16,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"in the middle...","pos":98303,"shortLink":"NbUv1Pwu","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":None,"dueComplete":False,"start":None},"dueComplete":False,"due":None,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/NbUv1Pwu","start":None,"subscribed":False,"url":"https://trello.com/c/NbUv1Pwu/16-in-the-middle","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}},{"id":"609aeb90cf3555641903122f","checkItemStates":None,"closed":False,"dateLastActivity":"2021-06-15T19:07:39.140Z","desc":"description right here.....","descData":{"emoji":{}},"dueReminder":None,"idBoard":"607f1ee7c99b117ea947851a","idList":"607f1ee7c99b117ea947851d","idMembersVoted":[],"idShort":11,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"straight to done?","pos":81919,"shortLink":"bK6T1MOP","isTemplate":False,"cardRole":None,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":True,"due":None,"dueComplete":False,"start":None},"dueComplete":False,"due":None,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/bK6T1MOP","start":None,"subscribed":False,"url":"https://trello.com/c/bK6T1MOP/11-straight-to-done","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None}}]
    
    if url == f'https://api.trello.com/1/cards':
        response = Mock()
    
    if url == f'https://api.trello.com/1/cards':
        response = Mock()
    
    if url == f'https://api.trello.com/1/cards/123':
        response = Mock()
        response.json.return_value = {"id":"123","checkItemStates":[],"closed":False,"dateLastActivity":"2021-04-20T21:05:35.171Z","desc":"","descData":None,"dueReminder":None,"idBoard":"607f1ee7c99b117ea947851a","idList":"607f1ee7c99b117ea947851c","idMembersVoted":[],"idShort":8,"idAttachmentCover":None,"idLabels":[],"manualCoverAttachment":False,"name":"API UPDATE","pos":147455,"shortLink":"JPLs9iCH","isTemplate":False,"cardRole":None,"dueComplete":False,"due":None,"email":None,"labels":[],"shortUrl":"https://trello.com/c/JPLs9iCH","start":None,"url":"https://trello.com/c/JPLs9iCH/8-api-update","cover":{"idAttachment":None,"color":None,"idUploadedBackground":None,"size":"normal","brightness":"dark","idPlugin":None},"idMembers":[],"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":False,"votes":0,"viewingMemberVoted":False,"subscribed":False,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":None,"comments":0,"attachments":0,"description":False,"due":None,"dueComplete":False,"start":None},"subscribed":False,"idChecklists":[]}

    return response
