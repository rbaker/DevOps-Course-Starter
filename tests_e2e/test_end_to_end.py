import os
import unittest
import requests
import re
import time
from dotenv import find_dotenv, load_dotenv
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from todo_app.app import create_app
from todo_app.data.session_items import get_lists
from threading import Thread
from selenium import webdriver

class TestE2E (unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")

        self._driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=options)
        self._driver.implicitly_wait(5)

        print("board id: " + os.getenv('BOARD_ID'))
        print("board id: " + os.getenv('TRELLO_ACCOUNT_KEY'))

        file_path = find_dotenv('.env')
        load_dotenv(file_path, override=True)
        board_id = self.create_trello_board()

        os.environ['BOARD_ID'] = board_id
        self._board_id = board_id
        lists = list(get_lists())
        os.environ['TODO_LIST_ID'] = lists[0]
        os.environ['IN_PROGRESS_LIST_ID'] = lists[1]
        os.environ['DONE_LIST_ID'] = lists[2]

        application = create_app()
        self._thread = Thread(target=lambda:application.run(use_reloader=False))
        self._thread.daemon = True
        self._thread.start()

    def create_trello_board(self):
        params = {
            'key': os.environ['TRELLO_ACCOUNT_KEY'],
            'token': os.environ['TRELLO_SECRET_KEY'],
            'name' : "selenium test board"
        }
        board = requests.post('https://api.trello.com/1/boards/', params)
        json = board.json()
        return json['id']

    def test_task_journey(self):
        self._driver.get('http://localhost:5000/')
        assert self._driver.title == 'To-Do App'
        with self.assertRaises(NoSuchElementException):
            self._driver.find_element_by_class_name("todoItem")
            self._driver.find_element_by_class_name("doingItem")
            self._driver.find_element_by_class_name("doneItem")

        self._driver.find_element_by_id('name').send_keys('This is a selenium test item')
        self._driver.find_element_by_id('description').send_keys('Test description')
        self._driver.find_element_by_id('submitItem').submit()

        assert f'This is a selenium test item -- Test description' == self._driver.find_element_by_class_name('todoItem').text

        startItemPattern = re.compile('(startItem[0-9a-f]{24})')
        startItemId = startItemPattern.search(self._driver.page_source).group()

        self._driver.find_element_by_id(startItemId).submit()
        time.sleep(2)

        with self.assertRaises(NoSuchElementException):
            self._driver.find_element_by_class_name("todoItem")
            self._driver.find_element_by_class_name("doneItem")
        
        assert f'This is a selenium test item -- Test description' == self._driver.find_element_by_class_name('doingItem').text

        completeItemPattern = re.compile('(completeItem[0-9a-f]{24})')
        completeItemId = completeItemPattern.search(self._driver.page_source).group()

        self._driver.find_element_by_id(completeItemId).submit()
        time.sleep(2)

        with self.assertRaises(NoSuchElementException):
            self._driver.find_element_by_class_name("todoItem")
            self._driver.find_element_by_class_name("doingItem")
        
        assert f'This is a selenium test item -- Test description' == self._driver.find_element_by_class_name('doneItem').text

        deletePattern = re.compile('(delete[0-9a-f]{24})')
        deleteId = deletePattern.search(self._driver.page_source).group()

        assert deleteId in self._driver.page_source

        self._driver.find_element_by_id(deleteId).click()
        time.sleep(2)

        with self.assertRaises(NoSuchElementException):
            self._driver.find_element_by_class_name("todoItem")
            self._driver.find_element_by_class_name("doingItem")
            self._driver.find_element_by_class_name("doneItem")


    def tearDown(self):
        self._thread.join(1)
        requests.delete('https://api.trello.com/1/boards/' + self._board_id + '?key=' + os.environ['TRELLO_ACCOUNT_KEY'] + "&token=" + os.environ['TRELLO_SECRET_KEY'])
