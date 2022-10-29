# AI sokoban game

## Symbols used to simulate objects in the sokoban game:

- A : represents the object that the user controls
- E : represents the object where there are two objects: user control and target location
- X : represents the block object that needs to be pushed to the target location
- \# : represents objects that are blocks (or walls)
- \_ : represents the object that is the target position that we need to push the box to
- O : represents the object where there are two objects: the box and the target location

## Instructions to run the code:

Step 1: Enter the command:
  > pip install numpy
Step 2: Enter the command:
  > python main.py
- Step 3: select input input (mini, micro) and algorithm type (DFS, Astar) for the problem

## More information

- Inputs folder: contains the starting state for the game, including 2 types, mini and micro

- Output directory: is the result of step-by-step solution of the corresponding input after running the algorithm

- The algorithm running time is printed at the console screen after running, if the algorithm can't find a possible result, the console will return the message "Can't find the solution" if it does. about the number of steps that the algorithm can find and print the output file

## Example for console output after running:

```
Select input type (1 - Mini Comos, 2 - Micro Comos): 1
Select lever (1 - 60): 20
Select search algorithm (1 - DFS algorithm, 2 - A start algorithm): 2
Using the A start algorithm to solve...
Runtime: 2.8360002040863037 second.
Total step: 113
```
