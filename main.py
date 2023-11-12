from matching_puzzle_helper import MatchingPuzzleHelper


def main():
    while True:
        helper = MatchingPuzzleHelper()
        helper.input_board()
        result = helper.solve()
        if result:
            print('🎉 Solved with %d steps!' % helper.steps)
            print('Result:')
            print(helper.board.get_result_description())
            print('\n\n')
        else:
            print('😭 No solution!')


if __name__ == '__main__':
    """
    case 1:
    ++E*
    D*DO
    E*  
    """
    main()