# Depth First Search (DFS)
# Real Life Example - Bank Department Visit
# AI Semester 5
# Import Required Libraries
import time                 # Used to create delay
import os                   # Used to display Operating System
import datetime             # Used to display Date and Time
# Display Program Title
print("=" * 65)
print("         DEPTH FIRST SEARCH (DFS)")
print("=" * 65)
# Display Date and Time
current = datetime.datetime.now()
print("\nDate :", current.strftime("%d-%m-%Y"))
print("Time :", current.strftime("%H:%M:%S"))
# Display Operating System
print("\nOperating System :", os.name)
# Create Bank Graph
# Dictionary Representation
bank = {
    "Bank": ["Account Section", "Loan Section"],
    "Account Section": ["Saving Account", "Current Account"],
    "Saving Account": [],
    "Current Account": [],
    "Loan Section": ["Home Loan", "Car Loan"],
    "Home Loan": [],
    "Car Loan": []
}
# Display Graph
print("\nBank Department Structure")
print("-" * 40)
for node in bank:
    print(node, "->", bank[node])
# Create Empty Visited Set
visited = set()
# DFS Function
def dfs(graph, node):
    # Check whether node already visited
    if node not in visited:
        # Mark node as visited
        visited.add(node)
        # Display current node
        print("\n--------------------------------")
        print("Current Department :", node)
        print("Visited Nodes :", visited)
        # AI Thinking Delay
        time.sleep(1)
        # Visit every connected department
        for neighbour in graph[node]:
            print("Moving To :", neighbour)
            time.sleep(1)
            dfs(graph, neighbour)
# Start DFS Traversal
print("\n")
print("=" * 65)
print("DFS Traversal Started")
print("=" * 65)
start_node = "Bank"
print("\nStarting Department :", start_node)
time.sleep(2)
dfs(bank, start_node)
# ----------------------------------------------------------
# Traversal Completed
# ----------------------------------------------------------
print("\n")
print("=" * 65)
print("DFS Traversal Completed")
print("=" * 65)
print("\nFinal Traversal")
for department in visited:
    print(department)
print("\nTotal Departments Visited :", len(visited))
print("\nProgram Completed Successfully.")
print("=" * 65)