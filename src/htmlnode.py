from typing import List

class HTMLNode:
    def __init__(self, tag: str, value: str, children: List, props: dict):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
        
    def props_to_html(self) -> str:
        result = ""
        if self.props is None:
            return result
        for k, v in self.props.items():
            result += f" {k}=\"{v}\""
        return result


    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"
    
