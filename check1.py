import json


def main():
    try:
        with open('scraped_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        by_source = {}

        for r in data:
            key = r.get('source', 'unknown')

            if key not in by_source:
                by_source[key] = {'total': 0, 'with_price': 0}

            by_source[key]['total'] += 1

            if r.get('price'):
                by_source[key]['with_price'] += 1

        for source, stats in by_source.items():
            total = stats['total']
            with_price = stats['with_price']
            pct = (with_price / total * 100) if total > 0 else 0

            print(f"{source:12} → {with_price}/{total} have price ({pct:.0f}%)")

    except FileNotFoundError:
        print("Error: scraped_data.json not found.")
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()