import json
from collections import deque

for n in [100, 500, 1000, 5000, 10000]:
    path = f"qa/data_large/graph_{n}.json"
    data = json.load(open(path, encoding="utf-8"))

    nodes = data["nodes"]
    edges = data["edges"]
    ids = {node["id"] for node in nodes}

    assert len(nodes) == n
    assert all("id" in node and "name" in node and "lat" in node and "lng" in node for node in nodes)
    assert all(e["from"] in ids and e["to"] in ids for e in edges)
    assert all(e["from"] != e["to"] for e in edges)
    assert all(e["weight"] > 0 for e in edges)

    adj = {i: [] for i in ids}
    for e in edges:
        adj[e["from"]].append(e["to"])
        adj[e["to"]].append(e["from"])

    start = nodes[0]["id"]
    visited = {start}
    q = deque([start])

    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                q.append(v)

    assert len(visited) == len(nodes)

    print(f"graph_{n}.json OK | nodes={len(nodes)} | edges={len(edges)}")