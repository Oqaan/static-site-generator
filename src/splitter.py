from textnode import TextType, TextNode
from extractor import extract_markdown_images, extract_markdown_links


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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if not images:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for alt, url in images:
                    parts = remaining_text.split(f"![{alt}]({url})", 1)
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    remaining_text = parts[1]
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if not links:
                new_nodes.append(node)
            else:
                remaining_text = node.text
                for anchor, url in links:
                    parts = remaining_text.split(f"[{anchor}]({url})", 1)
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(anchor, TextType.LINK, url))
                    remaining_text = parts[1]
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
