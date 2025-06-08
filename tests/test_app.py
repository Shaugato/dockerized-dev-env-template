"""Integration tests using the real Flask package and a temporary SQLite DB."""

import os
import importlib
from pathlib import Path
from unittest.mock import patch

import pytest

@pytest.fixture(scope="module")
def app_module(tmp_path_factory):
    db_file = tmp_path_factory.mktemp('db') / 'test.db'
    os.environ['DATABASE_URL'] = f'sqlite:///{db_file}'
    import app.main as main
    importlib.reload(main)

    # apply database schema
    conn = main.get_db_connection()
    sql = Path('db/init.sql').read_text().replace('SERIAL', 'INTEGER')
    conn.executescript(sql)
    conn.close()
    yield main


@pytest.fixture
def client(app_module):
    with app_module.app.test_client() as client:
        yield client


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.get_json() == {"message": "Welcome to Dockerized Dev Env Template!"}


def test_list_users(client):
    resp = client.get('/users')
    assert resp.status_code == 200
    assert resp.get_json() == [
        {"id": 1, "name": 'Alice Example', 'email': 'alice@example.com'},
        {"id": 2, "name": 'Bob Example', 'email': 'bob@example.com'}
    ]


def test_health_ok(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "OK"}


def test_health_fail(client, app_module):
    with patch.object(app_module, 'get_db_connection', side_effect=Exception('db down')):
        resp = client.get('/health')
    assert resp.status_code == 500
    assert resp.get_json() == {"status": "FAIL"}
