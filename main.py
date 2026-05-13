def main():
    print("  HỆ THỐNG TÌM ĐƯỜNG ĐẠI HỌC BÁCH KHOA HÀ NỘI")
    print("  ___________________________________________")
    graph, nodes_data = load_data("map_data.json")

    if not graph or not nodes_data:
        print("Khởi động thất bại. Vui lòng kiểm tra lại file dữ liệu.")
        return

    while True:
        print("\n--- DANH SÁCH CÁC ĐỊA ĐIỂM ---")
        for node_id, info in nodes_data.items():
            print(f"[{node_id}] - {info['name']}")

        print("\n------------------------------")

        try:
            start_input = input("Nhập ID điểm BẮT ĐẦU (hoặc ấn ENTER để thoát): ")
            if start_input =="":
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

            result = findShortestPath(graph, start_id, end_id)

            if result['distance'] == float('inf'):
                print("Không tìm thấy đường đi kết nối giữa 2 điểm này!")
            else:
                print(f"TỔNG QUÃNG ĐƯỜNG: {result['distance']} mét")
                print("QUÃNG ĐƯỜNG DI CHUYỂN LÀ:")

                path_names = [nodes_data[node_id]['name'] for node_id in result['path']]
                print(" ➡ ".join(path_names))

        except ValueError:
            print("Lỗi: Vui lòng chỉ nhập SỐ (ID) của địa điểm!")

        print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
