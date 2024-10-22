from Node import Node
import numpy as np
import random

node_id = 0  # 记录每个node的id方便后续在随机池中检索
# 两种操作的次数控制在都不超过十次
counter_e = 0
counter_t = 0
counter_u = 0
counter_r = 0
cv = ["p", "q", "r", "s", "T", "F"]
level = 0
probability = np.array([0.6, 0.4, 0.0])


# 用来批量生成想要的node，是为了方便一次性需要生成多个node。
# 即E to E→T这样就可以一次生成三个node，对应'E', '→', 'T'
def generate_nodes(elements):
    global node_id
    res = []
    for i in elements:
        new = Node(node_id, i)
        node_id += 1
        res.append(new)
    return res


# 因为我们要同时生成左右两边，所以这里后面应该改成有两个参数
def generate(node):
    if node.element == 'E':
        generate_E(node)
    elif node.element == 'T':
        generate_T(node)
    elif node.element == 'U':
        generate_U(node)
    elif node.element == 'R':
        generate_R(node)
    return

'''def generate_two(node,node1):
    if node.element == 'E':
        generate_E(node)
    elif node.element == 'T':
        generate_T(node)
    elif node.element == 'U':
        generate_U(node)
    elif node.element == 'R':
        generate_R(node)
    return'''


def update(root):
    # 从底部依次update每个node的attri，检查整棵树的attri只需要root的attri即可
    if root.left == None and root.right == None and root.mid == None:
        root.attri = root.element
        return
    elif root.left != None and root.right == None and root.mid == None:
        update(root.left)
        root.attri = root.left.attri
        return
    elif root.left != None and root.right != None and root.mid == None:
        update(root.right)
        root.attri = "┐" + root.right.attri
        return
    elif root.left.element == '(' and root.right.element == ')' and root.mid != None:
        update(root.mid)
        root.attri = '(' + root.mid.attri + ')'
        return
    else:
        update(root.left)
        update(root.right)
        root.attri = root.left.attri + root.mid.element + root.right.attri
        return


# 这里的四个函数是对应不同node时的相应变换操作
def generate_E(node):
    global level, probability, counter_e, node_id
    level += 1
    if level > 8:
        probability = np.array([0.05, 0.05, 0.9])
    option = np.random.choice([1, 2, 3], p=probability.ravel())
    if counter_e < 3:
        if option == 1:
            nodes = generate_nodes(['E', '→', 'T'])
            counter_e += 1
            node.left = nodes[0]
            node.mid = nodes[1]
            node.right = nodes[2]
            generate(node.left)
            generate(node.right)
        else:
            node_left = Node(node_id, 'T')
            node_id += 1
            node.left = node_left
            generate(node.left)
    else:
        node_left = Node(node_id, 'T')
        node_id += 1
        node.left = node_left
        generate(node.left)


def generate_T(node):
    global level, probability, counter_t, node_id
    level += 1
    if level > 8:
        probability = np.array([0.05, 0.05, 0.9])
    option = np.random.choice([1, 2, 3], p=probability.ravel())
    if counter_t < 3:
        if option == 1:
            nodes = generate_nodes(['T', '∨', 'U'])
            counter_t += 1
            node.left = nodes[0]
            node.mid = nodes[1]
            node.right = nodes[2]
            generate(node.left)
            generate(node.right)
        else:
            node_left = Node(node_id, 'U')
            node_id += 1
            node.left = node_left
            generate(node.left)
    else:
        node_left = Node(node_id, 'U')
        node_id += 1
        node.left = node_left
        generate(node.left)


def generate_U(node):
    global level, probability, counter_u, node_id
    level += 1
    if level > 8:
        probability = np.array([0.05, 0.05, 0.9])
    option = np.random.choice([1, 2, 3], p=probability.ravel())
    if counter_u < 3:
        if option == 1:
            nodes = generate_nodes(['U', '∧', 'R'])
            counter_u += 1
            node.left = nodes[0]
            node.mid = nodes[1]
            node.right = nodes[2]
            generate(node.left)
            generate(node.right)
        else:
            node_left = Node(node_id, 'R')
            node_id += 1
            node.left = node_left
            generate(node.left)
    else:
        node_left = Node(node_id, 'R')
        node_id += 1
        node.left = node_left
        generate(node.left)


def generate_R(node):
    global level, probability, counter_r, node_id
    level += 1
    if level > 8:
        probability = np.array([0.05, 0.05, 0.9])
    option = np.random.choice([1, 2, 3], p=probability.ravel())
    if counter_r < 3:
        if option == 1:
            nodes = generate_nodes(['┐', 'R'])
            counter_r += 1
            node.left = nodes[0]
            node.right = nodes[1]
            generate(node.right)
        elif option == 2:
            nodes = generate_nodes(['(', 'E', ')'])
            node.left = nodes[0]
            node.mid = nodes[1]
            node.right = nodes[2]
            generate(node.mid)
        else:
            val = random.choice(cv)
            node_left = Node(node_id, val)
            node_id += 1
            node.left = node_left
    else:
        if option == 1:
            nodes = generate_nodes(['(', 'E', ')'])
            node.left = nodes[0]
            node.mid = nodes[1]
            node.right = nodes[2]
            generate(node.mid)
        else:
            val = random.choice(cv)
            node_left = Node(node_id, val)
            node_id += 1
            node.left = node_left
