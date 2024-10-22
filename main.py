from Node import Node
import Generator, generation
def print_tree(root, indent=0):
    '''if node is not None:
        print(' ' * indent + str(node.element))
        if node.left is not None or node.mid is not None or node.right is not None:
            if node.left is not None:
                print_tree(node.left, indent + 2)
            if node.mid is not None:
                print_tree(node.mid, indent + 2)
            if node.right is not None:
                print_tree(node.right, indent + 2)'''
    if not root:
        return

    queue = [root]

    while queue:
        level_length = len(queue)

        for _ in range(level_length):
            node = queue.pop(0)
            print(node.element, end=' ')

            if node.left:
                queue.append(node.left)
            if node.mid:
                queue.append(node.mid)
            if node.right:
                queue.append(node.right)

        print()

def generate_questons(question_num, rule_num):
    questions = []
    i = 0
    while i < question_num :
        test = Node('E' )
        test1 = Node('E' )
        generation.generate_two(test,test1)
        generation.update(test)
        generation.update(test1)
        print(test.attri + '  =  ' + test1.attri)
        #print_tree(test)
        #print_tree(test1)
        flag = generation.reset_counter(rule_num)
        if not flag:
            print('not qualified')
        else:
            i += 1
            questions.append(test.attri + '  =  ' + test1.attri)
        print(' ')
    print('Here are the ' + str(question_num) + ' questions we generated which need to use at least ' + str(rule_num) + ' rules:')
    for j in questions:
        print( j )


generate_questons(5,3)
'''
test00 = Node('E')
left00 = Node('F')
right00 = Node('T')
mid00 = Node('∨')
test00.left = left00
test00.mid = mid00
test00.right = right00
generation.update(test00)
print("new test:"+test00.attri)
'''

