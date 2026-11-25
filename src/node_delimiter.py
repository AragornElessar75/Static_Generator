from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode],
    delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_node = old_node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("Delimiter is an invalid Markdown syntax")
        for i in range(len(split_node)):
            if split_node[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes
