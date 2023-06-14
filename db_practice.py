import os
import sqlite3

from typing import List, Set


def execute_query(query_sql: str) -> List:
    """
    Функция для выполнения запроса
    :param query_sql: запрос
    :return: результат выполнения запроса
    """
    db_pass = os.path.join(os.getcwd(), 'chinook.db')
    connection = sqlite3.connect(db_pass)
    cur = connection.cursor()
    result = cur.execute(query_sql).fetchall()
    connection.close()
    return result


def unwrapper(records: List):
    """
    Функция для вывода результата выполнения запроса
    :param records: список ответа БД
    """
    for record in records:
        print(*record)
    return records


def get_employees() -> None:
    """
    Возвращает список
    """
    query_sql = f'''
        SELECT *
          FROM employees;
    '''
    unwrapper(execute_query(query_sql))


# get_employees()


def get_customers(state_name=None, city_name=None) -> dict:
    query_sql = '''
        SELECT FirstName
              ,City
              ,State
          FROM customers
        '''
    filter_query = ''
    if city_name and state_name:
        filter_query = f" WHERE City = '{city_name}' and State = '{state_name}'"
    if city_name and not state_name:
        filter_query = f" WHERE City = '{city_name}'"
    if state_name and not city_name:
        filter_query = f" WHERE State = '{state_name}'"

    query_sql += filter_query
    return execute_query(query_sql)


# get_customers()
# get_customers(city_name='Budapest')
# get_customers(state_name='RJ')
# get_customers(state_name='RJ', city_name='Rio de Janeiro')


def get_unique_customers_by_python():
    query_sql = f'''
        SELECT FirstName
          FROM customers
    '''
    records = execute_query(query_sql)
    result = set()
    for record in records:
        result.add(record[0])
    return len(result)


# print(get_unique_customers_by_python())


def get_unique_customers_by_sql():
    query_sql = f'''
            SELECT count(distinct FirstName) as first_names_qty
              FROM customers
    '''

    result = execute_query(query_sql)[0][0]
    return result


# print(get_unique_customers_by_sql())


query_sql = '''
      SELECT FirstName
            ,LastName
        FROM customers
'''

result = execute_query(query_sql)


# print(result)
# print(result[2][1])


def get_invoice_profit() -> float:
    """
    Возвращает прибыль по таблице invoice_items
    """
    query_sql = '''
        SELECT SUM(UnitPrice * Quantity) as TotalProfit
          FROM invoice_items;
    '''
    result = execute_query(query_sql)
    total_profit = result[0][0] if result and result[0] else 0.0
    return round(total_profit, 2)


print(f"Прибыль по таблице invoice_items = {get_invoice_profit()}")


def get_duplicate_customers() -> None:
    """
    Выводит повторяющиеся FirstName из таблицы customers и их количество вхождений
    """
    query_sql = '''
        SELECT FirstName, COUNT(*) as Count
          FROM customers
          GROUP BY FirstName
          HAVING COUNT(*) > 1;
    '''
    print("\nПовторяющиеся FirstName из таблицы customers и кол-во их вхождений в таблицу:")
    unwrapper(execute_query(query_sql))


get_duplicate_customers()
