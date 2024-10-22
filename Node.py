class Node(object):
    def __init__(self,  element, left=None, mid=None, right=None, father = None, id = None):
        self.element = element
        self.left = left
        self.mid = mid
        self.right = right
        self.attri = ""
        self.id = id
        self.father = father

