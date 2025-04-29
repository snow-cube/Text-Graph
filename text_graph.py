import re
from collections import defaultdict


class TextGraph:
    def __init__(self, text: str):
        self.text = text
        self.nodes = set()
        self.edge_count = defaultdict(int)
        # 添加邻接表结构，提高图操作效率
        self.out_edges = defaultdict(list)  # 存储每个节点的出边
        self.in_edges = defaultdict(list)  # 存储每个节点的入边
        self._parse_text()

    def _parse_text(self):
        clean_text = re.sub(r"[^\w\s]", "", self.text).lower()
        words = clean_text.split()
        for i in range(len(words) - 1):
            a, b = words[i], words[i + 1]
            self.edge_count[(a, b)] += 1
            # 添加节点
            self.nodes.add(a)
            self.nodes.add(b)

        # 构建邻接表，提高后续操作效率
        for (src, tgt), weight in self.edge_count.items():
            self.out_edges[src].append((tgt, weight))
            self.in_edges[tgt].append((src, weight))

    @property
    def node_count(self):
        """返回图中的节点数量"""
        return len(self.nodes)

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

        # 优化桥接词查找算法，使用邻接表结构，避免遍历所有边
        if word1 in self.out_edges and word2 in self.in_edges:
            # 获取word1的所有后继节点
            for mid, w1_to_mid_weight in self.out_edges[word1]:
                # 检查mid是否能到达word2（即mid是否是word2的前驱）
                for src, _ in self.in_edges[word2]:
                    if src == mid:  # 找到桥接词
                        bridge_words.add(mid)
                        # 添加从word1到mid的边
                        word1_to_bridge_edges.append(
                            {"source": word1, "target": mid, "type": "bridge"}
                        )
                        # 添加从mid到word2的边
                        bridge_to_word2_edges.append(
                            {"source": mid, "target": word2, "type": "bridge"}
                        )
                        break  # 已找到连接，无需继续检查

        # 返回 (桥接词列表, word1到桥接词的边, 桥接词到word2的边)
        return list(bridge_words), word1_to_bridge_edges, bridge_to_word2_edges

    def get_shortest_path(self, word1, word2):
        import heapq

        word1 = word1.lower()
        word2 = word2.lower()
        if word1 not in self.nodes or word2 not in self.nodes:
            return [], 0

        # 使用预构建的邻接表，避免每次调用时重复构建图结构
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

            # 直接使用邻接表，提高查找效率
            for neighbor, edge_weight in self.out_edges.get(current, []):
                new_cost = cost + edge_weight
                if neighbor not in visited or new_cost < visited.get(
                    neighbor, float("inf")
                ):
                    heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))
        return [], 0

    def get_in_edges(self, node):
        """
        返回指向指定节点的所有入边

        Args:
            node: 目标节点

        Returns:
            dict: 键为源节点，值为边的权重
        """
        in_edge_dict = {}
        for source, weight in self.in_edges.get(node, []):
            in_edge_dict[source] = weight
        return in_edge_dict

    def get_out_edges(self, node):
        """
        返回从指定节点出发的所有出边

        Args:
            node: 源节点

        Returns:
            dict: 键为目标节点，值为边的权重
        """
        out_edge_dict = {}
        for target, weight in self.out_edges.get(node, []):
            out_edge_dict[target] = weight
        return out_edge_dict

    @staticmethod
    def calculate_next_random_walk_step(current_node, edge_count):
        """
        Calculate the next step in a random walk based on the current node and edge weights.

        Args:
            current_node: The current node in the random walk
            edge_count: Dictionary with (src, tgt) tuples as keys and weights as values

        Returns:
            A tuple containing (next_node, edge_weight)
            - next_node: The selected next node (None if there are no outgoing edges)
            - edge_weight: The weight of the edge to the next node (0 if next_node is None)
        """
        import random

        # Get all outgoing edges from the current node
        out_edges = []
        for (src, tgt), weight in edge_count.items():
            if src == current_node and weight > 0:
                out_edges.append((tgt, weight))

        # If there are no outgoing edges, return None and 0
        if not out_edges:
            return None, 0

        # Randomly select the next node (higher weight = higher probability)
        weights = [w for _, w in out_edges]
        next_node = random.choices([n for n, _ in out_edges], weights=weights)[0]

        # Get the edge weight
        edge_weight = next(
            w
            for (s, t), w in edge_count.items()
            if s == current_node and t == next_node
        )

        return next_node, edge_weight

    def calculate_pagerank(
        self, damping_factor=0.85, max_iterations=100, tolerance=1e-6
    ):
        """
        Calculate PageRank for all nodes in the graph.

        Args:
            damping_factor: The damping factor (default: 0.85)
            max_iterations: Maximum number of iterations (default: 100)
            tolerance: Convergence tolerance (default: 1e-6)

        Returns:
            A dictionary mapping node labels to their PageRank values
        """
        # Initialize PageRank values
        N = self.node_count
        if N == 0:
            return {}

        pagerank = {node: 1.0 / N for node in self.nodes}

        # Identify nodes with zero out-degree
        zero_outdegree_nodes = {node for node in self.nodes if not self.out_edges[node]}

        for _ in range(max_iterations):
            # Store previous PageRank values to check for convergence
            prev_pagerank = pagerank.copy()

            # Collect the "leaked" PageRank from nodes with zero out-degree
            zero_outdegree_sum = (
                sum(prev_pagerank[node] for node in zero_outdegree_nodes)
                * damping_factor
                / N
            )

            # Update PageRank for each node
            for node in self.nodes:
                # Initialize with the random teleport probability
                pagerank[node] = (1 - damping_factor) / N

                # Add the contribution from nodes pointing to this node
                for source, _ in self.in_edges[node]:
                    # Divide the source's PageRank by its out-degree
                    out_degree = len(self.out_edges[source])
                    if out_degree > 0:  # Should always be true for nodes in in_edges
                        pagerank[node] += (
                            damping_factor * prev_pagerank[source] / out_degree
                        )

                # Add the contribution from zero out-degree nodes
                pagerank[node] += zero_outdegree_sum

            # Check for convergence
            diff = sum(abs(pagerank[node] - prev_pagerank[node]) for node in self.nodes)
            if diff < tolerance:
                break

        return pagerank
