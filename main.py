import functools
import glob
import operator
import re
import os

from anytree import ChildResolverError, Node, PreOrderIter, RenderTree, Resolver, search


processed_paths = []


def main():
    pass


def get_tree_from_files(starting_path):
    files = get_python_files(starting_path)
    print(f"Files to process: {files}")
    tree = create_tree(files)
    tree_text = get_ascii_tree(tree)
    print(tree_text)
    python_file_nodes = search.findall(tree, filter_=lambda node: ".py" in node.name)
    python_file_names = []
    for node in python_file_nodes:
        node_path_str = get_path_string(node)
        python_file_names.append(node_path_str)
    root_remove_python_filenames = [f.replace("root/", "") for f in python_file_names]
    for file_name in root_remove_python_filenames:
        best_path = get_valid_path(file_name)
        with open(best_path, "r") as file:
            file_text = file.read()
            classes = get_classes_from_file(file_text)
            r = Resolver("name")
            for found_class in classes:
                tree_path = "/root/" + file_name
                parent_node = r.get(tree, tree_path)
                x = Node(found_class, parent=parent_node, type="class")
    return tree


def get_valid_path(path):
    if os.path.exists(path):
        return path
    abs_path = "/" + path
    if os.path.exists(abs_path):
        return abs_path


def get_path_string(node):
    path_names = [n.name for n in node.path]
    node_path_str = functools.reduce(lambda a, b: a + "/" + b, path_names)
    return node_path_str


def create_html_from_tree(node, html=""):
    html = """<html><head>
    <style>
        div {
            border: 1px outset lightgray;
            margin: 5px;
            padding: 5px;

        }

        .dir {
            color: gray;
        }

        .file {
            color: black;
            color: green;
            background-color: lightgreen;
        }

        .class {
            color: blue;
            background-color: lightblue;
            border: 2px outset blue;
            width: 200px;
        }
    </style>
</head>

<body>"""
    html += create_html_from_tree_nodes(node, "")
    html += "</body></html>"
    print(processed_paths)
    return html


def create_html_from_tree_nodes(node, html=""):

    file_children = [n for n in node.children if n.type == "file"]
    if file_children:
        processed_paths.append(get_path_string(node))
        print(f"\tadding subdir with file: {node.name}")
        html += f"\n<div class='{node.type}'>{node.name} (added in loop)"
        file_and_class_html = ""
        for child in file_children:
            if child.type == "file":
                processed_paths.append(get_path_string(child))
                print(f"\tprocessing file: {child.name}")
                file_and_class_html += f"\n<div class='{child.type}'>{child.name}"
                for class_child in child.children:
                    file_and_class_html += (
                        f"\n<div class='{class_child.type}'>{class_child.name}</div>"
                    )
                file_and_class_html += "</div>"
        html += file_and_class_html
        html += "</div>"

    dir_children = [n for n in node.children if n.type == "dir"]
    for child in dir_children:
        print(f"about to recurse for {child.name}")
        child_html = create_html_from_tree_nodes(child, "")
        print(f"\tprocessed_paths: {processed_paths}")
        if get_path_string(node) in processed_paths:
            html += child_html
        else:
            html += f"\n<div class='{child.type}'>" + node.name + child_html + "</div>"
        print(f"recurse done for {child.name}\n")

    print(f"output_html: {html}\n")
    processed_paths.append(get_path_string(node))
    return html


def get_python_files(starting_path, exclude_pattern="venv|test_|__init__"):
    glob_path = f"{starting_path}/**/*.py"
    print(f"glob_path: {glob_path}")
    files = glob.glob(glob_path, recursive=True)
    included_files = [f for f in files if not re.findall(exclude_pattern, f)]
    return included_files


def create_tree(files):
    root = Node("root", type="root")
    parent_node = root

    r = Resolver("name")
    for file in files:
        # print(f"working file: {file}")
        parent_node = root
        paths = []
        path = "/root"
        for part in file.split("/"):
            path = path + "/" + part
            try:
                found_node_already = r.get(root, path)
                parent_node = found_node_already
            except ChildResolverError:
                node_type = "dir"
                if part.endswith(".py"):
                    node_type = "file"
                current_node = Node(part, parent=parent_node, type=node_type)
                parent_node = current_node
    return root


def get_ascii_tree(root, include_types=False):
    tree_text = ""
    type_text = ""
    for pre, _, node in RenderTree(root):
        if include_types:
            type_text = " (" + node.type + ")"
        tree_text = tree_text + f"{pre}{node.name}{type_text}\n"
    return tree_text


def get_classes_from_file(file_text):
    classes = re.findall("class [^:]+", file_text)
    remove_class_definition = [c.replace("class ", "") for c in classes]
    remove_empty_paran = [c.replace("()", "") for c in remove_class_definition]
    return remove_empty_paran


if __name__ == "__main__":
    main()
