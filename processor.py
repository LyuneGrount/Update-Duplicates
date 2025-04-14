# processor.py
import re
from collections import Counter, defaultdict

def process_chunk(chunk, bin_db):
    """Process a chunk of cards and group by BIN"""
    # Debug: In mẫu dữ liệu đầu vào
    print(f"Sample input (first 5): {chunk[:5]}")

    # Biểu thức chính quy để kiểm tra định dạng: card|mm|yy|cvv
    pattern = re.compile(r'^(\d{14,16})\|(\d{1,2})\|(\d{1,4})\|(\d{3,4})$')

    bin_groups = defaultdict(list)
    not_found = []
    bin_count = Counter()

    for card in chunk:
        card = card.strip()
        match = pattern.match(card)
        if not match:
            bin_groups["invalid"].append(f"{card} | Invalid format!")
            continue

        card_number, month, year, cvv = match.groups()
        # Kiểm tra dữ liệu
        if not (len(card_number) >= 14 and 1 <= int(month) <= 12 and len(cvv) in (3, 4)):
            bin_groups["invalid"].append(f"{card} | Invalid data!")
            continue

        bin_num = card_number[:6]
        bin_info = bin_db.get(bin_num, "No BIN info found")
        bin_groups[bin_num].append(f"{card} | {bin_info}")

        if bin_info == "No BIN info found":
            not_found.append(card)
        bin_count[bin_num] += 1

    return dict(bin_groups), not_found, dict(bin_count)