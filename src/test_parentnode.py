import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class Test_ParentNode(unittest.TestCase):
    def test_to_html(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        print(parent_node.to_html())
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", parent_node.to_html())

if __name__ == "__main__":
    unittest.main()