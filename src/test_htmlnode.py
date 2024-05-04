import unittest

from htmlnode import HTMLNode

class Test_HTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "hello", [], {1:"a", 2:"b"})
        self.assertEqual(" 1=\"a\" 2=\"b\"", node.props_to_html())
  

if __name__ == "__main__":
    unittest.main()