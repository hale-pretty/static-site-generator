from textnode import TextNode
from parentnode import ParentNode
from htmlnode import HTMLNode
from leafnode import LeafNode
from typing import List, Tuple
import re

tag_dict = {"paragraph": "p", "quote": "blockquote", "code_block": "code",
            "unordered_lst": "ul", "ordered_lst": "ol",
            "heading_1": "h1", "heading_2": "h2", "heading_3": "h3",
            "heading_4": "h4", "heading_5": "h5", "heading_6": "h6"}

markdown = '''
# h1 Heading

## h2 Heading

### h3 Heading

#### h4 Heading

##### h5 Heading

###### h6 Heading

## Emphasis

**This is bold text**
*This is italic text*

## Blockquotes

> Blockquotes can also be nested...
> ...by using additional greater-than signs right next to each other...


## Lists

Unordered

- Create a list by starting a line with `+`, `-`, or `*`
- Sub-lists are made by indenting 2 spaces:
* Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


## Code

Inline `code`

Block code "fences"

```Sample text here...```
'''

# 1. TextNode to HTMLNode
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    result = None
    if text_node.text_type == "text":
        result = LeafNode(None, text_node.text)
    elif text_node.text_type == "bold":
        result = LeafNode("b", text_node.text)
    elif text_node.text_type == "italic":
        result = LeafNode("i", text_node.text)
    elif text_node.text_type == "code":
        result = LeafNode("code", text_node.text)
    elif text_node.text_type == "link":
        result = LeafNode("a", text_node.text, {"href": "link_props"})
    elif text_node.text_type == "image":
        result = LeafNode("img", text_node.text, {"src": "URL", "alt": "alt_text"})
    else:
        raise Exception("Master of None")
    return result

def text_nodes_block_to_html_nodes_block(text_nodes: List[TextNode]) -> List[HTMLNode]:
    #final function
    result = []
    for text_node in text_nodes:
        result.append(text_node_to_html_node(text_node))
    return result


# 2. Text to TextNode
def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: str) -> List[TextNode]:
    result = []
    for node in old_nodes:
        if type(node) != TextNode:
            result.append(node)
            continue
        text = node.text
        last_index = 0
        is_newtype = False
        for index, char in enumerate(text):
            if char == delimiter[0] and text[index:index+len(delimiter)] == delimiter:
                new_text = text[last_index:index]
                if len(new_text) != 0:
                    new_textnode = TextNode(new_text, node.text_type)
                    if is_newtype:
                        new_textnode.text_type = text_type
                    result.append(new_textnode)
                is_newtype = not is_newtype
                last_index = index + len(delimiter)
        if len(text[last_index:]) != 0:
            if is_newtype:
                print(text)
                raise Exception("Did not find closing delimiter")
            last_textnode = TextNode(text[last_index:], node.text_type)
            result.append(last_textnode)
    return result

def extract_markdown_image(input_text: str) -> List[Tuple]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", input_text)

def extract_markdown_link(input_text: str) -> List[Tuple]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", input_text)

def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    result = []
    for node in old_nodes:
        text = node.text
        extraction_img = extract_markdown_image(text)
        if len(extraction_img) == 0 and node is not None:
            result.append(node)
            continue
        latest_text = text
        for tup in extraction_img:
            splited_text_list = latest_text.split(f"![{tup[0]}]({tup[1]})", 1)           
            TextNode_text = TextNode(splited_text_list[0], node.text_type)
            TextNode_img = TextNode(tup[0], "image", tup[1])
            result.append(TextNode_text)
            result.append(TextNode_img)
            latest_text = splited_text_list[1]
        if len(latest_text) > 0:
            TextNode_text2 = TextNode(latest_text, node.text_type)
            result.append(TextNode_text2)
    return result

def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    result = []
    for node in old_nodes:
        text = node.text
        extraction_link = extract_markdown_link(text)
        if len(extraction_link) == 0 and node is not None:
            result.append(node)
            continue
        latest_text = text
        for tup in extraction_link:
            splited_text_list = latest_text.split(f"[{tup[0]}]({tup[1]})", 1)           
            TextNode_text = TextNode(splited_text_list[0], node.text_type)
            TextNode_link = TextNode(tup[0], "link", tup[1])
            result.append(TextNode_text)
            result.append(TextNode_link)
            latest_text = splited_text_list[1]
        if len(latest_text) > 0:
            TextNode_text2 = TextNode(latest_text, node.text_type)
            result.append(TextNode_text2)       
    return result

def text_block_to_text_nodes_block(text_block: str) -> List[TextNode]:
    #final function
    texts = text_block.split("\n")
    result = []
    for text in texts:
        result.extend(text_to_textnodes(text))
    return result

def text_to_textnodes(text: str) -> List[TextNode]:
    node = TextNode(text, "text")
    nodes_split_b = split_nodes_delimiter([node], "**", "bold")
    nodes_split_b_c = split_nodes_delimiter(nodes_split_b, "`", "code")
    nodes_split_b_c_i = split_nodes_delimiter(nodes_split_b_c, "*", "italic")    
    nodes_split_b_i_c_img = split_nodes_image(nodes_split_b_c_i)
    final_nodes = split_nodes_link(nodes_split_b_i_c_img)
    return final_nodes


# 3. Markdown to Blocks
def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return blocks

def block_to_block_type(text: str) -> str:
    lst_types = [
        ("heading_1", r"^#{1}\s(.+)$"), ("heading_2", r"^#{2}\s(.+)$"),
        ("heading_3", r"^#{3}\s(.+)$"), ("heading_4", r"^#{6}\s(.+)$"),
        ("heading_5", r"^#{5}\s(.+)$"), ("heading_6", r"^#{6}\s(.+)$"),
        ("code_block", r"^```[\s\S]*?^```"), ("quote", r"^(?:>[^\n]*\n?)+$"),
        ("unordered_lst", r"^(?:[*-][^\n]*\n?)+$"),
        ("ordered_lst", r"^1\.[^\n]*\n?(?:(?<=\d)\.\s[^\n]*\n?)*$")
    ]
    for block_type in lst_types:
        match = re.match(block_type[1], text)
        if match:
            return block_type[0]
    return "paragraph"


# 4. Other Inline text to HTML
def list_text_to_LeafNode(text_block: str) -> List[LeafNode]:
    lines = text_block.split('\n')
    result = []
    for line in lines:
        new_line = line[1:]
        leaf_node = LeafNode("li", new_line)
        result.append(leaf_node)
    return result

    # lines_with_insertion = [f"<{inserted_str[1]}>" + line + f"</{inserted_str[1]}>" for line in lines]
    # result_string = '\n'.join(lines_with_insertion)
    # return f"<{inserted_str[0]}\n" + result_string + f"\n</{inserted_str[0]}>"


# 5. Final function to HTML
def markdown_to_HTML_node(markdown: str):
    text_blocks = markdown_to_blocks(markdown)
    result_html_blocks = []
    for text_block in text_blocks:
        block_type = block_to_block_type(text_block)
        chidlren = []
        if block_type == 'unordered_lst' or block_type == 'ordered_list':
            chidlren = list_text_to_LeafNode(text_block)
        else:
            text_nodes_blocks = text_block_to_text_nodes_block(text_block)
            chidlren = text_nodes_block_to_html_nodes_block(text_nodes_blocks)
        parent_node = ParentNode(tag_dict[block_type], chidlren)
        html_block = parent_node.to_html()
        result_html_blocks.append(html_block)
    result = "\n\n".join(result_html_blocks)
    return "<div>\n" + result + "\n</div>"

def clean_text_block(text: str, block_type: str) -> str:
    if block_type == 

print(markdown_to_HTML_node(markdown))
