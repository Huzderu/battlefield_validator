import numpy as np


def validate_battlefield(field, x=0, y=0, label=1, counter=0):
    labels = {}
    ships = []
    ships_height = {}
    ships_width = {}
    ship_count = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    current_ship_count = []

# first pass of Connected Component Algorithm to find and label all different
# ships on the battlefield
    while x < 10 and y < 10:
        # checking if current position is not empty on the first column
        if field[x][y] and x != 0 and y == 0:
            # if the position to above is empty, we assign a new
            # label to the newly discovered ship
            if not field[x-1][y]:
                field[x][y] = label
                ships.append(field[x][y])
                label += 1
            # if the position above is already labelled, that means
            # the current position is part of it and we label it as such
            if field[x-1][y]:
                field[x][y] = field[x-1][y]

        # if the first position on the field is not empty, we label it
        if field[x][y] and x == 0 and y == 0:
            field[x][y] == label
            ships.append(field[x][y])
            label += 1

        # checking if current position is not empty on the first row
        if field[x][y] and x == 0 and y != 0:
            # if the position to the left is empty, we assign a new
            # label to the newly discovered ship
            if not field[x][y-1]:
                field[x][y] = label
                ships.append(field[x][y])
                label += 1
            # if the position to the left is already labelled, that means
            # the current position is part of it and we label it as such
            if field[x][y-1]:
                field[x][y] = field[x][y-1]

        # checking if current position is not empty after the first row
        if field[x][y] and x != 0 and y != 0:
            # if the position to the left and above are both empty, we assign a new
            # label to the newly discovered ship
            if not field[x-1][y] and not field[x][y-1]:
                field[x][y] = label
                ships.append(field[x][y])
                label += 1
        # if the position to the left or above are already labelled, that means
        # the current position is part of them and we label it as such
            if field[x-1][y] or field[x][y-1]:
                if field[x-1][y]:
                    field[x][y] = field[x-1][y]
                if field[x][y-1]:
                    field[x][y] = field[x][y-1]
        # if the position to the left and above are both labelled differently
        # that means both labels are actually the same and we assign the bigger
        # label to the smaller one in a dictionary for future correction in the
        # second pass
            if field[x-1][y] and field[x][y-1]:
                if field[x-1][y] != field[x][y-1]:
                    if field[x-1][y] < field[x][y-1]:
                        field[x][y] = field[x-1][y]
                        labels[field[x][y-1]] = field[x-1][y]
                    else:
                        field[x][y] = field[x][y-1]
                        labels[field[x-1][y]] = field[x][y-1]

        # conditions so that the while loop keeps running
        if y < 9:
            y += 1
        else:
            x += 1
            y = 0

# second pass Connected Component Labeling to check for ship label
#  inconsistencies and correct them
    for i in range(len(field)):
        for x in range(len(field[i])):
            while field[i][x] in labels.keys():
                field[i][x] = labels[field[i][x]]

# now that we have correctly identified and labelled all ships on the battlefield
# we can start checking to see if the battlefield and ship positions are valid

# measuring each ship's height
    for ship in ships:
        for row in field:
            if ship in row:
                height = row.count(ship)
                ships_height[ship] = height

# measuring each ship's width
    for ship in ships:
        for row in np.transpose(field).tolist():
            if ship in row:
                width = row.count(ship)
                ships_width[ship] = width

# making sure that ships do not touch each other horizontally and vertically
# by making sure that at least the width or the height is equal to 1
    for height, width in zip(ships_height.values(), ships_width.values()):
        if height == 1 or width == 1:
            pass
        else:
            print("Ships touching horizontally or vertically!")
            return False

# making sure that ships do not touch each other diagonally by checking for
# nearby different ships
    for i in range(len(field)):
        for x in range(len(field[i])):
            if field[i][x] != 0:
                if i and x:
                    try:
                        # making a list of all positions diagonal to our current ship
                        dgs = [field[i-1][x-1], field[i-1][x+1],
                               field[i+1][x-1], field[i+1][x+1]]
        # checking the diagonals for different ships
                        for dg in dgs:
                            if dg != field[i][x] and dg != 0:
                                print(dg)
                                print("Ships touching diagonally!")
                                return False
                    except IndexError:
                        pass


# measuring each ship's height * width and appending to a list of current ships
    for height, width in zip(ships_height.values(), ships_width.values()):
        current_ship_count.append(height * width)
# checking our current list of ships against the default correct list
    if sorted(current_ship_count) != ship_count:
        print("Not the right amount of ships!")
        print(sorted(current_ship_count))
        return False

# returning True if we passed all previous checks
    return True


battlefield =   [[0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 [1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, 1, 0, 1]]

print(validate_battlefield(battlefield))
