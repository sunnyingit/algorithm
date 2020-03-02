#  -*- coding:utf8 -*-

"""
    设计：
    1. 使用dict保存所有的元素，使用双向链表保存使用状态
    2. 当数据最新使用后，把node插入到链表尾部，当链表元素超过capacity之后，删除链表头元素
    3. 注意：每次使用元素后，都需要更新元素在链表的位置
"""

class Node(object):

    __slots__ = ["key", "value", "prev", "next"]

    def __init__(self, key, value):
        self.value = value
        self.key = key
        self.next = None
        self.prev = None


class RLUCache(object):

    def __init__(self, capacity):
        self.dic = {}
        self.capacity = capacity

        self.prev = Node(-1, -1)
        self.tail = Node(-1, -1)

        self.prev.next = self.tail
        self.tail.prev = self.prev

    def set(self, key, value):
        if key in self.dic:
            node = self.dic[key]
            self.remove(node)

        node = Node(key, value)
        self.dic[key] = node
        self.append_to_tail(node)

        if len(self.dic) > self.capacity:
            node = self.prev.next
            self.remove(node)
            del self.dic[node.key]

    def append_to_tail(self, node):
        t = self.tail.prev
        t.next = node
        node.prev = t

        node.next = self.tail
        self.tail.prev = node

    def remove(self, node):
        p = node.prev
        n = node.next
        p.next = n
        n.prev = p


    def get(self, key, default=None):
        if key not in self.dic:
            return default

        node = self.dic[key]
        self.remove(node)
        self.append_to_tail(node)

        return node.value

    def dump(self):
        print self.dic
        node = self.prev
        while node.next:
            node = node.next
            print node.value



if __name__ == "__main__":
    dic = RLUCache(3)
    dic.set('a', 1)
    dic.set('b', 2)
    dic.set('c', 3)
    dic.set('d', 4)
    dic.set('e', 5)
