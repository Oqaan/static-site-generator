from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise ValueError("Invalid markdown, closing delimiter not found")
            temp = []
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    temp.append(TextNode(part, TextType.TEXT))
                else:
                    temp.append(TextNode(part, text_type))
            new_nodes.extend(temp)
    return new_nodes
