# Practical No. 2
# Breadth First Search (BFS)
# AI Semester 5
# Import Required Libraries
from collections import deque     # Queue for BFS
import time                       # Delay
import os                         # Operating System
import datetime                   # Date and Time
import heapq                      # Future use in UCS
# Display Program Title
print("=" * 65)
print("          BREADTH FIRST SEARCH (BFS)")
print("=" * 65)
# Display Current Date and Time
current = datetime.datetime.now()
print("\nDate :", current.strftime("%d-%m-%Y"))
print("Time :", current.strftime("%H:%M:%S"))
# Display Operating System
print("\nOperating System :", os.name)
# Graph Creation
# Dictionary Representation
graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": [],
    "E": [],
    "F": [],
    "G": []
}

# Display Graph
print("\nGraph Structure")
for node in graph:
    print(node, "->", graph[node])
# Create Empty Queue
queue = deque()
# Create Empty Visited List
visited = []
# Starting Node
start_node = "A"
print("\nStarting Node :", start_node)
# Add Starting Node into Queue
queue.append(start_node)
# Mark Starting Node as Visited
visited.append(start_node)
print("\nQueue :", list(queue))
print("Visited :", visited)
print("\nAI is Preparing BFS Traversal...")
time.sleep(2)
print("\nTraversal Started...\n")

# BFS Loop Starts Here
while queue:
    # Remove First Element
    # FIFO Operation
    current_node = queue.popleft()
    # Display Current Node
    print("--------------------------------------")
    print("Current Node :", current_node)

    print("Queue After Removal :", list(queue))
    # Check Neighbor Nodes
    print("Checking Neighbor Nodes...")
    time.sleep(1)
    # Visit Every Neighbor
    for neighbour in graph[current_node]:
        # Check Whether Already Visited
        if neighbour not in visited:
            print("Found New Node :", neighbour)
            # Add into Queue
            queue.append(neighbour)
            # Mark as Visited
            visited.append(neighbour)
            print("Added to Queue :", neighbour)
            print("Current Queue :", list(queue))
            print("Visited Nodes :", visited)
            print()
# Continue BFS Traversal
    # Display Queue Status
    print("--------------------------------------")
    print("Queue Status :", list(queue))
    # Small Delay
    time.sleep(1)
# ------------------------------------------------------------
# BFS Traversal Completed
# ------------------------------------------------------------
print("\n" + "=" * 65)
print("          BFS TRAVERSAL COMPLETED")
print("=" * 65)
print("\nFinal Visited Nodes")
for node in visited:
    print(node, end=" ")
print("\n")
print("Total Nodes Visited :", len(visited))
print("\nTraversal Completed Successfully.")
print("=" * 65)
#This statement prints the equal (=) symbol 65 times in a single line.(Design)