import re
from pathlib import Path

INIT_SQL = Path('db/init.sql').read_text()

def test_users_table_created():
    # Check that users table is created with id, name and email columns
    pattern = re.compile(r"CREATE TABLE IF NOT EXISTS\s+users", re.IGNORECASE)
    assert pattern.search(INIT_SQL)
    assert 'id SERIAL PRIMARY KEY' in INIT_SQL
    assert 'name VARCHAR(100) NOT NULL' in INIT_SQL
    assert 'email VARCHAR(100) NOT NULL UNIQUE' in INIT_SQL

def test_seed_users():
    # Ensure seed data contains at least Alice and Bob
    assert "('Alice Example', 'alice@example.com')" in INIT_SQL
    assert "('Bob Example', 'bob@example.com')" in INIT_SQL
