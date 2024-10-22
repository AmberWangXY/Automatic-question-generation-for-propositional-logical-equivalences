from Node import Node
import numpy as np
import random
import Equation
from Hash import number
# node_id = 0  # 记录每个node的id方便后续在随机池中检索

# 两种操作的次数控制在都不超过十次
counter_e = 1
counter_t = 1
counter_u = 1
counter_r = 1
# for calculate the current ID number
index = 0
counter_ring = 0
prime = [1,2,3,5,7,11,13,17,19,23,26,29,31,33,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149]
new_number = ''
start = 0
# character pool
cv = ["p", "q", "r", "s", "T", "F"]
# rules number
level = 0
# probability
probability = np.array([0.6, 0.4, 0.0])
e_pro = 10
# truth table
truth_table_and = np.array([['T','F'],['F','F']])
truth_table_or = np.array([['T','T'],['T','F']])
truth_table_to = np.array([['T','F'],['T','T']])

def reset_counter(rule_num):
    global counter_e, counter_r, counter_t, counter_u, level, e_pro, probability
    level = 0
    probability = np.array([0.6, 0.4, 0.0])
    e_pro = 10
    counter_e = 1
    counter_t = 1
    counter_u = 1
    counter_r = 1
    if Equation.counter_e + Equation.counter_d + Equation.counter_m < rule_num:
        flag = False
    else:
        flag = True
    Equation.reset_level()
    return flag

def current_index():
    global index, new_number
    if index == len(new_number):
        reconsisitue()
    if(new_number[index].isalpha()):
        res = ord(new_number[index]) - 87
        index += 1
        return res
    res = int(new_number[index])
    index += 1
    return res

def reconsisitue():
    global number, prime, counter_ring, new_number, start
    '''
    temp1 = prime[counter_ring]
    temp = number[start::temp1]
    start = (start+(len(temp))*prime[counter_ring])%31
    new_number += temp
    if len(new_number) % 32 == 0:
        counter_ring += 1
        start = 0
        return
    else:
        reconsisitue()'''
    for i in range(32):
        new_number += number[start]
        start += prime[counter_ring]
        if start == 31:
            continue
        else:
            start %= 31
    start = 0
    counter_ring += 1
    return


# 用来批量生成想要的node，是为了方便一次性需要生成多个node。

# 即E to E→T这样就可以一次生成三个node，对应'E', '→', 'T'
def generate_nodes(elements):
    res = []
    for i in elements:
        new = Node(i)

        res.append(new)
    return res


def cal_priority(operator):
    if operator == '→':
        return 1
    elif operator == '∨':
        return 2
    elif operator == '∧':
        return 3
    elif operator == '┐':
        return 4
    elif operator == '@':
        return 4
    elif operator == '@f':
        return 0


def compare_priority(father, child):
    f = cal_priority(father)
    c = cal_priority(child)
    if c < f:
        return True
    else:
        return False

def calculate_constant(mid, left, right):
    row = column = 0
    if left == 'F':
        row = 1
    if right == 'F':
        column = 1
    if mid ==  '→':
        return truth_table_to[row][column]
    elif mid ==  '∨':
        return truth_table_or[row][column]
    elif mid ==  '∧':
        return truth_table_and[row][column]



# 因为一些rule的特殊性，需要单独对节点进行变换
def generate(node):
    if node.element == 'E':
        generate_E(node, None)
    elif node.element == 'N':
        generate_T(node, node)
    elif node.element == 'U':
        generate_U(node, node)
    elif node.element == 'R':
        generate_R(node, None)
    return


# 因为我们要同时生成左右两边，所以这里后面应该改成有两个参数

def generate_two(node, node1):
    if node.element == 'E':
        generate_E(node, node1)
    elif node.element == 'N':
        generate_T(node, node1)
    elif node.element == 'U':
        generate_U(node, node1)
    elif node.element == 'R':
        generate_R(node, node1)
    return


def update_supplementary(root, flag, flag1):
    if flag and flag1:
        root.attri = '(' + root.left.attri + ')' + root.mid.element + '(' + root.right.attri + ')'
    elif flag and not flag1:
        root.attri = '(' + root.left.attri + ')' + root.mid.element + root.right.attri
    elif flag1 and not flag:
        root.attri = root.left.attri + root.mid.element + '(' + root.right.attri + ')'
    else:
        root.attri = root.left.attri + root.mid.element + root.right.attri


def update(root):
    # 从底部依次update每个node的attri，检查整棵树的attri只需要root的attri即可
    # terminal
    if root.left == None and root.right == None and root.mid == None:
        if root.element == 'T' or root.element == 'F':
            root.id = root.element
            #print("terminal:"+root.element)
        root.attri = root.element
        #print(root.attri)
        return '@'
    elif root.left != None and root.right == None and root.mid == None:
        # nonterminal
        child = update(root.left)
        father = '@f'
        flag = compare_priority(father, child)
        #
        if root.left.id == 'T' or root.left.id == 'F':
            root.id = root.left.id
            #print("non-terminal:"+root.id)
        #
        if flag:
            root.attri = '(' + root.left.attri + ')'
            #print(root.attri)
            return father
        root.attri = root.left.attri
        #print(root.attri)
        return child
    elif root.left == None:
        child = update(root.right)
        father = '┐'
        flag = compare_priority(father, child)

        #

        if root.right.attri == 'T':

            root.id = root.attri = 'F'
           # print('T becomes '+root.attri)
            #print(root.attri)
            return '@'
        elif root.right.attri == 'F':
            root.id = root.attri = 'T'
            #print('F becomes '+root.attri)
            #print(root.attri)
            return '@'
        #

        if flag:
            root.attri = '┐' + '(' + root.right.attri + ')'
            #print(root.attri)
            return father
        root.attri = '┐' + root.right.attri
        #print(root.attri)
        return father
    else:

        father = root.mid.element
        child = update(root.left)
        child1 = update(root.right)
        #
        if root.left.attri == 'T' or root.left.attri == 'F':
            if root.right.attri == 'T' or root.right.attri == 'F':
                root.id = root.attri = calculate_constant(root.mid.element, root.left.id, root.right.id)
                #print("make " + root.left.id + root.mid.element + root.right.id + " to " + root.id)
                #print(root.attri)
                return '@'
        #
        flag = compare_priority(father, child)
        flag1 = compare_priority(father, child1)
        update_supplementary(root, flag, flag1)
        #print(root.attri)
        return father


# 这里的四个函数是对应不同node时的相应变换操作
def generate_E(node, node1):
    judge = current_index()
    
    global level, probability, counter_e, e_pro
    '''level += 1
    
    if level > 8:
        probability = np.array([0.05, 0.05, 0.9])
        option = np.random.choice([1, 2, 3], p=probability.ravel())
    else:'''
    # use one rule in two steps
    # goto using rules probability: epro/16
    if judge < e_pro:
        option = 2
        e_pro = 10
    elif judge < (16-e_pro)/4 + e_pro:
        option = 1
        e_pro += 4#先试着改改 本来是3
    else:
        option = 3
        e_pro += 4#先试着改改 本来是3
    

    "这里不用通过e_pro决定的option，而是单独再判断"
    # only one side needs transformation
    if node1 == None:
        if judge < 14:#先试着改改 本来是12
            option = 3
        else:
            option = 1
        if option == 1:
            nodes = generate_nodes(['E', '→', 'N'])
           # print('E', '→', 'N')
            counter_e += 1
            node.left = nodes[0]
            node.mid = nodes[1]
            node.right = nodes[2]
            generate_two(node.left, None)
            generate_two(node.right, None)
            return
        else:
            node_left = Node('N')
            #print('N')
            node.left = node_left
            generate_two(node.left, None)
            return

     # control the most number of e, control the number of rules. e.g. counter_e < 5, rules in [2,4]
    # 参数修改1
    if counter_e < 3: #本来是4
        if option == 1:
            nodes = generate_nodes(['E', '→', 'N', 'E', '→', 'N'])
            #print('E', '→', 'N')
            counter_e += 1
            node.left = nodes[0]
            node.mid = nodes[1]
            node.right = nodes[2]
            node1.left = nodes[3]
            node1.mid = nodes[4]
            node1.right = nodes[5]
            generate_two(node.left, node1.left)
            generate_two(node.right, node1.right)
            return
        elif option == 2:
            counter_e += 1
            Equation.transform(node, node1, judge)
            return
            # generate_two(node2,node3)

        else:
            node_left = Node('N')
            node1_left = Node('N')
            #print('N')
            node.left = node_left
            node1.left = node1_left
            generate_two(node.left, node1.left)
            return
    else:
        node_left = Node('N')
        node1_left = Node('N')
        #print('N')
        node.left = node_left
        node1.left = node1_left
        generate_two(node.left, node1.left)
        return


def generate_T(node, node1):
    global level, probability, counter_t
    judge = current_index()
    '''
    level += 1
    if level > 8:
        probability = np.array([0.05, 0.05, 0.9])
    option = np.random.choice([1, 2, 3], p=probability.ravel())
    '''
    # 修改参数2，包括满足counter前后的概率调整
    if counter_t < 2:
        if judge < 15:#先试着改改 本来是12
            option = 2
        else:
            option = 1
    else:
        # 将这里直接改为进入option 2的U node生成，以缩短整体长度
        """if judge < 15:
            option = 2
        else:
            option = 1"""
        option = 2
    if node1 == None:
        if option == 1:
            nodes = generate_nodes(['N', '∨', 'U'])
            #print('N', '∨', 'U')
            counter_t += 1
            node.left = nodes[0]
            node.mid = nodes[1]
            node.right = nodes[2]
            generate_two(node.left, None)
            generate_two(node.right, None)
            return
        else:
            node_left = Node('U')
            #print('U')
            node.left = node_left
            generate_two(node.left, None)
            return
    if option == 1:
        nodes = generate_nodes(['N', '∨', 'U', 'N', '∨', 'U'])
        #print('N', '∨', 'U')
        counter_t += 1
        node.left = nodes[0]
        node.mid = nodes[1]
        node.right = nodes[2]
        node1.left = nodes[3]
        node1.mid = nodes[4]
        node1.right = nodes[5]
        generate_two(node.left, node1.left)
        generate_two(node.right, node1.right)
        return
    else:
        node_left = Node('U')
        node1_left = Node('U')
        #print('U')
        node.left = node_left
        node1.left = node1_left
        generate_two(node.left, node1.left)
        return


def generate_U(node, node1):
    global level, probability, counter_u
    judge = current_index()
    # 修改参数3，修改思路同上面的generate_T
    if counter_u < 2:
        if judge < 15:#先试着改改 本来是10
            option = 2
        else:
            option = 1
    else:
        """if judge < 15:
            option = 2
        else:
            option = 1"""
        option = 2
    if node1 == None:
        if option == 1:
            nodes = generate_nodes(['U', '∧', 'R'])
            #print('N', '∨', 'U')
            counter_u += 1
            node.left = nodes[0]
            node.mid = nodes[1]
            node.right = nodes[2]
            generate_two(node.left, None)
            generate_two(node.right, None)
            return
        else:
            node_left = Node('R')
           # print('U')
            node.left = node_left
            generate_two(node.left, None)
            return
    if option == 1:
        nodes = generate_nodes(['U', '∧', 'R', 'U', '∧', 'R'])
        #print('U', '∧', 'R')
        counter_u += 1
        node.left = nodes[0]
        node.mid = nodes[1]
        node.right = nodes[2]
        node1.left = nodes[3]
        node1.mid = nodes[4]
        node1.right = nodes[5]
        generate_two(node.left, node1.left)
        generate_two(node.right, node1.right)
        return
    else:
        node_left = Node('R')
        node1_left = Node('R')
        #print('R')
        # node_id += 1
        node.left = node_left
        node1.left = node1_left
        generate_two(node.left, node1.left)
        return


def generate_R(node, node1):
    global level, probability, counter_r
    judge = current_index()
    # 修改参数4
    if counter_r < 2:
        if judge < 2:#本来是4
            option = 1
        elif judge < 15:#本来是14
            option = 3
        else:
            option = 2
    else:
        if judge < 13:
            option = 3
        elif judge < 15:
            option = 2
        else:
            option = 1
    if node1 == None:
        if option == 2:
            nodes = generate_nodes(['┐', 'R'])
            #print('┐', 'R')
            counter_r += 1
            node.mid = nodes[0]
            node.right = nodes[1]
            generate_two(node.right, None)
            return
        elif option == 1:
            nodes = generate_nodes(['E'])
           # print('E')
            counter_r += 1
            node.left = nodes[0]
            generate_two(node.left, None)
            return
        else:
            judge = current_index() # 这里应该用一个新的bit来控制生成，而不是用旧的，此行为新加代码
            if judge < 14:
                val = cv[judge % (len(cv) - 2)]
            elif judge == 14:
                val = cv[4]
            else:
                val = cv[5]
            #print('terminal: '+val)
            node_left = Node(val)
            # node_id += 1
            node.left = node_left
            return
    if option == 2:
        nodes = generate_nodes(['┐', 'R', '┐', 'R'])
        #print('┐', 'R')
        counter_r += 1
        node.mid = nodes[0]
        node.right = nodes[1]
        node1.mid = nodes[2]
        node1.right = nodes[3]
        generate_two(node.right, node1.right)
        return
    elif option == 1:
        nodes = generate_nodes(['E', 'E'])
        #print('E')
        counter_r += 1
        node.left = nodes[0]
        node1.left = nodes[1]
        generate_two(node.left, node1.left)
        return
    else:
        judge = current_index()  # 这里应该用一个新的bit来控制生成，而不是用旧的，此行为新加代码
        if judge < 14:
            val = cv[judge%(len(cv)-2)]
        elif judge == 14:

            val = cv[4] # T
            new_judge = current_index()
            choice = new_judge % 2
            node_left = Node(val)
            if choice == 0:
                nodes = generate_nodes([ '∨', 'R']) # domination
                node.left = nodes[1]
                node.mid = nodes[0]
                node.right = node_left
                node1.left = node_left
                generate_R(node.left, None)
                return
            else:
                nodes = generate_nodes(['┐', 'R', '∨','R']) # negation
                node.left = nodes[1]
                node.mid = nodes[2]
                node.right = nodes[3]
                node.right.mid = nodes[0]
                node.right.right = nodes[1]
                node1.left = node_left
                generate_R(node.left, None)
                return

        else:
            val = cv[5] #F
            new_judge = current_index()
            choice = new_judge % 2
            node_left = Node(val)
            if choice == 0:
                # 之前这里和上面一样所以出问题了，domination的两个operator是不一样的
                nodes = generate_nodes(['∧', 'R'])  # domination
                node.left = nodes[1]
                node.mid = nodes[0]
                node.right = node_left
                node1.left = node_left
                generate_R(node.left, None)
                return
            else:
                nodes = generate_nodes(['┐', 'R', '∧', 'R'])  # negation
                node.left = nodes[1]
                node.mid = nodes[2]
                node.right = nodes[3]
                node.right.mid = nodes[0]
                node.right.right = nodes[1]
                node1.left = node_left
                generate_R(node.left, None)
                return
        #print('terminal: '+val)
        node_left = Node(val)
        node1_left = Node(val)
        # node_id += 1
        node.left = node_left
        node1.left = node1_left
        return
    
