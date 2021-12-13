class Node:
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.next = next
        self.prev = prev


class DoublyLinkedList:
    def __init__(self, length):
        self.head = None
        self.tail = None
        self.length = length
        self.size = 0

    def addFirst(self, data):
        removedNode = None
        if self.size == self.length:
            removedNode = self.removeLast()

        if self.head is None:
            if self.tail is None:
                newNode = Node(data, None, None)
                self.head = newNode
                self.tail = newNode
                self.size += 1
                return newNode, removedNode
        else:
            newNode = Node(data, None, self.head)
            self.head.prev = newNode
            self.head = newNode
            self.size += 1
            return newNode, removedNode

    def removeLast(self):
        removedNode = self.tail
        self.tail.prev.next = None
        self.tail = self.tail.prev
        self.size -= 1
        return removedNode

    def moveFront(self, node):
        if self.size != 1 and node is not self.head:
            if node is self.tail:
                self.tail = self.tail.prev
                self.tail.next = None
            else:
                node.next.prev = node.prev
                node.prev.next = node.next
            self.head.prev = node
            node.next = self.head
            node.prev = None
            self.head = node

    def getList(self):
        l = []
        node = self.head
        while node is not None:
            l.append(node.data)
            node = node.next

        return l


class LRUCache:
    def __init__(self, cacheSize):
        self.cacheSize = cacheSize
        self.IdToNode = {}
        self.IdToValue = {}
        self.dll = DoublyLinkedList(cacheSize)

    def set(self, key, value):
        self.IdToValue[key] = value
        node, removedNode = self.dll.addFirst((key, value))
        self.IdToNode[key] = node
        if removedNode is not None:
            del self.IdToNode[removedNode.data[0]]
            del self.IdToValue[removedNode.data[0]]

    def get(self, key):
        if key not in self.IdToValue.keys():
            return None
        node = self.IdToNode[key]
        self.dll.moveFront(node)
        return self.IdToValue[key]
