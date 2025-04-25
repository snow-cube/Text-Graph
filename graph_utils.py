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
        """
        返回所有桥接词word3，使得存在word1->word3和word3->word2的边。
        """
        word1 = word1.lower()
        word2 = word2.lower()
        bridge_words = set()
        for (src, mid) in self.edge_count:
            if src == word1:
                if (mid, word2) in self.edge_count:
                    bridge_words.add(mid)
        return list(bridge_words)
