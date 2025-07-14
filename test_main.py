from argparse import Namespace

import pytest
from pytest import CaptureFixture

from main import main


class ExpectedResult:
    WITHOUT_ARGUMENTS = [
        {"name": "iphone 15 pro", "brand": "apple", "price": 999, "rating": 4.9},
        {"name": "galaxy s23 ultra", "brand": "samsung", "price": 1199, "rating": 4.8},
        {"name": "redmi note 12", "brand": "xiaomi", "price": 199, "rating": 4.6},
        {"name": "iphone 14", "brand": "apple", "price": 799, "rating": 4.7},
        {"name": "galaxy a54", "brand": "samsung", "price": 349, "rating": 4.2},
        {"name": "poco x5 pro", "brand": "xiaomi", "price": 299, "rating": 4.4},
        {"name": "iphone se", "brand": "apple", "price": 429, "rating": 4.1},
        {"name": "galaxy z flip 5", "brand": "samsung", "price": 999, "rating": 4.6},
        {"name": "redmi 10c", "brand": "xiaomi", "price": 149, "rating": 4.1},
        {"name": "iphone 13 mini", "brand": "apple", "price": 599, "rating": 4.5}
    ]


    WHERE_PRICE_LESS_400 = [
        {"name": "redmi note 12", "brand": "xiaomi", "price": 199, "rating": 4.6},
        {"name": "galaxy a54", "brand": "samsung", "price": 349, "rating": 4.2},
        {"name": "poco x5 pro", "brand": "xiaomi", "price": 299, "rating": 4.4},
        {"name": "redmi 10c", "brand": "xiaomi", "price": 149, "rating": 4.1}
    ]

    WHERE_PRICE_GREATER_400 = [
        {"name": "iphone 15 pro", "brand": "apple", "price": 999, "rating": 4.9},
        {"name": "galaxy s23 ultra", "brand": "samsung", "price": 1199, "rating": 4.8},
        {"name": "iphone 14", "brand": "apple", "price": 799, "rating": 4.7},
        {"name": "iphone se", "brand": "apple", "price": 429, "rating": 4.1},
        {"name": "galaxy z flip 5", "brand": "samsung", "price": 999, "rating": 4.6},
        {"name": "iphone 13 mini", "brand": "apple", "price": 599, "rating": 4.5}
    ]

    WHERE_PRICE_EQUAL_999 = [
        {"name": "iphone 15 pro", "brand": "apple", "price": 999, "rating": 4.9},
        {"name": "galaxy z flip 5", "brand": "samsung", "price": 999, "rating": 4.6}
    ]

    AGGREGATE_RATING_MIN = [{"min": 4.1}]

    AGGREGATE_RATING_MAX = [{"max": 4.9}]

    AGGREGATE_RATING_AVG = [{"avg": 4.49}]

    ORDER_BY_BRAND_ASC = [
        {"name": "iphone 15 pro", "brand": "apple", "price": 999, "rating": 4.9},
        {"name": "iphone 14", "brand": "apple", "price": 799, "rating": 4.7},
        {"name": "iphone se", "brand": "apple", "price": 429, "rating": 4.1},
        {"name": "iphone 13 mini", "brand": "apple", "price": 599, "rating": 4.5},
        {"name": "galaxy s23 ultra", "brand": "samsung", "price": 1199, "rating": 4.8},
        {"name": "galaxy a54", "brand": "samsung", "price": 349, "rating": 4.2},
        {"name": "galaxy z flip 5", "brand": "samsung", "price": 999, "rating": 4.6},
        {"name": "redmi note 12", "brand": "xiaomi", "price": 199, "rating": 4.6},
        {"name": "poco x5 pro", "brand": "xiaomi", "price": 299, "rating": 4.4},
        {"name": "redmi 10c", "brand": "xiaomi", "price": 149, "rating": 4.1}
    ]

    ORDER_BY_BRAND_DESC = [
        {"name": "redmi note 12", "brand": "xiaomi", "price": 199, "rating": 4.6},
        {"name": "poco x5 pro", "brand": "xiaomi", "price": 299, "rating": 4.4},
        {"name": "redmi 10c", "brand": "xiaomi", "price": 149, "rating": 4.1},
        {"name": "galaxy s23 ultra", "brand": "samsung", "price": 1199, "rating": 4.8},
        {"name": "galaxy a54", "brand": "samsung", "price": 349, "rating": 4.2},
        {"name": "galaxy z flip 5", "brand": "samsung", "price": 999, "rating": 4.6},
        {"name": "iphone 15 pro", "brand": "apple", "price": 999, "rating": 4.9},
        {"name": "iphone 14", "brand": "apple", "price": 799, "rating": 4.7},
        {"name": "iphone se", "brand": "apple", "price": 429, "rating": 4.1},
        {"name": "iphone 13 mini", "brand": "apple", "price": 599, "rating": 4.5}
    ]

    ERR_MESSAGE_INVALID_PRICE = 'Указан некорректный столбец для аргумента --where: "invalid_price"'
    ERR_MESSAGE_INVALID_RATING = 'Указан некорректный столбец для аргумента --aggregate: "invalid_rating"'
    ERR_MESSAGE_INVALID_BRAND = 'Указан некорректный столбец для аргумента --order-by: "invalid_brand"'


class TData:
    FILE_NAME = "products.csv"

    WITHOUT_ARGUMENTS = None
    ARGUMENT_WHERE_PRICE_LESS_400 = ("where", "price<400")
    ARGUMENT_WHERE_PRICE_GREATER_400 = ("where", "price>400")
    ARGUMENT_WHERE_PRICE_EQUAL_999 = ("where", "price=999")
    ARGUMENT_AGGREGATE_RATING_MIN = ("aggregate", "rating=min")
    ARGUMENT_AGGREGATE_RATING_MAX = ("aggregate", "rating=max")
    ARGUMENT_AGGREGATE_RATING_AVG = ("aggregate", "rating=avg")
    ARGUMENT_ORDER_BY_BRAND_ASC = ("order_by", "brand=asc")
    ARGUMENT_ORDER_BY_BRAND_DESC = ("order_by", "brand=desc")

    ARGUMENT_WHERE_INVALID_PRICE_LESS_400 = ("where", "invalid_price<400")
    ARGUMENT_WHERE_INVALID_PRICE_GREATER_400 = ("where", "invalid_price>400")
    ARGUMENT_WHERE_INVALID_PRICE_EQUAL_999 = ("where", "invalid_price=999")
    ARGUMENT_AGGREGATE_INVALID_RATING_MIN = ("aggregate", "invalid_rating=min")
    ARGUMENT_AGGREGATE_INVALID_RATING_MAX = ("aggregate", "invalid_rating=max")
    ARGUMENT_AGGREGATE_INVALID_RATING_AVG = ("aggregate", "invalid_rating=avg")
    ARGUMENT_ORDER_BY_INVALID_BRAND_ASC = ("order_by", "invalid_brand=asc")
    ARGUMENT_ORDER_BY_INVALID_BRAND_DESC = ("order_by", "invalid_brand=desc")

file_name = "products.csv"
valid_data = [
    {
        "description": "without arguments",
        "argument": TData.WITHOUT_ARGUMENTS,
        "expected_result": ExpectedResult.WITHOUT_ARGUMENTS
    },
    {
        "description": "where price<400",
        "argument": TData.ARGUMENT_WHERE_PRICE_LESS_400,
        "expected_result": ExpectedResult.WHERE_PRICE_LESS_400
    },
    {
        "description": "where price>400",
        "argument": TData.ARGUMENT_WHERE_PRICE_GREATER_400,
        "expected_result": ExpectedResult.WHERE_PRICE_GREATER_400},
    {
        "description": "where price=999",
        "argument": TData.ARGUMENT_WHERE_PRICE_EQUAL_999,
        "expected_result": ExpectedResult.WHERE_PRICE_EQUAL_999},
    {
        "description": "aggregate rating=min",
        "argument": TData.ARGUMENT_AGGREGATE_RATING_MIN,
        "expected_result": ExpectedResult.AGGREGATE_RATING_MIN},
    {
        "description": "aggregate rating=max",
        "argument": TData.ARGUMENT_AGGREGATE_RATING_MAX,
        "expected_result": ExpectedResult.AGGREGATE_RATING_MAX},
    {
        "description": "aggregate rating=avg",
        "argument": TData.ARGUMENT_AGGREGATE_RATING_AVG,
        "expected_result": ExpectedResult.AGGREGATE_RATING_AVG},
    {
        "description": "order_by brand=asc",
        "argument": TData.ARGUMENT_ORDER_BY_BRAND_ASC,
        "expected_result": ExpectedResult.ORDER_BY_BRAND_ASC},
    {
        "description": "order_by brand=desc",
        "argument": TData.ARGUMENT_ORDER_BY_BRAND_DESC,
        "expected_result": ExpectedResult.ORDER_BY_BRAND_DESC}
]

invalid_columns = [
    {
        "description": "where invalid_price<400",
        "argument": TData.ARGUMENT_WHERE_INVALID_PRICE_LESS_400,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_PRICE
    },
    {
        "description": "where invalid_price>400",
        "argument": TData.ARGUMENT_WHERE_INVALID_PRICE_GREATER_400,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_PRICE
    },
    {
        "description": "where invalid_price=999",
        "argument": TData.ARGUMENT_WHERE_INVALID_PRICE_EQUAL_999,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_PRICE
    },
    {
        "description": "aggregate invalid_rating=min",
        "argument": TData.ARGUMENT_AGGREGATE_INVALID_RATING_MIN,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_RATING
    },
    {
        "description": "aggregate invalid_rating=max",
        "argument": TData.ARGUMENT_AGGREGATE_INVALID_RATING_MAX,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_RATING
    },
    {
        "description": "aggregate invalid_rating=avg",
        "argument": TData.ARGUMENT_AGGREGATE_INVALID_RATING_AVG,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_RATING
    },
    {
        "description": "order_by invalid_brand=asc",
        "argument": TData.ARGUMENT_ORDER_BY_INVALID_BRAND_ASC,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_BRAND
    },
    {
        "description": "order_by invalid_brand=desc",
        "argument": TData.ARGUMENT_ORDER_BY_INVALID_BRAND_DESC,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_BRAND
    }
]


class TestProcessingCsvFile:

    @pytest.mark.parametrize("data", valid_data)
    def test_valid_data(self, data):
        actual_result = main(file_name=TData.FILE_NAME, argument=data["argument"])
        expected_result = data["expected_result"]

        err_text = f"В тесте {data["description"]} \nфактический результат: \n{actual_result} \nне совпадает с ожидаемым: \n{expected_result}"

        assert actual_result == expected_result, err_text

    @pytest.mark.parametrize("data", invalid_columns)
    def test_invalid_columns(self, data, capsys: pytest.CaptureFixture[str]):
        try:
            actual_result = main(file_name=TData.FILE_NAME, argument=data["argument"])
        except:
            pass
        expected_result = data["expected_result"]

        err_text = f"В тесте {data["description"]} \nфактический результат: \n{actual_result} \nне совпадает с ожидаемым: \n{expected_result}"

        assert actual_result == expected_result, err_text
