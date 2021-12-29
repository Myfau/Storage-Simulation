from sprites import *
from queue import PriorityQueue

class Search:
    def __init__(self, istate, goal, walls, padles):
        self.istate = istate
        self.goal = goal
        self.walls = walls
        self.padles = padles

    def heuristic(self, a, b):
        a.p += abs(a.state.x - b.x) + abs(a.state.y - b.y)
        if a.parent != None:
            a.p += a.parent.p
            for padle in self.padles:
                if padle.x == a.state.x and padle.y == a.state.y:
                    #Poniżej jest ustawiany koszt przejechania przez kałużę
                    a.p += 100
        return a.p

    def greedy_search(self):
        start_node = Node(self.istate)
        if self.goal_test(start_node.state):
            return []
        fringe = PriorityQueue()
        fringe.put((0, start_node))
        action_list = []
        explored = []
        while fringe.qsize() > 0:
            current_node = fringe.get()[1]
            explored.append(current_node.state)
            if self.goal_test(current_node.state):
                while (current_node.parent != None):
                    action_list.append(current_node.action)
                    current_node = current_node.parent
                action_list.reverse()
                return action_list
            
            for succesor in self.succesors(current_node.state, self.walls):
                succesor.parent = current_node
                power = self.heuristic(succesor, self.goal[0])
                succesor.p = power
                if self.node_list_state_test_queue(succesor, fringe) and self.state_list_test(succesor.state, explored):
                    fringe.put((power, succesor))
                elif not self.node_list_state_test_queue(succesor, fringe):
                    return_node, index = self.node_list_state_test_values(succesor, fringe)
                    if return_node[0] > power:
                        temp_queue = PriorityQueue()
                        for i in range(index):
                            temp_queue.put(fringe.get())
                        fringe.put((power, succesor))
                        for j in range(index-1):
                            fringe.put(temp_queue.get())

    def search(self):
        start_node = Node(self.istate)
        if self.goal_test(start_node.state):
            return []
        fringe = []
        fringe.append(start_node)
        action_list = []
        explored = []
        while fringe:
            current_node = fringe.pop(0)
            explored.append(current_node.state)
            if self.goal_test(current_node.state):
                while (current_node.parent != None):
                    action_list.append(current_node.action)
                    current_node = current_node.parent
                action_list.reverse()
                return action_list
            
            for succesor in self.succesors(current_node.state, self.walls):
                if self.node_list_state_test(succesor, fringe) and self.state_list_test(succesor.state, explored):
                    succesor.parent = current_node
                    fringe.append(succesor)

                    
    def goal_test(self, state):
        if self.state_list_test(state, self.goal) == False:
            return True
        return False

    def node_list_state_test(self, test_node, test_node_list):
        for node in test_node_list:
            if node.state.x == test_node.state.x and node.state.y == test_node.state.y and node.state.rotation == test_node.state.rotation:
                return False
        return True

    def node_list_state_test_queue(self, test_node, test_node_list):
        for node in test_node_list.queue:
            if node[1].state.x == test_node.state.x and node[1].state.y == test_node.state.y and node[1].state.rotation == test_node.state.rotation:
                return False
        return True

    def node_list_state_test_values(self, test_node, test_node_list):
        i = 0
        for node in test_node_list.queue:
            i += 1
            if node[1].state.x == test_node.state.x and node[1].state.y == test_node.state.y and node[1].state.rotation == test_node.state.rotation:
                return node, i

    def state_list_test(self, test_state, state_list):
        for state in state_list:
            if state.x == test_state.x and state.y == test_state.y and state.rotation == test_state.rotation:
                return False
        return True

    def succesors(self, state, walls):
        succesor_list = []
        forward_flag = True
        left_flag = True
        right_flag = True
    
        if state.rotation == 0:
            for wall in walls:
                if wall.x == state.x and wall.y == state.y-1:
                    forward_flag = False
            if forward_flag == True:
                succesor_list.append(Node(State(state.x, state.y-1, 0), "forward"))
            succesor_list.append(Node(State(state.x, state.y, 270), "rotate_left"))
            succesor_list.append(Node(State(state.x, state.y, 90), "rotate_right"))
        elif state.rotation == 90:
            for wall in walls:
                if wall.x == state.x+1 and wall.y == state.y:
                    forward_flag = False
            if forward_flag == True:
                succesor_list.append(Node(State(state.x+1, state.y, 90), "forward"))
            succesor_list.append(Node(State(state.x, state.y, 0), "rotate_left"))
            succesor_list.append(Node(State(state.x, state.y, 180), "rotate_right"))
        elif state.rotation == 180:
            for wall in walls:
                if wall.x == state.x and wall.y == state.y+1:
                    forward_flag = False
            if forward_flag == True:
                succesor_list.append(Node(State(state.x, state.y+1, 180), "forward"))
            succesor_list.append(Node(State(state.x, state.y, 90), "rotate_left"))
            succesor_list.append(Node(State(state.x, state.y, 270), "rotate_right"))
        elif state.rotation == 270:
            for wall in walls:
                if wall.x == state.x-1 and wall.y == state.y:
                    forward_flag = False
            if forward_flag == True:
                succesor_list.append(Node(State(state.x-1, state.y, 270), "forward"))
            succesor_list.append(Node(State(state.x, state.y, 180), "rotate_left"))
            succesor_list.append(Node(State(state.x, state.y, 0), "rotate_right"))

        return succesor_list

    
class Node:
    def __init__(self, state, action = None, parent = None, p = 1):
        self.state = state
        self.parent = parent
        self.action = action
        self.p = p
    def __lt__(self, other):
        return self.state.x < other.state.y and self.state.y < other.state.y   

class State:
    def __init__(self, x, y, rotation, cost = 1):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.cost = cost