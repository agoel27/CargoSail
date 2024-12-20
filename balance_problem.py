import copy
from collections import deque
from heapq import heappop, heappush
from itertools import chain, combinations

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
        self.uniform_cost = 0
        self.heuristic_cost = 0
        self.crane_location = (-1, 0)
        self.balance_operation_info = (None, None)

    def __lt__(self, other):
        return self.uniform_cost + self.heuristic_cost < other.uniform_cost + other.heuristic_cost
    
    def get_state(self):
        return self.data
    
    def get_crane_location(self):
        return self.crane_location
    
    def get_balance_operation_info(self):
        return self.balance_operation_info
    
    def get_uniform_cost(self):
        return self.uniform_cost

    def get_heuristic_cost(self):
        return self.heuristic_cost
    
    def get_solution_length_and_path(self, solution_node):

        path_length = 0
        current_node = solution_node
        solution_stack = deque()

        while(current_node.parent):
            solution_stack.append(current_node)
            path_length += 1
            current_node = current_node.parent

        return path_length, solution_stack
    
    def set_crane_location(self, coordinates):
        self.crane_location = coordinates

    def set_balance_operation_info(self, balance_operation_info):
        self.balance_operation_info = balance_operation_info

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
        self.sift_goal_state = [[(0, "UNUSED")] * 12 for _ in range(8)]

    def get_initial_state(self):
        """
        Return the initial state which represents the ship's incoming manifest
        """
        return self.initial_state
    
    def get_sift_goal_state(self):
        return self.sift_goal_state

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
    
    def is_balancable(self):
        left_side_weights = []
        right_side_weights = []
        
        for row in self.initial_state:
            for i in range(len(row)):
                if row[i][1] != "UNUSED" and row[i][1] != "NAN":
                    if i  < (len(row) / 2):
                        left_side_weights.append(row[i][0])
                    else:
                        right_side_weights.append(row[i][0])
        
        if len(left_side_weights) == 0 and len(right_side_weights) == 0:
            return True
        
        all_weights = left_side_weights + right_side_weights
        for subset in chain.from_iterable(combinations(all_weights, r) for r in range(1, (len(all_weights) // 2) + 1)):
            left_weights = list(subset)

            right_weights = all_weights.copy()
            for weight in left_weights:
                right_weights.remove(weight)

            left_sum = sum(left_weights)
            right_sum = sum(right_weights)

            if min(left_sum, right_sum) > 0 and max(left_sum, right_sum) / min(left_sum, right_sum) < 1.1:
                return True
            
        return False
    
    def set_sift_goal_state(self):
        valid_entries = [(weight, name) for row in self.initial_state for weight, name in row if name != "UNUSED" and name != "NAN"]
        sorted_entries = sorted(valid_entries, key=lambda x: x[0], reverse=True)

        num_cols = len(self.initial_state[0])
        for row in reversed(range(len(self.initial_state))):
            left_ctr = 0
            right_ctr = 0
            for col in range(num_cols):
                if col%2 == 0:
                    left_ctr += 1
                    col = num_cols // 2 - left_ctr
                else:
                    col = num_cols // 2 + right_ctr
                    right_ctr += 1

                if sorted_entries and self.initial_state[row][col][1] != "NAN":
                    self.sift_goal_state[row][col] = sorted_entries.pop(0)
                elif self.initial_state[row][col][1] == "NAN":
                    self.sift_goal_state[row][col] = (0, "NAN")
    
    def sift_goal_test(self, current_state):
        if current_state == self.sift_goal_state:
            return True
        return False

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
    
    # sort both lists in descending order based on the weights
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

def calculate_sift_heuristic(current_state, problem):
    heuristic_cost = 0
    goal_state_copy = copy.deepcopy(problem.get_sift_goal_state())

    def get_location(value, state):
        for row in range(len(state)):
            for col in range(len(state[0])):
                if value == state[row][col]:
                    return row, col
    
    for my_row in range(len(current_state)):
        for my_col in range(len(current_state[0])):
            if current_state[my_row][my_col][1] != "UNUSED" and current_state[my_row][my_col][1] != "NAN":
                other_row, other_col = get_location(current_state[my_row][my_col], goal_state_copy)
                heuristic_cost += calculate_manhattan_dist(my_row, my_col, other_row, other_col)
                goal_state_copy[other_row][other_col] = (0, "UNUSED")
    
    return heuristic_cost

def move_container(current_state, my_row, my_col, other_row, other_col):
    """
    Move the container from (my_row, my_col) to (other_row, other_col)
    """
    copy_state = copy.deepcopy(current_state)
    copy_state[other_row][other_col] = copy_state[my_row][my_col]
    copy_state[my_row][my_col] = (0, "UNUSED")
    return copy_state

def expand_node(current_node, explored_states, is_sift, problem):
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
                    location_from = "["+ str(my_row) + "," + str(my_col) + "]"
                    location_to = "["+ str(other_row) + "," + str(other_col) + "]"
                    node_to_add = Node(new_state)
                    node_to_add.set_uniform_cost(current_node.uniform_cost + calculate_manhattan_dist(crane_coordinates[0], crane_coordinates[1], my_row, my_col) + calculate_manhattan_dist(my_row, my_col, other_row, other_col))
                    if not is_sift:
                        node_to_add.set_heuristic_cost(calculate_balance_heuristic(node_to_add.get_state()))
                    else:
                        node_to_add.set_heuristic_cost(calculate_sift_heuristic(node_to_add.get_state(), problem))
                    node_to_add.set_crane_location((other_row, other_col))
                    node_to_add.set_balance_operation_info((location_from, location_to, calculate_manhattan_dist(crane_coordinates[0], crane_coordinates[1], my_row, my_col) + calculate_manhattan_dist(my_row, my_col, other_row, other_col)))
                    expanded_nodes.append(node_to_add)

    
    current_node.add_children(expanded_nodes)
    return expanded_nodes

def a_star(manifest_data):
    is_sift = False
    problem = BalanceProblem(manifest_data)
    initial_state = problem.get_initial_state()

    if(not problem.is_balancable()):
        is_sift = True
        problem.set_sift_goal_state()
    
    queue = []
    heappush(queue, Node(initial_state))

    explored_states = set()
    explored_states.add(tuple(map(tuple, initial_state)))

    while(queue):
        current_node = heappop(queue)
        if not is_sift and problem.goal_test(current_node.get_state()):
            return current_node
        if is_sift and problem.sift_goal_test(current_node.get_state()):
            return current_node
        # print("--------------------------------------------------")
        # print("\nExpanding Node:\n")
        # for row in current_node.get_state():
        #     print(row)
        # print("Uniform  Cost: ", current_node.get_uniform_cost())
        # print("Heuristic Cost: ", current_node.get_heuristic_cost(), "\n")
        child_nodes = expand_node(current_node, explored_states, is_sift, problem)
        for child_node in child_nodes:
            heappush(queue, child_node)
            explored_states.add(tuple(map(tuple, child_node.get_state())))

        # print("\nNodes in Frontier:\n")
        # for node in queue:
        #     for row in node.get_state():
        #         print(row)
        #     print("Uniform  Cost: ", node.get_uniform_cost())
        #     print("Heuristic Cost: ", node.get_heuristic_cost(), "\n")
    return None

def get_balance_operations_info(solution_node):

    total_minutes = solution_node.get_uniform_cost()
    total_moves, solution_path = solution_node.get_solution_length_and_path(solution_node)
    balance_operations_list = []
    manifest_list = []

    # print("--------------------------------------------------")
    # print("\nSolution Path:\n")
    for _ in range(len(solution_path)):
        current_node = solution_path.pop()
        balance_operation_info = current_node.get_balance_operation_info()
        balance_operations_list.append(balance_operation_info)
        manifest_list.append(current_node.get_state())
        # print("Move from [", balance_operation_info[0], "] to [", balance_operation_info[1], "]")
        # for row in current_node.get_state():
        #     print(row)
        # print()


    return total_minutes, total_moves, balance_operations_list, manifest_list

# example = [
#     [(0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED")],
#     [(0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED")],
#     [(0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED")],
#     [(0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (70, "LionKi"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED")],
#     [(0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (40, "LionKi"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED")],
#     [(0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (60, "LionKi"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED")],
#     [(20, "LionKi"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (70, "LionKi"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED")],
#     [(30, "LionKi"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (999999, "LionKi"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED"), (0, "UNUSED")]
# ]

# solution_node = a_star(example)

# for row in solution_node.get_state():
#     print(row)