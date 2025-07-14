# Processing csv-file

Processing csv-file - это скрипт для обработки CSV-файла, поддерживающий следующие операции:
- фильтрация с операторами «больше», «меньше» и «равно»; 
- агрегация с расчетом среднего (avg), минимального (min) и максимального (max) значения;
- сортировка по возрастанию (asc) и по убыванию (desc).


## Параметры запуска

Для использования скрипта необходимо:
1. Клонировать данный репозиторий
2. Создать и активировать виртуальное окружение в директории скрипта
3. Установить необходимые зависимости (pip install -r requirements.txt)
4. В терминале в директории скрипта запустить:

- для вывода исходной таблицы:  
    python main.py --file file_name


- для фильтрации таблицы:  
    - python main.py --file file_name --where "column>value"  
    - python main.py --file file_name --where "column<value"  
    - python main.py --file file_name --where "column=value"


- для агрегации значений таблицы:  
    - python main.py --file file_name --aggregate "column=min"  
    - python main.py --file file_name --aggregate "column=max"  
    - python main.py --file file_name --aggregate "column=avg"


- для сортировки таблицы:  
    - python main.py --file file_name --order-by "column=asc"  
    - python main.py --file file_name --order-by "column=asc"

где необходимо заменить следующие параметры:  
file_name - путь к файлу;  
column - столбец таблицы;  
value - значение.


## Примеры запуска
Запуск скрипта на примере файла [exemple/products.csv](exemple/products.csv)

### 1) Вывод таблицы в исходном состоянии
python main.py --file exemple/products.csv

![img_1.png](exemple/screenshots/img_1.png)


### 2) Фильтрация. Вывод строк, где значение цены ниже 400
python main.py --file exemple/products.csv --where "price<400"

![img_2.png](exemple/screenshots/img_2.png)


### 3) Фильтрация. Вывод строк, где значение цены выше 400
python main.py --file exemple/products.csv --where "price>400"

![img_3.png](exemple/screenshots/img_3.png)


### 4) Фильтрация. Вывод строк, где значение цены равно 999
python main.py --file exemple/products.csv --where "price=999"

![img_4.png](exemple/screenshots/img_4.png)


### 5) Агрегация. Вывод минимального рейтинга
python main.py --file exemple/products.csv --aggregate "rating=min"

![img_5.png](exemple/screenshots/img_5.png)


### 6) Агрегация. Вывод максимального рейтинга
python main.py --file exemple/products.csv --aggregate "rating=max"

![img_6.png](exemple/screenshots/img_6.png)


### 7) Агрегация. Вывод среднего арифметического рейтинга
python main.py --file exemple/products.csv --aggregate "rating=avg"

![img_7.png](exemple/screenshots/img_7.png)


### 8) Сортировка. Вывод отсортированной по возрастанию бренда таблицы
python main.py --file exemple/products.csv --order-by "brand=asc"

![img_8.png](exemple/screenshots/img_8.png)


### 9) Сортировка. Вывод отсортированной по убыванию бренда таблицы
python main.py --file exemple/products.csv --order-by "brand=desc"

![img_9.png](exemple/screenshots/img_9.png)



## Тестирование скрипта

Скрипт протестирован с помощью pytets. 82% покрытия по pytest-cov

![screenshots/img.png](tests/screenshots/img.png)