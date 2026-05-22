# QA Descriptions

File này mô tả ngắn gọn ý nghĩa các thư mục và file chính trong phần `qa/` để các thành viên trong nhóm dễ theo dõi.

## Cấu trúc chính

```text
qa/
├── bug_reports/
├── charts/
├── data_large/
├── results/
├── scripts/
├── temp/
└── testcases/
```

## `qa/testcases/`

Chứa bộ test case chính thức dùng để kiểm thử thuật toán Dijkstra.

- `test_cases_dijkstra.csv`: bảng mô tả TC01-TC15, gồm source, destination, expected distance, expected path và ghi chú.
- `graphs/`: chứa các file graph JSON riêng cho từng test case, từ `tc01.json` đến `tc15.json`.

## `qa/scripts/`

Chứa các script Python phục vụ QA/QC.

- `run_qa_test_cases.py`: chạy functional test TC01-TC15.
- `generate_large_graphs.py`: sinh graph lớn liên thông để đo performance.
- `run_performance_test.py`: đo thời gian chạy Dijkstra trên graph lớn.
- `check_results.py`: tổng hợp kết quả test và sinh bug report nếu có lỗi.
- `draw_performance_chart.py`: vẽ biểu đồ performance từ file CSV kết quả.

## `qa/results/`

Chứa kết quả đầu ra sau khi chạy các script.

- `functional_test_results.csv`: kết quả functional test.
- `large_graph_summary.csv`: thông tin tổng kết các graph lớn đã sinh.
- `performance_results.csv`: kết quả đo hiệu năng Dijkstra.

## `qa/data_large/`

Chứa các graph lớn dùng riêng cho performance test.

Các file chính:

```text
graph_100.json
graph_500.json
graph_1000.json
graph_5000.json
graph_10000.json
```

Các graph này được sinh bởi `generate_large_graphs.py`.

## `qa/charts/`

Chứa biểu đồ performance dùng cho báo cáo hoặc slide thuyết trình.

- `dijkstra_performance.png`: biểu đồ performance dạng thường.
- `dijkstra_performance.pdf`: bản PDF của biểu đồ.
- `dijkstra_performance_log.png`: biểu đồ performance dùng log scale.

## `qa/bug_reports/`

Chứa bug report tự động sinh từ `check_results.py`.

- `bug_report.md`: ghi các bug Critical/Major nếu có. Nếu không có lỗi nghiêm trọng, file ghi rằng không có bug cần báo cáo.

## `qa/temp/`

Chứa file tạm trong quá trình kiểm thử.

Không nên commit các file sinh tạm trong thư mục này. Chỉ nên giữ `.gitkeep` nếu cần giữ lại folder rỗng.

## Các file tổng hợp

- `qa_summary.md`: tóm tắt kết quả QA/QC hiện tại.
- `qa_descriptions.md`: mô tả ngắn gọn ý nghĩa các thư mục và file trong `qa/`.

## Cách chạy lại toàn bộ QA

Chạy từ thư mục gốc repo:

```powershell
python qa/scripts/run_qa_test_cases.py
python qa/scripts/generate_large_graphs.py
python qa/scripts/run_performance_test.py
python qa/scripts/check_results.py
python qa/scripts/draw_performance_chart.py
```

## Kết quả kỳ vọng

```text
Functional test: 15/15 PASS
Large graph: connected và format OK
Performance 10K: PASS dưới ngưỡng 5000 ms
Bug report: không có bug Critical hoặc Major
```
