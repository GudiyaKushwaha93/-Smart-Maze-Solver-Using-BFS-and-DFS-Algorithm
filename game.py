from collections import deque
import random
import tkinter as tk
from tkinter import messagebox

# Main Window
root = tk.Tk()
root.title("Smart Maze Solver - BFS & DFS Algorithm")
root.geometry("650x700")
root.configure(bg="#eeeeee")

# Game Heading
heading = tk.Label(
    root,
    text="MAZE SOLVER GAME",
    font=("Arial", 22, "bold"),
    bg="#eeeeee"
)
heading.pack(pady=5)

# Instructions
info = tk.Label(
    root,
    text="Use Arrow Keys to Play | BFS & DFS to Find Path",
    font=("Arial", 12),
    bg="#eeeeee"
)
info.pack()

# Maze Design
maze = [
    ["S", 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, "E"]
]

buttons = []

def show_maze():
    for i in range(5):
        row = []
        for j in range(5):

            cell = maze[i][j]

            if cell == "S":
                color = "green"
                text = "START"
            elif cell == "E":
                color = "red"
                text = "END"
            elif cell == 1:
                color = "black"
                text = ""
            else:
                color = "white"
                text = ""

            btn = tk.Label(
                grid_frame,
                text=text,
                width=9,
                height=4,
                bg=color,
                relief="raised",
                borderwidth=2
            )
            btn.grid(row=i, column=j, padx=3, pady=3)
            row.append(btn)

        buttons.append(row)

# Grid Frame
grid_frame = tk.Frame(root, bg="#eeeeee")
grid_frame.pack(pady=25)

show_maze()

# Status
status = tk.Label(
    root,
    text="Maze Ready!",
    font=("Arial", 13, "bold"),
    bg="#eeeeee"
)
status.pack(pady=15)


reset_btn = tk.Button(
    root,
    text="RESET GAME",
    font=("Arial", 12, "bold")),
# Improved Reset Function

# Reset Function
def reset_game():
    player_position[0] = 0
    player_position[1] = 0

    for i in range(5):
        for j in range(5):
            cell = maze[i][j]

            if cell == "S":
                color = "green"
            elif cell == "E":
                color = "red"
            elif cell == 1:
                color = "black"
            else:
                color = "white"

            buttons[i][j].config(bg=color)

   
# Reset Button
reset_btn = tk.Button(
    root,
    text="RESET GAME",
    font=("Arial", 12, "bold"),
    bg="orange",
    command=reset_game
)
reset_btn.pack(pady=3)



# BFS Algorithm
def bfs():
    queue = deque([(0, 0, [(0, 0)])])
    visited = {(0, 0)}

    while queue:
        x, y, path = queue.popleft()

        if maze[x][y] == "E":
            show_path(path)
            return

        for dx, dy in [(0, 1), (1, 0),
                       (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy

            if (0 <= nx < 5 and 0 <= ny < 5
                and maze[nx][ny] != 1
                and (nx, ny) not in visited):

                visited.add((nx, ny))
                queue.append(
                    (nx, ny, path + [(nx, ny)])
                )

    status.config(text="No Path Found!")


# Display Shortest Path
def show_path(path):
    for x, y in path:
        if maze[x][y] not in ("S", "E"):
            buttons[x][y].config(bg="yellow")

    status.config(
        text=f"Path Found! Steps: {len(path)-1}"
    )


# BFS Button
bfs_btn = tk.Button(
    root,
    text="SOLVE USING BFS",
    font=("Arial", 12, "bold"),
    bg="lightgreen",
    command=bfs
)
bfs_btn.pack(pady=10)



# DFS Algorithm

def dfs():
    stack = [(0, 0, [(0, 0)])]
    visited = set()

    while stack:
        x, y, path = stack.pop()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if maze[x][y] == "E":
            show_path(path)
            status.config(
                text="DFS Path Found! Steps: " + str(len(path) - 1)
            )
            return

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < 5 and 0 <= ny < 5:
                if maze[nx][ny] != 1:
                    if (nx, ny) not in visited:
                        stack.append(
                            (nx, ny, path + [(nx, ny)])
                        )

    status.config(text="No Path Found!")


# DFS Button

dfs_btn = tk.Button(
    root,
    text="SOLVE USING DFS",
    font=("Arial", 12, "bold"),
    bg="lightblue",
    command=dfs
)

dfs_btn.pack(pady=10)

# Manual Player Movement
player_position = [0, 0]

def move_player(dx, dy):
    x, y = player_position
    nx = x + dx
    ny = y + dy

    if 0 <= nx < 5 and 0 <= ny < 5:
        if maze[nx][ny] != 1:

            if maze[x][y] == "S":
                buttons[x][y].config(bg="green")
            else:
                buttons[x][y].config(bg="white")

            player_position[0] = nx
            player_position[1] = ny

            buttons[nx][ny].config(bg="blue")

            if maze[nx][ny] == "E":
                messagebox.showinfo(
                    "Congratulations!",
                    "You Solved the Maze!"
                )

# Movement Buttons
control_frame = tk.Frame(root, bg="#eeeeee")
control_frame.pack(pady=10)

tk.Button(
    control_frame,
    text="UP",
    width=8,
    command=lambda: move_player(-1, 0)
).grid(row=0, column=1)

tk.Button(
    control_frame,
    text="LEFT",
    width=8,
    command=lambda: move_player(0, -1)
).grid(row=1, column=0)

tk.Button(
    control_frame,
    text="DOWN",
    width=8,
    command=lambda: move_player(1, 0)
).grid(row=1, column=1)

tk.Button(
    control_frame,
    text="RIGHT",
    width=8,
    command=lambda: move_player(0, 1)
).grid(row=1, column=2)


# BFS vs DFS Comparison

import time
from collections import deque

def compare_algorithms():

    def search(method):
        start = time.perf_counter()

        if method == "BFS":
            frontier = deque([(0, 0, 0)])
        else:
            frontier = [(0, 0, 0)]

        visited = {(0, 0)}

        while frontier:

            if method == "BFS":
                x, y, steps = frontier.popleft()
            else:
                x, y, steps = frontier.pop()

            if maze[x][y] == "E":
                elapsed = time.perf_counter() - start
                return steps, elapsed

            for dx, dy in [(0, 1), (1, 0),
                           (0, -1), (-1, 0)]:

                nx = x + dx
                ny = y + dy

                if (0 <= nx < len(maze)
                    and 0 <= ny < len(maze[0])
                    and maze[nx][ny] != 1
                    and (nx, ny) not in visited):

                    visited.add((nx, ny))
                    frontier.append((nx, ny, steps + 1))

        return None, time.perf_counter() - start

    bfs_steps, bfs_time = search("BFS")
    dfs_steps, dfs_time = search("DFS")

    result = (
        f"BFS Steps: {bfs_steps}\n"
        f"BFS Time: {bfs_time:.6f} seconds\n\n"
        f"DFS Steps: {dfs_steps}\n"
        f"DFS Time: {dfs_time:.6f} seconds"
    )

    messagebox.showinfo("BFS vs DFS Comparison", result)


# Comparison Button

compare_btn = tk.Button(
    root,
    text="COMPARE BFS VS DFS",
    font=("Arial", 12, "bold"),
    bg="lightyellow",
    command=compare_algorithms
)

compare_btn.pack(pady=10)


# Random Maze Generator

def generate_random_maze():
    global maze

    while True:
        new_maze = []

        for i in range(5):
            row = []
            for j in range(5):
                if random.random() < 0.25:
                    row.append(1)
                else:
                    row.append(0)
            new_maze.append(row)

        new_maze[0][0] = "S"
        new_maze[4][4] = "E"

        # Check if path exists using BFS
        queue = deque([(0, 0)])
        visited = {(0, 0)}

        while queue:
            x, y = queue.popleft()

            for dx, dy in [(0, 1), (1, 0),
                           (0, -1), (-1, 0)]:
                nx = x + dx
                ny = y + dy

                if (0 <= nx < 5 and 0 <= ny < 5
                    and new_maze[nx][ny] != 1
                    and (nx, ny) not in visited):

                    visited.add((nx, ny))
                    queue.append((nx, ny))

        if (4, 4) in visited:
            maze = new_maze
            break

    # Reset player position
    player_position[0] = 0
    player_position[1] = 0

    # Update maze display
    for i in range(5):
        for j in range(5):
            cell = maze[i][j]

            if cell == "S":
                color, label = "green", "START"
            elif cell == "E":
                color, label = "red", "END"
            elif cell == 1:
                color, label = "black", ""
            else:
                color, label = "white", ""

            buttons[i][j].config(
                bg=color,
                text=label
            )

    status.config(text="New Maze Generated!")


# Generate Maze Button

random_btn = tk.Button(
    root,
    text="GENERATE NEW MAZE",
    font=("Arial", 12, "bold"),
    bg="lightpink",
    command=generate_random_maze
)

random_btn.pack(pady=10)


# Keyboard Arrow Controls

def keyboard_move(event):
    if event.keysym == "Up":
        move_player(-1, 0)

    elif event.keysym == "Down":
        move_player(1, 0)

    elif event.keysym == "Left":
        move_player(0, -1)

    elif event.keysym == "Right":
        move_player(0, 1)


# Connect Keyboard with Game
root.bind("<Up>", keyboard_move)
root.bind("<Down>", keyboard_move)
root.bind("<Left>", keyboard_move)
root.bind("<Right>", keyboard_move)


# Algorithm Complexity Information

def show_complexity():
    information = (
        "ALGORITHM COMPLEXITY\n\n"
        "BFS (Breadth First Search)\n"
        "Time Complexity: O(V + E)\n"
        "Space Complexity: O(V)\n\n"
        "DFS (Depth First Search)\n"
        "Time Complexity: O(V + E)\n"
        "Space Complexity: O(V)\n\n"
        "V = Number of Vertices\n"
        "E = Number of Edges\n\n"
        "BFS finds the shortest path.\n"
        "DFS does not guarantee the shortest path."
    )

    messagebox.showinfo(
        "Algorithm Complexity",
        information
    )


# Complexity Button
complexity_btn = tk.Button(
    root,
    text="SHOW ALGORITHM COMPLEXITY",
    font=("Arial", 12, "bold"),
    bg="lightcyan",
    command=show_complexity
)

complexity_btn.pack(pady=10)
def start_game(event):
    reset_game()
    buttons[0][0].config(bg="blue")
    status.config(text="Game Started! Use Arrow Keys to Move.")

buttons[0][0].bind("<Button-1>", start_game)
root.mainloop()



