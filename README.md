# KẾ HOẠCH DỰ ÁN
## Hệ thống Dẫn đường trong Khuôn viên Trường học (Dijkstra)

**Nhóm thực hiện:** 5 sinh viên ngành Toán Tin từ Đại học Bách Khoa Hà Nội (HUST)  

---

## Mục lục

1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Yêu cầu nộp bài](#2-yêu-cầu-nộp-bài)
3. [Phân công nhóm](#3-phân-công-nhóm)
4. [Lịch trình 8 tuần](#4-lịch-trình-8-tuần)
5. [Phân tích bài toán](#5-phân-tích-bài-toán)
6. [Thiết kế hệ thống](#6-thiết-kế-hệ-thống)
7. [Thuật toán Dijkstra](#7-thuật-toán-dijkstra)
8. [Kiểm thử & Đo hiệu năng](#8-kiểm-thử--đo-hiệu-năng)
9. [Cấu trúc báo cáo PDF](#9-cấu-trúc-báo-cáo-pdf)
10. [Kế hoạch Video thuyết trình](#10-kế-hoạch-video-thuyết-trình)

---

## 1. Tổng quan dự án

**Ngôn ngữ lựa chọn:** C++ / Java / Python (chọn 1)

### 1.1 Mô tả bài toán

Xây dựng hệ thống tìm đường đi ngắn nhất trong khuôn viên trường học, sử dụng thuật toán Dijkstra. Người dùng chọn điểm xuất phát và điểm đích (tòa nhà, cổng, sân, thư viện...), hệ thống trả về đường đi ngắn nhất và tổng khoảng cách/thời gian.

### 1.2 Mục tiêu

- Mô hình hóa khuôn viên trường dưới dạng đồ thị có trọng số.
- Cài đặt thuật toán Dijkstra tối ưu với Priority Queue (min-heap).
- Xây dựng giao diện Console hoặc GUI thân thiện.
- Đọc/ghi dữ liệu từ file qua hàm `loadData()` và `saveData()`.
- Kiểm thử hiệu năng với 10.000+ nút và ghi lại thời gian thực thi.

---

## 2. Yêu cầu nộp bài

| Hạng mục | Yêu cầu chi tiết |
|---|---|
| Báo cáo PDF | Định dạng `.pdf`, tối đa 40 trang |
| Mã nguồn | File nén `.zip` hoặc `.rar`, có README |
| Video thuyết trình | Tối đa 20 phút, tối đa 100 MB |
| Thành viên video | Tất cả 5 người đều phải tham gia thuyết trình |
| Ngôn ngữ | C++, Java hoặc Python |
| Hàm bắt buộc | `loadData()` và `saveData()` |
| Dữ liệu test | Tạo bộ dữ liệu lớn (ví dụ: 10.000 nút) để test tốc độ |

**Nội dung báo cáo bắt buộc:**

- **Phân tích:** Xác định rõ đầu vào, đầu ra và cấu trúc dữ liệu phù hợp. Giải thích lý do lựa chọn.
- **Thiết kế:** Vẽ sơ đồ lớp (Class Diagram) nếu dùng OOP (C++/Java).
- **Triển khai:** Chia module, đề xuất thuật toán, pseudocode, phân tích Big-O (thời gian & không gian).
- **Kết luận:** Đo thời gian thực thi (Performance test) với dữ liệu lớn.
- **Phân công & đánh giá:** Mức độ hoàn thành và thái độ làm việc từng thành viên.

---

## 3. Phân công nhóm

### 3.1 Nguyễn Minh Đức — Trưởng nhóm / Thiết kế:

**Vai trò:** Project Manager · Class Diagram · Cấu trúc dữ liệu chính

**Nhiệm vụ cụ thể:**
- Lên kế hoạch tổng thể, phân công nhiệm vụ hàng tuần, theo dõi tiến độ nhóm.
- Xác định rõ đầu vào / đầu ra của bài toán.
- Chọn cấu trúc dữ liệu chính: đồ thị vô hướng có trọng số, biểu diễn bằng Adjacency List (tiết kiệm không gian với đồ thị thưa).
- Vẽ Class Diagram (UML) cho toàn hệ thống: `Graph`, `Node`, `Edge`, `Navigator`, `FileHandler`, `UI`.
- Tổng hợp phần Phân tích & Thiết kế trong báo cáo.
- Điều phối quay và dựng video thuyết trình cuối kỳ.

### 3.2 Dương Tiến Dũng — Lập trình viên Core (Thuật toán) 

**Vai trò:** Cài đặt thuật toán Dijkstra · Logic xử lý chính

**Nhiệm vụ cụ thể:**
- Cài đặt cấu trúc đồ thị (`addNode`, `addEdge`, `getNeighbors`).
- Cài đặt thuật toán Dijkstra sử dụng Priority Queue (min-heap).
- Viết hàm `findShortestPath(source, destination)`.
- Viết hàm `reconstructPath(prev[], destination)`.
- Viết pseudocode chi tiết cho thuật toán.
- Phân tích độ phức tạp thời gian `O((V + E) log V)` và không gian `O(V + E)`.
- Tạo script `generateLargeGraph(n)` tạo đồ thị ngẫu nhiên.

### 3.3 Tống Ngọc Kiên — Lập trình viên Giao diện / Dữ liệu

**Vai trò:** Console/GUI · `loadData()` · `saveData()`

**Nhiệm vụ cụ thể:**
- Khảo sát thực tế khuôn viên trường học: vẽ sơ đồ, xác định các địa điểm chính.
- Số hóa sơ đồ: gán ID cho từng nút, đo khoảng cách các cạnh.
- Xây dựng file dữ liệu đồ thị (JSON, CSV hoặc TXT).
- Viết hàm `loadData(filename)` và `saveData(filename, result)`.
- Xây dựng giao diện người dùng (Console hoặc GUI).
- Xử lý lỗi ngoại lệ (file không tồn tại, địa điểm không hợp lệ).

### 3.4 Nguyễn Khánh Toàn — Kiểm thử QA/QC

**Vai trò:** Test case · Dữ liệu lớn · Performance test

**Nhiệm vụ cụ thể:**
- Thiết kế bộ test case bao phủ đầy đủ các trường hợp.
- Tạo script sinh dữ liệu lớn tự động với các kích thước: 100 / 1.000 / 5.000 / 10.000 nút.
- Thực hiện Performance test: đo thời gian thực thi, lặp 5 lần lấy trung bình.
- Lập bảng kết quả và vẽ biểu đồ thời gian theo số nút.

### 3.5 Nguyễn Duy Hoàng — Tài liệu / Báo cáo

**Vai trò:** Báo cáo PDF · Big-O · Slide · Video

**Nhiệm vụ cụ thể:**
- Viết toàn bộ báo cáo PDF (tối đa 40 trang) theo đúng cấu trúc.
- Viết phần phân tích độ phức tạp Big-O chi tiết.
- Tổng hợp bảng phân công công việc và phần đánh giá cá nhân.
- Làm slide thuyết trình và hỗ trợ quay/dựng video.
- Kiểm tra chính tả, định dạng báo cáo.

---

## 4. Lịch trình 8 tuần

| Tuần | TV1 (Trưởng nhóm) | TV2 (Core Algo) | TV3 (UI/Data) | TV4 (QA) | TV5 (Báo cáo) |
|---|---|---|---|---|---|
| 1 | Lập KH, phân tích | Nghiên cứu Dijkstra | Khảo sát sơ đồ tr. | Lên kế hoạch test | Soạn outline BC |
| 2 | Vẽ Class Diagram | Thiết kế struct đồ | Số hóa nút/cạnh | Viết TC01–TC05 | Viết phần Phân tích |
| 3 | Review design | Cài đặt Graph class | Xây dựng file data | Chuẩn bị data nhỏ | Viết phần Thiết kế |
| 4 | Hỗ trợ tích hợp | Cài đặt Dijkstra | Viết `loadData()` | Test TC01–TC05 | Viết pseudocode |
| 5 | Review code | Viết pseudocode | Viết `saveData()` | Tạo data lớn 10K | Viết Big-O |
| 6 | Tích hợp module | Tối ưu, tái tạo path | Xây dựng UI | Performance test | Viết phần Triển khai |
| 7 | Kiểm tra tổng thể | Hỗ trợ fix bug | Fix bug UI | Tổng hợp kết quả | Viết Kết luận + BC |
| 8 | Nộp bài (PDF+ZIP) | Review video | Quay demo UI | Kiểm tra file nộp | Dựng video, slide |

---

## 5. Phân tích bài toán

### 5.1 Đầu vào (Input) và Đầu ra (Output)

**Đầu vào:**
- Danh sách địa điểm (nodes): ID, tên (Cổng A, Tòa A, Thư viện, ...)
- Danh sách đường đi (edges): `node_u`, `node_v`, trọng số.
- Điểm xuất phát (source) và Điểm đích (destination).

**Đầu ra:**
- Danh sách các địa điểm trên đường đi ngắn nhất.
- Tổng khoảng cách / thời gian đi.
- Thông báo nếu không tồn tại đường đi.

### 5.2 Cấu trúc dữ liệu

| Cấu trúc | Mục đích | Lý do chọn |
|---|---|---|
| Adjacency List | Biểu diễn đồ thị | Tiết kiệm bộ nhớ `O(V+E)`, phù hợp đồ thị thưa |
| Min-Heap | Chọn nút có khoảng cách nhỏ nhất | Giảm độ phức tạp từ `O(V²)` xuống `O((V+E) log V)` |
| Mảng `dist[]` | Lưu khoảng cách ngắn nhất | Truy cập `O(1)` |
| Mảng `prev[]` | Tái tạo đường đi | Truy ngược từ đích về nguồn |
| Mảng `visited[]` | Đánh dấu nút đã xử lý | Tránh xử lý lại |

---

## 6. Thiết kế hệ thống

### 6.1 Class Diagram

```
+----------+     +----------+     +-----------------+
|   Node   |     |   Edge   |     |      Graph      |
+----------+     +----------+     +-----------------+
| id: int  |     | from:int |     | nodes: list     |
| name:str |     | to: int  |     | adjList: map    |
| x,y:float|     | weight:  |     +--------+--------+
+----------+     |   float  |     | addNode()       |
                 +----------+     | addEdge()       |
                                  | getNeighbors()  |
                                  +-----------------+

+-----------+     +----------+     +-------------+     +-------------+
| Navigator |     |    UI    |     | FileHandler |     | PerformTest |
+-----------+     +----------+     +-------------+     +-------------+
| graph:    |     |showMenu()|     | loadData()  |     | runTest()   |
|   Graph   |     |display() |     | saveData()  |     |measureTime()|
| dijkstra()|     +----------+     +-------------+     +-------------+
| getPath() |
+-----------+
```

### 6.2 Format file dữ liệu (JSON)

```json
{
  "nodes": [
    {"id": 0, "name": "Cổng chính"},
    {"id": 1, "name": "Tòa A"}
  ],
  "edges": [
    {"from": 0, "to": 1, "weight": 150}
  ]
}
```

---

## 7. Thuật toán Dijkstra

### 7.1 Pseudocode

```
DIJKSTRA(Graph G, source s):

  1. Khởi tạo:
       dist[v] = ∞  cho mọi v trong G
       dist[s] = 0
       prev[v] = -1 cho mọi v trong G
       visited[v] = false cho mọi v

  2. Tạo Priority Queue PQ (min-heap)
       PQ.push( (0, s) )

  3. WHILE PQ không rỗng:
       (d, u) = PQ.pop()
       IF visited[u] == true: CONTINUE
       visited[u] = true
       FOR EACH cạnh (u, v, w) trong G.getNeighbors(u):
           IF dist[u] + w < dist[v]:
               dist[v] = dist[u] + w
               prev[v] = u
               PQ.push( (dist[v], v) )

  4. RETURN dist[], prev[]


RECONSTRUCT_PATH(prev[], destination):

  path = []
  cur  = destination
  WHILE cur != -1:
      path.prepend(cur)
      cur = prev[cur]
  RETURN path
```

### 7.2 Phân tích độ phức tạp

**Thời gian:** `O((V + E) log V)`
- V lần pop từ PQ → `O(V log V)`
- Mỗi cạnh có thể push vào PQ → `O(E log V)`

**Không gian:** `O(V + E)`
- Adjacency List: `O(V + E)`
- Mảng `dist[]`, `prev[]`, `visited[]`: `O(V)`
- PQ tối đa: `O(E)`

---

## 8. Kiểm thử & Đo hiệu năng

**Kế hoạch Performance Test:**

1. Tạo đồ thị ngẫu nhiên với số nút: 100, 500, 1.000, 5.000, 10.000.
2. Với mỗi kích thước, chạy Dijkstra 5 lần, lấy thời gian trung bình.
3. Ghi lại kết quả vào bảng và vẽ biểu đồ.

| Số nút (V) | Số cạnh (E) | Lần 1 (ms) | Lần 2 (ms) | Lần 3 (ms) | TB (ms) |
|---|---|---|---|---|---|
| 100 | ~500 | | | | |
| 500 | ~2.500 | | | | |
| 1.000 | ~5.000 | | | | |
| 5.000 | ~25.000 | | | | |
| 10.000 | ~50.000 | | | | |

---

## 9. Cấu trúc báo cáo PDF

| Phần | Nội dung | Số trang |
|---|---|---|
| Giới thiệu | Bối cảnh, mục tiêu dự án | 2–3 trang |
| Phân tích | Đầu vào, đầu ra, cấu trúc dữ liệu | 5–7 trang |
| Thiết kế | Class Diagram, format dữ liệu | 5–7 trang |
| Triển khai | Module, pseudocode, Big-O | 15–18 trang |
| Kiểm thử & Kết quả | Test case, performance test, biểu đồ | 5–6 trang |
| Kết luận | Tổng kết, hướng phát triển | 1–2 trang |
| Phân công & Đánh giá | Bảng phân công, đánh giá cá nhân | — |

---

## 10. Kế hoạch Video thuyết trình

- **Tổng thời gian:** ≤ 20 phút | **Dung lượng:** ≤ 100 MB
- Tất cả 5 thành viên phải xuất hiện trên camera và nói trong video.
- Demo chương trình chạy thực tế (không dùng ảnh chụp màn hình).
