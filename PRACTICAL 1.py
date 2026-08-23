# Practical No. 1
# Goal-Based Agent
# ===========================================================

# Import Required Libraries
import random          # Generate random starting position
import time            # Delay for AI thinking
import os              # Operating System information
import datetime        # Current Date and Time

# Display Program Title
print("=" * 65)
print("             GOAL-BASED AGENT")
print("=" * 65)

# Display Date and Time

current = datetime.datetime.now()
print("\nDate :", current.strftime("%d-%m-%Y"))
print("Time :", current.strftime("%H:%M:%S"))

# Display Operating System

print("\nOperating System :", os.name)

# Generate Random Starting Position

current_position = random.randint(1, 4)
# Goal Position
goal_position = 5
print("\nRobot Current Position :", current_position)
print("Goal Position          :", goal_position)
print("\nAI is Planning Path...")
time.sleep(2)

# Goal-Based Decision

while current_position < goal_position:
    print("Robot Moving Forward...")
    time.sleep(1)
    current_position += 1
    print("Current Position :", current_position)

# Goal Achieved

print("\nGoal Reached Successfully!")
print("Robot Arrived at Position", goal_position)
print("\nTask Completed Successfully.")
print("=" * 65)