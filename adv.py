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
        self.trav_graph = {
            
        }
        # self.avail_rooms = {
        #     0: {},
        # }
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
                    # player.travel(item)
                    # print(f'CURRENT ROOM: {player.current_room.name}')
                    # traversal_path.append(item)
                    # path.pop(0)
                # if len(path) == 0:
                #     path = None
                #     break

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

    def dft(self, start_room):
        dft_stack = Stack()
        dft_stack.push(start_room)

        self.my_route.append(player.current_room.id)

        visited = set()

        while dft_stack.size() > 0:
            next_neighbor = dft_stack.pop()

            if next_neighbor not in visited:
                # print(self.possible_moves(player.current_room.id))
                start_room = player.current_room
                # print(f'Start room: {start_room.name}')
                # print(f'Current room to travel to: {next_neighbor}')
                visited.add(next_neighbor)
                reverse_dict = {value : key for (key, value) in self.avail_rooms[start_room.id].items()}
                moving_dir = reverse_dict.get(next_neighbor)
                # print(f'Direction to Move: {moving_dir}')
    
                before_travel = player.current_room.id
                if moving_dir is not None:
                    self.trav_graph[before_travel][moving_dir] = next_neighbor
                    player.travel(moving_dir)
                    self.get_neighbors(player.current_room.id)
                    print(f'Line 178: {self.trav_graph}')
                    self.possible_moves(player.current_room.id)
                    self.my_route.append(player.current_room.id)
                    # print(f'New neighbors after travel: {self.get_neighbors(player.current_room)}')
                    
                    after_travel = player.current_room.id
                    # print(f'Current Room after last move: {after_travel}')

                    if before_travel is not after_travel:
                        traversal_path.append(moving_dir)

                    if moving_dir == "n":
                        self.trav_graph[player.current_room.id]["s"] = start_room.id
                    elif moving_dir == "s":
                        self.trav_graph[player.current_room.id]["n"] = start_room.id
                    elif moving_dir == "e":
                        self.trav_graph[player.current_room.id]["w"] = start_room.id
                    elif moving_dir == "w":
                        self.trav_graph[player.current_room.id]["e"] = start_room.id

                    print(f'Traversal Path: {traversal_path}')
                    # print(f'Available Rooms: {self.avail_rooms}')
                    print(f'My route so far: {self.my_route}')

                for neighbors in self.get_neighbors(player.current_room):
                    dft_stack.push(neighbors)
            
        self.go_back(self.my_route)
        self.possible_moves(player.current_room.id)
        # self.dft(player.current_room)     

    def dft_but_better(self):
        current_room = player.current_room
        self.add_room(current_room)
        # self.my_route.append(current_room.id)
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
        

graph = TraversalGraph()
# print(graph.dft(player.current_room.id))
# print(f'Neighbors after DFT: {graph.get_neighbors(player.current_room)}')
# print(type(player.current_room.id))
# print(graph.possible_moves(player.current_room.id))
# print(graph.dft_but_better())

# print(graph.go_back(graph.my_route))
print(graph.explore())
# print(graph.get_neighbors(0))
# print(graph.bfs(4, 0))






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
