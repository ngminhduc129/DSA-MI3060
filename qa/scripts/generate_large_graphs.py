"""
SCRIPT Sinh đồ thị liên thông cho performance test Dijkstra
Output:
-qa/data_large/graph_100.json
-qa/data_large/graph_500.json
-qa/data_large/graph_1000.json
-qa/data_large/graph_5000.json
-qa/data_large/graph_10000.json
-qa/results/large_graph_summary.csv
"""

from __future__ import annotations

import csv
import json
import random
import time
from collections import deque
from pathlib import Path
from typing import Any

SIZES = [100, 500, 1000, 5000, 10000]

#Weight tính theo mét, dùng số dương để phù hợp với Dijkstra.
WEIGHT_MIN = 10
WEIGHT_MAX = 1000

#Số cạnh mục tiêu là E = 5 * V.
TARGET_EDGE_FACTOR = 5
BASE_SEED = 42


def find_root_dir() -> Path:
    #Tìm root repo để script chạy ổn từ root hoặc từ qa/scripts
    script_dir = Path(__file__).resolve().parent
    if script_dir.name == "scripts" and script_dir.parent.name == "qa":
        return script_dir.parent.parent
    return Path.cwd()


ROOT_DIR = find_root_dir()
OUTPUT_DIR = ROOT_DIR / "qa" / "data_large"
RESULTS_DIR = ROOT_DIR / "qa" / "results"
SUMMARY_FILE = RESULTS_DIR / "large_graph_summary.csv"


def make_node(node_id: int, n: int) -> dict[str, Any]:
    #Tạo node có đủ id, name, lat và lng
    width = max(1, int(n**0.5))
    row = node_id // width
    col = node_id % width
    return {
        "id": node_id,
        "name": f"Node_{node_id}",
        "lat": round(21.000000 + row * 0.0001, 6),
        "lng": round(105.800000 + col * 0.0001, 6),
    }


def add_edge(edges: list[dict[str, Any]], edge_set: set[tuple[int, int]], u: int, v: int, w: int) -> bool:
    #Thêm cạnh vô hướng nếu không trùng, không self-loop và weight hợp lệ
    if u == v or w <= 0:
        return False

    key = (min(u, v), max(u, v))
    if key in edge_set:
        return False

    edge_set.add(key)
    edges.append({"from": u, "to": v, "weight": w})
    return True


def generate_graph(n: int, seed: int = BASE_SEED) -> dict[str, Any]:
    """
    Sinh đồ thị vô hướng liên thông.

    Bước 1: Tạo toàn bộ node.
    Bước 2: Tạo spanning tree để đảm bảo graph liên thông.
    Bước 3: Thêm cạnh phụ đến khi tổng cạnh đạt E = 5 * V.
    """
    if n <= 0:
        raise ValueError("n phải là số nguyên dương")

    rng = random.Random(seed)
    nodes = [make_node(i, n) for i in range(n)]
    edges: list[dict[str, Any]] = []
    edge_set: set[tuple[int, int]] = set()

    if n == 1:
        return {"nodes": nodes, "edges": edges}

    #Tạo spanning tree bằng cách nối mỗi node mới với một node đã xuất hiện.
    shuffled = list(range(n))
    rng.shuffle(shuffled)

    for i in range(1, n):
        u = shuffled[i]
        v = shuffled[rng.randint(0, i - 1)]
        w = rng.randint(WEIGHT_MIN, WEIGHT_MAX)
        add_edge(edges, edge_set, u, v, w)

    max_possible_edges = n * (n - 1) // 2
    target_edges = min(max_possible_edges, TARGET_EDGE_FACTOR * n)
    needed = target_edges - len(edges)

    if needed <= 0:
        return {"nodes": nodes, "edges": edges}

    #Với graph nhỏ và khá dày, candidate list giúp tránh thử cạnh trùng quá nhiều.
    if n <= 1000 and target_edges > 0.2 * max_possible_edges:
        candidates = [
            (u, v)
            for u in range(n)
            for v in range(u + 1, n)
            if (u, v) not in edge_set
        ]
        rng.shuffle(candidates)

        for u, v in candidates[:needed]:
            w = rng.randint(WEIGHT_MIN, WEIGHT_MAX)
            add_edge(edges, edge_set, u, v, w)
    else:
        attempts = 0
        max_attempts = needed * 50 + 1000

        while len(edges) < target_edges and attempts < max_attempts:
            u = rng.randint(0, n - 1)
            v = rng.randint(0, n - 1)
            w = rng.randint(WEIGHT_MIN, WEIGHT_MAX)
            attempts += 1
            add_edge(edges, edge_set, u, v, w)

        if len(edges) < target_edges:
            print(
                f"Cảnh báo: graph_{n}.json chỉ sinh được {len(edges)} trên {target_edges} cạnh "
                f"sau {attempts} lần thử."
            )

    return {"nodes": nodes, "edges": edges}


def verify_format(graph_data: dict[str, Any]) -> tuple[bool, str]:
    #Kiểm tra format JSON trước khi lưu
    if "nodes" not in graph_data or "edges" not in graph_data:
        return False, "Thiếu key nodes hoặc edges"

    nodes = graph_data["nodes"]
    edges = graph_data["edges"]
    node_ids = {node.get("id") for node in nodes}

    if len(node_ids) != len(nodes):
        return False, "Trùng hoặc thiếu node id"

    for node in nodes:
        for key in ("id", "name", "lat", "lng"):
            if key not in node:
                return False, f"Node thiếu key {key}: {node}"

    seen_edges: set[tuple[int, int]] = set()
    for edge in edges:
        for key in ("from", "to", "weight"):
            if key not in edge:
                return False, f"Edge thiếu key {key}: {edge}"

        u = edge["from"]
        v = edge["to"]
        w = edge["weight"]

        if u not in node_ids or v not in node_ids:
            return False, f"Edge trỏ tới node không tồn tại: {edge}"
        if u == v:
            return False, f"Edge tự vòng: {edge}"
        if not isinstance(w, (int, float)) or w <= 0:
            return False, f"Weight phải lớn hơn 0: {edge}"

        edge_key = (min(u, v), max(u, v))
        if edge_key in seen_edges:
            return False, f"Cạnh bị trùng: {edge}"
        seen_edges.add(edge_key)

    return True, "OK"


def verify_connected(graph_data: dict[str, Any]) -> bool:
    #Kiểm tra graph liên thông bằng BFS
    nodes = graph_data.get("nodes", [])
    if not nodes:
        return False

    adj = {node["id"]: [] for node in nodes}
    for edge in graph_data.get("edges", []):
        adj[edge["from"]].append(edge["to"])
        adj[edge["to"]].append(edge["from"])

    start = nodes[0]["id"]
    visited = {start}
    queue: deque[int] = deque([start])

    while queue:
        cur = queue.popleft()
        for nb in adj[cur]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)

    return len(visited) == len(nodes)


def save_graph(graph_data: dict[str, Any], n: int) -> Path:
    #Lưu graph ra file JSON trong qa/data_large
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filepath = OUTPUT_DIR / f"graph_{n}.json"
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    return filepath


def write_summary(rows: list[dict[str, Any]]) -> None:
    #Ghi bảng tổng kết graph lớn ra CSV
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with SUMMARY_FILE.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "File",
                "Nodes",
                "Edges",
                "V_plus_E",
                "Connected",
                "FormatOK",
                "FileSizeKB",
                "GenerateMs",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    print("=" * 72)
    print("Sinh đồ thị liên thông cho performance test")
    print(f"Root dir: {ROOT_DIR}")
    print(f"Sizes: {SIZES}")
    print(f"Target edges: E = {TARGET_EDGE_FACTOR} * V")
    print(f"Weight: từ {WEIGHT_MIN} đến {WEIGHT_MAX} mét")
    print(f"Output dir: {OUTPUT_DIR}")
    print("=" * 72)

    summary_rows: list[dict[str, Any]] = []

    for n in SIZES:
        t0 = time.perf_counter()
        graph_data = generate_graph(n, seed=BASE_SEED + n)
        generate_ms = (time.perf_counter() - t0) * 1000

        format_ok, format_msg = verify_format(graph_data)
        connected = verify_connected(graph_data)
        filepath = save_graph(graph_data, n)
        file_size_kb = filepath.stat().st_size / 1024
        n_edges = len(graph_data["edges"])
        status = "OK" if connected and format_ok else "FAIL"

        print(
            f"File: {filepath.name}; "
            f"V: {n}; "
            f"E: {n_edges}; "
            f"V_plus_E: {n + n_edges}; "
            f"SizeKB: {file_size_kb:.1f}; "
            f"GenerateMs: {generate_ms:.1f}; "
            f"Status: {status}"
        )

        if not format_ok:
            print(f"Lỗi format: {format_msg}")
        if not connected:
            print("Lỗi liên thông: BFS không thăm được toàn bộ node")

        summary_rows.append(
            {
                "File": filepath.name,
                "Nodes": n,
                "Edges": n_edges,
                "V_plus_E": n + n_edges,
                "Connected": "YES" if connected else "NO",
                "FormatOK": "YES" if format_ok else "NO",
                "FileSizeKB": round(file_size_kb, 1),
                "GenerateMs": round(generate_ms, 1),
            }
        )

    write_summary(summary_rows)

    print("=" * 72)
    print(f"Đã ghi file graph vào: {OUTPUT_DIR}")
    print(f"Đã ghi summary vào: {SUMMARY_FILE}")
    print("Ghi chú: graph_*.json chỉ dùng cho performance test, không dùng để thay expected của TC01-TC15.")


if __name__ == "__main__":
    main()