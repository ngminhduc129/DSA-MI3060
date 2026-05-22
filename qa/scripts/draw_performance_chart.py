"""
Vẽ biểu đồ performance test cho thuật toán Dijkstra.
Input:
- qa/results/performance_results.csv

Output:
- qa/charts/dijkstra_performance.png
- qa/charts/dijkstra_performance.pdf
- qa/charts/dijkstra_performance_log.png nếu dữ liệu có độ chênh đủ lớn
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any


#Đường dẫn chính
SCRIPT_DIR = Path(__file__).resolve().parent
QA_DIR = SCRIPT_DIR.parent
ROOT_DIR = QA_DIR.parent

INPUT_CSV = QA_DIR / "results" / "performance_results.csv"
CHART_DIR = QA_DIR / "charts"

OUTPUT_PNG = CHART_DIR / "dijkstra_performance.png"
OUTPUT_PDF = CHART_DIR / "dijkstra_performance.pdf"
OUTPUT_LOG_PNG = CHART_DIR / "dijkstra_performance_log.png"


def import_matplotlib():
    """Import matplotlib và báo lỗi rõ nếu chưa cài."""
    try:
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        print("Missing required package: matplotlib")
        print("Cài bằng lệnh: pip install matplotlib")
        sys.exit(1)


def normalize_column_name(name: str) -> str:
    """Chuẩn hóa tên cột để tìm cột linh hoạt hơn."""
    return (
        name.strip()
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )


def find_column(fieldnames: list[str], candidates: list[str], error_message: str) -> str:
    """Tìm cột theo danh sách tên ưu tiên."""
    normalized_map = {
        normalize_column_name(col): col
        for col in fieldnames
    }

    for candidate in candidates:
        key = normalize_column_name(candidate)
        if key in normalized_map:
            return normalized_map[key]

    raise ValueError(error_message)


def to_int(value: Any, column_name: str) -> int:
    """Chuyển dữ liệu sang int."""
    try:
        return int(float(str(value).strip()))
    except Exception as exc:
        raise ValueError(f"Không chuyển được giá trị '{value}' ở cột {column_name} sang int") from exc


def to_float(value: Any, column_name: str) -> float:
    """Chuyển dữ liệu sang float."""
    try:
        return float(str(value).strip())
    except Exception as exc:
        raise ValueError(f"Không chuyển được giá trị '{value}' ở cột {column_name} sang float") from exc


def read_performance_csv(csv_path: Path) -> list[dict[str, Any]]:
    """Đọc performance_results.csv và trả về dữ liệu đã chuẩn hóa."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file CSV: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        if not fieldnames:
            raise ValueError("CSV không có header")

        nodes_col = find_column(
            fieldnames,
            ["n_nodes", "Nodes", "nodes"],
            "Missing required column for number of nodes",
        )
        edges_col = find_column(
            fieldnames,
            ["n_edges", "Edges", "edges"],
            "Missing required column for number of edges",
        )
        avg_col = find_column(
            fieldnames,
            ["avg_ms_run2to5", "avg_ms", "Avg Dijkstra(ms)", "avg_dijkstra_ms"],
            "Missing required column for average time",
        )

        records: list[dict[str, Any]] = []
        for row in reader:
            if not row:
                continue

            n_nodes = to_int(row[nodes_col], nodes_col)
            n_edges = to_int(row[edges_col], edges_col)
            avg_ms = to_float(row[avg_col], avg_col)

            if n_nodes <= 0:
                raise ValueError(f"Số nodes phải lớn hơn 0, nhận được {n_nodes}")
            if n_edges < 0:
                raise ValueError(f"Số edges không được âm, nhận được {n_edges}")
            if avg_ms < 0:
                raise ValueError(f"Average time không được âm, nhận được {avg_ms}")

            records.append(
                {
                    "n_nodes": n_nodes,
                    "n_edges": n_edges,
                    "avg_ms": avg_ms,
                }
            )

    records.sort(key=lambda item: item["n_nodes"])
    return records


def compute_scaled_complexity(records: list[dict[str, Any]]) -> list[float]:
    """
    Tính đường lý thuyết O((V + E) log V) và scale về cùng mức với dữ liệu đo.

    Giá trị Big-O thô không có đơn vị ms, nên cần nhân hệ số scale.
    Hệ số scale được chọn để điểm lý thuyết đầu tiên bằng điểm đo thực tế đầu tiên.
    """
    raw_values = []

    for record in records:
        v = record["n_nodes"]
        e = record["n_edges"]
        raw = (v + e) * math.log2(max(v, 2))
        raw_values.append(raw)

    first_raw = raw_values[0]
    first_measured = records[0]["avg_ms"]

    if first_raw <= 0:
        raise ValueError("Không thể scale đường lý thuyết vì giá trị Big-O đầu tiên không hợp lệ")

    scale = first_measured / first_raw
    return [value * scale for value in raw_values]


def plot_chart(
    plt,
    records: list[dict[str, Any]],
    scaled_theory: list[float],
    output_png: Path,
    output_pdf: Path | None = None,
    use_log_scale: bool = False,
) -> None:
    """Vẽ và lưu biểu đồ performance."""
    x_values = [record["n_nodes"] for record in records]
    measured = [record["avg_ms"] for record in records]

    plt.figure(figsize=(10, 6))

    plt.plot(
        x_values,
        measured,
        marker="o",
        linewidth=2,
        label="Measured avg time",
    )

    plt.plot(
        x_values,
        scaled_theory,
        marker="s",
        linewidth=2,
        linestyle="--",
        label="Scaled O((V+E)logV)",
    )

    plt.title("Dijkstra Performance Test")
    plt.xlabel("Number of nodes (V)")
    plt.ylabel("Average time (ms)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    note = "First 2 runs are warm-up. Average time uses stable average after trimming min/max."
    plt.figtext(0.5, 0.01, note, ha="center", fontsize=9)

    if use_log_scale:
        plt.yscale("log")
        plt.title("Dijkstra Performance Test - Log Scale")

    plt.tight_layout(rect=(0, 0.04, 1, 1))

    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png, dpi=200)

    if output_pdf is not None:
        plt.savefig(output_pdf)

    plt.close()


def should_create_log_chart(records: list[dict[str, Any]]) -> bool:
    """Quyết định có cần vẽ thêm biểu đồ log scale không."""
    times = [record["avg_ms"] for record in records if record["avg_ms"] > 0]

    if len(times) < 2:
        return False

    min_time = min(times)
    max_time = max(times)

    return max_time / min_time >= 10


def print_data_summary(records: list[dict[str, Any]]) -> None:
    """In dữ liệu đã đọc để dễ kiểm tra nhanh."""
    print("Dữ liệu dùng để vẽ chart:")
    print("Nodes; Edges; AvgMs")

    for record in records:
        print(f"{record['n_nodes']}; {record['n_edges']}; {record['avg_ms']:.4f}")


def main() -> None:
    plt = import_matplotlib()

    print(f"Đọc CSV từ: {INPUT_CSV}")

    records = read_performance_csv(INPUT_CSV)

    if not records:
        raise ValueError("CSV không có dòng dữ liệu hợp lệ")

    print(f"Số dòng dữ liệu đọc được: {len(records)}")
    print_data_summary(records)

    scaled_theory = compute_scaled_complexity(records)

    CHART_DIR.mkdir(parents=True, exist_ok=True)

    plot_chart(
        plt=plt,
        records=records,
        scaled_theory=scaled_theory,
        output_png=OUTPUT_PNG,
        output_pdf=OUTPUT_PDF,
        use_log_scale=False,
    )

    print(f"Đã lưu PNG: {OUTPUT_PNG}")
    print(f"Đã lưu PDF: {OUTPUT_PDF}")

    if should_create_log_chart(records):
        plot_chart(
            plt=plt,
            records=records,
            scaled_theory=scaled_theory,
            output_png=OUTPUT_LOG_PNG,
            output_pdf=None,
            use_log_scale=True,
        )
        print(f"Đã lưu log chart PNG: {OUTPUT_LOG_PNG}")
    else:
        print("Không tạo log chart vì dữ liệu không chênh lệch đủ lớn.")

    print("Ghi chú: các run warm-up không được tính. Average time lấy từ cột avg_ms_run2to5 hoặc cột tương đương trong CSV.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Lỗi: {exc}")
        sys.exit(1)