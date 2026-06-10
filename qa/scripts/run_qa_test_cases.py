from __future__ import annotations

import ast
import csv
import json
import math
import re
import sys
import traceback
from pathlib import Path
from typing import Any


def find_project_root() -> Path:
    #Tìm thư mục gốc của repo để import được các module chính
    start = Path(__file__).resolve().parent
    for folder in [start, *start.parents]:
        if (folder / "MinHeap_Graph.py").exists() or (folder / "qa").exists():
            return folder
    return start


ROOT_DIR = find_project_root()
sys.path.insert(0, str(ROOT_DIR))

QA_DIR = ROOT_DIR / "qa"
TESTCASE_CSV = QA_DIR / "testcases" / "test_cases_dijkstra.csv"
GRAPH_DIR = QA_DIR / "testcases" / "graphs"
RESULTS_DIR = QA_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RESULT_FILE = RESULTS_DIR / "functional_test_results.csv"

try:
    from core.MinHeap_Graph import Graph
    from core.findShortestPath_reconstructPath import findShortestPath
except Exception as import_error:
    print("Fatal: Không import được Graph hoặc findShortestPath từ project.")
    print(f"Project root đang nhận diện: {ROOT_DIR}")
    print("Hãy chạy script từ thư mục gốc repo hoặc đặt script trong qa/scripts.")
    raise import_error


def distance_to_text(distance: Any) -> str:
    try:
        if math.isinf(float(distance)):
            return "inf"
    except Exception:
        pass
    return str(distance)


def path_to_text(path: Any) -> str:
    if path is None:
        return ""
    if isinstance(path, list):
        return " -> ".join(str(x) for x in path)
    return str(path)


def same_distance(actual: Any, expected: Any) -> bool:
    try:
        actual_f = float(actual)
        expected_f = float(expected)
    except Exception:
        return actual == expected

    if math.isinf(actual_f) or math.isinf(expected_f):
        return math.isinf(actual_f) and math.isinf(expected_f)
    return abs(actual_f - expected_f) < 1e-9


def normalize_result(result: Any) -> dict[str, Any]:
    if isinstance(result, dict):
        return {
            "distance": result.get("distance"),
            "path": result.get("path"),
            "raw": result,
        }
    return {"distance": None, "path": None, "raw": result}


def normalize_path(path: Any) -> list[Any]:
    if path is None:
        return []
    if isinstance(path, tuple):
        return list(path)
    if isinstance(path, list):
        return path
    return [path]


def build_graph_from_json(filepath: Path) -> Any:
    with filepath.open(encoding="utf-8") as f:
        data = json.load(f)

    if "edges" not in data:
        raise KeyError(f"{filepath.name} thiếu key 'edges'")

    graph = Graph()

    #Thêm node trước để giữ được node cô lập như TC07
    if hasattr(graph, "addNode"):
        for node in data.get("nodes", []):
            if isinstance(node, dict) and "id" in node:
                graph.addNode(node["id"])

    for edge in data["edges"]:
        graph.addEdge(edge["from"], edge["to"], edge["weight"])

    return graph


TEST_CASES: list[dict[str, Any]] = [
    {
        "id": "TC01", "group": "Happy path", "file": "tc01.json",
        "desc": "Đường ngắn nhất cùng khu C", "source": 1, "dest": 21,
        "expected_distance": 300, "expected_paths": [[1, 13, 3, 2, 21]], "check_path": True,
    },
    {
        "id": "TC02", "group": "Happy path", "file": "tc02.json",
        "desc": "Qua khu C đến cổng Trần Đại Nghĩa", "source": 21, "dest": 12,
        "expected_distance": 360, "expected_paths": [[21, 2, 20, 19, 22, 4, 12]], "check_path": True,
    },
    {
        "id": "TC03", "group": "Happy path", "file": "tc03.json",
        "desc": "Thư viện đến tòa D9, có cạnh trực tiếp", "source": 5, "dest": 11,
        "expected_distance": 220, "expected_paths": [[5, 11]], "check_path": True,
    },
    {
        "id": "TC04", "group": "Happy path", "file": "tc04.json",
        "desc": "Cổng Parabol đến tòa D9", "source": 1, "dest": 11,
        "expected_distance": 470, "expected_paths": [[1, 5, 11]], "check_path": True,
    },
    {
        "id": "TC05", "group": "Happy path", "file": "tc05.json",
        "desc": "Đường dài nhiều hop qua khu C và D", "source": 21, "dest": 16,
        "expected_distance": 610, "expected_paths": [[21, 2, 20, 19, 18, 17, 5, 6, 15, 16]], "check_path": True,
    },
    {
        "id": "TC06", "group": "Edge case", "file": "tc06.json",
        "desc": "Source trùng destination", "source": 5, "dest": 5,
        "expected_distance": 0, "expected_paths": [[5]], "check_path": True,
    },
    {
        "id": "TC07", "group": "Edge case", "file": "tc07.json",
        "desc": "Đồ thị không liên thông, node 99 cô lập", "source": 1, "dest": 99,
        "expected_distance": float("inf"), "expected_paths": [[]], "check_path": False,
    },
    {
        "id": "TC08", "group": "Edge case", "file": "tc08.json",
        "desc": "Node 23 Bia đá, chọn đường 2-20-19, không đi vòng qua 23", "source": 2, "dest": 19,
        "expected_distance": 140, "expected_paths": [[2, 20, 19]], "check_path": True,
    },
    {
        "id": "TC09", "group": "Edge case", "file": "tc09.json",
        "desc": "Node 24 Ngã tư Hồ Tiền - D9, đường ngắn nhất đi qua 24", "source": 6, "dest": 11,
        "expected_distance": 170, "expected_paths": [[6, 24, 11]], "check_path": True,
    },
    {
        "id": "TC10", "group": "Error case", "file": "tc10.json",
        "desc": "Node đích không tồn tại", "source": 1, "dest": 999,
        "expected_distance": float("inf"), "expected_paths": [[]], "check_path": False,
    },
    {
        "id": "TC11", "group": "Error case", "file": "tc11.json",
        "desc": "Node nguồn không tồn tại", "source": 999, "dest": 1,
        "expected_distance": float("inf"), "expected_paths": [[]], "check_path": False,
    },
    {
        "id": "TC12", "group": "Error case", "file": "tc12.json",
        "desc": "Hai thành phần liên thông tách rời", "source": 1, "dest": 4,
        "expected_distance": float("inf"), "expected_paths": [[]], "check_path": False,
    },
    {
        "id": "TC13", "group": "Edge case", "file": "tc13.json",
        "desc": "Có nhiều đường ngắn nhất bằng nhau", "source": 1, "dest": 4,
        "expected_distance": 4, "expected_paths": [[1, 2, 4], [1, 3, 4]], "check_path": True,
    },
    {
        "id": "TC14", "group": "Edge case", "file": "tc14.json",
        "desc": "Đồ thị có chu trình", "source": 1, "dest": 4,
        "expected_distance": 3, "expected_paths": [[1, 2, 3, 4]], "check_path": True,
    },
    {
        "id": "TC15", "group": "Edge case", "file": "tc15.json",
        "desc": "Có cạnh trùng cặp khác trọng số", "source": 1, "dest": 3,
        "expected_distance": 5, "expected_paths": [[1, 2, 3]], "check_path": True,
    },
]


def norm_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.strip().lower())


def get_value(row: dict[str, str], *names: str, default: str = "") -> str:
    normalized = {norm_key(k): v for k, v in row.items()}
    for name in names:
        value = normalized.get(norm_key(name))
        if value is not None and str(value).strip() != "":
            return str(value).strip()
    return default


def parse_distance(text: str) -> Any:
    s = str(text).strip()
    if s.lower() in {"inf", "infinity", "\u221e"}:
        return float("inf")
    try:
        value = float(s)
        return int(value) if value.is_integer() else value
    except Exception:
        return s


def parse_node(text: str) -> Any:
    s = str(text).strip()
    try:
        return int(s)
    except Exception:
        return s


def parse_path_one(text: str) -> list[Any]:
    s = str(text).strip()
    if s in {"", "[]", "None", "none", "null"}:
        return []

    #Thử parse dạng Python list hoặc JSON list
    try:
        value = ast.literal_eval(s)
        if isinstance(value, list):
            if value and all(isinstance(x, list) for x in value):
                return value[0]
            return value
    except Exception:
        pass

    #Hỗ trợ các dạng nhập path phổ biến trong CSV
    parts = re.split(r"\s*(?:\u2192|->|,|;)\s*", s)
    if len(parts) == 1:
        parts = re.split(r"\s+-\s+", s)
    return [parse_node(p) for p in parts if p.strip()]


def parse_expected_paths(text: str) -> list[list[Any]]:
    s = str(text).strip()
    if s in {"", "[]", "None", "none", "null"}:
        return [[]]

    #Thử parse dạng nhiều path, ví dụ [[1, 2, 4], [1, 3, 4]]
    try:
        value = ast.literal_eval(s)
        if isinstance(value, list):
            if value and all(isinstance(x, list) for x in value):
                return value
            return [value]
    except Exception:
        pass

    return [parse_path_one(part) for part in s.split("|")]


def parse_bool(text: str, default: bool = True) -> bool:
    s = str(text).strip().lower()
    if s in {"true", "1", "yes", "y", "co", "có"}:
        return True
    if s in {"false", "0", "no", "n", "khong", "không"}:
        return False
    if s == "multiple":
        return True
    return default


def load_cases_from_csv() -> tuple[list[dict[str, Any]], str]:
    if not TESTCASE_CSV.exists():
        return TEST_CASES, "TEST_CASES trong script"

    cases: list[dict[str, Any]] = []
    with TESTCASE_CSV.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tc_id = get_value(row, "ID", "TestCaseID", "TC", default="")
            if not tc_id:
                continue

            graph_file = get_value(row, "GraphFile", "File", "Graph", default=f"{tc_id.lower()}.json")
            cases.append(
                {
                    "id": tc_id,
                    "group": get_value(row, "Group", "Type", default=""),
                    "file": graph_file,
                    "desc": get_value(row, "Description", "Desc", "Mo ta", "Mô tả", default=""),
                    "source": parse_node(get_value(row, "Source", "Start")),
                    "dest": parse_node(get_value(row, "Destination", "Dest", "Target", "End")),
                    "expected_distance": parse_distance(
                        get_value(row, "ExpectedDistance", "Distance", "Expected Dist")
                    ),
                    "expected_paths": parse_expected_paths(
                        get_value(row, "ExpectedPath", "ExpectedPaths", "Path")
                    ),
                    "check_path": parse_bool(get_value(row, "CheckPath", default="true"), default=True),
                }
            )

    if not cases:
        return TEST_CASES, "TEST_CASES trong script do CSV không có test case hợp lệ"
    return cases, str(TESTCASE_CSV.relative_to(ROOT_DIR))


def resolve_graph_file(filename: str) -> Path:
    raw = Path(str(filename))
    candidates: list[Path] = []

    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.append(GRAPH_DIR / raw)
        candidates.append(ROOT_DIR / raw)
        if raw.suffix == "":
            candidates.append(GRAPH_DIR / raw.with_suffix(".json"))
        if raw.suffix == ".js":
            candidates.append(GRAPH_DIR / raw.with_suffix(".json"))

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]


def run_one_case(case: dict[str, Any]) -> dict[str, Any]:
    graph_file = resolve_graph_file(case["file"])

    try:
        graph = build_graph_from_json(graph_file)
        raw_result = findShortestPath(graph, case["source"], case["dest"])
        result = normalize_result(raw_result)
        actual_distance = result["distance"]
        actual_path = normalize_path(result["path"])

        distance_ok = same_distance(actual_distance, case["expected_distance"])
        if case["check_path"]:
            path_ok = actual_path in case["expected_paths"]
        else:
            path_ok = actual_path in ([], None) or distance_ok

        passed = distance_ok and path_ok
        note = ""
        if distance_ok and not path_ok:
            note = "Distance đúng nhưng path không nằm trong expected_paths. Cần kiểm tra tie-breaking."

        return {
            "ID": case["id"],
            "Group": case["group"],
            "Description": case["desc"],
            "GraphFile": str(graph_file.relative_to(ROOT_DIR)) if graph_file.exists() else str(graph_file),
            "Source": case["source"],
            "Destination": case["dest"],
            "ExpectedDistance": distance_to_text(case["expected_distance"]),
            "ExpectedPath": " | ".join(path_to_text(p) for p in case["expected_paths"]),
            "ActualDistance": distance_to_text(actual_distance),
            "ActualPath": path_to_text(actual_path),
            "Status": "PASS" if passed else "FAIL",
            "Note": note,
        }

    except Exception as exc:
        return {
            "ID": case.get("id", "?"),
            "Group": case.get("group", ""),
            "Description": case.get("desc", ""),
            "GraphFile": str(graph_file.relative_to(ROOT_DIR)) if graph_file.exists() else str(graph_file),
            "Source": case.get("source", ""),
            "Destination": case.get("dest", ""),
            "ExpectedDistance": distance_to_text(case.get("expected_distance", "")),
            "ExpectedPath": " | ".join(path_to_text(p) for p in case.get("expected_paths", [])),
            "ActualDistance": "CRASH",
            "ActualPath": "",
            "Status": "FAIL",
            "Note": f"{type(exc).__name__}: {exc}",
        }


def write_results(rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with RESULT_FILE.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_all() -> None:
    cases, case_source = load_cases_from_csv()

    print("=" * 76)
    print("QA functional test cho Dijkstra TC01-TC15")
    print(f"Project root: {ROOT_DIR}")
    print(f"Graph dir: {GRAPH_DIR}")
    print(f"Case source: {case_source}")
    print(f"Case count: {len(cases)}")
    print("=" * 76)

    if len(cases) != 15:
        print(f"Warning: Số test case hiện tại là {len(cases)}, số chính thức là 15.")

    rows: list[dict[str, Any]] = []
    for case in cases:
        row = run_one_case(case)
        rows.append(row)

        print(f"{row['Status']}: {row['ID']} - {row['Description']}")
        if row["Status"] != "PASS":
            print(f"Expected distance: {row['ExpectedDistance']}")
            print(f"Expected path: {row['ExpectedPath']}")
            print(f"Actual distance: {row['ActualDistance']}")
            print(f"Actual path: {row['ActualPath']}")
            if row["Note"]:
                print(f"Note: {row['Note']}")
        print()

    write_results(rows)

    total = len(rows)
    passed = sum(1 for r in rows if r["Status"] == "PASS")
    failed = [r for r in rows if r["Status"] == "FAIL"]

    print("=" * 76)
    print(f"Kết quả functional test: {passed}/{total} PASS")
    print(f"Đã ghi kết quả vào: {RESULT_FILE}")

    if failed:
        print("Danh sách test case FAIL:")
        for row in failed:
            print(f"{row['ID']}: {row['Description']}. Note: {row['Note']}")

    print("=" * 76)


if __name__ == "__main__":
    try:
        run_all()
    except Exception:
        print("Fatal: Test runner gặp lỗi ngoài dự kiến.")
        traceback.print_exc()