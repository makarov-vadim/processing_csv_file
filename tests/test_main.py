from argparse import Namespace

import pytest

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
    FILE_NAME = "exemple/products.csv"

    ARGUMENT_ONLY_FILE = Namespace(**{"file": FILE_NAME})
    ARGUMENTS_WHERE_PRICE_LESS_400 = Namespace(**{"file": FILE_NAME, "where": "price<400"})
    ARGUMENTS_WHERE_PRICE_GREATER_400 = Namespace(**{"file": FILE_NAME, "where": "price>400"})
    ARGUMENTS_WHERE_PRICE_EQUAL_999 = Namespace(**{"file": FILE_NAME, "where": "price=999"})
    ARGUMENTS_AGGREGATE_RATING_MIN = Namespace(**{"file": FILE_NAME, "aggregate": "rating=min"})
    ARGUMENTS_AGGREGATE_RATING_MAX = Namespace(**{"file": FILE_NAME, "aggregate": "rating=max"})
    ARGUMENTS_AGGREGATE_RATING_AVG = Namespace(**{"file": FILE_NAME, "aggregate": "rating=avg"})
    ARGUMENTS_ORDER_BY_BRAND_ASC = Namespace(**{"file": FILE_NAME, "order_by": "brand=asc"})
    ARGUMENTS_ORDER_BY_BRAND_DESC = Namespace(**{"file": FILE_NAME, "order_by": "brand=desc"})

    ARGUMENTS_WHERE_INVALID_PRICE_LESS_400 = Namespace(**{"file": FILE_NAME, "where": "invalid_price<400"})
    ARGUMENTS_WHERE_INVALID_PRICE_GREATER_400 = Namespace(**{"file": FILE_NAME, "where": "invalid_price>400"})
    ARGUMENTS_WHERE_INVALID_PRICE_EQUAL_999 = Namespace(**{"file": FILE_NAME, "where": "invalid_price=999"})
    ARGUMENTS_AGGREGATE_INVALID_RATING_MIN = Namespace(**{"file": FILE_NAME, "aggregate": "invalid_rating=min"})
    ARGUMENTS_AGGREGATE_INVALID_RATING_MAX = Namespace(**{"file": FILE_NAME, "aggregate": "invalid_rating=max"})
    ARGUMENTS_AGGREGATE_INVALID_RATING_AVG = Namespace(**{"file": FILE_NAME, "aggregate": "invalid_rating=avg"})
    ARGUMENTS_ORDER_BY_INVALID_BRAND_ASC = Namespace(**{"file": FILE_NAME, "order_by": "invalid_brand=asc"})
    ARGUMENTS_ORDER_BY_INVALID_BRAND_DESC = Namespace(**{"file": FILE_NAME, "order_by": "invalid_brand=desc"})


valid_data = [
    {
        "description": "argument only file",
        "argument": TData.ARGUMENT_ONLY_FILE,
        "expected_result": ExpectedResult.WITHOUT_ARGUMENTS
    },
    {
        "description": "where price<400",
        "argument": TData.ARGUMENTS_WHERE_PRICE_LESS_400,
        "expected_result": ExpectedResult.WHERE_PRICE_LESS_400
    },
    {
        "description": "where price>400",
        "argument": TData.ARGUMENTS_WHERE_PRICE_GREATER_400,
        "expected_result": ExpectedResult.WHERE_PRICE_GREATER_400},
    {
        "description": "where price=999",
        "argument": TData.ARGUMENTS_WHERE_PRICE_EQUAL_999,
        "expected_result": ExpectedResult.WHERE_PRICE_EQUAL_999},
    {
        "description": "aggregate rating=min",
        "argument": TData.ARGUMENTS_AGGREGATE_RATING_MIN,
        "expected_result": ExpectedResult.AGGREGATE_RATING_MIN},
    {
        "description": "aggregate rating=max",
        "argument": TData.ARGUMENTS_AGGREGATE_RATING_MAX,
        "expected_result": ExpectedResult.AGGREGATE_RATING_MAX},
    {
        "description": "aggregate rating=avg",
        "argument": TData.ARGUMENTS_AGGREGATE_RATING_AVG,
        "expected_result": ExpectedResult.AGGREGATE_RATING_AVG},
    {
        "description": "order_by brand=asc",
        "argument": TData.ARGUMENTS_ORDER_BY_BRAND_ASC,
        "expected_result": ExpectedResult.ORDER_BY_BRAND_ASC},
    {
        "description": "order_by brand=desc",
        "argument": TData.ARGUMENTS_ORDER_BY_BRAND_DESC,
        "expected_result": ExpectedResult.ORDER_BY_BRAND_DESC}
]

invalid_columns = [
    {
        "description": "where invalid_price<400",
        "argument": TData.ARGUMENTS_WHERE_INVALID_PRICE_LESS_400,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_PRICE
    },
    {
        "description": "where invalid_price>400",
        "argument": TData.ARGUMENTS_WHERE_INVALID_PRICE_GREATER_400,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_PRICE
    },
    {
        "description": "where invalid_price=999",
        "argument": TData.ARGUMENTS_WHERE_INVALID_PRICE_EQUAL_999,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_PRICE
    },
    {
        "description": "aggregate invalid_rating=min",
        "argument": TData.ARGUMENTS_AGGREGATE_INVALID_RATING_MIN,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_RATING
    },
    {
        "description": "aggregate invalid_rating=max",
        "argument": TData.ARGUMENTS_AGGREGATE_INVALID_RATING_MAX,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_RATING
    },
    {
        "description": "aggregate invalid_rating=avg",
        "argument": TData.ARGUMENTS_AGGREGATE_INVALID_RATING_AVG,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_RATING
    },
    {
        "description": "order_by invalid_brand=asc",
        "argument": TData.ARGUMENTS_ORDER_BY_INVALID_BRAND_ASC,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_BRAND
    },
    {
        "description": "order_by invalid_brand=desc",
        "argument": TData.ARGUMENTS_ORDER_BY_INVALID_BRAND_DESC,
        "expected_result": ExpectedResult.ERR_MESSAGE_INVALID_BRAND
    }
]


class TestProcessingCsvFile:

    @pytest.mark.parametrize("data", valid_data)
    def test_valid_data(self, data):
        actual_result = main(arguments=data["argument"])
        expected_result = data["expected_result"]

        err_text = f"В тесте {data["description"]} \nфактический результат: \n{actual_result} \nне совпадает с ожидаемым: \n{expected_result}"

        assert actual_result == expected_result, err_text

    @pytest.mark.parametrize("data", invalid_columns)
    def test_invalid_columns(self, data):
        try:
            actual_result = main(arguments=data["argument"])
        except:
            pass
        expected_result = data["expected_result"]

        err_text = f"В тесте {data["description"]} \nфактический результат: \n{actual_result} \nне совпадает с ожидаемым: \n{expected_result}"

        assert actual_result == expected_result, err_text
