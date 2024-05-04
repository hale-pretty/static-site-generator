from typing import List, Type
from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node tag cannot be none")
        if self.children is None:
            raise ValueError("No child no life")
        children_html_value = ""
        for child in self.children:
            children_html_value += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html_value}</{self.tag}>"