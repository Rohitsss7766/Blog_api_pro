import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app import crud, models, schemas


@pytest.fixture
def mock_post_data():
    return schemas.PostCreate(
        title="Test Title",
        content="Test Content",
        author="Test Author"
    )


def test_create_post(mock_post_data):
    mock_db = MagicMock()
    mock_db.refresh = lambda post: None  # Bypass refresh
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    mock_db_post = models.Post(id=1, **mock_post_data.dict(), is_deleted=False)

    with patch("app.models.Post", return_value=mock_db_post):
        result = crud.create_post(mock_db, mock_post_data)

    assert result.title == "Test Title"
    assert result.content == "Test Content"
    assert result.author == "Test Author"


def test_get_posts():
    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_filter.offset.return_value.limit.return_value.all.return_value = [
        models.Post(id=1, title="A", content="B", author="C", is_deleted=False)
    ]

    result = crud.get_posts(mock_db)
    assert len(result) == 1
    assert result[0].title == "A"


def test_get_post_found():
    mock_db = MagicMock()
    mock_post = models.Post(id=1, title="Title", is_deleted=False)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_post

    result = crud.get_post(mock_db, 1)
    assert result.id == 1
    assert result.title == "Title"


def test_get_post_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = crud.get_post(mock_db, 999)
    assert result is None


def test_update_post_success(mock_post_data):
    mock_db = MagicMock()
    db_post = models.Post(id=1, title="Old", content="Old", author="Old", is_deleted=False)
    mock_db.query.return_value.filter.return_value.first.return_value = db_post

    updated_post = crud.update_post(mock_db, 1, mock_post_data)

    assert updated_post.title == "Test Title"
    assert updated_post.content == "Test Content"
    assert updated_post.author == "Test Author"
    assert isinstance(updated_post.updated_at, datetime)


def test_update_post_not_found(mock_post_data):
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = crud.update_post(mock_db, 99, mock_post_data)
    assert result is None


def test_delete_post_success():
    mock_db = MagicMock()
    db_post = models.Post(id=1, title="Delete", is_deleted=False)
    mock_db.query.return_value.filter.return_value.first.return_value = db_post

    result = crud.delete_post(mock_db, 1)
    assert result is True
    assert db_post.is_deleted is True


def test_delete_post_already_deleted():
    mock_db = MagicMock()
    db_post = models.Post(id=1, title="Delete", is_deleted=True)
    mock_db.query.return_value.filter.return_value.first.return_value = db_post

    result = crud.delete_post(mock_db, 1)
    assert result is False


def test_delete_post_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = crud.delete_post(mock_db, 1)
    assert result is False


def test_get_deleted_posts():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.all.return_value = [
        models.Post(id=1, title="Deleted", is_deleted=True)
    ]

    result = crud.get_deleted_posts(mock_db)
    assert len(result) == 1
    assert result[0].is_deleted is True


def test_restore_post_success():
    mock_db = MagicMock()
    db_post = models.Post(id=1, title="Restore", is_deleted=True)
    mock_db.query.return_value.filter.return_value.first.return_value = db_post

    result = crud.restore_post(mock_db, 1)
    assert result.is_deleted is False


def test_restore_post_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = crud.restore_post(mock_db, 1)
    assert result is None


def test_restore_post_not_deleted():
    mock_db = MagicMock()
    db_post = models.Post(id=1, title="Restore", is_deleted=False)
    mock_db.query.return_value.filter.return_value.first.return_value = db_post

    result = crud.restore_post(mock_db, 1)
    assert result is None
