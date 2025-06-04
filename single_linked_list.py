class Node:
    def __init__(self, value):
        self.val = value
        self.next = None
    
    def __repr__(self):
        return str(self.val)

class SinglyLinkedList:
    def __init__(self, values=[]):
        self.head = None
        for val in values:
            self.add(val)
    
    def add(self, val):
        insert = Node(val) # Node to be inserted
        if not self.head:
            self.head = insert
            return True
        
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = insert

        return True
    
    def remove(self, val): # first node that contains val
        curr = self.head
        prev = None
        while curr and curr.val != val:
            prev = curr
            curr = curr.next
        
        if not curr: # Didn't find val
            return False
        
        # Found val, lets remove this node
        if not prev:
            # means value was head
            self.head = curr.next
        else:
            prev.next = curr.next
        return True
    
    def weave(self):
        # Given a slow/fast pointer, when the fast pointer reaches the end, the slow pointer will be at the middle (lets assume we don't know how long the list is)
        tortise = hare = self.head

        while hare:
            tortise = tortise.next
            hare = hare.next.next if hare.next else None

        # Now tortise is pointing at the middle, lets go back to the start and weave
        a = self.head
        b = tortise
        if b == self.head:
            return self # only length 1, no weaving to do

        # a1, a2, ..., aN, b1, b2, ..., bN
        # a1, b1, a2, b2, ..., aN, bN
        stop = b # this will tell us when to stop when a reaches the original b
        while a != stop:
            a_temp = a.next
            b_temp = b.next
            a.next = b
            b.next = a_temp
            a = a_temp
            b = b_temp

        return self
        
    def __repr__(self):
        values = []
        curr = self.head
        while curr:
            values.append(str(curr.val))
            curr = curr.next
        return ' -> '.join(values)

a = SinglyLinkedList(['a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4', 'b5'])
print(f"a: {a}")
print("weaving...")
print(f"a: {a.weave()}")

# a = SinglyLinkedList([1,2,3,4,5,6,7,8,9,10])
# print(f"a: {a}")
# b = 7,3,1,10,5
# for i in b:
#     a.remove(i)
#     print(f"Removed {i}: {a}")
