from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

class TraversalGraph:
    def __init__(self):
        self.trav_graph = {
            0: {},
        }
    def add_room(self, room_id):
        if room_id not in self.trav_graph:
            self.trav_graph[room_id] = {}

    def add_edge(self, dir, new_room):
        self.trav_graph[player.current_room.id][new_room] = dir
        
    def get_neighbors(self, current_room=player.current_room.id):
        neighbors = []
        exit_dir = player.current_room.get_exits()
        # print(f'Possible Exits from {player.current_room.name}: {exit_dir}')
        # print(f'Currently in Room {player.current_room.id}')
        for i in range(len(exit_dir)):
            if exit_dir[i] not in self.trav_graph[player.current_room.id]:
                self.trav_graph[player.current_room.id][exit_dir[i]] = '?'
                # print(self.trav_graph[player.current_room.id])
            room_to_add = player.current_room.get_room_in_direction(exit_dir[i]).id
            neighbors.append(room_to_add)
            # print(f'New room to the {one_dir} is: {room_to_add.id}')
            self.add_room(room_to_add)
            self.add_edge(room_to_add, exit_dir[i])
        # print(f'New trav_graph: {self.trav_graph}')
        # print(f'Neighbors: {neighbors}')
        return neighbors

    def bfs(self, start_room, destination):
        # CURRENTLY CAN'T FIND PATH UNLESS THERE IS ONLY ONE STEP NEEDED, OTHERWISE INFINITE LOOP
        # IS ONLY GETTING NEIGHBORS OF ORIGIN ROOM
        queue = Queue()
        queue.enqueue([start_room])

        visited = set()

        while queue.size() > 0:
            current_path = queue.dequeue()
            current_vertex = current_path[-1]

            if current_vertex not in visited:
                if current_vertex == destination:
                    print(f'Successful Path: {current_path}')
                    return current_path
                visited.add(current_vertex)
            for neighbor in self.get_neighbors(current_vertex):
                new_path = list(current_path)
                new_path.append(neighbor)
                print(f'New Path: {new_path}')
                queue.enqueue(new_path)

    def dft(self, start_room):
        dft_stack = Stack()
        dft_stack.push(start_room)

        visited = set()

        while dft_stack.size() > 0:
            next_neighbor = dft_stack.pop()

            if next_neighbor not in visited:
                # if player.current_room exits do not lead to next neighbor (off the stack), bfs
                # for exit in player.current_room.get_exits():
                #     if player.current_room.get_room_in_direction(exit) is not next_neighbor:
                #         self.bfs(player.current_room.id, next_neighbor)
                
                start_room = player.current_room
                print(f'Start room: {start_room.name}')
                print(f'Current room to travel to: {next_neighbor}')
                visited.add(next_neighbor)
                reverse_dict = {value : key for (key, value) in self.trav_graph[start_room.id].items()}
                moving_dir = reverse_dict.get(next_neighbor)

                before_travel = player.current_room.id
                player.travel(moving_dir)
                after_travel = player.current_room.id

                if before_travel is not after_travel:
                    traversal_path.append(moving_dir)

                if moving_dir == "n":
                    self.trav_graph[player.current_room.id]["s"] = start_room
                elif moving_dir == "s":
                    self.trav_graph[player.current_room.id]["n"] = start_room
                elif moving_dir == "e":
                    self.trav_graph[player.current_room.id]["w"] = start_room
                elif moving_dir == "w":
                    self.trav_graph[player.current_room.id]["e"] = start_room

                print(f'Traversal Path: {traversal_path}')

                for neighbors in self.get_neighbors():
                    dft_stack.push(neighbors)
            



graph = TraversalGraph()
# print(graph.get_neighbors())
# print(graph.dft(player.current_room.id))
# print(graph.bfs(0, 8))






# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
