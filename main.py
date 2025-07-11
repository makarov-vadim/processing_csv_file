import argparse
import csv
import statistics
from argparse import Namespace

from tabulate import tabulate


class ProcessingCsvFile:

    def __init__(self, delimiter: str = ",", quotechar: str = '"'):
        self._delimiter = delimiter
        self._quotechar = quotechar

        self._args = None
        self._file_name = None
        self._file_content = None

        self._parse_args()
        self._open_file()



    @property
    def delimiter(self):
        return self._delimiter


    @property
    def quotechar(self):
        return self._quotechar


    @property
    def file_content(self):
        return self._file_content

    @property
    def args(self):
        return self._args


    @property
    def file_name(self):
        return self._file_name


    @staticmethod
    def convert_to_numeric(value: str):
        try:
            result = float(value)
            assert str(result) == value
        except AssertionError:
            result = int(value)
        except ValueError:
            result = value

        return result


    @staticmethod
    def _print_table(tabular_data: list[dict]):
        print(tabulate(tabular_data, headers="keys", tablefmt="psql"))


    def _open_file(self):
        if self.file_name is None:
            print('Не указан путь к файлу. Пример: "--file file_path"')
            exit()
        try:
            with open(self.file_name, encoding='utf-8') as file:
                rows = csv.DictReader(file, delimiter=self.delimiter, quotechar=self.quotechar)
                self._file_content = [{key: self.convert_to_numeric(value) for key, value in row.items()} for row in rows]
        except FileNotFoundError:
            print('Введен некорректный путь к файлу. Пример: "--file file_path"')
            exit()


    def _parse_args(self):
        self._parser = argparse.ArgumentParser()

        self._parser.add_argument("--file", type=str, help='Путь к файлу. Пример: "--file file_path')
        self._parser.add_argument("--where", type=str, help='Условие фильтрации. Пример: --where "column_name=value"')
        self._parser.add_argument("--aggregate", type=str, help='Способ агрегации. Пример: --aggregate "column_name=max"')
        self._parser.add_argument("--order-by", type=str, help='Способ сортировки. Пример: --order-by "column_name=desc"')

        self._args = self._parser.parse_args()
        self._file_name = self.args.file


    def print_file_content(self):
        self._print_table(self.file_content)


    def filter_equal(self, column: str, value: str | int | float):
        try:
            result = [row for row in self.file_content if row[column] == value]
            self._print_table(result)
        except KeyError:
            print('Указан некорректный столбец для аргумента --where')
            exit()


    def filter_less_than(self, column: str, value: str | int | float):
        try:
            result = [row for row in self.file_content if row[column] < value]
            self._print_table(result)
        except KeyError:
            print(f'Указан некорректный столбец для аргумента --where: "{column}"')
            exit()
        except TypeError:
            print(f'Указано некорректное значение для аргумента --where: "{value}"')
            exit()



    def filter_greater_than(self, column: str, value: str | int | float):
        try:
            result = [row for row in self.file_content if row[column] > value]
            self._print_table(result)
        except KeyError:
            print(f'Указан некорректный столбец для аргумента --where: "{column}"')
            exit()
        except TypeError:
            print(f'Указано некорректное значение для аргумента --where: "{value}"')
            exit()

    def aggregate_min(self, column: str):
        try:
            min_row = min(self.file_content, key=lambda row: row[column])
            result = [
                {"min": min_row[column]}
            ]
            self._print_table(result)
        except KeyError:
            print(f'Указан некорректный столбец для аргумента --aggregate: "{column}"')
            exit()


    def aggregate_max(self, column: str):
        try:
            max_row = max(self.file_content, key=lambda row: row[column])
            result = [
                {"max": max_row[column]}
            ]
            self._print_table(result)
        except KeyError:
            print(f'Указан некорректный столбец для аргумента --aggregate: "{column}"')
            exit()


    def aggregate_avg(self, column: str):
        try:
            result = [
                {"avg": statistics.mean([row[column] for row in self.file_content])}
            ]
            self._print_table(result)
        except KeyError:
            print(f'Указан некорректный столбец для аргумента --aggregate: "{column}"')
            exit()


    def order_by_asc(self, column: str):
        try:
            result = sorted(self.file_content, key=lambda row: row[column], reverse=False)
            self._print_table(result)
        except KeyError:
            print(f'Указан некорректный столбец для аргумента --order-by: "{column}"')
            exit()


    def order_by_desc(self, column: str):
        try:
            result = sorted(self.file_content, key=lambda row: row[column], reverse=True)
            self._print_table(result)
        except KeyError:
            print(f'Указан некорректный столбец для аргумента --order-by: "{column}"')
            exit()


def where(processing_csv_file: ProcessingCsvFile, args: Namespace):
    _functions = {
        "<": processing_csv_file.filter_less_than,
        ">": processing_csv_file.filter_greater_than,
        "=": processing_csv_file.filter_equal
    }
    _err_message = 'Некорректное условие в аргументе --where. Пример: --where "column_name=value"'

    try:
        for operator in _functions:
            if operator in args.where:
                column, value = args.where.split(operator)
                value = processing_csv_file.convert_to_numeric(value)
                _functions[operator](column, value)
                break
        else:
            print(_err_message)
    except ValueError:
        print(_err_message)


def aggregate(processing_csv_file: ProcessingCsvFile, args: Namespace):
    _functions = {
        "min": processing_csv_file.aggregate_min,
        "max": processing_csv_file.aggregate_max,
        "avg": processing_csv_file.aggregate_avg
    }
    _err_message = 'Некорректное условие в аргументе --aggregate. Пример: --aggregate "column_name=max"'

    try:
        column, method = args.aggregate.split("=")
        _functions[method](column)
    except ValueError:
        print(_err_message)
    except KeyError:
        print('Некорректный способ агрегации. Используйте "min", "max" или "avg"')


def order_by(processing_csv_file: ProcessingCsvFile, args: Namespace):
    _functions = {
        "asc": processing_csv_file.order_by_asc,
        "desc": processing_csv_file.order_by_desc
    }
    _err_message = 'Некорректное условие в аргументе --order-by. Пример: --order-by "column_name=desc"'

    try:
        column, method = args.order_by.split("=")
        _functions[method](column)
    except ValueError:
        print(_err_message)
    except KeyError:
        print('Некорректный способ сортировки. Используйте "asc" или "desc"')


def main():
    processing_csv_file = ProcessingCsvFile()
    args = processing_csv_file.args

    if args.file is None:
        print("Не указан путь к файлу")

    if args.where:
        where(processing_csv_file, args)
    elif args.aggregate:
        aggregate(processing_csv_file, args)
    elif args.order_by:
        order_by(processing_csv_file, args)

    elif args.file:
        print(args.file)
        processing_csv_file.print_file_content()




if __name__ == "__main__":
    main()
