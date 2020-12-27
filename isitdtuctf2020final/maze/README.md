# ISITDTU CTF 2020 Final - Maze

## Introduction
**Given file:** `maze.exe`.

**Category:** Reverse engineering

**Summary:** This is what I called an *algorithmic/mathematical* type of reverse engineering challenge. The program is simple: it asks for an input, checks if its correct and then decodes the flag based on the given input and prints it out. Our task is to reverse engineer the checking process.

## TL;DR:
1. Analyze the program => Learn that it takes in the input as a path to get to the destination in a maze and checks it.
2. Learn how the program actually stores the maze and checks the path.
3. Model the problem mathematically and use `z3` to solve it.
4. Adding constraints to z3: coordinates bound (1), don't go back (2), initial and final coordinates (3), valid moves (4). 
5. Let it run => Get flag.

## Analyzing the program to learn the checking algorithm
The program takes in an input string, then checks if its length is 34. If that's the case then it will iterate through our string character by character. It only accepts 4 characters: `U`, `D`, `L`, `R` corresponding to up, down, left and right.

Initially, it sets the coordinates to be `(3, 0)`, moving up will decrement the X coordinate, down will increment it, moving left will decrement the Y coordinate, right will increment it. The way it checks if a move is valid is as follow: It stores a large array of size 256 in data that contains only 0s and 1s. It indexes the array by `4 * (coord_X + 8 * coord_Y)` plus 0, 1, 2 or 3. That means this is an array of quadruples, each corresponds to one `(X, Y)` coordinates. The value of each element in the quadruples is either 0 or 1, with 0 being "invalid move" and 1 being "valid move", the order of the elements is `(up, down, left, right)`. Because the array is of size 256, there are 64 quadruples, and by the way it is indexed, I knew that the maze is `8x8`.

Finally, it checks if we end up at `(4, 7)`. If we do, it uses our given path to decrypt the flag and prints it out for us. So the only thing I needed to do is find the correct path.

## Modeling the problem
Because I just read some great writeups about very cool `z3` solutions for algorithmic challenges like this, my initial thought was to use `z3` to solve it (although I forgot one constraint when I was onsite and didn't solve it by using z3 but by using another kinda luck-based solution, but the way I modeled the problem was correct). Initially, I thought of treating every of the 34 moves in the path as a z3 variable and model it from there, but this was actually not good enough because I couldn't index the valid-move array with these variables. Therefore, I changed the variables to `(X, Y)` coordinates after every move, even though it makes the number of variables becomes 70 (2*35, because I also treat the initial coordinates as a variable for easier construction of equations), it makes it so much easier to write all the z3 equations this way.

With this type of modeling, we have the following constraints:
1. **Coordinate bound condition:** All `X` and `Y` must be within the `8x8` maze.
2. **Don't go back condition:** Never go back to a coordinates that has already been explored (this is what I forgot at the competition).
3. **Initial and final coordinates:** Starts at `(3, 0)` and ends at `(4, 7)`.
4. **Valid move condition:** This is the most complex condition, constructed by using the array in the program.

## Writing z3 equations
For all the values of X and Y, I used `IntVector` data type in z3 because my advisor `@cothan` said that `IntVector` actually helps z3 solve faster than normal array of `Int`.

The 1st and 3rd conditions are simple:

```python
# Coordinates condition
for i in range(CNT):
    s.add(And(X[i] >= 0, X[i] < 8))
    s.add(And(Y[i] >= 0, Y[i] < 8))
# Initial coordinate condition
s.add(And(X[0] == 3, Y[0] == 0))
# Final coordinate condition
s.add(And(X[34] == 4, Y[34] == 7))
```

The 2nd condition is also not hard, but needs a bit of thought put into it. If I simply say that every `(X, Y)` pair is strictly different from all others, it will create too much constraints for z3 to solve (*34!* constraints). Therefore, I think of a more clever way to say it: If at step *i*, we are at coordinates `(X_i, Y_i)`, then at step *i+2*, if we are at the same `X_i`, then we must be at a different `Y` than `Y_i`, and vice versa, we don't care about step *i+1* because it must be different from step *i* no matter what:

```python
# Don't go back condition
for i in range(2, CNT):
    s.add(If(X[i] == X[i-2], Y[i] != Y[i-2], True))
    s.add(If(Y[i] == Y[i-2], X[i] != X[i-2], True))
``` 

For the 3rd condition, the first big problem is that I couldn't index a normal python array using a z3 variable, z3 simply doesn't allow that. Googling this issue leads me to a solution as below, using the `Array` type in z3:

```python
MAZE = Array('MAZE', IntSort(), IntSort())
i = 0
for elem in maze:
    MAZE = Store(MAZE, i, elem)
    i = i + 1
```

This way, I could index the `MAZE` z3 array using the function `Select()`. The rest of the work is to check each element in the quadruple corresponds to the last coordinates, if it equals to 1, I add in a possibility for z3 (using `Or()`):

```python
for i in range(1, CNT):
    cond1 = If(Select(MAZE, 4 * (X[i-1] + 8 * Y[i-1]) + 2) == 1, And(X[i] == X[i-1] - 1, Y[i] == Y[i-1]), False)
    cond2 = If(Select(MAZE, 4 * (X[i-1] + 8 * Y[i-1]) + 3) == 1, And(X[i] == X[i-1] + 1, Y[i] == Y[i-1]), False)
    cond3 = If(Select(MAZE, 4 * (X[i-1] + 8 * Y[i-1]) + 0) == 1, And(X[i] == X[i-1], Y[i] == Y[i-1] - 1), False)
    cond4 = If(Select(MAZE, 4 * (X[i-1] + 8 * Y[i-1]) + 1) == 1, And(X[i] == X[i-1], Y[i] == Y[i-1] + 1), False)
    s.add(Or(cond1, cond2, cond3, cond4))
```

## Running the z3 solver
Those are all of the constrains that can be constructed from the model of our problem, the only small step left to do is to convert the list of X and Y in the result into moves (remember, the program takes in the path as input, not the coordinates). Running the script and wait for a bit gave me the correct path: `LLDRRDLLLDRDLDDDRRULURRULURRDDDLDR`.

Inputting this into the program, I got the flag:
```
flag{FLa9_I5_w41tIN9_foR_YoU_A7_th3_w@y_ouT}
```

## Appendix
The z3 script to solve the problem is `a.py`.
