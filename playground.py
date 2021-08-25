# array = [[1,2,3], 
#         [4,5,6], 
#         [7,8,9]]

# for _ in range(3):
#     array = list(zip(*array[::-1]))

# for x in array:
#     print(x)




def fits_left_right(word, letter_num, letter, row, square_num, square):
    enough_space_right = False
    enough_space_left = False

    # calculate space required before and after letter for word to fit
    before_space_needed = word.index(letter, letter_num)

    if square_num != '0':
        #  +1 to ensure there's space before any letters if not on left edge of board
        before_space_needed + 1

    after_space_needed = len(
        word) - word.index(letter, letter_num)
    # no space needed to right if last letter of word is on right edge of the board
    # square_num == 14 and letter is word[-1] or
    if square_num + after_space_needed == 15:
        after_space_needed -= 1

    # check sufficient space after letter:
    after_space_available = 0
    for square in row[square_num+1:]:
        if square == '.':
            after_space_available += 1
        else:  #  if not consecutive '.'s break
            break
    if after_space_needed <= after_space_available:
        enough_space_right = True

    # check sufficient space before letter:
    before_space_available = 0
    for square in reversed(row[:square_num]):
        if square == '.':
            before_space_available += 1
        else:
            break  #  if not consecutive '.'s break
    if before_space_needed <= before_space_available:
        enough_space_left = True

    return (enough_space_left, enough_space_right)