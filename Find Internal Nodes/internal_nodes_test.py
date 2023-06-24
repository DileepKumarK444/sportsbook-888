def find_internal_nodes_num(tree):
    # Initialize a counter for internal nodes
    internal_nodes = 0
    # Create a dictionary to store the child nodes for each parent node
    child_nodes = {}
    # Iterate over each node in the tree
    for i, parent in enumerate(tree):
        # Exclude the root node
        if parent != -1:
            if parent in child_nodes:
                child_nodes[parent].append(i)
            else:
                child_nodes[parent] = [i]
    return len(child_nodes)

my_tree = [4, 4, 1, 5, -1, 4, 5]
print(find_internal_nodes_num(my_tree))
