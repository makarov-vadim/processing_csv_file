import argparse
import csv
import statistics

from tabulate import tabulate


class ProcessingCsvFile:
    def __init__(self, file_name: str, delimiter: str = ",", quotechar: str = '"'):
        with open(file_name, encoding='utf-8') as file:
            rows = csv.DictReader(file, delimiter=delimiter, quotechar=quotechar)
            self._file_content = [{key: self._convert_to_numeric(value) for key, value in row.items()} for row in rows]

    @property
    def file_content(self):
        return self._file_content

    @staticmethod
    def _convert_to_numeric(value: str):
        try:
            result = float(value)
            assert str(result) == value
        except AssertionError:
            result = int(value)
        except ValueError:
            result = value

        return result

    def filter_equal(self, column: str, value: str | int | float):
        return [row for row in self.file_content if row.get(column) == value]

    def filter_less_than(self, column: str, value: str | int | float):
        return [row for row in self.file_content if row.get(column) < value]

    def filter_greater_than(self, column: str, value: str | int | float):
        return [row for row in self.file_content if row.get(column) > value]

    def aggregate_min(self, column: str):

        return min(self.file_content, key=lambda row: row.get(column))

    def aggregate_max(self, column: str):
        return max(self.file_content, key=lambda row: row.get(column))

    def aggregate_avg(self, column: str):
        return statistics.mean([row.get(column) for row in self.file_content])

    def order_by(self, column: str, method: str = "asc"):
        _reverse = {
            "asc": False,
            "desc": True
        }

        return sorted(self.file_content, key=lambda row: row.get(column), reverse=_reverse.get(method))


if __name__ == "__main__":
    # file_n_1 = "products.csv"
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="Путь к файлу")
    parser.add_argument("--where", type=str, help='Условие фильтрации. Пример: --where "column_name=value"')
    parser.add_argument("--aggregate", type=str, help='Способ агрегации. Пример: --aggregate "column_name=max"')
    parser.add_argument("--order-by", type=str, help='Способ сортировки. Пример: --order-by "column_name=desc"')

    args = parser.parse_args()
    # print(args)

    processing_csv_file = ProcessingCsvFile(args.file)
    if args.where:
        if "<" in args.where:
            column, value = args.where.split("<")
            print(processing_csv_file.filter_less_than(column=column, value=value))
        elif ">" in args.where:
            column, value = args.where.split(">")
            print(processing_csv_file.filter_greater_than(column=column, value=value))
        elif "=" in args.where:
            column, value = args.where.split("=")
            print((processing_csv_file.filter_equal(column=column, value=value)))

    elif args.aggregate:
        column, method = args.aggregate.split("=")
        if method == "min":
            print(processing_csv_file.aggregate_min(column=column))
        elif method == "max":
            print(processing_csv_file.aggregate_max(column=column))
        elif method == "avg":
            print(processing_csv_file.aggregate_avg(column=column))

    elif args.order_by:
        column, method = args.order_by.split("=")
        print(processing_csv_file.order_by(column=column, method=method))

    elif args.file:
        print(processing_csv_file.file_content)


    # column_2 = "price"
    #
    # order_by_1 = processing_csv_file.order_by(column=column_2, method="asc")
    # order_by_2 = processing_csv_file.order_by(column=column_2, method="desc")
    #
    # print(tabulate(order_by_1, headers="keys", tablefmt="psql"))
    # print(tabulate(order_by_2, headers="keys", tablefmt="psql"))

