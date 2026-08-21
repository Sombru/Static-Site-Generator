from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST =  "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    split_blocks = markdown.split("\n\n")
    return [block.strip() for block in split_blocks if block.strip()]

def lines_starts_with(lines: str, pattern: str) -> bool:
    block_lines = lines.splitlines()
    return bool(block_lines) and all(re.search(pattern, line) for line in block_lines)


def block_to_block_type(md_block: str) -> BlockType:
    if md_block.startswith("#"):
        return BlockType.HEADING
    elif md_block.startswith("```\n") and md_block.endswith("```"):
        return BlockType.CODE
    elif lines_starts_with(md_block, ">"):
        return BlockType.QUOTE
    elif lines_starts_with(md_block, "- "):
        return BlockType.UNORDERED_LIST
    elif lines_starts_with(md_block , r"\d\."):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH