"""
Đọc kết quả functional test và performance test để tổng hợp pass/fail.

Input:
- qa/results/functional_test_results.csv
- qa/results/performance_results.csv

Output:
- In tổng kết ra terminal.
- Ghi bug report vào qa/bug_reports/bug_report.md.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
QA_DIR = SCRIPT_DIR.parent
RESULTS_DIR = QA_DIR / "results"
BUG_DIR = QA_DIR / "bug_reports"

FUNC_CSV = RESULTS_DIR / "functional_test_results.csv"
PERF_CSV = RESULTS_DIR / "performance_results.csv"
BUG_MD = BUG_DIR / "bug_report.md"

THRESHOLD_10K_MS = 5000.0
STD_NOISE_RATIO = 0.20


def read_csv(path: Path) -> list[dict]:
    #Đọc CSV, nếu file không tồn tại thì trả về list rỗng
    if not path.exists():
        print(f"Không tìm thấy file: {path}")
        return []

    with path.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def severity_functional(row: dict) -> str:
    #Xác định severity cho functional bug
    note = row.get("Note", "")
    actual_dist = row.get("ActualDistance", "")

    if actual_dist == "CRASH":
        return "Critical"
    if "distance" in note.lower() or row.get("ExpectedDistance") != row.get("ActualDistance"):
        return "Critical"
    return "Major"


def check_functional(rows: list[dict]) -> list[dict]:
    #Lọc các test case FAIL từ functional_test_results.csv
    bugs = []

    for row in rows:
        if row.get("Status") == "PASS":
            continue
        row["Severity"] = severity_functional(row)
        bugs.append(row)

    return bugs


def complexity_scale(v: int, e: int) -> float:
    #Tính thang đo tham khảo theo O((V + E) log V)
    return (v + e) * math.log2(max(v, 2))


def get_std_ratio(row: dict) -> float:
    #Đọc std_ratio nếu có, nếu không thì tính từ std_ms và avg_ms_run2to5
    if row.get("std_ratio") not in (None, ""):
        try:
            return float(row["std_ratio"])
        except Exception:
            pass

    try:
        avg = float(row.get("avg_ms_run2to5", 0))
        std = float(row.get("std_ms", 0))
        return std / avg if avg > 0 else 0.0
    except Exception:
        return 0.0


def check_performance(rows: list[dict]) -> list[dict]:
    #Kiểm tra performance result và trả về danh sách issue
    issues = []

    for row in rows:
        n = int(row.get("n_nodes", 0))
        avg_ms = float(row.get("avg_ms_run2to5", 0))
        connected = row.get("connected", "YES")
        reachable = row.get("reachable", "YES")
        loader_used = row.get("loader_used", "")
        std_ratio = get_std_ratio(row)

        if n == 10000 and avg_ms >= THRESHOLD_10K_MS:
            issues.append(
                {
                    "n_nodes": n,
                    "avg_ms": avg_ms,
                    "Severity": "Critical",
                    "Issue": f"graph_{n}: avg={avg_ms:.1f} ms vượt ngưỡng {THRESHOLD_10K_MS:.0f} ms",
                }
            )

        if connected != "YES":
            issues.append(
                {
                    "n_nodes": n,
                    "avg_ms": avg_ms,
                    "Severity": "Major",
                    "Issue": f"graph_{n}.json không liên thông, kết quả đo không đáng tin",
                }
            )

        if reachable != "YES":
            issues.append(
                {
                    "n_nodes": n,
                    "avg_ms": avg_ms,
                    "Severity": "Major",
                    "Issue": f"graph_{n}.json không tìm được đường từ source đến dest",
                }
            )

        if loader_used == "manual Graph.addEdge fallback":
            issues.append(
                {
                    "n_nodes": n,
                    "avg_ms": avg_ms,
                    "Severity": "Info",
                    "Issue": f"graph_{n}.json đang dùng manual fallback, nên kiểm tra load_data hoặc loadData",
                }
            )

        if std_ratio > STD_NOISE_RATIO:
            issues.append(
                {
                    "n_nodes": n,
                    "avg_ms": avg_ms,
                    "Severity": "Info",
                    "Issue": f"graph_{n}.json có std/avg={std_ratio:.0%}, lớn hơn 20%, nên đo lại nếu cần",
                }
            )

    sorted_rows = sorted(rows, key=lambda r: int(r.get("n_nodes", 0)))

    by_n = {int(r.get("n_nodes", 0)): r for r in sorted_rows}
    r1k = by_n.get(1000)
    r10k = by_n.get(10000)
    ratio_1k_10k = None

    if r1k and r10k:
        avg_1k = float(r1k.get("avg_ms_run2to5", 0))
        avg_10k = float(r10k.get("avg_ms_run2to5", 0))
        if avg_1k > 0:
            ratio_1k_10k = avg_10k / avg_1k

    for i in range(1, len(sorted_rows)):
        prev = sorted_rows[i - 1]
        curr = sorted_rows[i]

        prev_v = int(prev["n_nodes"])
        prev_e = int(prev["n_edges"])
        curr_v = int(curr["n_nodes"])
        curr_e = int(curr["n_edges"])
        prev_avg = float(prev["avg_ms_run2to5"])
        curr_avg = float(curr["avg_ms_run2to5"])

        if prev_avg <= 0:
            continue

        actual_ratio = curr_avg / prev_avg
        theoretical_ratio = complexity_scale(curr_v, curr_e) / complexity_scale(prev_v, prev_e)

        if actual_ratio > 100 and curr_avg >= THRESHOLD_10K_MS:
            issues.append(
                {
                    "n_nodes": curr_v,
                    "avg_ms": curr_avg,
                    "Severity": "Critical",
                    "Issue": (
                        f"Tăng trưởng {prev_v} đến {curr_v}: "
                        f"actual={actual_ratio:.1f}x, theoretical={theoretical_ratio:.1f}x. "
                        "Nghi bug O(V^2)"
                    ),
                }
            )

        elif actual_ratio > theoretical_ratio * 5:
            severity = "Info"
            if curr_v == 10000 and curr_avg >= THRESHOLD_10K_MS:
                severity = "Major"
            elif ratio_1k_10k is not None and ratio_1k_10k > 100:
                severity = "Major"

            issues.append(
                {
                    "n_nodes": curr_v,
                    "avg_ms": curr_avg,
                    "Severity": severity,
                    "Issue": (
                        f"Tăng trưởng {prev_v} đến {curr_v}: "
                        f"actual={actual_ratio:.1f}x, theoretical={theoretical_ratio:.1f}x. "
                        "Đây là cảnh báo tham khảo, chưa đủ kết luận bug nếu 10K vẫn PASS"
                    ),
                }
            )

    return issues


def make_bug_entry(
    idx: int,
    tc_id: str,
    severity: str,
    desc: str,
    expected: str,
    actual: str,
    steps: str,
    suspect: str,
) -> str:
    return f"""
### BUG-{idx:03d} | {severity.upper()} | {tc_id}

| Trường | Nội dung |
|---|---|
| TC liên quan | {tc_id} |
| Mức độ | {severity} |
| Mô tả | {desc} |
| Expected | {expected} |
| Actual | {actual} |
| Bước tái hiện | {steps} |
| Nghi ngờ nguyên nhân | {suspect} |
| Trạng thái | Mở |
| Gửi cho | TV2 |

---"""


def write_bug_report(func_bugs: list[dict], perf_issues: list[dict]) -> None:
    #Ghi bug_report.md từ danh sách bug và issue
    BUG_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Bug Report - TV4\n",
        "> Tự động sinh từ check_results.py\n",
        f"> Nguồn: {FUNC_CSV.name} và {PERF_CSV.name}\n",
        "\n---\n",
    ]

    idx = 1

    if func_bugs:
        lines.append("## Functional bugs\n")

        for bug in func_bugs:
            tc_id = bug.get("ID", "?")
            severity = bug.get("Severity", "Major")
            desc = bug.get("Description", "")
            exp_d = bug.get("ExpectedDistance", "")
            exp_p = bug.get("ExpectedPath", "")
            act_d = bug.get("ActualDistance", "")
            act_p = bug.get("ActualPath", "")
            note = bug.get("Note", "")

            expected = f"distance={exp_d}, path={exp_p}"
            actual = f"distance={act_d}, path={act_p}"
            if act_d == "CRASH":
                actual = f"CRASH - {note}"

            steps = (
                "1. Chạy run_qa_test_cases.py\n"
                f"2. Xem dòng {tc_id} trong functional_test_results.csv"
            )
            suspect = note if note else "Cần kiểm tra lại findShortestPath hoặc reconstructPath"

            lines.append(make_bug_entry(idx, tc_id, severity, desc, expected, actual, steps, suspect))
            idx += 1

    perf_reportable = [p for p in perf_issues if p["Severity"] in ("Critical", "Major")]

    if perf_reportable:
        lines.append("\n## Performance issues\n")

        for issue in perf_reportable:
            n_nodes = issue["n_nodes"]
            severity = issue["Severity"]
            desc = issue["Issue"]
            tc_id = f"PERF-{n_nodes}"
            steps = (
                "1. Chạy generate_large_graphs.py\n"
                "2. Chạy run_performance_test.py\n"
                f"3. Xem dòng n_nodes={n_nodes} trong performance_results.csv"
            )
            suspect = (
                "Vòng lặp lồng nhau không cần thiết trong Dijkstra hoặc MinHeap"
                if "O(V^2)" in desc
                else "Kiểm tra graph generator hoặc cấu hình source/dest"
            )

            lines.append(
                make_bug_entry(
                    idx,
                    tc_id,
                    severity,
                    desc,
                    "Xem pass_fail_criteria.md",
                    f"avg={issue['avg_ms']:.2f} ms",
                    steps,
                    suspect,
                )
            )
            idx += 1

    if idx == 1:
        lines.append("\nKhông có bug nào cần báo cáo.\n")

    BUG_MD.write_text("\n".join(lines), encoding="utf-8")


SEVERITY_ORDER = {"Critical": 0, "Major": 1, "Minor": 2, "Info": 3}


def print_summary(
    func_rows: list[dict],
    func_bugs: list[dict],
    perf_rows: list[dict],
    perf_issues: list[dict],
) -> None:
    #In tổng kết kiểm thử ra terminal
    total_func = len(func_rows)
    passed_func = sum(1 for r in func_rows if r.get("Status") == "PASS")

    sep = "=" * 65

    print()
    print(sep)
    print("Tổng kết kiểm thử TV4")
    print(sep)

    print(f"\nFunctional: {passed_func}/{total_func} PASS")
    if func_bugs:
        print("Các test case FAIL:")
        for bug in sorted(func_bugs, key=lambda b: SEVERITY_ORDER.get(b["Severity"], 9)):
            sev = bug["Severity"]
            print(f"{sev}: {bug['ID']} - {bug.get('Description', '')}")
            if bug.get("Note"):
                print(f"Note: {bug['Note']}")
    else:
        print("Tất cả functional test đều PASS.")

    print(f"\nPerformance: {len(perf_rows)} kích thước đã đo")
    if perf_rows:
        print("Nodes; AvgMs; StdAvg; Check10K")
        for row in sorted(perf_rows, key=lambda x: int(x.get("n_nodes", 0))):
            n = int(row.get("n_nodes", 0))
            avg = float(row.get("avg_ms_run2to5", 0))
            std_ratio = get_std_ratio(row)
            p10 = row.get("pass_10k_under_5000ms", "")
            print(f"{n}; {avg:.3f}; {std_ratio:.1%}; {p10}")

    reportable = [p for p in perf_issues if p["Severity"] in ("Critical", "Major")]
    info = [p for p in perf_issues if p["Severity"] == "Info"]

    if reportable:
        print("\nIssue cần báo:")
        for issue in sorted(reportable, key=lambda x: SEVERITY_ORDER.get(x["Severity"], 9)):
            print(f"{issue['Severity']}: {issue['Issue']}")
    else:
        print("Không có issue Critical hoặc Major.")

    if info:
        print("\nGhi chú tham khảo:")
        for issue in info:
            print(f"Info: {issue['Issue']}")

    total_bugs = len(func_bugs) + len(reportable)
    print(f"\nBug report: {total_bugs} bug cần báo")
    print(f"Đã ghi: {BUG_MD}")
    print(sep)


def main() -> None:
    print("Đang đọc kết quả.")

    func_rows = read_csv(FUNC_CSV)
    perf_rows = read_csv(PERF_CSV)

    func_bugs = check_functional(func_rows)
    perf_issues = check_performance(perf_rows)

    write_bug_report(func_bugs, perf_issues)
    print_summary(func_rows, func_bugs, perf_rows, perf_issues)


if __name__ == "__main__":
    main()