def saveData(filename, start_node, end_node, result):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== KẾT QUẢ TÌM ĐƯỜNG HUST ===\n")
            f.write(f"Điểm đi: {start_node}\n")
            f.write(f"Điểm đến: {end_node}\n")
            if result['path']:
                f.write(f"Lộ trình: {' -> '.join(map(str, result['path']))}\n")
                f.write(f"Tổng quãng đường: {result['distance']} mét\n")
            else:
                f.write("Trạng thái: Không tìm thấy đường đi.\n")
        return True
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")
        return False