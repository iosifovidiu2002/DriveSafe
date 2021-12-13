from Server.LRUcache import DoublyLinkedList, LRUCache


def testDLL():
    dll = DoublyLinkedList(3)
    n1 = dll.addFirst(1)
    print(dll.getList())
    n2 = dll.addFirst(2)
    print(dll.getList())
    n3 = dll.addFirst(3)
    print(dll.getList())
    n4 = dll.addFirst(4)
    print(dll.getList())
    n5 = dll.addFirst(5)
    print(dll.getList())


def testLRU():
    lru = LRUCache(3)
    lru.set(1, 1)
    lru.set(2, 2)
    print(lru.dll.getList())
    print(lru.get(1))
    print(lru.get(1))
    print(lru.get(1))
    print(lru.get(1))
    print(lru.get(2))


if __name__ == "__main__":
    # testDLL()
    testLRU()