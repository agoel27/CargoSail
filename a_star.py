import numpy as np
import re 
import copy
from collections import deque

def goal_test(load_list,unload_list,current_state):
    #check if all the containers have been loaded/unloaded
    loads = copy.deepcopy(load_list)
    unloads = copy.deepcopy(unload_list)
    load_count = 0

    for row in current_state:
        for element in row:
            if len(loads) != 0:
                if in_list(element,load_list):
                    load_count += 1
            if len(unloads) != 0:
                if in_list(element,unloads):
                    return False           
    return load_count == len(loads)
                
def calc_hueristic_cost(node,containers_to_unload,containers_to_load_count,row_idx_of_top_container):
    cols = len(node.state[0])
    rows = len(node.state)
    unload_containers_cost = 0 
    shortest_distance = 10000 #big number so the first distance becomes the min

    #count the amount of containers that are at the top of the columns and need to be unloaded
    # for col in range(cols):
    #     for row in range(rows):
    #         if row_idx_of_top_container[col] != None:
    #             if in_list(node.state[row_idx_of_top_container[col]][col],containers_to_unload):
    #                 unload_containers -= 1
                    
    #find smallest distance between last loaded container and container to unload in the state

    for container in containers_to_unload:
        unload_containers_cost += manhattan_distance((-1, 0), container[2])

    if node.last_loaded_container_location != None and containers_to_unload:
        for row in range(rows):
            for col in range(cols):
                if in_list(node.state[row][col],containers_to_unload):
                    distance = manhattan_distance((row,col), node.last_loaded_container_location)
                    if distance < shortest_distance:
                        shortest_distance = distance
        return shortest_distance + unload_containers_cost + (containers_to_load_count * 2)
    return unload_containers_cost + (containers_to_load_count *2)


def manhattan_distance(point1, point2):
    distance = 0
    for i in range(len(point1)):
        distance += abs(point1[i] - point2[i])

    return distance

def in_list(element, arr):
    if len(arr) != 0:
        for item in arr:
            if element[0] == item[0] and element[1] == item[1]:
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
        return node
    
    def len(self):
        return len(self.queue)
    
#node class for each state 
class Node:
    def __init__(self, current_state,load_list,unload_list):
        self.state = current_state
        self.parent = None
        self.children = []
        self.cost_g = 0
        self.cost_h = 0
        self.last_loaded_container_location = None
        self.load_list = load_list
        self.unload_list = unload_list
        self.crane_location = (-1,0)
        self.operation_info = (None, None)
    
    def getState(self):
        return self.state
    
    def get_cost(self):
        return self.cost_g + self.cost_h

    def set_cost_g(self,cost_g):
        self.cost_g = cost_g
    
    def set_cost_h(self,cost_h):
        self.cost_h = cost_h
    
    def get_cost_g(self):
        return self.cost_g

    def get_operation_info(self):
        return self.operation_info

    def get_solution_length_and_path(self, solution_node):

        path_length = 0
        current_node = solution_node
        solution_stack = deque()

        while(current_node.parent):
            solution_stack.append(current_node)
            path_length += 1
            current_node = current_node.parent

        return path_length, solution_stack
    
    def set_operation_info(self, operation_info):
        self.operation_info = operation_info
    
    def add_children(self, children):
        for child in children:
            self.children.append(child)
            child.parent = self

    
    

    
def expand(node, containers_to_load,containers_to_unload,explored_states):
    children = []
    columns = len(node.state[0])
    rows = len(node.state)
    row_idx_of_top_container = [None] * columns    
    row_idx_of_valid_space = [None] * columns
    crane_cords = node.crane_location
    
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
        
        # check if the current container is an unload, if so then skip
        # logic behind this is we dont want it to waste time putting the container in another spot if it should just be unloaded
        skip_column = False
        for container in containers_to_unload:
            if (node.state[myRow][myCol][0] == container[0] and node.state[myRow][myCol][1] == container[1]):
                skip_column = True
                break
        if skip_column:
            continue
        
        # check if there are any containers below the top one that are unloads
        # if there arent any, skip
        # logic is we dont want to move a container for no reason
        container_below_needs_unloading = False
        for row_below in range(myRow + 1, rows):  # Iterate through rows below myRow
            below_container = node.state[row_below][myCol]
            for container in containers_to_unload:
                if below_container[0] == container[0] and below_container[1] == container[1]:
                    container_below_needs_unloading = True
                    break
            if container_below_needs_unloading:
                break

        # Only proceed if a container below needs unloading
        if not container_below_needs_unloading:
            continue
            
        for otherCol in range(columns):
            otherRow = row_idx_of_valid_space[otherCol]
            if otherRow != None and myCol != otherCol:
                #add func calls to calculate cost of node
                new_state = move_container(node.state, myRow, myCol, otherRow, otherCol)
                if tuple(map(tuple, new_state)) not in explored_states:
                    location_from = "["+ str(myRow) + "," + str(myCol) + "]"
                    location_to = "["+ str(otherRow) + "," + str(otherCol) + "]"
                    for i in range(len(containers_to_unload)):
                        if containers_to_unload[i][0] ==  new_state[otherRow][otherCol][0] and containers_to_unload[i][1] ==  new_state[otherRow][otherCol][1]:
                            containers_to_unload[i][2] = (otherRow, otherCol)
                    child = Node(new_state,copy.deepcopy(containers_to_load),copy.deepcopy(containers_to_unload))
                    child.set_cost_h(calc_hueristic_cost(child,containers_to_unload,len(containers_to_load),row_idx_of_top_container))
                    child.set_cost_g(manhattan_distance((myRow,myCol),(otherRow,otherCol)) + manhattan_distance((crane_cords[0],crane_cords[1]),(myRow,myCol)) + node.get_cost_g())
                    child.crane_location = (otherRow,otherCol)
                    child.set_operation_info((location_from,location_to))
                    children.append(child)
    
    #load each container that has to be loaded to one of the valid spots and add it as a new Node to children
    if containers_to_load: #check if load list is empty
        col_counter = 0
        for col in range(columns):
            valid_row = row_idx_of_valid_space[col]
                        
            if valid_row != None:
                if col_counter > 3:
                    break
                
                col_counter += 1 # only allow first 3 available cols to be added as a child
                #temp_list_load = containers_to_load.copy()
                for container in containers_to_load:
                    temp_list_load = copy.deepcopy(containers_to_load)
                    temp_list_load.remove(container)
                    new_state = load_container(node.state,valid_row,col,container)
                    if tuple(map(tuple,new_state)) not in explored_states:
                        location_from = "[truck]"
                        location_to = "["+ str(valid_row) + "," + str(col) + "]"
                        child = Node(new_state,temp_list_load,copy.deepcopy(containers_to_unload))
                        child.last_loaded_container_location = (valid_row,col)
                        child.set_cost_h(calc_hueristic_cost(child,containers_to_unload,len(temp_list_load),row_idx_of_top_container))
                        child.set_cost_g(manhattan_distance((valid_row,col),(-1,0)) +manhattan_distance((crane_cords[0],crane_cords[1]),(valid_row,col))+ 2 + node.get_cost_g())
                        child.crane_location = (valid_row,col)
                        child.set_operation_info((location_from,location_to))
                        children.append(child)
    
    #unload a container if its one of the containers at the top of a column and append that new node to children
    if containers_to_unload: #check if unload list is empty
        for col in range(columns):
            row = row_idx_of_top_container[col]
            if row != None:
                #temp_list_unload = containers_to_unload.copy()
                for container in containers_to_unload:
                    if container[1] == node.state[row][col][1]:
                        temp_list_unload = copy.deepcopy(containers_to_unload)
                        temp_list_unload.remove(container)
                        new_state = unload_container(node.state,row,col)
                        if tuple(map(tuple,new_state)) not in explored_states:
                            location_from = "["+ str(row) + "," + str(col) + "]"
                            location_to = "[truck]"
                            child = Node(new_state,copy.deepcopy(containers_to_load),temp_list_unload)
                            child.set_cost_h(calc_hueristic_cost(child,temp_list_unload,len(containers_to_load), row_idx_of_top_container))
                            child.set_cost_g(manhattan_distance((row,col),(-1,0)) + manhattan_distance((crane_cords[0],crane_cords[1]),(row,col))+ 2 + node.get_cost_g())
                            child.crane_location = (-1,0)
                            child.set_operation_info((location_from,location_to))
                            children.append(child)
    node.add_children(children)
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
    copy_state[myRow][myCol] = (0,"UNUSED")
    return copy_state

def load_container(state, row, col,container):
    copy_state = copy.deepcopy(state)
    copy_state[row][col] = (container[0],container[1])
    return copy_state

def unload_container(state,row,col):
    copy_state = copy.deepcopy(state)
    copy_state[row][col] = (0,"UNUSED")
    return copy_state

#def a_star(problem,queueing_func):
    #nodes = makeQueue(Node(problem.initial_state))
    #loop do
    #if empty(nodes) then return fail
        #node = removeFront(nodes)
    #if goal_test(node.state) succeeds return node
        #nodes = queueing_function(nodes,expand(node,problem.operators))
    #end

    

def a_star_load_unload(cargo,containers_to_load,containers_to_unload):
    nodes = priorityQueue()
    initial_node = Node(cargo,containers_to_load,containers_to_unload)
    nodes.push(initial_node)
    explored_states = set()
    explored_states.add(tuple(map(tuple,initial_node.state)))

    while(nodes):
        current_node = nodes.pop()
        if goal_test(current_node.load_list, current_node.unload_list ,current_node.state):
            print("Goal reached! all the containers have been loaded/unloaded")
            return current_node
        else:
            print("not the goal node, expanding child node")
        children = expand(current_node,current_node.load_list,current_node.unload_list,explored_states)
        for child in children:
            explored_states.add(tuple(map(tuple,child.state)))
            nodes.push(child)

def get_operations_info(solution_node):

    total_minutes = solution_node.get_cost_g()
    total_moves, solution_path = solution_node.get_solution_length_and_path(solution_node)
    operations_list = []
    manifest_list = []

    print("--------------------------------------------------")
    print("\nSolution Path:\n")
    for _ in range(len(solution_path)):
        current_node = solution_path.pop()
        operation_info = current_node.get_operation_info()
        operations_list.append(operation_info)
        manifest_list.append(current_node.state)
    
    return total_minutes, total_moves, operations_list, manifest_list

def output_matrix(matrix):
    file = open("test2.txt", 'w')
    for row in matrix:
       file.write(" | ".join([str(x) for x in row]) + '\n')
    file.close()

#testing that the classes are working as intended
def main():

    manifest_path = "/Users/antho/Downloads/load_unload_small.txt"
    cargo_matrix = load_manifest(manifest_path)
    load = [(210,'walmart')]
    unload = []
    goal_node = a_star_load_unload(cargo_matrix,load,unload)
    output_matrix(goal_node.state)
   
    print(get_operations_info(goal_node))
   
    

    


    
    
    
    

  
    
    
    
if __name__ == "__main__": 
    main()
