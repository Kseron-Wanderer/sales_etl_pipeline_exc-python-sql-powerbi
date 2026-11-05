# ETL процесс обработки данных

import os
import pandas as pd
import shutil
from sqlalchemy import create_engine


engine = create_engine('postgresql://postgres:pass@localhost:5432/testdb')                  # подключение к БД

incoming_folder = 'C:\\Users\\HYPER\\Desktop\\My_Projects\\Incoming_Data'                   # папки для выгрузки новых данных
archive_folder = 'C:\\Users\\HYPER\\Desktop\\My_Projects\\Archive_Data'                     # папки для выгрузки старых данных (для бекапа и пропуска двойной проверки файла)

for filename in os.listdir(incoming_folder):                                                # os.listdir берет путь к папке (incoming_folder) и считывает имена всех объектов внутри неё
    file_path = os.path.join(incoming_folder, filename)                                     # клеим пути через os.path.join
    if not os.path.isfile(file_path):                                                       # если не наш файл - пропускаем
        continue
    ext = filename.split('.')[-1].lower()                                                   # отделяем расширение файла и файл в список [..., xlsx] для читки

    try:                                                                                    # определяем формат файла (csv,xls,xlsx) на лету
        print(f"Читаю файл: {filename}")
        if ext == 'csv':
            df = pd.read_csv(file_path)
        elif ext in ['xls', 'xlsx']:                            
            df = pd.read_excel(file_path)                                                   # df = pd.read_excel('file.xlsx', header=1, usecols='B:E') - если столбцы и строки в excel идут с разных строк/столбцов.
        else:
            print(f"Формат {ext} не поддерживается")
            continue

        # конвертируем дату для ЛЮБОГО файла (до загрузки в БД)
        if 'load_date' in df.columns:
            df['load_date'] = pd.to_datetime(df['load_date'], format='%d.%m.%Y')            # меняем формат даты

        with engine.begin() as connection:                                                  # сохраняем в БД в рамках транзакции (защита от сбоев)
            df.to_sql('raw_sales', connection, if_exists='append', index=False)

        shutil.move(file_path, os.path.join(archive_folder, filename))                      # перемещаем в архив через shutil.move
        print(f"Успех! Файл {filename} загружен и в архиве.")

    except Exception as e:
        print(f"ОШИБКА с файлом {filename}: {e}")