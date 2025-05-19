class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.alive = True
    
    def die(self):
        if not self.alive:
            raise RuntimeError("Already Dead")
        self.alive = False
    
    def isDead(self):
        return not self.alive
    
    def __repr__(self):
        repr_string = self.name
        if not self.alive:
            repr_string += " ☠️"
        return repr_string
    
    def print_tree(self, level=0):
        print("\t" * level, end="")
        print(self)
        for child in self.children:
            child.print_tree(level = level + 1)

def search(currNode, name):
    if not currNode:
        return None
    if currNode.name == name:
        return currNode
    for child in currNode.children:
        if found := search(child, name):
            return found

class ThroneInheritance:

    def __init__(self, kingName: str):
        self.king = Node(kingName)

    def birth(self, parentName: str, childName: str) -> None:
        parent = search(self.king, parentName)
        parent.children.append(Node(childName))

    def death(self, name: str) -> None:
        curr = search(self.king, name)
        curr.die()

    def getInheritanceOrder(self) -> list[str]:
        return self.getInheritanceOrderHelper(self.king)
    
    def getInheritanceOrderHelper(self, currNode: Node) -> list[str]:
        if not currNode:
            return None
        currOrder = [currNode.name] if currNode.alive else []
        for child in currNode.children:
            if exOrder := self.getInheritanceOrderHelper(child):
                currOrder.extend(exOrder)
        return currOrder    
        
    def print_tree(self):
        self.king.print_tree()

    def maxDescendantDistance(self, maxDistance: int):
        currNode = self.king
        if not currNode:
            return None, -1
        maxNode, maxScore = ThroneInheritance.maxDescendantDistanceHelper(self.king, maxDistance)
        return maxNode, maxScore
    
    @staticmethod
    def maxDescendantDistanceHelper(currNode: Node, maxDistance: int) -> Node:
        if not currNode:
            return None
        # Subproblem for children, get their max scores
        scores = [ ThroneInheritance.maxDescendantDistanceHelper(child, maxDistance) for child in currNode.children ]

        # Not actually the max but we'll check against children
        maxNode = currNode
        maxScore = ThroneInheritance.getDescendantDistance(currNode, maxDistance, 0)

        # find the max
        for node, score in scores:
            if score > maxScore:
                maxNode = node
                maxScore = score
        
        return maxNode, maxScore
    
    @staticmethod
    def getDescendantDistance(currNode: Node, maxDistance: int, distance: int) -> int:
        if not currNode:
            return 0
        if distance == maxDistance:
            return 1 # done traversing
        score = sum([ ThroneInheritance.getDescendantDistance(child, maxDistance, distance + 1) for child in currNode.children ])
        if distance != 0: 
            score += 1# were not counting the original node
        return score

# Your ThroneInheritance object will be instantiated and called as such:
kingName = "Caleb"
name = "Caleb"
obj = ThroneInheritance(kingName)
obj.birth("Caleb","Berlin")
obj.birth("Berlin","Kiki")
obj.birth("Kiki", "Jojo")
obj.birth("Kiki", "Dio")
obj.birth("Kiki", "Dio!")
obj.birth("Kiki", "Dio!!")
obj.birth("Kiki", "Dio!!!")
obj.print_tree()
maxNode, maxScore = obj.maxDescendantDistance(1)
print(f"Node: {maxNode}, Score: {maxScore}")
# obj.death(name)
# param_3 = obj.getInheritanceOrder()