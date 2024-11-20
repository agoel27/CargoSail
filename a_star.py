#work in progress, will discuss on friday 
class load_unload_problem:
    def __init__(self,initial_state):
        self.initial_state = initial_state
    
    def goal_test(self):
        print("hello")
    
    def operators(self,node):
        print("hello")

#priority queue implementation
class priorityQueue:
    def __init__(self):
        self.queue = []
    def is_empty(self):
        return len(self.queue) == 0
    
    def push(self,node):
        self.queue.append(node) 
    
    def pop(self):
        min_cost = self.queue[0].get_cost()
        size = len(self.queue)
        idx = 0
        for i in range(size):
            if self.queue[i].get_cost() < min_cost:
                min_cost = self.queue[i].get_cost()
                idx = i
        node = self.queue[idx]
        self.queue.pop(idx)
        #returning the cost for testing purposes, will return the actual node
        return node.get_cost()
    def len(self):
        return len(self.queue)
    
#node class for each state 
class Node:
    def __init__(self, current_state):
        self.state = current_state
        self.parent = None
        self.children = []
        self.cost_g = 0
        self.cost_h = 0
    
    def getState(self):
        return self.state
    
    def get_cost(self):
        return self.cost_g + self.cost_h

    def set_cost_g(self,cost_g):
        self.cost_g = cost_g
    
    def set_cost_h(self,cost_h):
        self.cost_h = cost_h
    

    







def a_star(problem,queueing_func):
    #nodes = makeQueue(Node(problem.initial_state))
    #loop do
    #if empty(nodes) then return fail
        #node = removeFront(nodes)
    #if problem.goal_test(node.state) succeeds return node
        #nodes = queueing_function(nodes,expand(node,problem.operators))
    #end
    print("hello")

#testing that the classes are working as intended
def main():
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node1.set_cost_g(1)
    node2.set_cost_g(2)
    node3.set_cost_g(3)

    p_queue = priorityQueue()
    p_queue.push(node1)
    p_queue.push(node2)
    p_queue.push(node3)

    for i in range(p_queue.len()):
        print(p_queue.pop())
    
if __name__ == "__main__": 
    main()
