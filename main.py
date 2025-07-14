import argparse
import csv
import statistics
from argparse import Namespace
from typing import Callable

from tabulate import tabulate


class ProcessingCsvFile:

    def __init__(
            self,
            arguments: Namespace | None = None,
            delimiter: str = ",",
            quotechar: str = '"'
    ):

        self._delimiter = delimiter
        self._quotechar = quotechar

        self._parser = argparse.ArgumentParser()

        if arguments is not None:
            self._args = self._parse_args(arguments)
        else:
            self._args = self._parse_args_from_console()
        self._file_content = self._read_file()

    @property
    def options(self) -> dict[str, Callable]:
        return {
            "where": self._where,
            "aggregate": self._aggregate,
            "order_by": self._order_by
        }

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
    def args(self) -> Namespace:
        return self._args


    @property
    def file_name(self):
        return self.args.file


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


    def _read_file(self):
        if not hasattr(self.args, "file") or self.args.file is None:
            _err_message = 'Не указан путь к файлу. Пример: "--file file_path"'
            print(_err_message)
            exit()
        else:
            self._file_name = self.args.file
        try:
            with open(self.file_name, encoding='utf-8') as file:
                rows = csv.DictReader(file, delimiter=self.delimiter, quotechar=self.quotechar)
                return [{key: self.convert_to_numeric(value) for key, value in row.items()} for row in rows]
        except FileNotFoundError:
            _err_message = 'Введен некорректный путь к файлу. Пример: "--file file_path"'
            print(_err_message)
            exit()


    def _parse_args(self, arguments: Namespace):
        print(vars(arguments))
        self._parser.parse_args([])
        return arguments


    def _parse_args_from_console(self):
        self._parser.add_argument("--file", type=str, help='Путь к файлу. Пример: "--file file_path')
        self._parser.add_argument("--where", type=str, help='Условие фильтрации. Пример: --where "column_name=value"')
        self._parser.add_argument("--aggregate", type=str, help='Способ агрегации. Пример: --aggregate "column_name=max"')
        self._parser.add_argument("--order-by", type=str, help='Способ сортировки. Пример: --order-by "column_name=desc"')

        return self._parser.parse_args()


    def _change_arg(self, arg: tuple[str, str]):
        option, value = arg
        if hasattr(self.args, option):
            setattr(self.args, option, value)
        else:
            _err_message = f"Аргумент {arg} задан неверно"
            print(_err_message)
            return _err_message


    def print_file_content(self):
        self._print_table(self.file_content)
        return self.file_content


    def _filter_equal(self, column: str, value: str | int | float):
        try:
            result = [row for row in self.file_content if row[column] == value]
            self._print_table(result)
            return result
        except KeyError:
            _err_message = f'Указан некорректный столбец для аргумента --where: "{column}"'
            print(_err_message)
            return _err_message



    def _filter_less_than(self, column: str, value: str | int | float):
        try:
            result = [row for row in self.file_content if row[column] < value]
            self._print_table(result)
            return result
        except KeyError:
            _err_message = f'Указан некорректный столбец для аргумента --where: "{column}"'
            print(_err_message)
            return _err_message
        except TypeError:
            _err_message = f'Указано некорректное значение для аргумента --where: "{value}"'
            print(_err_message)
            return _err_message


    def _filter_greater_than(self, column: str, value: str | int | float):
        try:
            result = [row for row in self.file_content if row[column] > value]
            self._print_table(result)
            return result
        except KeyError:
            _err_message = f'Указан некорректный столбец для аргумента --where: "{column}"'
            print(_err_message)
            return _err_message
        except TypeError:
            _err_message = f'Указано некорректное значение для аргумента --where: "{value}"'
            print(_err_message)
            return _err_message


    def _aggregate_min(self, column: str):
        try:
            min_row = min(self.file_content, key=lambda row: row[column])
            result = [
                {"min": min_row[column]}
            ]
            self._print_table(result)
            return result
        except KeyError:
            _err_message = f'Указан некорректный столбец для аргумента --aggregate: "{column}"'
            print(_err_message)
            return _err_message


    def _aggregate_max(self, column: str):
        try:
            max_row = max(self.file_content, key=lambda row: row[column])
            result = [
                {"max": max_row[column]}
            ]
            self._print_table(result)
            return result
        except KeyError:
            _err_message = f'Указан некорректный столбец для аргумента --aggregate: "{column}"'
            print(_err_message)
            return _err_message

    def _aggregate_avg(self, column: str):
        try:
            result = [
                {"avg": statistics.mean([row[column] for row in self.file_content])}
            ]
            self._print_table(result)
            return result
        except KeyError:
            _err_message = f'Указан некорректный столбец для аргумента --aggregate: "{column}"'
            print(_err_message)
            return _err_message


    def _order_by_asc(self, column: str):
        try:
            result = sorted(self.file_content, key=lambda row: row[column], reverse=False)
            self._print_table(result)
            return result
        except KeyError:
            _err_message = f'Указан некорректный столбец для аргумента --order-by: "{column}"'
            print(_err_message)
            return _err_message


    def _order_by_desc(self, column: str):
        try:
            result = sorted(self.file_content, key=lambda row: row[column], reverse=True)
            self._print_table(result)
            return result
        except KeyError:
            _err_message = f'Указан некорректный столбец для аргумента --order-by: "{column}"'
            print(_err_message)
            return _err_message


    def _where(self):
        _options: dict[str, Callable] = {
            "<": self._filter_less_than,
            ">": self._filter_greater_than,
            "=": self._filter_equal
        }
        _err_message = 'Некорректное условие в аргументе --where. Пример: --where "column_name=value"'

        try:
            for operator in _options:
                if operator in self.args.where:
                    column, value = self.args.where.split(operator)
                    value = self.convert_to_numeric(value)
                    return _options[operator](column, value)
            else:
                print(_err_message)
                return _err_message
        except ValueError:
            print(_err_message)
            return _err_message


    def _aggregate(self):
        _options: dict[str, Callable] = {
            "min": self._aggregate_min,
            "max": self._aggregate_max,
            "avg": self._aggregate_avg
        }
        _value_err_message = 'Некорректное условие в аргументе --aggregate. Пример: --aggregate "column_name=max"'
        _key_err_message = 'Некорректный способ агрегации. Используйте "min", "max" или "avg"'

        try:
            column, method = self.args.aggregate.split("=")
            return _options[method](column)
        except ValueError:
            print(_value_err_message)
            return _value_err_message
        except KeyError:
            print(_key_err_message)
            return _key_err_message



    def _order_by(self):
        _options: dict[str, Callable] = {
            "asc": self._order_by_asc,
            "desc": self._order_by_desc
        }
        _value_err_message = 'Некорректное условие в аргументе --order-by. Пример: --order-by "column_name=desc"'
        _key_err_message = 'Некорректный способ сортировки. Используйте "asc" или "desc"'

        try:
            column, method = self.args.order_by.split("=")
            return _options[method](column)
        except ValueError:
            print(_value_err_message)
            return _value_err_message
        except KeyError:
            print(_key_err_message)
            return _key_err_message

    def process_csv_file(self):
        args_without_file = {k: v for k, v in vars(self.args).items() if k != "file"}

        if all(map(lambda i: args_without_file[i] is None, args_without_file.keys())):
            return  self.print_file_content()
        else:
            for option, value in args_without_file.items():
                if value is not None:
                    return self.options[option]()
            return None


def main(arguments: Namespace | None = None):
    processing_csv_file = ProcessingCsvFile(arguments=arguments)
    return processing_csv_file.process_csv_file()


if __name__ == "__main__":
    main()
