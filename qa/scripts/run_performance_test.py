"""
SCRIPT ĐO HIỆU NĂNG DIJKSTRA
 Mục đích:
   - Đọc các file đồ thị lớn trong qa/data_large/
   - Gọi hàm load_data 
   - Gọi findShortestPath(graph, source, dest) để đo thời gian
   - Chạy 5 lần / kích thước, bỏ Run 1 làm warm-up
   - Ghi kết quả vào qa/results/performance_results.csv
"""

from __future__ import annotations

import csv
import gc
import json
import math
import statistics
import sys
import time
from collections import deque
from pathlib import Path
from typing import Any, Optional

SIZES = [100, 500, 1000, 5000, 10000]

#Chạy nhiều lần hơn để kết quả std/avg ổn định hơn.
RUNS = 9
WARMUP = 2
TRIM_MIN_MAX = True

SOURCE_NODE = 0
DEST_MODE = "middle"
THRESHOLD_10K_MS = 5000.0

SCRIPT_DIR = Path(__file__).resolve().parent
QA_DIR = SCRIPT_DIR.parent
ROOT_DIR = QA_DIR.parent

DATA_DIR = QA_DIR / "data_large"
RESULTS_DIR = QA_DIR / "results"
OUTPUT_CSV = RESULTS_DIR / "performance_results.csv"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT_DIR))

from core.MinHeap_Graph import Graph
from core.findShortestPath_reconstructPath import findShortestPath


PROJECT_LOADER = None
LOADER_NAME = "manual Graph.addEdge fallback"

try:
    from loadData import load_data as PROJECT_LOADER  # type: ignore
    LOADER_NAME = "load_data"
except Exception:
    try:
        from loadData import loadData as PROJECT_LOADER  # type: ignore
        LOADER_NAME = "loadData from load_data.py"
    except Exception:
        try:
            from loadData import loadData as PROJECT_LOADER  # type: ignore
            LOADER_NAME = "loadData"
        except Exception:
            PROJECT_LOADER = None
            LOADER_NAME = "manual Graph.addEdge fallback"


def read_json(filepath: Path) -> dict[str, Any]:
    """Đọc file JSON và trả về dữ liệu graph."""
    with filepath.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_graph_manually(graph_data: dict[str, Any]) -> Graph:
    """Build graph thủ công nếu loader của project không dùng được."""
    graph = Graph()

    if hasattr(graph, "addNode"):
        for node in graph_data.get("nodes", []):
            graph.addNode(node["id"])

    for edge in graph_data["edges"]:
        graph.addEdge(edge["from"], edge["to"], edge["weight"])

    return graph


def load_graph(filepath: Path) -> tuple[Graph, dict[str, Any], str, Optional[str]]:
    """Load graph bằng loader thật của project, fallback nếu loader lỗi."""
    graph_data = read_json(filepath)

    if PROJECT_LOADER is not None:
        try:
            loaded = PROJECT_LOADER(str(filepath))
            graph = loaded[0] if isinstance(loaded, tuple) else loaded
            return graph, graph_data, LOADER_NAME, None
        except Exception as exc:
            warning = (
                f"{LOADER_NAME} lỗi với {filepath.name}: {exc}. "
                "Script đã fallback sang Graph.addEdge thủ công."
            )
            graph = build_graph_manually(graph_data)
            return graph, graph_data, "manual Graph.addEdge fallback", warning

    graph = build_graph_manually(graph_data)
    return graph, graph_data, "manual Graph.addEdge fallback", None


def choose_source_dest(graph_data: dict[str, Any]) -> tuple[int, int]:
    """Chọn source và dest ổn định cho mỗi graph."""
    node_ids = [node["id"] for node in graph_data["nodes"]]
    if not node_ids:
        raise ValueError("Graph không có node nào.")

    source = SOURCE_NODE if SOURCE_NODE in node_ids else node_ids[0]
    dest = node_ids[len(node_ids) // 2] if DEST_MODE == "middle" else node_ids[-1]

    if dest == source and len(node_ids) > 1:
        dest = node_ids[-1]

    return source, dest


def verify_connected(graph_data: dict[str, Any]) -> bool:
    """Kiểm tra liên thông bằng BFS trên dữ liệu JSON."""
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    if not nodes:
        return False

    ids = {node["id"] for node in nodes}
    adj = {node_id: [] for node_id in ids}

    for edge in edges:
        u = edge["from"]
        v = edge["to"]
        if u not in ids or v not in ids:
            return False
        adj[u].append(v)
        adj[v].append(u)

    start = nodes[0]["id"]
    visited = {start}
    queue = deque([start])

    while queue:
        cur = queue.popleft()
        for nb in adj[cur]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)

    return len(visited) == len(ids)


def validate_graph_format(graph_data: dict[str, Any]) -> None:
    """Bắt lỗi format cơ bản trước khi benchmark."""
    if "nodes" not in graph_data:
        raise ValueError("JSON thiếu key 'nodes'.")
    if "edges" not in graph_data:
        raise ValueError("JSON thiếu key 'edges'.")

    nodes = graph_data["nodes"]
    edges = graph_data["edges"]
    ids = {node.get("id") for node in nodes}

    if len(ids) != len(nodes):
        raise ValueError("Node id bị trùng hoặc thiếu id.")

    for node in nodes:
        for key in ("id", "name", "lat", "lng"):
            if key not in node:
                raise ValueError(f"Node thiếu key '{key}': {node}")

    seen_edges: set[tuple[int, int]] = set()

    for edge in edges:
        for key in ("from", "to", "weight"):
            if key not in edge:
                raise ValueError(f"Edge thiếu key '{key}': {edge}")

        u = edge["from"]
        v = edge["to"]
        w = edge["weight"]

        if u == v:
            raise ValueError(f"Cạnh tự vòng: {edge}")
        if u not in ids or v not in ids:
            raise ValueError(f"Cạnh trỏ đến node không tồn tại: {edge}")
        if w <= 0:
            raise ValueError(f"Trọng số phải lớn hơn 0 cho Dijkstra: {edge}")

        edge_key = (min(u, v), max(u, v))
        if edge_key in seen_edges:
            raise ValueError(f"Cạnh bị trùng: {edge}")
        seen_edges.add(edge_key)


def measure_find_shortest_path(graph: Graph, source: int, dest: int) -> tuple[float, dict[str, Any]]:
    """Đo riêng thời gian chạy findShortestPath."""
    gc.collect()
    old_gc_state = gc.isenabled()

    if old_gc_state:
        gc.disable()

    try:
        start = time.perf_counter()
        result = findShortestPath(graph, source, dest)
        elapsed_ms = (time.perf_counter() - start) * 1000
    finally:
        if old_gc_state:
            gc.enable()

    return elapsed_ms, result


def select_stable_times(raw_times: list[float]) -> tuple[list[float], list[float], str]:
    """
    Chọn các lần đo dùng để tính thống kê.

    Với RUNS = 9 và WARMUP = 2, script còn 7 lần đo thật.
    Nếu trim min/max, script loại 1 giá trị nhỏ nhất và 1 giá trị lớn nhất.
    Phần còn lại dùng để tính avg, std và range.
    """
    measured = raw_times[WARMUP:]

    if TRIM_MIN_MAX and len(measured) >= 6:
        ordered = sorted(measured)
        stable_times = ordered[1:-1]
        dropped_times = [ordered[0], ordered[-1]]
        return stable_times, dropped_times, "trim_min_max_after_warmup"

    return measured, [], "all_after_warmup"


def run_one_size(n: int) -> Optional[dict[str, Any]]:
    filepath = DATA_DIR / f"graph_{n}.json"

    if not filepath.exists():
        print(f"Cảnh báo: Không tìm thấy {filepath}")
        return None

    load_start = time.perf_counter()
    graph, graph_data, loader_used, warning = load_graph(filepath)
    load_ms = (time.perf_counter() - load_start) * 1000

    if warning:
        print(f"Cảnh báo: {warning}")

    validate_graph_format(graph_data)
    connected = verify_connected(graph_data)

    actual_nodes = len(graph_data["nodes"])
    actual_edges = len(graph_data["edges"])
    source, dest = choose_source_dest(graph_data)

    raw_times: list[float] = []
    final_result: Optional[dict[str, Any]] = None

    for run_idx in range(1, RUNS + 1):
        time.sleep(0.01)
        elapsed_ms, result = measure_find_shortest_path(graph, source, dest)
        raw_times.append(elapsed_ms)
        final_result = result

        label = "warm-up, không tính trung bình" if run_idx <= WARMUP else "tính trung bình"
        print(f"Run {run_idx}: {elapsed_ms:.4f} ms. Ghi chú: {label}")

    stable_times, dropped_times, stats_method = select_stable_times(raw_times)

    avg_ms = statistics.mean(stable_times)
    min_ms = min(stable_times)
    max_ms = max(stable_times)
    range_ms = max_ms - min_ms
    std_ms = statistics.stdev(stable_times) if len(stable_times) > 1 else 0.0
    std_ratio = std_ms / avg_ms if avg_ms > 0 else 0.0

    path = final_result.get("path", []) if final_result else []
    distance = final_result.get("distance", math.inf) if final_result else math.inf
    reachable = bool(path) and distance != math.inf

    record = {
        "graph_file": filepath.name,
        "n_nodes": actual_nodes,
        "n_edges": actual_edges,
        "connected": connected,
        "loader_used": loader_used,
        "load_ms": load_ms,
        "source": source,
        "dest": dest,
        "path_length": len(path),
        "distance_m": distance,
        "reachable": reachable,
        "avg_ms_run2to5": avg_ms,
        "min_ms": min_ms,
        "max_ms": max_ms,
        "range_ms": range_ms,
        "std_ms": std_ms,
        "std_ratio": std_ratio,
        "stats_method": stats_method,
        "used_times_ms": ";".join(f"{x:.4f}" for x in stable_times),
        "dropped_times_ms": ";".join(f"{x:.4f}" for x in dropped_times),
    }

    for i, value in enumerate(raw_times, start=1):
        record[f"run{i}_ms"] = value

    return record


def complexity_scale(record: dict[str, Any]) -> float:
    """Tính thang đo tham khảo theo O((V + E) log V)."""
    v = record["n_nodes"]
    e = record["n_edges"]
    return (v + e) * math.log2(max(v, 2))


def analyze_growth(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Phân tích tăng trưởng chỉ để tham khảo.

    Không dùng riêng tỉ lệ giữa hai graph để kết luận bug, vì graph random khác nhau
    và findShortestPath có thể dừng sớm khi tìm được dest.
    """
    growth = []

    for i in range(1, len(records)):
        prev = records[i - 1]
        curr = records[i]

        actual_ratio = (
            curr["avg_ms_run2to5"] / prev["avg_ms_run2to5"]
            if prev["avg_ms_run2to5"] > 0
            else math.inf
        )

        theoretical_ratio = complexity_scale(curr) / complexity_scale(prev)

        if actual_ratio > 100 and curr["avg_ms_run2to5"] >= THRESHOLD_10K_MS:
            flag = "NGHI O(V^2)"
        elif actual_ratio > theoretical_ratio * 5:
            flag = "CANH BAO NHE"
        else:
            flag = "HOP LY"

        growth.append(
            {
                "from_n": prev["n_nodes"],
                "to_n": curr["n_nodes"],
                "actual_ratio": actual_ratio,
                "theoretical_ratio": theoretical_ratio,
                "flag": flag,
            }
        )

    return growth


CSV_FIELDS = [
    "graph_file",
    "n_nodes",
    "n_edges",
    "connected",
    "loader_used",
    "load_ms",
    "source",
    "dest",
    "path_length",
    "distance_m",
    "reachable",
    *[f"run{i}_ms" for i in range(1, RUNS + 1)],
    "avg_ms_run2to5",
    "min_ms",
    "max_ms",
    "range_ms",
    "std_ms",
    "std_ratio",
    "stats_method",
    "used_times_ms",
    "dropped_times_ms",
    "pass_10k_under_5000ms",
    "note",
]


def save_csv(records: list[dict[str, Any]]) -> None:
    """Ghi kết quả benchmark ra CSV."""
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()

        for record in records:
            is_10k = record["n_nodes"] == 10000
            pass_10k = "" if not is_10k else (
                "PASS" if record["avg_ms_run2to5"] < THRESHOLD_10K_MS else "FAIL"
            )

            note_parts = []
            if not record["connected"]:
                note_parts.append("Graph khong lien thong")
            if not record["reachable"]:
                note_parts.append("Khong tim thay duong di source den dest")
            if record["loader_used"] == "manual Graph.addEdge fallback":
                note_parts.append("Dang dung manual fallback, can kiem tra load_data hoac loadData")
            if record["std_ratio"] > 0.20:
                note_parts.append("Std/Avg > 20%, moi truong do con nhieu")

            row = {}
            for field in CSV_FIELDS:
                value = record.get(field, "")
                if isinstance(value, float):
                    value = round(value, 4)
                row[field] = value

            row["connected"] = "YES" if record["connected"] else "NO"
            row["reachable"] = "YES" if record["reachable"] else "NO"
            row["distance_m"] = (
                round(record["distance_m"], 2)
                if record["distance_m"] != math.inf
                else "inf"
            )
            row["pass_10k_under_5000ms"] = pass_10k
            row["note"] = "; ".join(note_parts)

            writer.writerow(row)


def print_summary(records: list[dict[str, Any]]) -> None:
    """In bảng tóm tắt kết quả benchmark."""
    print()
    print("=" * 96)
    print("Tóm tắt performance test")
    print("Nodes; Edges; LoadMs; AvgStableMs; StdAvg; RangeMs; PathLength; Check10K")

    for record in records:
        pass_10k = ""
        if record["n_nodes"] == 10000:
            pass_10k = "PASS" if record["avg_ms_run2to5"] < THRESHOLD_10K_MS else "FAIL"

        print(
            f"{record['n_nodes']}; "
            f"{record['n_edges']}; "
            f"{record['load_ms']:.3f}; "
            f"{record['avg_ms_run2to5']:.4f}; "
            f"{record['std_ratio'] * 100:.1f}%; "
            f"{record['range_ms']:.4f}; "
            f"{record['path_length']}; "
            f"{pass_10k}"
        )

    print("=" * 96)


def print_growth(records: list[dict[str, Any]]) -> None:
    """In phân tích tăng trưởng chỉ để tham khảo."""
    growth = analyze_growth(records)

    if not growth:
        return

    print()
    print("Phân tích tăng trưởng tham khảo theo O((V + E) log V)")
    print("FromN; ToN; ActualRatio; TheoryRatio; DanhGia")

    for item in growth:
        print(
            f"{item['from_n']}; "
            f"{item['to_n']}; "
            f"{item['actual_ratio']:.2f}x; "
            f"{item['theoretical_ratio']:.2f}x; "
            f"{item['flag']}"
        )

    r1k = next((r for r in records if r["n_nodes"] == 1000), None)
    r10k = next((r for r in records if r["n_nodes"] == 10000), None)

    if r1k and r10k and r1k["avg_ms_run2to5"] > 0:
        ratio = r10k["avg_ms_run2to5"] / r1k["avg_ms_run2to5"]
        print()
        print(f"1K đến 10K: {ratio:.2f}x")
        if ratio > 100 and r10k["avg_ms_run2to5"] >= THRESHOLD_10K_MS:
            print("Kết luận sơ bộ: nghi bug O(V^2), cần gửi TV2 kiểm tra.")
        else:
            print("Kết luận sơ bộ: chưa có dấu hiệu O(V^2) rõ ràng từ tỉ lệ 1K đến 10K.")


def main() -> None:
    print("=" * 96)
    print("TV4 - Đo hiệu năng Dijkstra")
    print(f"Root repo: {ROOT_DIR}")
    print(f"Data dir: {DATA_DIR}")
    print(f"Output CSV: {OUTPUT_CSV}")
    print(f"Sizes: {SIZES}")
    print(f"Runs: {RUNS} lần mỗi size, bỏ {WARMUP} lần warm-up")
    print("Stats: trim 1 min và 1 max sau warm-up nếu đủ mẫu")
    print("=" * 96)

    records: list[dict[str, Any]] = []

    for n in SIZES:
        print()
        print(f"Đang đo graph_{n}.json. Source: {SOURCE_NODE}. Dest: node gần giữa danh sách.")

        try:
            record = run_one_size(n)
        except Exception as exc:
            print(f"Lỗi khi đo graph_{n}.json: {exc}")
            continue

        if record is None:
            continue

        records.append(record)

        print(
            f"Avg stable: {record['avg_ms_run2to5']:.4f} ms. "
            f"Std/Avg: {record['std_ratio'] * 100:.1f}%. "
            f"Range: {record['range_ms']:.4f} ms. "
            f"Path length: {record['path_length']}. "
            f"Distance: {record['distance_m']}."
        )

    if not records:
        print()
        print("Không có record nào. Kiểm tra lại thư mục qa/data_large và tên file graph_*.json.")
        return

    print_summary(records)
    print_growth(records)

    save_csv(records)

    print()
    print(f"Đã ghi kết quả vào: {OUTPUT_CSV}")
    print("Có thể gửi performance_results.csv và biểu đồ cho TV5 đưa vào báo cáo.")


if __name__ == "__main__":
    main()