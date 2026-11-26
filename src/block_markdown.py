from enum import Enum

from htmlnode import HTMLNode, ParentNode
from text_to_textnode import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        new_blocks.append(block)
    return new_blocks

def block_to_block_type(markdown: str) -> BlockType:
    lines = markdown.split("\n")
    if markdown.startswith(("# ","## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    quote = True
    for line in lines:
        if not line.startswith(">"):
            quote = False
            break
    if quote:
        return BlockType.QUOTE
    quote = True
    for line in lines:
        if not line.startswith("- "):
                quote = False
                break
    if quote:
            return BlockType.UNORDERED_LIST
    quote = True
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            quote = False
            break
    if quote:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown: str) -> HTMLNode:
    children = [block_to_html_node(block) for block in markdown_to_blocks(markdown)]
    return ParentNode("div", children)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    raise ValueError(f"invalid block type: {block_type}")


def text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def paragraph_to_html_node(block: str) -> HTMLNode:
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block: str) -> HTMLNode:
    level = len(block) - len(block.lstrip("#"))
    text = block[level:].strip()
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block: str) -> HTMLNode:
    text = block[4:-3]
    code = text_node_to_html_node(TextNode(text, TextType.TEXT))
    return ParentNode("pre", [ParentNode("code", [code])])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = [line.lstrip(">").strip() for line in block.split("\n")]
    return ParentNode("blockquote", text_to_children(" ".join(lines)))


def ulist_to_html_node(block: str) -> HTMLNode:
    items = [ParentNode("li", text_to_children(line[2:])) for line in block.split("\n")]
    return ParentNode("ul", items)


def olist_to_html_node(block: str) -> HTMLNode:
    items = [
        ParentNode("li", text_to_children(line.split(". ", 1)[1]))
        for line in block.split("\n")
    ]
    return ParentNode("ol", items)
