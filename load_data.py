def load_data(file_path="map_data.json"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        nodes_data = {}
        for node in data['nodes']:
            nodes_data[node['id']] = {
                'name': node['name'],
                'lat': node['lat'],
                'lng': node['lng']
            }
        graph = Graph()
        for edge in data['edges']:
            graph.addEdge(edge['from'], edge['to'], edge['weight'])
        return graph, nodes_data
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{file_path}'. Hãy kiểm tra lại!")
        return None, None
    except json.JSONDecodeError:
        print("Lỗi: File JSON bị sai định dạng cú pháp!")
        return None, None
