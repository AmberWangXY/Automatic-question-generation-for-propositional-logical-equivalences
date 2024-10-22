# 这个文件是我们去年写的那个方法的实现
'''
equRules = [
    '┐(p∧q) = ┐p∨┐q',  # 0-
    '┐(p∨q) = ┐p∧┐q',  # 1-
    'p∨(q∧r) = (p∨q)∧(p∨r)',  # 2-
    '(q∧r)∨p = (p∨q)∧(p∨r)',  # 3 -顺序可以调换
    'p∧(q∨r) = (p∧q)∨(p∧r)',  # 4-
    '(q∨r)∧p = (p∧q)∨(p∧r)',  # 5-
    'p→q = ┐p∨q',  # 6
    'p→q = ┐q→┐p',  # 7zz
    '(p→q)∨(p→r) = p→(q∨r)',  # 8
    '(p→r)∨(q→r) = (p∧q)→r)',  # 9
    '(p→q)∧(p→r) = p→(q∧r)',  # 10
    '(p→r)∧(q→r) = (p∨q)→r)',  # 11
    '┐(┐q) = q',  # 12
]

def printnodecheck(root):
    print("node id:", root.id, "  element:", root.element)
    if root.left == None and root.right == None:
        return
    else:
        printnodecheck(root.left)
    if root.right is not None:
        printnodecheck(root.right)

def transform_0(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∨'
        p = root.left.left
        q = root.left.right
        node_left = Node(node_id, '┐')
        node_left.left = p
        node_id += 1
        node_right = Node(node_id, '┐')
        node_right.left = q
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    transform_0(root.left, id)
    if root.right is not None:
        transform_0(root.right, id)


def transform_1(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∧'
        p = root.left.left
        q = root.left.right
        node_left = Node(node_id, '┐', p)
        node_id += 1
        node_right = Node(node_id, '┐', q)
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    transform_1(root.left, id)
    if root.right is not None:
        transform_1(root.right, id)


def transform_2(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∧'
        p = root.left
        q = root.right.left
        r = root.right.right
        node_left = Node(node_id, '∨')
        node_left.left = p
        node_left.right = q
        node_id += 1
        node_right = Node(node_id, '∨')
        node_right.left = p
        node_right.right = r
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_2(root.left, id)
    if root.right is not None:
        transform_2(root.right, id)


def transform_3(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∧'
        p = root.left.left
        r = root.left.right
        q = root.right
        node_left = Node(node_id, '∨')
        node_left.left = p
        node_left.right = q
        node_id += 1
        node_right = Node(node_id, '∨')
        node_right.left = p
        node_right.right = r
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_3(root.left, id)
    if root.right is not None:
        transform_3(root.right, id)


def transform_4(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∨'
        p = root.left
        q = root.left.left
        r = root.right.right
        node_left = Node(node_id, '∧')
        node_left = p
        node_id += 1
        node_right = Node(node_id, '∧')
        node_right.left = q
        node_right.right = r
        node_id += 1
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_4(root.left, id)
    if root.right is not None:
        transform_4(root.right, id)


def transform_5(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∨'
        p = root.right
        q = root.left.left
        r = root.left.right
        node_left = Node(node_id, '∧')
        node_id += 1
        node_right = Node(node_id, '∧')
        node_id += 1
        node_left.left = q
        node_left.right = r
        node_right.left = p
        node_right.right = r
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_5(root.left, id)
    if root.right is not None:
        transform_5(root.right, id)


def transform_6(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '∨'
        p = root.left
        q = root.right
        node_left = Node(node_id, '┐')
        node_id += 1
        node_left.left = p
        root.left = node_left
        root.right = q
        return
    else:
        transform_6(root.left, id)
    if root.right is not None:
        transform_6(root.right, id)


def transform_7(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        # root.element = '∨'
        p = root.left
        q = root.right
        node_left = Node(node_id, '┐')
        node_id += 1
        node_right = Node(node_id, '┐')
        node_id += 1
        node_left.left = q
        node_right.left = p
        root.left = node_left
        root.right = node_right
        return
    else:
        transform_7(root.left, id)
    if root.right is not None:
        transform_7(root.right, id)


def transform_8(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '→'
        p = root.left.left
        q = root.left.right
        r = root.right.right

        node_right = Node(node_id, '∨')
        node_id += 1

        node_right.left = q
        node_right.right = r
        root.left = p
        root.right = node_right
        return
    else:
        transform_8(root.left, id)
    if root.right is not None:
        transform_8(root.right, id)


def transform_9(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '→'
        p = root.left.left
        r = root.left.right
        q = root.right.left

        node_left = Node(node_id, '∧')
        node_id += 1

        node_left.left = p
        node_left.right = q
        root.right = r
        root.left = node_left
        return
    else:
        transform_9(root.left, id)
    if root.right is not None:
        transform_9(root.right, id)


def transform_10(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '→'
        p = root.left.left
        q = root.left.right
        r = root.right.right

        node_right = Node(node_id, '∧')
        node_id += 1

        node_right.left = q
        node_right.right = r
        root.left = p
        root.right = node_right
        return
    else:
        transform_10(root.left, id)
    if root.right is not None:
        transform_10(root.right, id)


def transform_11(root, id):
    global node_id
    if root.left == None and root.right == None:
        return
    if root.id == id:
        root.element = '→'
        p = root.left.left
        r = root.left.right
        q = root.right.left

        node_left = Node(node_id, '∨')
        node_id += 1

        node_left.left = p
        node_left.right = q
        root.right = r
        root.left = node_left
        return
    else:
        transform_11(root.left, id)
    if root.right is not None:
        transform_11(root.right, id)


def transform_12(root, id):
    if root.left == None and root.right == None:
        return
    if root.id == id:
        temp = root.left.left
        root.id = temp.id
        root.element = temp.element
        root.left = temp.left
        root.right = temp.right
        return
    transform_12(root.left, id)
    if root.right is not None:
        transform_12(root.right, id)


def transform(root, times):
    global pool
    if times >= 5:
        print("enough times transform!!")
        return
    if pool == []:
        print("no longer trzansform!!")
        return
    index = random.randint(0, len(pool) - 1)
    rule = pool[index]
    print("use rule:", rule)
    if rule[1] == 0:
        transform_0(root, rule[0])

    elif rule[1] == 1:
        transform_1(root, rule[0])

    elif rule[1] == 2:
        transform_2(root, rule[0])

    elif rule[1] == 3:
        transform_3(root, rule[0])

    elif rule[1] == 4:
        transform_4(root, rule[0])

    elif rule[1] == 5:
        transform_5(root, rule[0])

    elif rule[1] == 6:
        transform_6(root, rule[0])

    elif rule[1] == 7:
        transform_7(root, rule[0])

    elif rule[1] == 8:
        transform_8(root, rule[0])

    elif rule[1] == 9:
        transform_9(root, rule[0])
    elif rule[1] == 10:
        transform_10(root, rule[0])
    elif rule[1] == 11:
        transform_11(root, rule[0])
    elif rule[1] == 12:
        transform_12(root, rule[0])
    update(root)
    pool.clear()
    check(root)
    print(test.attri)
    print("随机池：", pool)
    times += 1
    transform(root, times)


def check(root):
    global pool
    # 找到能使用equivalent rule进行变换的tree structure，并将其node的id及其对应的equivalent rule加入随机池
    if root.left == None and root.right == None:
        return
    if root.element == '┐':
        if root.left.element == '∧':
            tmp = [root.id, 0]  # tmp[nodeID, equRules]
            pool.append(tmp)
        if root.left.element == '∨':
            tmp = [root.id, 1]
            pool.append(tmp)
        if root.left.element == '┐':
            tmp = [root.id, 12]
            pool.append(tmp)
        check(root.left)
    elif root.element == '∨':
        if root.right.element == '∧':
            tmp = [root.id, 2]
            pool.append(tmp)
        elif root.left.element == '∧':
            tmp = [root.id, 3]
            pool.append(tmp)
        elif root.left.element == '→' and root.right.element == '→':
            if root.left.left.attri == root.right.left.attri:
                tmp = [root.id, 8]
                pool.append(tmp)
            if root.left.right.attri == root.right.right.attri:
                tmp = [root.id, 9]
                pool.append(tmp)
        check(root.left)
        check(root.right)
    elif root.element == '∧':
        if root.right.element == '∨':
            tmp = [root.id, 4]
            pool.append(tmp)
        elif root.left.element == '∨':
            tmp = [root.id, 5]
            pool.append(tmp)
        elif root.left.element == '→' and root.right.element == '→':
            if root.left.left.attri == root.right.left.attri:
                tmp = [root.id, 10]
                pool.append(tmp)
            if root.left.right.attri == root.right.right.attri:
                tmp = [root.id, 11]
                pool.append(tmp)
        check(root.left)
        check(root.right)
    elif root.element == '→':
        tmp1 = [root.id, 6]
        pool.append(tmp1)
        tmp2 = [root.id, 7]
        pool.append(tmp2)
        check(root.left)
        check(root.right)


'''
