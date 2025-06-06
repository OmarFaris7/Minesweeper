import random

def main():
    # Game is always 16x16 grid (for now)
    rows, cols = 16, 16

    # Difficulty Selection
    difficulty = int(input("Select your difficult (1 = Easy, 2 = Medium, 3 = Hard): "))

    # Number of mines based on difficulty
    num_mines = 0
    if difficulty == 1:
        num_mines = 20
    elif difficulty == 2:
        num_mines = 40
    elif difficulty == 3:
        num_mines = 60

    # Grid Creation w/ bomb placement, Randomly place mines (represented by -1), also a separate revealed grid
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    revealed = [[False for _ in range(cols)] for _ in range(rows)]

    # Randomizing and placing bombs throughout grid
    mines_placed = 0
    while mines_placed < num_mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        if grid[r][c] != -1:
            grid[r][c] = -1
            mines_placed += 1

    # Fill in grid with tile bomb count for each location
    for r in range(rows):
        for c in range(cols):
            #Checks for bomb in spot
            if grid[r][c] == -1:
                continue
            count = 0
            # Parsing each of the 8 surrounding tiles
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    # Skip center tile
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    # Checks for boundary / corner tiles
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == -1:
                            count += 1
            grid[r][c] = count

    # Game loop starts here
    while True:

        # Displaying Grid
        display(grid, revealed)
        tile_guess = input("Select your tile (e.g., H7): ")

        # Converting inputs to integer
        column_guess = ord(tile_guess[0].upper()) - ord('A')
        row_guess = int(tile_guess[1:]) - 1

        # Validation check
        if column_guess > 15 or row_guess > 15 or column_guess < 0 or row_guess < 0:
            print("Invalid selection, keep choices between A-P for column and 1-16 for row.")
            continue

        # Checks if bomb tile was selected
        if grid[row_guess][column_guess] == -1:
            # Creates a new grid that reveals entire board on loss
            display(grid, [[True] * cols for _ in range(rows)])
            print("\nYOU LOSE!")
            break

        # Flood reveal
        reveal(grid, revealed, row_guess, column_guess)

        # Check if game's been won
        if check_win(grid, revealed):
            display(grid, revealed)
            print("\nYOU WIN!")
            break

def reveal(grid, revealed, row_guess, column_guess):
    if revealed[row_guess][column_guess]:
        return

    # Stop flood iteration on number tile
    revealed[row_guess][column_guess] = True
    if grid[row_guess][column_guess] > 0:
        return

    # Flooding recursively
    for row_checker in [-1, 0, 1]:
        for column_checker in [-1, 0, 1]:
            new_row, new_col = row_guess + row_checker, column_guess + column_checker
            if (row_checker != 0 or column_checker != 0) and 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                reveal(grid, revealed, new_row, new_col)

def display(grid, revealed):

    # Prints column labels
    print("   A B C D E F G H I J K L M N O P")

    # Printing grid
    for r in range(len(grid)):
        # Prints row label while maintaining spacing
        print(f"{r+1:2} ", end='')
        for c in range(len(grid[0])):
            if not revealed[r][c]:
                print('■', end=' ')
            else:
                if grid[r][c] == -1:
                    print('X', end=' ')
                elif grid[r][c] == 0:
                    print(' ', end=' ')
                else:
                    print(grid[r][c], end=' ')
        print()

# Check if revealed grid is filled out
def check_win(grid, revealed):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != -1 and not revealed[r][c]:
                return False
    return True

if __name__ == "__main__":
    main()