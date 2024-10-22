from Node import Node
import numpy as np
import random
import generation
import Generator

equRules = [
    '┐(p∧q) = ┐p∨┐q',  # 0-de morgan
    '┐(p∨q) = ┐p∧┐q',  # 1-de morgan
    'p∨(q∧r) = (p∨q)∧(p∨r)',  # 2-//distribute
    '(q∧r)∨p = (p∨q)∧(p∨r)',  # 3 -顺序可以调换//
    '(p)v((p)∧(q)) = p',  # 4-//absorption x
    '(p)∧((p)v(q)) = p',  # 5-//
    'p→q = ┐p∨q',  # 6
    'p→q = ┐q→┐p',  # 7zz
    '(p→q)∨(p→r) = p→(q∨r)',  # 8
    '(p→r)∨(q→r) = (p∧q)→r)',  # 9
    '(p→q)∧(p→r) = p→(q∧r)',  # 10
    '(p→r)∧(q→r) = (p∨q)→r)',  # 11
    '┐(┐q) = q',  # 12 double negation
    'p^T = p',  # 13 identity
    'p∨F = p',  # 14 identity//
    'p^q = q^p',  # 15 commutative
    'p∨q = q∨p',  # 16
    '(p^q)^r = p^(q^r)',  # 17 association
    '(p∨q)∨r = p∨(q∨r)',  # 18
    'p∨p = p',  # 19
    'p^p = p'  # 20
]

easy = [8, 9, 12, 13, 14]
easy_exclusive_dn = [8, 9, 13, 14]
medium = [0, 1, 2, 3, 6, 7, 10, 11]
difficult = [4, 5, 15, 16, 17, 18]
commmutative = [4, 5, 6, 7, 12, 13, 14]
commmutative_exclusive_dn = [4, 5, 6, 7, 13, 14]
counter_e = 0
counter_m = 0
counter_d = 0
flag_dn = 0


def reset_level():
    global counter_e, counter_d, counter_m
    counter_e = 0
    counter_m = 0
    counter_d = 0


def determine(current):
    global easy, medium, difficult, counter_e, counter_m, counter_d, commmutative, flag_dn
    if current == -1:
        current = generation.current_index()
        if flag_dn:
            flag_dn = 0
            return commmutative_exclusive_dn[current % len(commmutative_exclusive_dn)]
        if commmutative[current % len(commmutative)] == 12:
            flag_dn = 1
            return commmutative[current % len(commmutative)]
    if current == -2:
        current = generation.current_index()
        temp = [0,1]
        return temp[current % len(temp)]
    if counter_m == 0:
        counter_m += 1
        return medium[current % len(medium)]
    elif counter_d == 0:
        counter_d += 1
        return difficult[current % len(difficult)]
    elif counter_e == 0:
        if flag_dn:
            flag_dn = 0
            counter_e += 1
            return easy_exclusive_dn[current % len(easy_exclusive_dn)]
        counter_e += 1
        if easy[current % len(easy)] == 12:
            flag_dn = 1
        return easy[current % len(easy)]
    else:
        if counter_m % 2 != 0:
            counter_m += 1
            return medium[current % len(medium)]
        else:
            if flag_dn:
                flag_dn = 0
                counter_e += 1
                return easy_exclusive_dn[current % len(easy_exclusive_dn)]
            counter_e += 1
            if easy[current % len(easy)] == 12:
                flag_dn = 1
            return easy[current % len(easy)]


def transform(node, node1, current):
    # index = random.randint(0, 4)0, 1, 2, 3, , 4, 5, 12
    # index = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13,14,15,16,17,18])
    index = determine(current)
    if index == 0:
        # ┐(p∧q) = ┐p∨┐q
        # node_p, node_q = add_and(add_bracket(add_negation(node)))
        print('use rule 0: ┐(p∧q) = ┐p∨┐q')
        node_p, node_q = add_and(add_negation(node))
        new0, new1 = add_or(node1)
        node_p1 = add_negation(new0)
        node_q1 = add_negation(new1)
        generation.generate_two(node_p, node_p1)
        generation.generate_two(node_q, node_q1)
    elif index == 1:
        # '┐(p∨q) = ┐p∧┐q'
        print('use rule 1: ┐(p∨q) = ┐p∧┐q')
        temp = add_negation(node)
        nodep, nodeq = add_or(temp)
        new0, new1 = add_and(node1)
        nodep1 = add_negation(new0)
        nodeq1 = add_negation(new1)
        generation.generate_two(nodep, nodep1)
        generation.generate_two(nodeq, nodeq1)
    elif index == 2:
        # p∨((q)∧(r)) = ((p)v(q))∧((p)v(r))
        # 这是左边的等式
        print('use rule 2: p∨(q∧r) = (pvq)∧(pvr)')
        node_p, temp = add_or(node)  # E1
        node_q, node_r = add_and(temp)  # E2 and E3
        # 这是右边的等式 由于方法返回两个值，必须要有temp来承接这些返回值并继续操作
        temp1, temp2 = add_and(node1)
        node_p1, node_q1 = add_or(temp1)  # E1 and E2
        temp3, node_r1 = add_or(temp2)  # E3
        temp2.left = node_p1  # E1
        # 调用进行下一步的生成
        generation.generate_two(node_p, node_p1)
        generation.generate_two(node_q, node_q1)
        generation.generate_two(node_r, node_r1)
    elif index == 3:
        # p∧((q)∨(r)) = ((p)∧(q))v((p)∧(r)) 和上面的基本一摸一样，都属于distributive
        # 这是左边的等式
        print('use rule 3: p∧(q∨r) = (p∧q)v(p∧r)')
        node_p, temp = add_and(node)  # E1
        node_q, node_r = add_or(temp)  # E2 and E3
        # 这是右边的等式 由于方法返回两个值，必须要有temp来承接这些返回值并继续操作
        temp1, temp2 = add_or(node1)
        node_p1, node_q1 = add_and(temp1)  # E1 and E2
        temp3, node_r1 = add_and(temp2)  # E3
        temp2.left = node_p1  # E1
        # 调用进行下一步的生成
        generation.generate_two(node_p, node_p1)
        generation.generate_two(node_q, node_q1)
        generation.generate_two(node_r, node_r1)
    elif index == 4:
        #  (p)v((p)∧(q)) = p
        # 左边等式
        print('use rule 4: pv(p∧q) = p')
        node_p, temp = add_or(node)  # E1
        temp1, node_q = add_and(temp)  # E2
        temp.left = node_p
        #  右边等式
        # node1.left = node_p
        generation.generate_two(node_p, node1)
        generation.generate_two(node_q, None)
    elif index == 5:
        #  (p)∧((p)v(q)) = p
        # 左边等式
        print('use rule 5: p∧(pvq) = p')
        node_p, temp = add_and(node)  # E1
        temp1, node_q = add_or(temp)  # E2
        temp.left = node_p
        #  右边等式
        # node1.left = node_p
        generation.generate_two(node_p, node1)
        generation.generate_two(node_q, None)
    elif index == 6:
        print('use rule 6: p∧p = p')
        node_p = Node('E')
        node.left = node_p
        node.mid = Node('∧')
        node.right = node_p
        generation.generate_two(node_p, node1)
    elif index == 7:
        print('use rule 7: p∨p = p')
        node_p = Node('E')
        node.left = node_p
        node.mid = Node('∨')
        node.right = node_p
        generation.generate_two(node_p, node1)
    elif index == 8:
        print('use rule 8: p∨T = T')
        # p∨F = p',   # 14 identity
        nodes = generation.generate_nodes(['∨', 'E', 'T', 'T'])
        node.left = nodes[1]
        # left = add_bracket(node.left)
        node.mid = nodes[0]
        node.right = nodes[2]
        node1.left = nodes[3]
        generation.generate_two(nodes[1], None)
    elif index == 9:
        print('use rule 9: p∧F = F')
        # 'p^T = p',  # 13 identity
        nodes = generation.generate_nodes(['∧', 'E', 'F'])
        node.left = nodes[1]
        # left = add_bracket(node.left)
        node.mid = nodes[0]
        node.right = nodes[2]
        node1.left = nodes[2]
        generation.generate_two(node.left, None)
    elif index == 10:
        print('use rule 10: p∧┐p = F')
        node_p, temp = add_and(node)
        node_p1 = add_negation(temp)
        temp.right = node_p
        node1.left = Node('F')
        generation.generate_two(node_p, None)
    elif index == 11:
        print('use rule 11: p∨┐p = T')
        node_p, temp = add_or(node)
        node_p1 = add_negation(temp)
        temp.right = node_p
        node1.left = Node('T')
        generation.generate_two(node_p, None)
    elif index == 12:
        print('use rule 12: ┐┐p = p')
        nodes = generation.generate_nodes(['┐', '┐', 'E', 'E'])
        node.mid = nodes[0]
        node.right = nodes[3]
        node.right.mid = nodes[1]
        node.right.right = nodes[2]
        flag = generation.current_index()
        if flag < 14:
            generation.generate_two(node.right.right, node1)
        else:
            transform(node.right.right, node1, -2)
    elif index == 13:
        print('use rule 13: p∧T = p')
        # 'p^T = p',  # 13 identity
        nodes = generation.generate_nodes(['∧', 'E', 'T'])
        node.left = nodes[1]
        # left = add_bracket(node.left)
        node.mid = nodes[0]
        node.right = nodes[2]
        generation.generate_two(node.left, node1)
    elif index == 14:
        print('use rule 14: p∨F = p')
        # p∨F = p',   # 14 identity
        nodes = generation.generate_nodes(['∨', 'E', 'F'])
        node.left = nodes[1]
        # left = add_bracket(node.left)
        node.mid = nodes[0]
        node.right = nodes[2]
        generation.generate_two(node.left, node1)
    elif index == 15:
        print('use rule 15: p∧q = q∧p')
        # 'p^q = q^p',    # 15 commutative
        left, right = add_and(node)
        left1, right1 = add_and(node1)
        transform(left, right1, -1)
        generation.generate_two(right, left1)
    elif index == 16:
        print('use rule 16: p∨q = q∨p')
        # 'p∨q = q∨p',    # 16
        left, right = add_or(node)
        left1, right1 = add_or(node1)
        transform(left, right1, -1)
        generation.generate_two(right, left1)
    elif index == 17:
        print('use rule 17: (p∧q)∧r = p∧(q∧r)')
        # '(p^q)^r = p^(q^r)',    # 17 association
        e0, r0 = add_and(node)
        p0, q0 = add_and(e0)
        p1, e1 = add_and(node1)
        q1, r1 = add_and(e1)
        transform(q0, q1, -1)
        generation.generate_two(p0, p1)
        generation.generate_two(r0, r1)
    elif index == 18:
        print('use rule 18: (p∨q)∨r = p∨(q∨r)')
        # '(p∨q)∨r = p∨(q∨r)',    # 18
        e0, r0 = add_or(node)
        p0, q0 = add_or(e0)
        p1, e1 = add_or(node1)
        q1, r1 = add_or(e1)
        transform(q0, q1, -1)
        generation.generate_two(p0, p1)
        generation.generate_two(r0, r1)


def add_negation(node):
    nodes = generation.generate_nodes(['┐', 'E'])
    node.mid = nodes[0]
    node.right = nodes[1]
    # new = add_bracket(node.right)
    return node.right


def add_or(node):
    nodes = generation.generate_nodes(['E', '∨', 'E'])
    node.left = nodes[0]
    # new0 = add_bracket(node.left)
    node.mid = nodes[1]
    node.right = nodes[2]
    # new1 = add_bracket(node.right)
    return node.left, node.right


def add_and(node):
    nodes = generation.generate_nodes(['E', '∧', 'E'])
    node.left = nodes[0]
    # new0 = add_bracket(node.left)
    node.mid = nodes[1]
    node.right = nodes[2]
    # new1 = add_bracket(node.right)
    return node.left, node.right


def add_bracket(node):
    nodes = generation.generate_nodes(['(', 'E', ')'])
    node.left = nodes[0]
    node.mid = nodes[1]
    node.right = nodes[2]
    return node.mid
