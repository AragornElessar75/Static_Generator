import re

from textnode import TextNode, TextType

IMAGE_PATTERN = re.compile(r"!\[([^\[\]]*)\]\(([^()]*)\)")
LINK_PATTERN = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^()]*)\)")


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return IMAGE_PATTERN.findall(text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return LINK_PATTERN.findall(text)


def _split_nodes(
    old_nodes: list[TextNode],
    pattern: re.Pattern[str],
    match_type: TextType,
) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        cursor = 0

        for match in pattern.finditer(text):
            start, end = match.span()
            if start > cursor:
                new_nodes.append(TextNode(text[cursor:start], TextType.TEXT))

            label, url = match.groups()
            new_nodes.append(TextNode(label, match_type, url))
            cursor = end

        if cursor == 0:
            new_nodes.append(node)  # No matches: keep the original node.
        elif cursor < len(text):
            new_nodes.append(TextNode(text[cursor:], TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes(old_nodes, IMAGE_PATTERN, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes(old_nodes, LINK_PATTERN, TextType.LINK)
