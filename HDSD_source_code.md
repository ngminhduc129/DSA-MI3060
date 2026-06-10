## Hướng dẫn chạy và kiểm thử mã nguồn

### 1. Môi trường

Yêu cầu:

* Python 3.10 trở lên
* Thư viện ngoài:

  * `Pillow`: dùng cho GUI
  * `matplotlib`: dùng cho script vẽ biểu đồ hiệu năng

Cài đặt:

```bash
pip install Pillow matplotlib
```

Tất cả lệnh bên dưới cần chạy từ thư mục gốc của repo.

---

### 2. Cấu trúc chính

```text
DSA-MI3060/
├── core/
│   ├── MinHeap_Graph.py
│   ├── findShortestPath_reconstructPath.py
│   └── saveData.py
│
├── data/
│   ├── map_data.json
│   ├── danh_sach_ke.json
│   └── history_search.txt
│
├── qa/
│   ├── testcases/
│   │   ├── test_cases_dijkstra.csv
│   │   └── graphs/
│   │       └── *.json
│   │
│   ├── data_large/
│   │   └── graph_*.json
│   │
│   ├── scripts/
│   │   ├── run_qa_test_cases.py
│   │   ├── generate_large_graphs.py
│   │   ├── run_performance_test.py
│   │   ├── check_results.py
│   │   └── draw_performance_chart.py
│   │
│   ├── results/
│   │   ├── functional_test_results.csv
│   │   ├── large_graph_summary.csv
│   │   └── performance_results.csv
│   │
│   ├── bug_reports/
│   │   └── bug_report.md
│   │
│   ├── charts/
│   │   ├── dijkstra_performance.png
│   │   ├── dijkstra_performance.pdf
│   │   └── dijkstra_performance_log.png
│   │
│   ├── qa_descriptions.md
│   └── qa_summary.md
│
├── main.py
├── GUI.py
├── loaddata.py
├── mangluoi.py
├── vebando.py
├── hust_map.png
├── README.md
└── .gitignore
```

Các thành phần chính:

| Thành phần                                 | Vai trò                                                            |
| ------------------------------------------ | ------------------------------------------------------------------ |
| `core/MinHeap_Graph.py`                    | Cài đặt `Graph` và `MinHeap` dùng cho thuật toán                   |
| `core/findShortestPath_reconstructPath.py` | Cài đặt Dijkstra và truy vết đường đi ngắn nhất                    |
| `core/saveData.py`                         | Lưu kết quả tìm đường                                              |
| `data/map_data.json`                       | Dữ liệu bản đồ HUST chính, gồm danh sách đỉnh và cạnh              |
| `data/danh_sach_ke.json`                   | Dữ liệu danh sách kề được sinh từ bản đồ                           |
| `data/history_search.txt`                  | Lưu lịch sử / kết quả tìm kiếm                                     |
| `main.py`                                  | Chạy chương trình ở chế độ console                                 |
| `GUI.py`                                   | Chạy chương trình ở chế độ giao diện đồ họa bằng `tkinter`         |
| `loaddata.py`                              | Đọc dữ liệu bản đồ từ file JSON                                    |
| `mangluoi.py`                              | Script phụ để trực quan hóa / kiểm tra mạng lưới bản đồ            |
| `vebando.py`                               | Script phụ để sinh danh sách kề từ dữ liệu bản đồ                  |
| `hust_map.png`                             | Ảnh nền bản đồ dùng cho GUI                                        |
| `qa/testcases/`                            | Bộ test case chức năng cho thuật toán Dijkstra                     |
| `qa/data_large/`                           | Dữ liệu graph lớn dùng cho performance test                        |
| `qa/scripts/`                              | Các script chạy test, sinh dữ liệu, tổng hợp kết quả và vẽ biểu đồ |
| `qa/results/`                              | Kết quả functional test và performance test                        |
| `qa/bug_reports/`                          | Báo cáo lỗi sau khi tổng hợp kết quả test                          |
| `qa/charts/`                               | Biểu đồ hiệu năng của thuật toán                                   |
| `qa/qa_descriptions.md`                    | Mô tả chi tiết bộ kiểm thử QA                                      |
| `qa/qa_summary.md`                         | Tóm tắt kết quả kiểm thử QA                                        |
| `.gitignore`                               | Khai báo các file/thư mục không đưa vào Git                        |

---

### 3. Chạy chương trình

#### 3.1. Chạy console

```bash
python main.py
```

Chương trình sẽ yêu cầu nhập ID điểm bắt đầu và ID điểm đích, sau đó in ra:

* Tổng khoảng cách ngắn nhất
* Lộ trình tương ứng
* Thông báo nếu không tồn tại đường đi

#### 3.2. Chạy GUI

```bash
python GUI.py
```

Giao diện cho phép chọn điểm bắt đầu, điểm kết thúc và trực quan hóa quá trình tìm đường trên bản đồ.

Các file cần có để GUI hoạt động:

```text
GUI.py
hust_map.png
data/map_data.json
```

---

### 4. Chạy functional test

Bộ test chức năng nằm tại:

```text
qa/testcases/
```

Chạy:

```bash
python qa/scripts/run_qa_test_cases.py
```

Script sẽ đọc các test case trong:

```text
qa/testcases/test_cases_dijkstra.csv
qa/testcases/graphs/
```

và ghi kết quả vào:

```text
qa/results/functional_test_results.csv
```

Kết quả kỳ vọng:

```text
15/15 PASS
```

Các nhóm test bao gồm:

| Nhóm         | Mục đích                                                                   |
| ------------ | -------------------------------------------------------------------------- |
| Normal cases | Kiểm tra các đường đi hợp lệ                                               |
| Edge cases   | Source trùng destination, graph không liên thông, nhiều đường đi ngắn nhất |
| Error cases  | Source hoặc destination không tồn tại                                      |

---

### 5. Chạy performance test

Nếu cần sinh lại dữ liệu graph lớn:

```bash
python qa/scripts/generate_large_graphs.py
```

Dữ liệu được tạo tại:

```text
qa/data_large/
```

Chạy kiểm thử hiệu năng:

```bash
python qa/scripts/run_performance_test.py
```

Kết quả được ghi vào:

```text
qa/results/performance_results.csv
```

Tiêu chí chính:

```text
graph_10000.json: PASS dưới ngưỡng 5000 ms
```

---

### 6. Tổng hợp kết quả test

Sau khi chạy functional test và performance test:

```bash
python qa/scripts/check_results.py
```

Báo cáo được sinh tại:

```text
qa/bug_reports/bug_report.md
```

Kết quả mong muốn:

```text
Không có bug nào cần báo cáo.
```

---

### 7. Vẽ biểu đồ hiệu năng

```bash
python qa/scripts/draw_performance_chart.py
```

Biểu đồ được sinh tại:

```text
qa/charts/
```

Các file đầu ra:

```text
dijkstra_performance.png
dijkstra_performance.pdf
dijkstra_performance_log.png
```

---

### 8. Quy trình kiểm tra khuyến nghị

Để kiểm tra toàn bộ mã nguồn, chạy lần lượt:

```bash
python qa/scripts/run_qa_test_cases.py
python qa/scripts/generate_large_graphs.py
python qa/scripts/run_performance_test.py
python qa/scripts/check_results.py
python qa/scripts/draw_performance_chart.py
```

Hoặc chỉ kiểm tra nhanh độ đúng thuật toán:

```bash
python qa/scripts/run_qa_test_cases.py
```

---

### 9. Kết quả kiểm thử hiện tại

Kết quả hiện tại của nhóm:

```text
Functional test: 15/15 PASS
Performance test với graph_10000.json: PASS
Bug report: Không có bug nào cần báo cáo
```

Các file kết quả có thể đối chiếu:

```text
qa/results/functional_test_results.csv
qa/results/performance_results.csv
qa/bug_reports/bug_report.md
```

---

### 10. Ghi chú khi chấm

* Chạy lệnh từ thư mục gốc của repo.
* Không tách riêng các file `.py` khỏi cấu trúc thư mục hiện tại.
* Dữ liệu bản đồ chính nằm trong `data/map_data.json`.
* GUI phụ thuộc vào `hust_map.png`.
* Thuật toán chính sử dụng `Graph` và `MinHeap` tự cài đặt trong `core/`.
* Bộ test QA được đặt trong `qa/` và có thể chạy độc lập với GUI.
