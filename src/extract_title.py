from block_markdown import markdown_to_blocks


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if blocks[0].startswith("#"):
        block = blocks[0].lstrip("#")
        return block.strip()
    raise ValueError("No Title")
