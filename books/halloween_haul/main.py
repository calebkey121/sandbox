from __future__ import annotations

class Node:
    def __init__(self, left: Node, right: Node, candy: int=None):
        self.candy = candy
        self.left = left
        self.right = right
    
    def __repr__(self):
        if self.candy:
            return f"House {self.candy}"
        return f"Street"

# Problem constraints to houses and streets
def house(candy: int) -> Node:
    return Node(None, None, candy)

def street(left: Node, right: Node) -> Node:
    return Node(left, right)

def create_tree(tree_tuple) -> Node:
    if tree_tuple  == ():
        return None
    elif isinstance(tree_tuple, int): # House
        return house(tree_tuple)
    elif len(tree_tuple) == 2: # Street
        return street(left=create_tree(tree_tuple[0]), right=create_tree(tree_tuple[1]))
    else:
        raise NotImplementedError

class Tree:
    def __init__(self, tree_tuple: tuple):
        self.root = create_tree(tree_tuple)
        self.candy = Tree.tree_candy(self.root)
        self.height = Tree.tree_height(self.root)
        self.num_nodes = Tree.num_nodes(self.root)
    
    @staticmethod
    def tree_height(root) -> int:
        if not root.left and not root.right:
            return 0
        return 1 + max(Tree.tree_height(root.left), Tree.tree_height(root.right))
    
    @staticmethod
    def num_nodes(root) -> int:
        if not root.left and not root.right:
            return 1
        return 1 + Tree.num_nodes(root.left) + Tree.num_nodes(root.right)

    @staticmethod
    def tree_candy(root) -> int:
        if root.candy: # leaf
            return root.candy
        return Tree.tree_candy(root.left) + Tree.tree_candy(root.right)


# Stack Implementation
# def tree_candy(root: Node) -> int:
#     total_candy = 0
# 
#     # lets make a stack to track the nodes we have left to process
#     stack = [ root ]
#     while len(stack) != 0:
#         top = stack[-1]
#         if top.candy:
#             print(f"Found House {top.candy}")
#             total_candy += top.candy
#             del stack[-1]
#         else:
#             del stack[-1]
#             stack.extend([top.left, top.right])
#     return total_candy

root = Tree(
    ( # tree tuple
        (
            (
                72,
                3
            ),
            (
                6,
                (
                    (
                        (
                            4,
                            9
                        ),
                        15
                    ),
                    2
                )
            )
        ),
        (
            7,
            41
        )
    )
)
print(f"Num Candy: {root.candy}\nNum Nodes: {root.num_nodes}\nTree Height: {root.height}")
