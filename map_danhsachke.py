import json
from pathlib import Path

file1 = Path("danh_sach_ke.json")
file2 = Path("map_data.json")
output = Path("merged.json")

with file1.open("r", encoding="utf-8") as f:
    data1 = json.load(f)

with file2.open("r", encoding="utf-8") as f:
    data2 = json.load(f)

if isinstance(data1, dict) and isinstance(data2, dict):
    merged = {**data1, **data2}
elif isinstance(data1, list) and isinstance(data2, list):
    merged = data1 + data2
else:
    merged = {
        "danh_sach_ke": data1,
        "map_data": data2
    }

with output.open("w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print("Đã tạo merged.json")