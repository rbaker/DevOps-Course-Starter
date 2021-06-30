import os
import pytest
import requests
import re
import time
from dotenv import find_dotenv, load_dotenv
from todo_app.app import create_app
from todo_app.data.session_items import get_lists
from threading import Thread
from selenium import webdriver

@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    board_id = create_trello_board()

    os.environ['BOARD_ID'] = board_id
    lists = list(get_lists())
    print(lists)
    os.environ['TODO_LIST_ID'] = lists[0]
    os.environ['IN_PROGRESS_LIST_ID'] = lists[1]
    os.environ['DONE_LIST_ID'] = lists[2]

    application = create_app()
    thread = Thread(target=lambda:application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
    thread.join(1)
    delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Chrome() as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
    assert not f'This is a selenium test item' in driver.page_source

    driver.find_element_by_id('name').send_keys('This is a selenium test item')
    driver.find_element_by_id('description').send_keys('Test description')
    driver.find_element_by_id('submitItem').submit()

    assert f'This is a selenium test item' in driver.page_source

    deletePattern = re.compile('(delete[0-9a-f]{24})')
    deleteId = deletePattern.search(driver.page_source).group()

    assert deleteId in driver.page_source

    driver.find_element_by_id(deleteId).click()
    time.sleep(2)

    assert not f'This is a selenium test item' in driver.page_source


def create_trello_board():
    params = {
        'key': os.environ['TRELLO_ACCOUNT_KEY'],
        'token': os.environ['TRELLO_SECRET_KEY'],
        'name' : "selenium test board"
    }
    board = requests.post('https://api.trello.com/1/boards/', params)
    json = board.json()
    return json['id']

def delete_trello_board(board_id):
    requests.delete('https://api.trello.com/1/boards/' + board_id + '?key=' + os.environ['TRELLO_ACCOUNT_KEY'] + "&token=" + os.environ['TRELLO_SECRET_KEY'])
