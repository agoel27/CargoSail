
#from app.operations import send_container_list
import numpy as np
import re 
import copy

def goal_test(load_list,unload_list,current_state):
    #check if all the containers have been loaded/unloaded
    loads = load_list.copy()
    unloads = unload_list.copy()
    len_loads = len(loads)
    len_unloads = len(unloads)

    for row in current_state:
        for element in row:
            if len_loads != 0:
                if in_list(element[1],loads):
                    loads.remove(element)
            if len_unloads != 0:
                if in_list(element[1],unloads):
                    return False
    return len(loads) == 0
                
def calc_hueristic_cost(node,containers_to_unload,row_idx_of_top_container):
    cols = len(node.state[0])
    rows = len(node.state)
    unload_containers = 0 
    shortest_distance = 10000 #big number so the first distance becomes the min

    #count the amount of containers that are at the top of the columns and need to be unloaded
    for col in range(cols):
        for row in range(rows):
            if row_idx_of_top_container[col] != None:
                if in_list(node.state[row_idx_of_top_container[col], col],containers_to_unload):
                    unload_containers += 1
    
    #find smallest distance between last loaded container and container to unload in the state
    if node.last_loaded_container_location != None:
        for row in range(rows):
            for col in range(cols):
                if in_list(node.state[row][col],containers_to_unload):
                    distance = manhattan_distance((row,col), node.last_loaded_container_location)
                    if distance < shortest_distance:
                        shortest_distance = distance
        return shortest_distance + unload_containers
    return unload_containers 


def manhattan_distance(point1, point2):
    distance = 0
    for i in range(len(point1)):
        distance += abs(point1[i] - point2[i])

    return distance

def in_list(element, arr):
    if len(arr) != 0:
        for item in arr:
            if element == item[1]:
                return True
    return False 

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
        self.last_loaded_container_location = None
    
    def getState(self):
        return self.state
    
    def get_cost(self):
        return self.cost_g + self.cost_h

    def set_cost_g(self,cost_g):
        self.cost_g = cost_g
    
    def set_cost_h(self,cost_h):
        self.cost_h = cost_h
    
    

    
def expand(node, containers_to_load,containers_to_unload):
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
        for otherCol in range(columns):
            otherRow = row_idx_of_valid_space[otherCol]
            if otherRow != None and myCol != otherCol:
                #add func calls to calculate cost of node
                child = Node(move_container(node.state, myRow, myCol, otherRow, otherCol))
                child.set_cost_h(calc_hueristic_cost(child,containers_to_unload,row_idx_of_top_container))
                children.append(child)
    
    #load each container that has to be loaded to one of the valid spots and add it as a new Node to children
    if containers_to_load: #check if load list is empty
        for container in containers_to_load:
            for col in range(columns):
                valid_row = row_idx_of_valid_space[col]
                if valid_row != None:
                    child = Node(load_container(node.state,valid_row,col,container))
                    child.last_loaded_container_location = (valid_row,col)
                    child.set_cost_h(calc_hueristic_cost(child,containers_to_unload,row_idx_of_top_container))
                    children.append(child)
    
    #unload a container if its one of the containers at the top of a column and append that new node to children
    if containers_to_unload: #check if unload list is empty
        for col in range(columns):
            row = row_idx_of_top_container[col]
            if row != None:
                for container in containers_to_unload:
                    if container[1] == node.state[row][col][1]:
                        child = Node(unload_container(node.state,row,col))
                        child.set_cost_h(calc_hueristic_cost(child,containers_to_unload,row_idx_of_top_container))
                        children.append(child)
    
    return children
            

def load_manifest(file_path):
    matrix = np.empty((8, 12), dtype=object)
    pattern = r"\[(\d{2},\d{2})\], \{(\d+)\}, (\w+|NAN)"
    
    with open(file_path, "r") as file:
        content = file.read()
    
    # Find all matches
    matches = re.findall(pattern, content)
    
    for coord,weight,container_name in matches:
        coord_tuple = tuple(map(int, coord.split(',')))  # Convert coordinate to a tuple of integers

        # flip the y coordinate to match the matrix
        coord_tuple = (matrix.shape[0] - coord_tuple[0], coord_tuple[1] - 1)

        '''
            Set the matrix value to a tuple instead of int to store the location type and node 
        '''
        matrix[coord_tuple] = (weight,container_name)

    return matrix



def move_container(current_state, myRow, myCol, otherRow, otherCol):
    """
    Move the container from (myRow, myCol) to (otherRow, otherCol)
    """
    copy_state = copy.deepcopy(current_state)
    copy_state[otherRow][otherCol] = copy_state[myRow][myCol]
    copy_state[myRow][myCol] = ('0000',"UNUSED")
    return copy_state

def load_container(state, row, col,container):
    copy_state = copy.deepcopy(state)
    copy_state[row][col] = (container[0],container[1])
    return copy_state

def unload_container(state,row,col):
    copy_state = copy.deepcopy(state)
    copy_state[row][col] = ('0000',"UNUSED")
    return copy_state

#def a_star(problem,queueing_func):
    #nodes = makeQueue(Node(problem.initial_state))
    #loop do
    #if empty(nodes) then return fail
        #node = removeFront(nodes)
    #if goal_test(node.state) succeeds return node
        #nodes = queueing_function(nodes,expand(node,problem.operators))
    #end

    

def a_star(cargo,containers_to_load,containers_to_unload):
    nodes = priorityQueue()
    initial_state = Node(cargo)
    nodes.push(initial_state)

    while(nodes):
        current_node = nodes.pop()
        if goal_test(current_node):
            print("Goal reached! all the containers have been loaded/unloaded")
            return current_node
        children = expand(current_node,containers_to_load,containers_to_unload)
        for child in children:
            nodes.push(child)
    
def output_matrix(matrix):
    file = open("test.txt", 'w')
    for row in matrix:
       file.write(" | ".join([str(x) for x in row]) + '\n')
    file.close()

#testing that the classes are working as intended
def main():

    manifest_path = "/Users/antho/Downloads/load_unload_small.txt"
    cargo_matrix = load_manifest(manifest_path)
    output_matrix(cargo_matrix)
    
    
    
    

  
    
    
    
if __name__ == "__main__": 
    main()
