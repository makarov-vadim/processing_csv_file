from argparse import Namespace

import pytest
from main import main

class CorrectData:
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

file_name = "products.csv"
valid_data = [
    {"description": "without arguments", "argument": None,
     "correct_result": CorrectData.WITHOUT_ARGUMENTS},
    {"description": "where price<400", "argument": ("where", "price<400"),
     "correct_result": CorrectData.WHERE_PRICE_LESS_400},
    {"description": "where price>400", "argument": ("where", "price>400"),
     "correct_result": CorrectData.WHERE_PRICE_GREATER_400},
    {"description": "where price=999", "argument": ("where", "price=999"),
     "correct_result": CorrectData.WHERE_PRICE_EQUAL_999},
    {"description": "aggregate rating=min", "argument": ("aggregate", "rating=min"),
     "correct_result": CorrectData.AGGREGATE_RATING_MIN},
    {"description": "aggregate rating=max", "argument": ("aggregate", "rating=max"),
     "correct_result": CorrectData.AGGREGATE_RATING_MAX},
    {"description": "aggregate rating=avg", "argument": ("aggregate", "rating=avg"),
     "correct_result": CorrectData.AGGREGATE_RATING_AVG},
    {"description": "order_by brand=asc", "argument": ("order_by", "brand=asc"),
     "correct_result": CorrectData.ORDER_BY_BRAND_ASC},
    {"description": "order_by brand=desc", "argument": ("order_by", "brand=desc"),
     "correct_result": CorrectData.ORDER_BY_BRAND_DESC}
]


class TestProcessingCsvFile:

    @pytest.mark.parametrize("data", valid_data)
    def test_valid_data(self, data):
        actual_result = main(file_name=file_name, argument=data["argument"])
        correct_result = data["correct_result"]

        err_text = f"В тесте {data["description"]} \nфактический результат: \n{actual_result} \nне совпадает с ожидаемым: \n{correct_result}"

        assert actual_result == correct_result, err_text
