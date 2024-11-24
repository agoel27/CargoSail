import re
import numpy as np

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

def load_manifest(file_path):
    matrix = np.empty((8, 12), dtype=object)
    pattern = r"\[(\d{2},\d{2})\], \{\d+\}, (\w+|NAN)"
    
    with open(file_path, "r") as file:
        content = file.read()
    
    # Find all matches
    matches = re.findall(pattern, content)
    
    for coord, container in matches:
        coord_tuple = tuple(map(int, coord.split(',')))  # Convert coordinate to a tuple of integers

        # flip the y coordinate to match the matrix
        coord_tuple = (matrix.shape[0] - coord_tuple[0], coord_tuple[1] - 1)

        '''
            Set the matrix value to a tuple instead of int to store the location type and node 
        '''
        if container == "NAN":
            matrix[coord_tuple] = -1 # Set to -1 if container is "NAN"
        elif container == "UNUSED":
            matrix[coord_tuple] = 0
        else:
            matrix[coord_tuple] = 1

    return matrix
    

#testing that the classes are working as intended
def main():
    manifest_path = "/Users/jerryli/Downloads/load_unload_small.txt"
    cargo_matrix = load_manifest(manifest_path) 

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
