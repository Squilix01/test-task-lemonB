import csv
import io


COLUMN_ALIASES = {
    "name": ["name", "назва", "название", "title", "product_name"],
    "category": ["category", "категорія", "категория"],
    "price": ["price", "ціна", "цена"],
    "rating": ["rating", "рейтинг"],
    "number_of_reviews": ["number_of_reviews", "reviews", "відгуки", "отзывы", "кількість відгуків"],
    "keywords": ["keywords", "ключові слова", "ключевые слова", "tags", "теги"],
    "product_url": ["product_url", "url", "link", "посилання", "ссылка"],
    "image_url": ["image_url", "image", "photo", "фото", "зображення"],
}


def parse_sales_csv(content: str) -> list[dict]:
    # Remove BOM if present
    content = content.lstrip("\ufeff")
    reader = csv.DictReader(io.StringIO(content))

    if not reader.fieldnames:
        raise ValueError("CSV файл пустий або не має заголовків.")

    # Build header mapping
    header_map = {}
    for raw_header in reader.fieldnames:
        clean = raw_header.strip().lower()
        for canonical, aliases in COLUMN_ALIASES.items():
            if clean in aliases:
                header_map[raw_header] = canonical
                break

    # Verify required columns exist
    mapped_canonical = set(header_map.values())
    if "name" not in mapped_canonical or "category" not in mapped_canonical or "price" not in mapped_canonical:
        raise ValueError("У CSV відсутні обов'язкові колонки: name (назва), category (категорія), price (ціна).")

    items = []
    for row in reader:
        item = {
            "name": "",
            "category": "",
            "price": 0.0,
            "rating": 0.0,
            "number_of_reviews": 0,
            "keywords": "",
            "product_url": "",
            "image_url": "",
        }

        for raw_header, val in row.items():
            canonical = header_map.get(raw_header)
            if not canonical or val is None:
                continue
            val_clean = val.strip()

            if canonical == "price":
                try:
                    cleaned_num = val_clean.replace("$", "").replace(",", "")
                    item["price"] = max(0.0, float(cleaned_num)) if cleaned_num else 0.0
                except ValueError:
                    item["price"] = 0.0
            elif canonical == "rating":
                try:
                    item["rating"] = float(val_clean) if val_clean else 0.0
                except ValueError:
                    item["rating"] = 0.0
            elif canonical == "number_of_reviews":
                try:
                    cleaned_rev = val_clean.replace(",", "").replace(".", "")
                    item["number_of_reviews"] = int(cleaned_rev) if cleaned_rev else 0
                except ValueError:
                    item["number_of_reviews"] = 0
            else:
                item[canonical] = val_clean

        if item["name"] and item["category"]:
            items.append(item)

    if not items:
        raise ValueError("CSV файл не містить валідних рядків даних.")

    return items
