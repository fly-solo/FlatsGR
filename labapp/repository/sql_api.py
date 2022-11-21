from .connector import StoreConnector
from pandas import DataFrame, Series
from datetime import datetime

"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""

# Вывод списка обработанных файлов с сортировкой по дате
def select_all_from_source_files(connector: StoreConnector):
    connector.start_transaction()  # начинаем выполнение запросов
    query = f'SELECT * FROM flats_for_sale LIMIT 2000'
    result = connector.execute(query).fetchall()
    connector.end_transaction()  # завершаем выполнение запросов
    return result

# Вставка строк в таблицу flats_for_sale
def insert_rows_into_flats_for_sale(connector: StoreConnector, df: DataFrame):
    connector.start_transaction()
    connector.execute(f'DELETE FROM flats_for_sale;')
    connector.execute(f'UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME=\'flats_for_sale\';')

    row_flats = df.to_dict('records')
    for row in row_flats:
        connector.execute(f'INSERT INTO flats_for_sale (Posted_On, BHK, Rent, Size_, Floor_, Area_Locality, City,'
                          f' Furnishing, Point_of_Contact) VALUES (\'{row["Posted_On"]}\', '
                          f'\'{row["BHK"]}\', \'{row["Rent"]}\', \'{row["Size_"]}\','
                          f'\'{row["Floor_"]}\', \'{row["Area_Locality"]}\', \'{row["City"]}\', '
                          f'\'{"Furnishing"}\', \'{row["Point_of_Contact"]}\')')
    connector.end_transaction()
