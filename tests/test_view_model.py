from todo_app.data.item import Item
from todo_app.view_model import ViewModel
import pytest

@pytest.fixture
def get_item_view_model():
    items = []
    items.append(Item('1', 'todo item 1', '', '1', 'To Do'))
    items.append(Item('2', 'todo item 2', '', '1', 'To Do'))
    items.append(Item('3', 'doing item 1', '', '2', 'Doing'))
    items.append(Item('4', 'doing item 2', '', '2', 'Doing'))
    items.append(Item('5', 'doing item 3', '', '2', 'Doing'))
    items.append(Item('6', 'done item 1', '', '3', 'Done'))
    print(items)

    yield ViewModel(items)

def test_todo_items(get_item_view_model):
    todo_items = get_item_view_model.todo_items
    assert len(todo_items) == 2
    item = todo_items[0]
    assert item.name == 'todo item 1'
    assert item.id == '1'
    item = todo_items[1]
    assert item.name == 'todo item 2'
    assert item.id == '2'


def test_doing_items(get_item_view_model):
    doing_items = get_item_view_model.doing_items
    assert len(doing_items) == 3
    item = doing_items[0]
    assert item.id == '3'
    assert item.name == 'doing item 1'
    item = doing_items[1]
    assert item.id == '4'
    assert item.name == 'doing item 2'
    item = doing_items[2]
    assert item.id == '5'
    assert item.name == 'doing item 3'


def test_done_items(get_item_view_model):
    done_items = get_item_view_model.done_items
    assert len(done_items) == 1
    item = done_items[0]
    assert item.name == 'done item 1'
    assert item.id == '6'
