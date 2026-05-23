# QA Summary - Dijkstra Shortest Path Project

File này tóm tắt nhanh phần QA/QC trong dự án DSA-MI3060. Mục tiêu là giúp các thành viên khác nắm được đã kiểm thử những gì, kết quả ra sao và cần dùng file nào khi báo cáo hoặc bảo vệ.

## 1. Phạm vi QA/QC

Phần QA tập trung vào thuật toán tìm đường ngắn nhất bằng Dijkstra trong project.

Các nhóm việc chính:

- Kiểm thử chức năng của `findShortestPath`.
- Chuẩn bị bộ test case TC01-TC15.
- Sinh graph lớn liên thông để đo hiệu năng.
- Đo performance của thuật toán trên nhiều kích thước graph.
- Tổng hợp kết quả pass/fail.
- Sinh bug report nếu phát hiện lỗi.
- Vẽ biểu đồ performance để đưa vào báo cáo.

TV4 chỉ kiểm thử và đánh giá, không sửa logic chính của thuật toán Dijkstra nếu không có lỗi rõ ràng.

## 2. Functional Test

Functional test dùng bộ 15 test case chính thức TC01-TC15.

File liên quan:

```text
qa/testcases/test_cases_dijkstra.csv
qa/testcases/graphs/tc01.json
qa/testcases/graphs/tc02.json
...
qa/testcases/graphs/tc15.json
qa/scripts/run_qa_test_cases.py
qa/results/functional_test_results.csv
```

Các nhóm test case:

- Happy path: kiểm tra các đường đi bình thường.
- Edge case: kiểm tra source trùng destination, graph không liên thông, nhiều shortest path, graph có chu trình, cạnh trùng khác trọng số.
- Error case: kiểm tra node nguồn hoặc node đích không tồn tại.

Kết quả hiện tại:

```text
Functional test: 15/15 PASS
```

Điều này cho thấy thuật toán trả về đúng distance/path theo bộ test case đã thiết kế.

## 3. Large Graph Generation

Graph lớn được sinh để phục vụ performance test, không dùng để thay expected result của TC01-TC15.

File liên quan:

```text
qa/scripts/generate_large_graphs.py
qa/data_large/graph_100.json
qa/data_large/graph_500.json
qa/data_large/graph_1000.json
qa/data_large/graph_5000.json
qa/data_large/graph_10000.json
qa/results/large_graph_summary.csv
```

Các kích thước graph:

```text
100 nodes / 500 edges
500 nodes / 2500 edges
1000 nodes / 5000 edges
5000 nodes / 25000 edges
10000 nodes / 50000 edges
```

Yêu cầu của graph lớn:

- Graph liên thông.
- Không có self-loop.
- Không có cạnh trùng.
- Weight lớn hơn 0.
- Edge không trỏ đến node không tồn tại.
- Node có đủ các trường cần thiết.

Kết quả hiện tại:

```text
Tất cả graph lớn đều sinh thành công.
Tất cả graph đều connected và format OK.
```

## 4. Performance Test

Performance test đo thời gian chạy Dijkstra trên các graph lớn.

File liên quan:

```text
qa/scripts/run_performance_test.py
qa/results/performance_results.csv
```

Cách đo:

- Dùng `time.perf_counter`.
- Đọc graph bằng loader thật của project nếu có thể.
- Không tính thời gian load file vào thời gian thuật toán.
- Chạy nhiều lần cho mỗi kích thước graph.
- Bỏ warm-up.
- Dùng stable average để giảm nhiễu đo hiệu năng.
- Ghi thêm `std_ratio`, `range_ms`, `loader_used`, `load_ms` để dễ kiểm tra.

Kết quả quan trọng:

```text
10000 nodes / 50000 edges: PASS
Average time nhỏ hơn ngưỡng 5000 ms
```

Nếu có dòng cảnh báo tăng trưởng hoặc std/avg cao, đó chỉ là thông tin tham khảo khi 10K vẫn PASS và functional test vẫn đúng.

## 5. Result Checking và Bug Report

Script tổng hợp kết quả:

```text
qa/scripts/check_results.py
```

Input:

```text
qa/results/functional_test_results.csv
qa/results/performance_results.csv
```

Output:

```text
qa/bug_reports/bug_report.md
```

Vai trò của `check_results.py`:

- Kiểm tra functional test có FAIL không.
- Kiểm tra performance có vượt ngưỡng không.
- Kiểm tra graph có connected không.
- Ghi bug report nếu có issue Critical hoặc Major.

Kết quả hiện tại:

```text
Bug report: 0 bug cần báo
```

Nghĩa là chưa có lỗi nghiêm trọng cần gửi lại cho thành viên phụ trách thuật toán.

## 6. Performance Chart

Biểu đồ performance được vẽ từ file CSV kết quả đo.

File liên quan:

```text
qa/scripts/draw_performance_chart.py
qa/charts/dijkstra_performance.png
qa/charts/dijkstra_performance.pdf
qa/charts/dijkstra_performance_log.png
```

Biểu đồ gồm:

- Đường thời gian đo thực tế.
- Đường lý thuyết `O((V + E) log V)` đã được scale.
- Biểu đồ thường.
- Biểu đồ log scale nếu dữ liệu chênh lệch lớn.

Biểu đồ dùng để đưa vào báo cáo hoặc slide thuyết trình.

## 7. Các lệnh chạy lại toàn bộ QA

Chạy từ thư mục gốc repo:

```powershell
python qa/scripts/run_qa_test_cases.py
python qa/scripts/generate_large_graphs.py
python qa/scripts/run_performance_test.py
python qa/scripts/check_results.py
python qa/scripts/draw_performance_chart.py
```

Thứ tự khuyến nghị:

1. Chạy functional test.
2. Sinh graph lớn.
3. Đo performance.
4. Kiểm tra kết quả và sinh bug report.
5. Vẽ biểu đồ performance.

## 8. Kết luận QA hiện tại

Tình trạng hiện tại của phần QA:

```text
Functional test: PASS
Large graph generation: PASS
Performance test 10K: PASS
Bug report: Không có bug cần báo
Chart generation: Hoàn thành
```

Có thể dùng các file trong thư mục `qa/` để commit lên GitHub và đưa vào báo cáo nhóm.

## 9. File nên đưa vào báo cáo

Các file nên trích dẫn hoặc chụp kết quả khi viết báo cáo:

```text
qa/results/functional_test_results.csv
qa/results/large_graph_summary.csv
qa/results/performance_results.csv
qa/bug_reports/bug_report.md
qa/charts/dijkstra_performance.png
qa/charts/dijkstra_performance_log.png
```

Trong báo cáo, nên nêu ngắn gọn:

- Bộ test case gồm 15 test case.
- Functional test đạt 15/15 PASS.
- Graph lớn có kích thước từ 100 đến 10000 nodes.
- Graph lớn đều connected và format OK.
- Dijkstra chạy tốt với graph 10000 nodes / 50000 edges.
- Không có bug Critical hoặc Major được phát hiện.