import time #Used to get program run time

def create_grid(fileName): #To create a 2D list for the sudoku grid from a .txt file
    sudokuGrid = []
    with open(fileName, "r") as file:
        for line in file:
            line = line.strip("\n")
            line = line.split(",")
            for i in range(len(line)):
                line[i] = int(line[i])
            sudokuGrid.append(line)
    return sudokuGrid

def valid(row, column, digit): #Used to check if the digit is valid in the given (row, column) position
    for i in range(0,9):
        if grid[row][i] == digit: #Checking in the row
            return False
        if grid[i][column] == digit: #Checking in the column
            return False
    row0 = (row//3)*3
    column0 = (column//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if grid[row0+i][column0+j] == digit: #Checking in the subgrid
                return False
    return True #If we reach here then none of the previous returns were made, so it must be valid

def solve(): #Will do the actual backtracking to solve the sudoku
    for row in range(9):
        for column in range(9):
            if grid[row][column] == 0: #Implies the square is blank
                for digit in range(1, 10): #Testing for values from 1-9
                    if valid(row, column, digit):
                        grid[row][column] = digit #Setting the cell to be our test digit (which has been verified at this point)
                        solve() #Calls the function again on the grid with the filled in digit
                        # Note:
                        # - In backtracking, we want to remember the previous steps we made so that we can reverse them if we come across an incorrect solution
                        # - Each call acts as a 'memory' for that step, as when the recursive calls after it finish, we will return back to this step's call
                        # - When we return back, we can then look for other solutions if there are any, and go back to previous steps if needed
                        grid[row][column] = 0 #The backtracking step
                return #We get here if none of the numbers were valid for our blank square
    #We get here if there were no more remaining blank squares
    for line in grid:
        print(line)
    input("Press return to search for further solutions.") #Using this to stop solutions from overwhelming the output (if multiple solutions exist)


if __name__ == "__main__":
    start = time.time() #Initial time before program starts
    grid = create_grid("\\Users\lavee\OneDrive\Documents\GitHub\Projects\Python\Sudoku Solver\sampleSudoku3.txt") #Can be accessed from all functions
    solve()
    #Eventually we will go back to the first solve() call, which will just return and finish there
    print("No further solutions were found.")
    print(f"Runtime: {time.time() - start} s") #Prints overall run time