import unittest

from textnode import TextNode
from utils import (
    split_nodes_delimiter, extract_markdown_image, extract_markdown_link,
    text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_HTML_node
)

markdown1 = """# This is a heading

### This is a smaller heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item"""
markdown1_blocks = [   
            '# This is a heading',
            '### This is a smaller heading', 
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is a list item\n* This is another list item'
        ]

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
>> ...by using additional greater-than signs right next to each other...


## Lists

Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


## Code

Inline `code`

Block code "fences"

```
Sample text here...
```
'''

class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter(self):

        node = TextNode("This is text with a `code block` word", "text")
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text")
        ]
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(expected_result, result)

        node = TextNode("This is text with a `code block`", "text")
        node2 = TextNode("Hello duy `cat`", 'text')
        expected_result = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode("Hello duy ", "text"),
            TextNode("cat", "code"),
        ]
        result = split_nodes_delimiter([node, node2], "`", "code")
        self.assertEqual(expected_result, result)

        node = TextNode("`code block` word", "text")
        expected_result = [
            TextNode("code block", "code"),
            TextNode(" word", "text")
        ]
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(expected_result, result)

    def test_split_nodes_delimiter_exception(self):

        node = TextNode("This is text with a `code block", "text")
        
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", "code")

        self.assertTrue('Did not find closing delimiter' in str(context.exception))

    def test_extract_image(self):
        result = extract_markdown_image("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        expected_result = [('image', 'https://i.imgur.com/zjjcJKZ.png')]
        self.assertEqual(result, expected_result)
    
    def test_extract_link(self):
        result = extract_markdown_link("This is text with an [link](https://i.imgur.com/zjjcJKZ.png)")
        expected_result = [('link', 'https://i.imgur.com/zjjcJKZ.png')]
        self.assertEqual(result, expected_result)

    def test_text_to_textnodes(self):
        result = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)")
        expected_result = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(result, expected_result)

    def test_markdown_to_blocks(self):
        print(markdown1)
        result = markdown_to_blocks(markdown1)
        print(result)
        expected_result = markdown1_blocks
        self.assertEqual(expected_result, result)

    def test_block_to_block_type(self):
        expected_types = ['heading', 'heading', 'paragraph', 'unordered_lst']
        types = []
        for text in markdown1_blocks:
            result = block_to_block_type(text)
            types.append(result)
        self.assertEqual(expected_types, types)

    def test_markdown_to_HTML_node(self):
        expected_str = ""
        result = markdown_to_HTML_node(markdown)
        self.assertEqual(expected_str, result)


        

if __name__ == "__main__":
    unittest.main()