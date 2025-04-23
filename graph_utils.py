import re
from collections import defaultdict


def build_graph_elements_from_text(text: str):
    text = re.sub(r"[^\w\s]", "", text).lower()
    words = text.split()

    edge_count = defaultdict(int)
    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        edge_count[(a, b)] += 1

    nodes = {w for pair in edge_count for w in pair}
    elements = [{"data": {"id": w, "label": w}} for w in nodes]

    for (src, tgt), weight in edge_count.items():
        elements.append({"data": {"source": src, "target": tgt, "weight": weight}})

    return elements
