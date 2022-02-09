import os
from typing import Dict, List
import sqlite3
from sqlalchemy import create_engine, select, MetaData, Table


db_filename = "campaigns.db"
conn = sqlite3.connect(os.path.join("db", db_filename))
cursor = conn.cursor()

engine = create_engine(f"sqlite:///db\\{db_filename}")
metadata = MetaData(bind=None)

Campaigns = Table("campaigns", metadata, autoload=True, autoload_with=engine)

table_mappings = {
    "campaigns": Campaigns
}  # для маппинга имен таблиц с экземлярами sqlalchemy.Table


def __init_db():
    """Инициализирует БД"""
    with open("createdb.sql", mode="r", encoding="utf-8") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def __check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute(
        "SELECT name FROM sqlite_master " "WHERE type='table' AND name='campaigns'"
    )
    table_exists = cursor.fetchall()
    if table_exists:
        return
    __init_db()


def __is_valid(table_name: str, column_values=None) -> bool:

    # проверка на корректность типа аргумента для поиска таблицы БД
    if not isinstance(table_name, str):
        print("Имя таблицы должно иметь строковый тип")
        return False

    # проверка на существование таблицы БД
    if table_name not in table_mappings.keys():
        print(f"Таблицы с именем '{table_name}' не существует")
        return False

    if (
        column_values != None
    ):  # None - когда выбираем в методе fetchall все поля из таблицы БД

        # проверка на существование полей таблицы БД
        table_instance = table_mappings[table_name]
        columns_from_table = set(
            table_instance.metadata.tables[table_name].columns.keys()
        )
        columns_from_query = set()
        if isinstance(column_values, Dict):  # column_values из метода insert
            columns_from_query = set(column_values.keys())
        elif isinstance(column_values, List):  # column_values из метода fetchall
            columns_from_query = set(column_values)
        not_valid_columns = (
            columns_from_query - columns_from_table
        )  # разность множеств для поиска несуществующих полей
        if len(not_valid_columns) != 0:
            print(
                "Одно или несколько полей, переданных в аргументах, не соответствуют полям из БД"
            )
            return False

        # проверка на соответствие типам полей таблицы БД
        if isinstance(column_values, Dict):
            field_types = dict()  # типы данных из таблицы
            for column in metadata.tables[table_name].columns:
                field_types[column.name] = column.type.python_type
            for key, value in column_values.items():
                if not isinstance(value, field_types[key]):
                    print(
                        f"Поле '{key}' из запроса не соответсвует типу {field_types[key]}"
                    )
                    return False

    return True


def fetchall(table_name: str, columns: List = None):

    connection = engine.connect()
    if __is_valid(table_name, columns):
        table_instance = table_mappings[table_name]
        if columns == None:  # для выбора всех полей из таблицы
            query = table_instance.select()
        else:  # для выбора конкретных полей из таблицы
            fields = [
                metadata.table_instance[table_name].columns.get(column)
                for column in columns
            ]
            query = select(fields)
        lines = connection.execute(query).fetchall()
        connection.close()
        return lines
    else:
        print(
            "Аргументы, переданные в функцию получения данных из БД, не прошли валидацию"
        )


def insert(table_name: str, column_values: Dict):

    connection = engine.connect()
    if __is_valid(table_name, column_values):
        table_instance = table_mappings[table_name]
        query = (
            table_instance.insert().prefix_with("OR REPLACE").values(column_values)
        )  # "OR REPLACE" - на случай, когда поступила запись с существующим в БД PK
        connection.execute(query)
        connection.close()
    else:
        print("Аргументы, переданные в функцию вставки в БД, не прошли валидацию")


__check_db_exists()
