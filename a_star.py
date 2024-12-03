#from app.operations import get_container_list
#work in progress, will discuss on friday 
import numpy as np
import re 
import copy
class load_unload_problem:
    def __init__(self,initial_state):
        self.initial_state = initial_state
    
    def goal_test(self):
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
    

    
def expand(node, operators, containers_to_load):
    children = []
    columns = len(node.state[0])
    rows = len(node.state)
    row_idx_of_top_container = [None] * columns    
    row_idx_of_valid_space = [None] * columns
    

    #find empty spaces in each column and find the index of the topmost container of each column
    for col in range(columns):
        for row in reversed(range(rows)):
            if node.state[row][col][1] == "UNUSED":
                if row != rows - 1 and node.state[row+1][col][1] != "NAN":
                    row_idx_of_top_container[col] = row + 1
                row_idx_of_valid_space[col] = row
                break
            elif node.state[row][col][1] != "NAN":
                if row == 0:
                    row_idx_of_top_container[col] = row
                continue

    #move container to the top of the other valid columns
    for myCol in range(columns):
        myRow = row_idx_of_top_container[myCol]
        # skip columns with no containers
        if myRow == None:
            continue
        # move container to the top of other valid columns
        for otherCol in range(columns):
            otherRow = row_idx_of_valid_space[otherCol]
            if otherRow != None and myCol != otherCol:
                children.append(Node(move_container(node.state, myRow, myCol, otherRow, otherCol)))
    
    #load each container that has to be loaded to one of the valid spots
    for container in containers_to_load:
        for col in range(columns):
            valid_row = row_idx_of_valid_space[col]
            if valid_row != None:
                children.append(Node(load_container(node.state,valid_row,col,container)))
    
    return children
            

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



def move_container(current_state, myRow, myCol, otherRow, otherCol):
    """
    Move the container from (myRow, myCol) to (otherRow, otherCol)
    """
    copy_state = copy.deepcopy(current_state)
    copy_state[otherRow][otherCol] = copy_state[myRow][myCol]
    copy_state[myRow][myCol] = (0,"UNUSED")
    return copy_state

def load_container(state, row, col,container):
    copy_state = copy.deepcopy(state)
    copy_state[row][col] = (1,container.name)
    return copy_state



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
    manifest_path = "/Users/antho/Downloads/load_unload_small.txt"
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
    print(cargo_matrix)
    for i in range(p_queue.len()):
        print(p_queue.pop())
    
if __name__ == "__main__": 
    main()
