import unittest
from leafnode import LeafNode

class Test_LeafNode(unittest.TestCase):
    def test_to_html(self):
        leaf_node = LeafNode("p", "hello", {1:"a"})
        print(leaf_node.to_html())
        self.assertEqual("<p 1=\"a\">hello</p>", leaf_node.to_html())

if __name__ == "__main__":
    unittest.main()