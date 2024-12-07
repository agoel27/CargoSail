import copy
from heapq import heappop, heappush

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
        self.uniform_cost = 0
        self.heuristic_cost = 0
        self.crane_location = (-1, 0)

    def __lt__(self, other):
        return self.uniform_cost + self.heuristic_cost < other.uniform_cost + other.heuristic_cost
    
    def get_state(self):
        return self.data
    
    def get_crane_location(self):
        return self.crane_location
    
    def get_uniform_cost(self):
        return self.uniform_cost

    def get_heuristic_cost(self):
        return self.heuristic_cost
    
    def set_crane_location(self, coordinates):
        self.crane_location = coordinates

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
        self.initial_state = initial_state

    def get_initial_state(self):
        """
        Return the initial state which represents the ship's incoming manifest
        """
        return self.initial_state

    def goal_test(self, current_state):
        """
        Check if the current state satisfies the balance condition
        The goal is achieved if the weights on the left and right sides are less than 10% different
        """
        left_side_weight = 0
        right_side_weight = 0
        
        for row in current_state:
            for i in range(len(row)):
                if i  < (len(row) / 2):
                    left_side_weight += row[i][0]
                else:
                    right_side_weight += row[i][0]

        if left_side_weight == 0 and right_side_weight == 0:
            return True
        if left_side_weight == 0 or right_side_weight == 0:
            return False
        return max(left_side_weight, right_side_weight) / min(left_side_weight, right_side_weight) < 1.1

def calculate_manhattan_dist(my_row, my_col, other_row, other_col):
    delta_y = abs(my_row - other_row)
    delta_x = abs(my_col - other_col)
    return delta_y + delta_x

def calculate_balance_heuristic(current_state):

    heuristic_cost = 0
    left_side_weight = 0
    right_side_weight = 0
    total_weight = 0
    num_rows = len(current_state)
    num_cols = len(current_state[0])
    mid_col = num_cols // 2

    # lists to store weights with their locations
    left_side_ordered_weights = []
    right_side_ordered_weights = []
    
    # iterate through the ship data and collect weights with locations
    for row_idx in range(num_rows):
        # collect weights from the left half
        for col_idx in range(mid_col):
            left_side_ordered_weights.append((current_state[row_idx][col_idx][0], (row_idx, col_idx)))
            left_side_weight += current_state[row_idx][col_idx][0]
            total_weight += current_state[row_idx][col_idx][0]
        
        # collect weights from the right half
        for col_idx in range(mid_col, num_cols):
            right_side_ordered_weights.append((current_state[row_idx][col_idx][0], (row_idx, col_idx)))
            right_side_weight += current_state[row_idx][col_idx][0]
            total_weight += current_state[row_idx][col_idx][0]
    
    # sort both lists in ascending order based on the weights
    left_side_ordered_weights.sort(key=lambda x: x[0], reverse=True)
    right_side_ordered_weights.sort(key=lambda x: x[0], reverse=True)
    
    range_min = total_weight / 2.1
    range_max = (total_weight * 1.1) / 2.1

    if left_side_weight > range_min and left_side_weight < range_max:
        return 0
    
    if left_side_weight > right_side_weight:
        heavier_side_ordered_weights = left_side_ordered_weights
        heavier_side_weight = left_side_weight
        lighter_side_weight = right_side_weight
    else:
        heavier_side_ordered_weights = right_side_ordered_weights
        heavier_side_weight = right_side_weight
        lighter_side_weight = left_side_weight
    
    for index, (weight, location) in enumerate(heavier_side_ordered_weights):
        if weight == 0 or lighter_side_weight + weight >= range_max:
            continue
        lighter_side_weight += weight
        heavier_side_weight -= weight
        heuristic_cost += mid_col - heavier_side_ordered_weights[index][1][1] if mid_col - heavier_side_ordered_weights[index][1][1] > 0 else abs(mid_col - heavier_side_ordered_weights[index][1][1]) + 1
    
    return heuristic_cost

def move_container(current_state, my_row, my_col, other_row, other_col):
    """
    Move the container from (my_row, my_col) to (other_row, other_col)
    """
    copy_state = copy.deepcopy(current_state)
    copy_state[other_row][other_col] = copy_state[my_row][my_col]
    copy_state[my_row][my_col] = (0, "UNUSED")
    return copy_state

def expand_node(current_node, explored_states):
    """
    Expand the current state by generating all possible new states where
    every top container is moved to the top of every other vaild column
    """
    current_state = current_node.data
    expanded_nodes = []                             # list to hold all expanded states
    num_rows = len(current_state)                   # total number of rows
    num_cols = len(current_state[0])                # total number of columns
    row_idx_of_top_container = [None] * num_cols    # array to store the row index of the top container in each column
    row_idx_of_valid_space = [None] * num_cols      # array to store the row index of valid locations for containers in each column
    crane_coordinates = current_node.get_crane_location()

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
    for my_col in range(num_cols):
        my_row = row_idx_of_top_container[my_col]
        # skip columns with no containers
        if my_row == None:
            continue
        # move container to the top of other valid columns
        for other_col in range(num_cols):
            other_row = row_idx_of_valid_space[other_col]
            if other_row != None and my_col != other_col:
                new_state = move_container(current_state, my_row, my_col, other_row, other_col)
                if tuple(map(tuple, new_state)) not in explored_states:
                    node_to_add = Node(new_state)
                    node_to_add.set_uniform_cost(current_node.uniform_cost + calculate_manhattan_dist(crane_coordinates[0], crane_coordinates[1], my_row, my_col) + calculate_manhattan_dist(my_row, my_col, other_row, other_col))
                    node_to_add.set_heuristic_cost(calculate_balance_heuristic(node_to_add.get_state()))
                    node_to_add.set_crane_location((other_row, other_col))
                    expanded_nodes.append(node_to_add)
    
    current_node.add_children(expanded_nodes)
    return expanded_nodes

def a_star(manifest_data):
    problem = BalanceProblem(manifest_data)
    initial_state = problem.get_initial_state()

    queue = []
    heappush(queue, Node(initial_state))

    explored_states = set()
    explored_states.add(tuple(map(tuple, initial_state)))

    while(queue):
        current_node = heappop(queue)
        if problem.goal_test(current_node.get_state()):
            return current_node
        child_nodes = expand_node(current_node, explored_states)
        for child_node in child_nodes:
            heappush(queue, child_node)
            explored_states.add(tuple(map(tuple, child_node.get_state())))
    return 0

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

example_manifest_data = [
    [(0, "UNUSED"), (0, "UNUSED"), (50, "DOG"), (0, "UNUSED")],
    [(0, "UNUSED"), (0, "UNUSED"), (50, "DOG"), (0, "NAN")],
    [(0, "UNUSED"), (1, "CAT"), (0, "NAN"), (0, "NAN")],
    [(0, "UNUSED"), (110, "CAT"), (0, "NAN"), (0, "NAN")]
]

solution_node = a_star(example_manifest_data)

for row in solution_node.data:
    print(row)

# array = [
#     [12, 2, 0, 8],
#     [3, 8, 2, 45],
#     [9, 8, 1, 4]
# ]