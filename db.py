import os
from typing import Dict, List, Tuple
import sqlite3

from sqlalchemy import create_engine, select, MetaData, Table

conn = sqlite3.connect(os.path.join("db", "campaigns.db"))
cursor = conn.cursor()

def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", mode="r", encoding='utf-8') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='campaigns'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()

engine = create_engine('sqlite:///db\\campaigns.db')
metadata = MetaData(bind=None)

Campaigns = Table(
    'campaigns', 
    metadata, 
    autoload=True, 
    autoload_with=engine
)

def test():
    """ORM"""
    connection = engine.connect()
    stmt = select([
    Campaigns.columns.id, 
    Campaigns.columns.company_name]
    )
    results = connection.execute(stmt).fetchall()
    # insert
    stmta = Campaigns.insert().values(id=333, company_name="test")
    connection.execute(stmta)
    # delete
    # stmt = delete(user_table).where(user_table.c.name == 'patrick')
    return results

test()