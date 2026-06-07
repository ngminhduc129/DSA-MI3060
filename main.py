import json
from loaData import load_data
from MinHeap_Graph import Graph
from findShortestPath_reconstructPath import findShortestPath


def main():
    print("  HỆ THỐNG TÌM ĐƯỜNG ĐẠI HỌC BÁCH KHOA HÀ NỘI")
    print("  ___________________________________________")

    graph_dict, nodes_list = load_data("map_data.json")

    if graph_dict is None or nodes_list is None:
        print("Khởi động thất bại. Vui lòng kiểm tra lại file dữ liệu.")
        return

    nodes_data = {node['id']: node for node in nodes_list}

    hust_graph = Graph()
    for node in nodes_list:
        hust_graph.addNode(node['id'])

    with open('map_data.json', 'r', encoding='utf-8') as f:
        edges = json.load(f)['edges']
        for edge in edges:
            hust_graph.addEdge(edge['from'], edge['to'], edge['weight'])

    while True:
        print("\n--- DANH SÁCH CÁC ĐỊA ĐIỂM ---")
        for node_id, info in nodes_data.items():
            print(f"[{node_id}] - {info['name']}")

        print("\n------------------------------")

        try:
            start_input = input("Nhập ID điểm BẮT ĐẦU (hoặc ấn ENTER để thoát): ")
            if start_input == "":
                break
            start_id = int(start_input)

            end_input = input("Nhập ID điểm ĐẾN (hoặc ấn ENTER để thoát): ")
            if end_input == "":
                break
            end_id = int(end_input)

            if start_id not in nodes_data or end_id not in nodes_data:
                print("Lỗi: ID địa điểm không tồn tại. Vui lòng nhập ID có trong danh sách!")
                continue

            print(f"\nĐang tìm đường từ [{nodes_data[start_id]['name']}] đến [{nodes_data[end_id]['name']}]...")

            result = findShortestPath(hust_graph, start_id, end_id)

            if result['distance'] == float('inf'):
                print("Không tìm thấy đường đi kết nối giữa 2 điểm này!")
            else:
                print(f"TỔNG QUÃNG ĐƯỜNG: {result['distance']} mét")
                print("QUÃNG ĐƯỜNG DI CHUYỂN LÀ:")

                # Tra cứu tên của các địa điểm đi qua dựa vào ID
                path_names = [nodes_data[node_id]['name'] for node_id in result['path']]
                print(" ➡ ".join(path_names))

        except ValueError:
            print("Lỗi: Vui lòng chỉ nhập SỐ (ID) của địa điểm!")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()