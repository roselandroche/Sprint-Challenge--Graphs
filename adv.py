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
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

opposite_direction = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

class TraversalGraph:
    def __init__(self):
        self.trav_graph = {}
        self.my_route = []

    def add_room(self, room):
        if room.id not in self.trav_graph:
            self.trav_graph[room.id] = {}
            for direction in room.get_exits():
                self.trav_graph[room.id][direction] = '?'

    def add_edge(self, prev_id, current_id, direction):
        self.trav_graph[prev_id][direction] = current_id
        self.trav_graph[current_id][opposite_direction[direction]] = prev_id

    def go_back(self):
        path = self.bfs(player.current_room.id, self.get_avail_rooms())
        path.pop(0)
        # print(f'PATH: {path}')
        next_dir = None
        while len(path) > 0:
            for item in self.trav_graph[player.current_room.id]:
                # print(f'LENGTH of Path at line 91: {len(path)}, Direction: {item}, Next Room: {path[0]}')
                # print(f'Trav Graph: {self.trav_graph[player.current_room.id]}')
                if self.trav_graph[player.current_room.id][item] == path[0]:
                    # print(f'ITEM: {item}')
                    next_dir = item
            if next_dir is not None:
                player.travel(next_dir)
                traversal_path.append(next_dir)
                path.pop(0)
                next_dir = None
        # print(f'Trav Graph: {self.trav_graph}')
        # print(f'Current Room: {player.current_room.name}')

    def possible_moves(self, current_room):
        options = []
        exits = player.current_room.get_exits()
        # print(exits)
        for exit in exits:
            # print(f'Exit {exit} to {self.trav_graph[player.current_room.id][exit]}')
            if self.trav_graph[player.current_room.id][exit] == '?':
                options.append(exit)
        # print(f'UNEXPLORED DIRECTIONS FROM {player.current_room.id} {options}')
        return options

    def get_avail_rooms(self):
        result = []
        for (key, value) in self.trav_graph.items():
            if not self.is_available(key):
                result += [key]
        return result

    def is_available(self, room_id):
        return '?' not in self.trav_graph[room_id].values()

    def get_neighbors(self, current_room):
        neighbors = [ i for i in self.trav_graph[current_room].values() if i != '?' ]
        return neighbors

    def bfs(self, start_room, destination):
        # print(f'DESTINATION: {destination}')
        queue = Queue()
        queue.enqueue([start_room])

        visited = set()

        while queue.size() > 0:
            current_path = queue.dequeue()
            current_vertex = current_path[-1]

            if current_vertex not in visited:
                if current_vertex in destination:
                    # print(f'Successful Path: {current_path}')
                    return current_path
                visited.add(current_vertex)
                for neighbor in self.get_neighbors(current_vertex):
                    new_path = list(current_path)
                    new_path.append(neighbor)
                    # print(f'New Path: {new_path}')
                    queue.enqueue(new_path)    

    def dft_but_better(self):
        current_room = player.current_room
        self.add_room(current_room)
        # print(f'My route {self.my_route}')
        avail_dir = self.possible_moves(current_room.id)
        # print(f'Line 216: {avail_dir}')
        current_dir = avail_dir[0]
        player.travel(current_dir)
        traversal_path.append(current_dir)
        self.add_room(player.current_room)
        self.add_edge(current_room.id, player.current_room.id, current_dir)
        # print(self.trav_graph)

    def explore(self):
        self.add_room(player.current_room)
        while len(self.get_avail_rooms()) > 0:
            while len(self.possible_moves(player.current_room.id)) > 0:
                # print(f'AVAIL ROOMS: {self.get_avail_rooms()}')
                self.dft_but_better()
            while len(self.possible_moves(player.current_room.id)) == 0 and len(self.get_avail_rooms()) != 0:
                # print(f'AVAIL ROOMS: {self.get_avail_rooms()}')
                self.go_back()
        print('While loop broke')
        # print(f'Traversal Path: {traversal_path}')
        

graph = TraversalGraph()
print(graph.explore())






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
