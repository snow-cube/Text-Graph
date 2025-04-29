import re
from collections import defaultdict


class TextGraph:
    def __init__(self, text: str):
        self.text = text
        self.nodes = set()
        self.edge_count = defaultdict(int)
        self._parse_text()

    def _parse_text(self):
        clean_text = re.sub(r"[^\w\s]", "", self.text).lower()
        words = clean_text.split()
        for i in range(len(words) - 1):
            a, b = words[i], words[i + 1]
            self.edge_count[(a, b)] += 1
        self.nodes = {w for pair in self.edge_count for w in pair}

    def get_elements(self):
        elements = [{"data": {"id": w, "label": w}} for w in self.nodes]
        for (src, tgt), weight in self.edge_count.items():
            elements.append({"data": {"source": src, "target": tgt, "weight": weight}})
        return elements

    def get_bridge_words(self, word1, word2):
        word1 = word1.lower()
        word2 = word2.lower()
        bridge_words = set()
        word1_to_bridge_edges = []
        bridge_to_word2_edges = []

        # 直接在查找桥接词的过程中构建边集合
        for (src, mid) in self.edge_count:
            if src == word1:  # 从word1出发的边
                if (mid, word2) in self.edge_count:  # 如果mid能到达word2
                    # 找到桥接词
                    bridge_words.add(mid)

                    # 同时添加从word1到mid的边
                    word1_to_bridge_edges.append({
                        "source": word1,
                        "target": mid,
                        "type": "bridge"
                    })

                    # 同时添加从mid到word2的边
                    bridge_to_word2_edges.append({
                        "source": mid,
                        "target": word2,
                        "type": "bridge"
                    })

        # 返回 (桥接词列表, word1到桥接词的边, 桥接词到word2的边)
        return list(bridge_words), word1_to_bridge_edges, bridge_to_word2_edges

    def get_shortest_path(self, word1, word2):
        import heapq

        word1 = word1.lower()
        word2 = word2.lower()
        if word1 not in self.nodes or word2 not in self.nodes:
            return [], 0

        # 直接使用原始权重（出现次数越多，权重越大）
        graph = defaultdict(list)
        for (src, tgt), weight in self.edge_count.items():
            if weight > 0:
                graph[src].append((tgt, weight))

        heap = []
        heapq.heappush(heap, (0, word1, [word1]))
        visited = {}

        while heap:
            cost, current, path = heapq.heappop(heap)
            if current == word2:
                return path, cost
            if current in visited and visited[current] <= cost:
                continue
            visited[current] = cost
            for neighbor, edge_weight in graph.get(current, []):
                if neighbor not in visited or cost + edge_weight < visited.get(
                    neighbor, float("inf")
                ):
                    heapq.heappush(
                        heap, (cost + edge_weight, neighbor, path + [neighbor])
                    )
        return [], 0
