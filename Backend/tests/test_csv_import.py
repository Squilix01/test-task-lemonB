from services.csv_import import parse_sales_csv


def test_parse_csv_english_headers():
    csv_text = """name,category,price,rating,reviews,keywords
Apple AirPods Pro 2,Electronics,249.00,4.8,125000,apple airpods wireless bluetooth
Hydro Flask Water Bottle,Sports & Outdoors,44.95,4.7,45000,hydro flask bottle insulated water
"""
    items = parse_sales_csv(csv_text)
    assert len(items) == 2
    assert items[0]["name"] == "Apple AirPods Pro 2"
    assert items[0]["category"] == "Electronics"
    assert items[0]["price"] == 249.00
    assert items[0]["rating"] == 4.8
    assert items[0]["number_of_reviews"] == 125000
    assert "apple" in items[0]["keywords"]


def test_parse_csv_ukrainian_headers():
    csv_text = """назва,категорія,ціна,рейтинг,відгуки,ключові слова
Бездротові навушники,Електроніка,89.99,4.6,8400,навушники бездротові bluetooth
"""
    items = parse_sales_csv(csv_text)
    assert len(items) == 1
    assert items[0]["name"] == "Бездротові навушники"
    assert items[0]["category"] == "Електроніка"
    assert items[0]["price"] == 89.99
    assert items[0]["number_of_reviews"] == 8400


def test_parse_csv_invalid_rows():
    csv_text = """name,category,price
,Empty Name,10.00
Valid Item,Electronics,-5.00
"""
    items = parse_sales_csv(csv_text)
    # Empty name should be skipped
    assert len(items) == 1
    assert items[0]["name"] == "Valid Item"
    assert items[0]["price"] == 0.0  # negative price normalized to 0.0


if __name__ == "__main__":
    test_parse_csv_english_headers()
    test_parse_csv_ukrainian_headers()
    test_parse_csv_invalid_rows()
    print("✅ test_csv_import.py passed!")
