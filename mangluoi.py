import json
import matplotlib.pyplot as plt

# 1. Đọc dữ liệu từ file JSON
with open('data/map_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Tạo từ điển để tra cứu tọa độ nhanh
nodes = {n['id']: n for n in data['nodes']}

plt.figure(figsize=(12, 10))

# 2. Vẽ các đường nối vuông góc (Orthogonal Edges)
for edge in data['edges']:
    start = nodes[edge['from']]
    end = nodes[edge['to']]
    
    x1, y1 = start['x'], start['y']
    x2, y2 = end['x'], end['y']
    
    mid_x = (x1 + x2) / 2
    
    # Vẽ đường gấp khúc vuông góc
    plt.plot([x1, mid_x], [y1, y1], color='gray', linestyle='-', linewidth=1, alpha=0.6)
    plt.plot([mid_x, mid_x], [y1, y2], color='gray', linestyle='-', linewidth=1, alpha=0.6)
    plt.plot([mid_x, x2], [y2, y2], color='gray', linestyle='-', linewidth=1, alpha=0.6)

for node_id, node in nodes.items():
    if "Nga" not in node['name']:  
        plt.scatter(node['x'], node['y'], color='limegreen', s=100, zorder=5)
        # Cộng thêm 15 pixel vào y để đẩy chữ xuống dưới chấm tròn một chút
        plt.text(node['x'], node['y'] + 15, node['name'], 
                 fontsize=8, ha='center', fontweight='bold')

plt.gca().invert_yaxis()  
plt.gca().set_aspect('equal')
plt.axis('off')           

plt.title("Bản đồ số hóa HUST", fontsize=14, fontweight='bold', pad=20)
plt.show()
