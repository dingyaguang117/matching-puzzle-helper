from unittest import TestCase
from matching_puzzle_helper import MatchingPuzzleHelper

class TestMatchingPuzzleHelper(TestCase):
    def test_solve(self):
        helper = MatchingPuzzleHelper(target=["++E*", "D*DO", "E*  "], debug=False)
        solved = helper.solve()
        self.assertTrue(solved)
        result = "5324\n5324\n11  "
        self.assertEqual(helper.board.get_result_description(), result)
