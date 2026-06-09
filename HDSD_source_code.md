---

## Hướng dẫn sử dụng mã nguồn và kiểm thử chương trình

### 1. Mục đích

Dự án cài đặt chương trình tìm đường đi ngắn nhất trong khuôn viên HUST bằng thuật toán **Dijkstra** trên đồ thị có trọng số.

Chương trình có hai cách sử dụng chính:

* Chạy bằng **console** thông qua `main.py`.
* Chạy bằng **giao diện đồ họa** thông qua `GUI.py`.

Ngoài ra, dự án có thư mục `qa/` chứa các script kiểm thử chức năng, kiểm thử hiệu năng, sinh dữ liệu lớn và vẽ biểu đồ kết quả.

---

### 2. Cấu trúc thư mục chính

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
│   ├── data_large/
│   ├── scripts/
│   ├── results/
│   ├── bug_reports/
│   └── charts/
│
├── GUI.py
├── main.py
├── loaddata.py
├── hust_map.png
└── README.md
```

Ý nghĩa các phần chính:

| Thành phần     | Vai trò                                                  |
| -------------- | -------------------------------------------------------- |
| `core/`        | Chứa phần cài đặt cấu trúc dữ liệu và thuật toán chính   |
| `data/`        | Chứa dữ liệu bản đồ HUST và lịch sử tìm kiếm             |
| `qa/`          | Chứa test case, script kiểm thử, kết quả test và biểu đồ |
| `main.py`      | Chạy chương trình ở chế độ console                       |
| `GUI.py`       | Chạy chương trình ở chế độ giao diện đồ họa              |
| `loaddata.py`  | Đọc dữ liệu bản đồ từ file JSON                          |
| `hust_map.png` | Ảnh nền bản đồ dùng cho GUI                              |

---

### 3. Yêu cầu môi trường

Khuyến nghị sử dụng Python 3.10 trở lên.

Kiểm tra phiên bản Python:

```bash
python --version
```

hoặc:

```bash
python3 --version
```

Chương trình console chỉ dùng thư viện chuẩn của Python.

Chương trình GUI cần thêm `Pillow`.

Script vẽ biểu đồ hiệu năng cần thêm `matplotlib`.

Cài thư viện cần thiết:

```bash
pip install Pillow matplotlib
```

Nếu có file `requirements.txt`, có thể cài bằng:

```bash
pip install -r requirements.txt
```

Nội dung `requirements.txt` đề xuất:

```text
Pillow
matplotlib
```

---

### 4. Cách chạy chương trình

Tất cả lệnh bên dưới cần chạy từ **thư mục gốc của repo**, tức thư mục chứa `main.py`, `GUI.py`, `core/`, `data/`, `qa/`.

Ví dụ:

```bash
cd DSA-MI3060
```

---

## 5. Chạy chương trình console

Chạy lệnh:

```bash
python main.py
```

Nếu máy dùng lệnh `python3`, chạy:

```bash
python3 main.py
```

Chương trình console sẽ thực hiện các bước:

1. Đọc dữ liệu bản đồ từ file dữ liệu.
2. Hiển thị danh sách các địa điểm và ID tương ứng.
3. Yêu cầu nhập ID điểm bắt đầu.
4. Yêu cầu nhập ID điểm đích.
5. Chạy thuật toán Dijkstra.
6. In ra đường đi ngắn nhất và tổng khoảng cách.

Ví dụ thao tác:

```text
Nhập ID điểm BẮT ĐẦU: 1
Nhập ID điểm ĐẾN: 11
```

Kết quả mong muốn:

```text
TỔNG QUÃNG ĐƯỜNG: ...
QUÃNG ĐƯỜNG DI CHUYỂN LÀ:
Địa điểm bắt đầu -> ... -> Địa điểm kết thúc
```

Nếu không tồn tại đường đi, chương trình sẽ thông báo không tìm thấy đường đi khả thi.

Để thoát khỏi chương trình console, nhấn `Enter` tại bước nhập ID.

---

## 6. Chạy chương trình GUI

Chạy lệnh:

```bash
python GUI.py
```

hoặc:

```bash
python3 GUI.py
```

Giao diện sẽ hiển thị bản đồ HUST và các ô chọn địa điểm.

Cách sử dụng:

1. Chọn điểm xuất phát.
2. Chọn điểm đến.
3. Nhấn nút tìm đường / trực quan hóa.
4. Quan sát quá trình duyệt đồ thị.
5. Xem kết quả đường đi ngắn nhất và tổng khoảng cách.

Các file cần có để GUI hoạt động:

```text
GUI.py
hust_map.png
data/map_data.json
```

Nếu GUI không mở được, kiểm tra lại:

* Đã cài `Pillow` chưa.
* Có file `hust_map.png` trong thư mục gốc chưa.
* Đang chạy lệnh từ đúng thư mục gốc của repo chưa.

---

## 7. Dữ liệu đầu vào

File dữ liệu bản đồ chính nằm trong thư mục:

```text
data/map_data.json
```

Cấu trúc dữ liệu gồm hai phần chính:

```json
{
  "nodes": [
    {
      "id": 1,
      "name": "Tên địa điểm",
      "lat": 21.0,
      "lng": 105.0,
      "x": 100,
      "y": 200
    }
  ],
  "edges": [
    {
      "from": 1,
      "to": 2,
      "weight": 120
    }
  ]
}
```

Ý nghĩa:

| Trường       | Ý nghĩa                                   |
| ------------ | ----------------------------------------- |
| `id`         | Mã định danh của địa điểm                 |
| `name`       | Tên địa điểm                              |
| `lat`, `lng` | Tọa độ địa lý tham khảo                   |
| `x`, `y`     | Tọa độ hiển thị trên ảnh bản đồ trong GUI |
| `from`       | Đỉnh đầu của cạnh                         |
| `to`         | Đỉnh cuối của cạnh                        |
| `weight`     | Trọng số cạnh, tương ứng khoảng cách      |

Trong chương trình, các cạnh được xử lý như đường đi hai chiều.

---

## 8. Cách chạy bộ test chức năng

Bộ test chức năng nằm trong thư mục:

```text
qa/testcases/
```

Script chạy test:

```text
qa/scripts/run_qa_test_cases.py
```

Chạy lệnh:

```bash
python qa/scripts/run_qa_test_cases.py
```

hoặc:

```bash
python3 qa/scripts/run_qa_test_cases.py
```

Script này sẽ:

1. Đọc danh sách test case từ `qa/testcases/test_cases_dijkstra.csv`.
2. Đọc các graph test tương ứng trong `qa/testcases/graphs/`.
3. Chạy thuật toán Dijkstra với từng test case.
4. So sánh kết quả thực tế với kết quả kỳ vọng.
5. Ghi kết quả vào file:

```text
qa/results/functional_test_results.csv
```

Kết quả mong muốn:

```text
15/15 PASS
```

Các nhóm test chính:

| Nhóm test  | Mục đích                                                                                                        |
| ---------- | --------------------------------------------------------------------------------------------------------------- |
| Happy path | Kiểm tra các đường đi hợp lệ thông thường                                                                       |
| Edge case  | Kiểm tra trường hợp biên như source trùng destination, đồ thị không liên thông, nhiều đường ngắn nhất bằng nhau |
| Error case | Kiểm tra node nguồn hoặc node đích không tồn tại                                                                |

---

## 9. Cách sinh dữ liệu lớn

Script sinh graph lớn:

```text
qa/scripts/generate_large_graphs.py
```

Chạy lệnh:

```bash
python qa/scripts/generate_large_graphs.py
```

hoặc:

```bash
python3 qa/scripts/generate_large_graphs.py
```

Script sẽ tạo các file graph lớn trong thư mục:

```text
qa/data_large/
```

Các kích thước dữ liệu gồm:

```text
graph_100.json
graph_500.json
graph_1000.json
graph_5000.json
graph_10000.json
```

Mục đích của bước này:

* Kiểm tra thuật toán với dữ liệu lớn.
* Đảm bảo graph sinh ra là graph liên thông.
* Đảm bảo không có self-loop.
* Đảm bảo không có cạnh trùng.
* Đảm bảo trọng số cạnh là số dương.

Kết quả tổng hợp được ghi vào:

```text
qa/results/large_graph_summary.csv
```

---

## 10. Cách chạy kiểm thử hiệu năng

Script kiểm thử hiệu năng:

```text
qa/scripts/run_performance_test.py
```

Chạy lệnh:

```bash
python qa/scripts/run_performance_test.py
```

hoặc:

```bash
python3 qa/scripts/run_performance_test.py
```

Script này sẽ:

1. Đọc các graph lớn trong `qa/data_large/`.
2. Chạy thuật toán Dijkstra trên từng graph.
3. Đo thời gian chạy thuật toán.
4. Lặp nhiều lần để giảm sai số đo.
5. Ghi kết quả vào file:

```text
qa/results/performance_results.csv
```

Kết quả cần quan sát:

* Graph `graph_10000.json` có 10000 node.
* Trường `pass_10k_under_5000ms` cần có giá trị `PASS`.

---

## 11. Cách kiểm tra tổng hợp kết quả test

Sau khi chạy functional test và performance test, chạy script tổng hợp:

```bash
python qa/scripts/check_results.py
```

hoặc:

```bash
python3 qa/scripts/check_results.py
```

Script này đọc các file kết quả:

```text
qa/results/functional_test_results.csv
qa/results/performance_results.csv
```

và sinh báo cáo lỗi tại:

```text
qa/bug_reports/bug_report.md
```

Kết quả mong muốn:

```text
Không có bug nào cần báo cáo.
```

Nếu có lỗi, file `bug_report.md` sẽ ghi rõ loại lỗi, ví dụ:

* Test chức năng bị FAIL.
* Kết quả thuật toán sai.
* Performance test vượt ngưỡng thời gian.
* Graph lớn không liên thông.
* Dữ liệu test không hợp lệ.

---

## 12. Cách vẽ biểu đồ hiệu năng

Script vẽ biểu đồ:

```text
qa/scripts/draw_performance_chart.py
```

Chạy lệnh:

```bash
python qa/scripts/draw_performance_chart.py
```

hoặc:

```bash
python3 qa/scripts/draw_performance_chart.py
```

Script này đọc file:

```text
qa/results/performance_results.csv
```

và sinh biểu đồ trong thư mục:

```text
qa/charts/
```

Các file biểu đồ đầu ra:

```text
qa/charts/dijkstra_performance.png
qa/charts/dijkstra_performance.pdf
qa/charts/dijkstra_performance_log.png
```

Các biểu đồ này có thể dùng để minh họa phần đánh giá hiệu năng trong báo cáo hoặc slide thuyết trình.

---

## 13. Thứ tự kiểm tra toàn bộ dự án

Khi giảng viên hoặc người chấm muốn kiểm tra toàn bộ chương trình, có thể chạy theo thứ tự sau:

```bash
python qa/scripts/run_qa_test_cases.py
python qa/scripts/generate_large_graphs.py
python qa/scripts/run_performance_test.py
python qa/scripts/check_results.py
python qa/scripts/draw_performance_chart.py
```

Nếu dùng `python3`:

```bash
python3 qa/scripts/run_qa_test_cases.py
python3 qa/scripts/generate_large_graphs.py
python3 qa/scripts/run_performance_test.py
python3 qa/scripts/check_results.py
python3 qa/scripts/draw_performance_chart.py
```

Ý nghĩa từng bước:

| Bước | Lệnh                        | Mục đích                                                     |
| ---- | --------------------------- | ------------------------------------------------------------ |
| 1    | `run_qa_test_cases.py`      | Kiểm tra độ đúng của thuật toán trên các test case chức năng |
| 2    | `generate_large_graphs.py`  | Sinh graph lớn để kiểm thử hiệu năng                         |
| 3    | `run_performance_test.py`   | Đo thời gian chạy thuật toán Dijkstra                        |
| 4    | `check_results.py`          | Tổng hợp kết quả pass/fail và sinh bug report                |
| 5    | `draw_performance_chart.py` | Vẽ biểu đồ hiệu năng                                         |

---

## 14. Kết quả kiểm thử hiện tại

Kết quả kiểm thử hiện tại của nhóm:

```text
Functional test: 15/15 PASS
Performance test với graph_10000.json: PASS
Bug report: Không có bug nào cần báo cáo
```

Các file kết quả có thể kiểm tra trực tiếp:

```text
qa/results/functional_test_results.csv
qa/results/performance_results.csv
qa/bug_reports/bug_report.md
qa/charts/dijkstra_performance.png
qa/charts/dijkstra_performance_log.png
```

---

## 15. Một số test case tiêu biểu

| Test case | Mục đích                           | Kết quả kỳ vọng                      |
| --------- | ---------------------------------- | ------------------------------------ |
| TC01      | Đường đi ngắn nhất thông thường    | PASS                                 |
| TC06      | Source trùng destination           | Khoảng cách bằng 0                   |
| TC07      | Đồ thị không liên thông            | Không tìm thấy đường đi              |
| TC10      | Node đích không tồn tại            | Không tìm thấy đường đi              |
| TC11      | Node nguồn không tồn tại           | Không tìm thấy đường đi              |
| TC13      | Có nhiều đường ngắn nhất bằng nhau | Chấp nhận một trong các đường đúng   |
| TC14      | Đồ thị có chu trình                | Vẫn tìm đúng đường đi ngắn nhất      |
| TC15      | Có cạnh trùng khác trọng số        | Chọn đường có tổng trọng số nhỏ nhất |

---

## 16. Lưu ý khi chấm hoặc chạy lại mã nguồn

* Cần chạy lệnh từ thư mục gốc của repo.
* Không nên di chuyển riêng lẻ các file `.py`, vì chương trình phụ thuộc vào cấu trúc thư mục.
* `data/map_data.json` là dữ liệu bản đồ chính.
* `hust_map.png` là ảnh nền dùng cho giao diện GUI.
* `qa/testcases/test_cases_dijkstra.csv` là bảng test case chính thức.
* `qa/results/functional_test_results.csv` là kết quả test chức năng.
* `qa/results/performance_results.csv` là kết quả test hiệu năng.
* Nếu chạy GUI, cần cài `Pillow`.
* Nếu chạy script biểu đồ, cần cài `matplotlib`.

---

## 17. Lỗi thường gặp và cách xử lý

### 17.1. Lỗi không tìm thấy module

Thông báo có thể gặp:

```text
ModuleNotFoundError
```

Cách xử lý:

* Đảm bảo đang chạy lệnh từ thư mục gốc repo.
* Đảm bảo thư mục `core/` tồn tại.
* Không đổi tên hoặc di chuyển các file trong `core/`.

---

### 17.2. Lỗi không tìm thấy file dữ liệu

Thông báo có thể gặp:

```text
FileNotFoundError
```

Cách xử lý:

* Kiểm tra file `data/map_data.json` có tồn tại.
* Kiểm tra đang chạy lệnh từ đúng thư mục gốc.
* Kiểm tra lại đường dẫn trong hàm đọc dữ liệu nếu đã thay đổi cấu trúc thư mục.

---

### 17.3. GUI không mở được ảnh nền

Cách xử lý:

* Kiểm tra file `hust_map.png` có nằm trong thư mục gốc repo.
* Không đổi tên file ảnh nền nếu chưa sửa code tương ứng.
* Đảm bảo đã cài thư viện `Pillow`.

Cài lại bằng lệnh:

```bash
pip install Pillow
```

---

### 17.4. Không vẽ được biểu đồ hiệu năng

Cách xử lý:

* Kiểm tra đã cài `matplotlib`.
* Kiểm tra file `qa/results/performance_results.csv` đã tồn tại.
* Nếu chưa có file kết quả hiệu năng, chạy trước:

```bash
python qa/scripts/run_performance_test.py
```

Sau đó chạy lại:

```bash
python qa/scripts/draw_performance_chart.py
```

---

## 18. Tóm tắt lệnh cần nhớ

Chạy console:

```bash
python main.py
```

Chạy GUI:

```bash
python GUI.py
```

Chạy test chức năng:

```bash
python qa/scripts/run_qa_test_cases.py
```

Sinh dữ liệu lớn:

```bash
python qa/scripts/generate_large_graphs.py
```

Chạy test hiệu năng:

```bash
python qa/scripts/run_performance_test.py
```

Tổng hợp kết quả test:

```bash
python qa/scripts/check_results.py
```

Vẽ biểu đồ hiệu năng:

```bash
python qa/scripts/draw_performance_chart.py
```

---

## 19. Kết luận

Để kiểm tra chương trình hoạt động, có thể chạy một trong hai lệnh:

```bash
python main.py
```

hoặc:

```bash
python GUI.py
```

Để kiểm tra thuật toán có vượt qua bộ test case đã thiết kế hay không, chạy:

```bash
python qa/scripts/run_qa_test_cases.py
```

Kết quả hợp lệ cần đạt:

```text
15/15 PASS
```

Để kiểm tra hiệu năng với dữ liệu lớn, chạy:

```bash
python qa/scripts/run_performance_test.py
```

Kết quả hợp lệ cần đạt:

```text
graph_10000.json: PASS dưới ngưỡng 5000 ms
```

Như vậy, mã nguồn có thể được đánh giá ở ba mức:

1. Chạy chương trình thực tế bằng console hoặc GUI.
2. Chạy functional test để kiểm tra độ đúng của thuật toán.
3. Chạy performance test để kiểm tra khả năng xử lý graph lớn.
