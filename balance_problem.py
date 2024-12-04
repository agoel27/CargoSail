import copy
from heapq import heappop, heappush

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
        self.uniform_cost = 0
        self.heuristic_cost = 0

    def get_state(self):
        return self.data
    
    def get_uniform_cost(self):
        return self.uniform_cost

    def get_heuristic_cost(self):
        return self.heuristic_cost

    def set_uniform_cost(self, uniform_cost):
        self.uniform_cost = uniform_cost

    def set_heuristic_cost(self, heuristic_cost):
        self.heuristic_cost = heuristic_cost

    def add_children(self, children):
        for child in children:
            self.children.append(child)
            child.parent = self

class BalanceProblem:

    def __init__(self, initial_state):
        """
        Initialize the balance problem with the initial state
        """
        self.initial_node = Node(initial_state)

    def get_initial_state(self):
        """
        Return the initial state which represents the ship's incoming manifest
        """
        return self.initial_node.data


    def expand_node(self, current_node):
        """
        Expand the current state by generating all possible new states where
        every top container is moved to the top of every other vaild column
        """
        current_state = current_node.data
        expanded_nodes = []                            # list to hold all expanded states
        num_rows = len(current_state)                   # total number of rows
        num_cols = len(current_state[0])                # total number of columns
        row_idx_of_top_container = [None] * num_cols    # array to store the row index of the top container in each column
        row_idx_of_valid_space = [None] * num_cols      # array to store the row index of valid locations for containers in each column
        

        # find row index of top container for each column and store in 'row_idx_of_top_container'
        # find row index of valid locations for containers for each column and store in 'row_idx_of_valid_space'
        """
        Example:
        
          0 1 2 3 4 5 6 7 8  9   10  11
        0 _ _ _ _ _ _ _ _ H ___ NAN ___
        1 _ _ _ _ _ _ _ _ I ___ NAN ___
        2 _ _ _ _ _ _ _ _ J ___ NAN ___         The top containers are C, E, F, H, G
        3 _ _ _ _ _ _ _ _ K ___ NAN ___     =>  row_idx_of_top_container = [None, None, 5, None, None, 6, 7, None, 0, None, None, 4]
        4 _ _ _ _ _ _ _ _ L ___ NAN  G          row_idx_of_valid_space   = [7, 7, 4, 7, 7, 5, 6, 7, None, 4, None, 3]
        5 _ _ C _ _ _ _ _ M NAN NAN NAN
        6 _ _ B _ _ E _ _ N NAN NAN NAN
        7 _ _ A _ _ D F _ O NAN NAN NAN
        """
        for col in range(num_cols):
            for row in reversed(range(num_rows)):
                if current_state[row][col][1] == "UNUSED":
                    if row != num_rows - 1 and current_state[row+1][col][1] != "NAN":
                        row_idx_of_top_container[col] = row + 1
                    row_idx_of_valid_space[col] = row
                    break
                elif current_state[row][col][1] != "NAN":
                    if row == 0:
                        row_idx_of_top_container[col] = row
                    continue

        # iterate over each column to find a top container to move
        for myCol in range(num_cols):
            myRow = row_idx_of_top_container[myCol]
            # skip columns with no containers
            if myRow == None:
                continue
            
            # move container to the top of other valid columns
            for otherCol in range(num_cols):
                otherRow = row_idx_of_valid_space[otherCol]
                if otherRow != None and myCol != otherCol:
                    expanded_nodes.append(Node(self.move_container(current_state, myRow, myCol, otherRow, otherCol)))
        
        return expanded_nodes

    def move_container(self, current_state, myRow, myCol, otherRow, otherCol):
        """
        Move the container from (myRow, myCol) to (otherRow, otherCol)
        """
        copy_state = copy.deepcopy(current_state)
        copy_state[otherRow][otherCol] = copy_state[myRow][myCol]
        copy_state[myRow][myCol] = (0,"UNUSED")
        return copy_state

    def goal_test(self, current_node):
        """
        Check if the current state satisfies the balance condition
        The goal is achieved if the weights on the left and right sides are less than 10% different
        """
        current_state = current_node.data
        left_side_weight = 0
        right_side_weight = 0
        
        for row in current_state:
            for i in range(len(row)):
                if i  < (len(row) / 2):
                    left_side_weight += row[i][0]
                else:
                    right_side_weight += row[i][0]
        return max(left_side_weight, right_side_weight) / min(left_side_weight, right_side_weight) < 1.1
        

example_ship_data = [
    [(109, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"),   (0, "UNUSED"),   (0, "UNUSED"),   (100, "UNUSED"), (0, "cat"),      (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"),  (1, "NAN")],
    [(0, "UNUSED"),   (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"),   (0, "UNUSED"),   (0, "UNUSED"),   (0, "dog"),      (0, "dog"),      (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"),  (0, "NAN")],
    [(0, "UNUSED"),   (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"),   (0, "UNUSED"),   (0, "lion"),     (0, "lion"),     (0, "lion"),     (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"),  (0, "NAN")],
    [(0, "UNUSED"),   (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"),   (0, "tiger"),    (0, "tiger"),    (0, "tiger"),    (0, "tiger"),    (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"),  (0, "NAN")],
    [(0, "UNUSED"),   (0, "UNUSED"), (0, "UNUSED"), (0, "elephant"), (0, "elephant"), (0, "elephant"), (0, "elephant"), (0, "elephant"), (0, "UNUSED"), (0, "UNUSED"), (0, "alien X"), (0, "NAN")],
    [(0, "UNUSED"),   (0, "UNUSED"), (0, "rabbit"), (0, "rabbit"),   (0, "rabbit"),   (0, "rabbit"),   (0, "rabbit"),   (0, "rabbit"),   (0, "NAN"),    (0, "UNUSED"), (0, "NAN"),     (0, "NAN")],
    [(0, "UNUSED"),   (0, "fox"),    (0, "fox"),    (0, "fox"),      (0, "fox"),      (0, "fox"),      (0, "fox"),      (0, "fox"),      (0, "NAN"),    (0, "UNUSED"), (0, "NAN"),     (0, "NAN")],
    [(0, "bear"),     (0, "bear"),   (0, "bear"),   (0, "bear"),     (0, "bear"),     (0, "bear"),     (0, "bear"),     (0, "bear"),     (0, "NAN"),    (0, "UNUSED"), (0, "NAN"),     (0, "NAN")]
]

# states = BalanceProblem(example_ship_data).expand_node(Node(example_ship_data))

# for state in states:
#     for row in state.data:
#         print(row)

#     print("end")

def a_star():
    return 0
