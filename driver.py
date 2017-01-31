import sys
import math
from collections import deque
import time
import resource
import cProfile
import unittest

profile_the_code = False
output_to_console = True
progress_log_granularity = 10000
should_log_progress = True
log_level = 2

def logit(method):
    def timed(*args, **kw):
        log('+ %r' % method.__name__, level=0)
        ts = time.perf_counter()
        result = method(*args, **kw)
        te = time.perf_counter()
        log('- %r %2.6f sec' % (method.__name__, te - ts), level=0)
        return result

    return timed

def log(msg, level=0):
    if level >= log_level:
        print(level, msg)


def dispatch_command(command, board_layout):
    if profile_the_code:
        pr = cProfile.Profile()
        pr.enable()

    searcher = None
    searcher = BreadthFirstSearch(board_layout) if command == "bfs" else searcher
    searcher = DepthFirstSearch(board_layout) if command == "dfs" else searcher
    searcher = AStarSearch(board_layout) if command == "ast" else searcher
    searcher = IDAStarSearch(board_layout) if command == "ida" else searcher
    if searcher is None:
        display_usage(command)
        return 1
    result = searcher.search()

    if profile_the_code:
        pr.disable()
        # after your program ends
        pr.print_stats(sort="tottime")
    return result

def display_usage(command):
    """please invoke like this: python driver.py <method> <board>, where board is a comma separated list of digits from 0 to 8"""
    print("dont understand ", command)
    print(
        "please invoke like this: python driver.py <method> <board>, where board is a comma separated list of digits from 0 to 8")


def swap_list_elements(l, from_idx, to_idx):
    tmp = l[to_idx]
    l[to_idx] = 0
    l[from_idx] = tmp

def parse_layout(layout_as_string):
    """convert a comma separated list of chars into a vector"""
    # check if list is already a list of integers (in which case just return a cloned copy of it)
    if all(isinstance(x, int) for x in layout_as_string):
        return list(layout_as_string)

    list_of_strings = layout_as_string.split(",")
    result = []
    for s in list_of_strings:
        result.append(int(s))
        # TODO: write code...
    return result


def contains(target, seq1):
    return target in seq1
    # for item in seq1:
    #     if target.board_layout._layout_hash == item.board_layout._layout_hash:
    #         return True
    # return False


class BoardLayout():
    """a class representing an instance of a configuration of the board"""

    def __init__(self, layout):
        """initialise from a comma separated list of characters"""
        self.state = layout
        x = math.trunc(math.sqrt(len(self.state)))
        # see whether the board is square
        if (x * x) != len(self.state):
            raise Exception("board is not square!")
        self.boardWidth = x
        self.boardHeight = x
        self._layout_hash = self.conv_layout_to_dense_int()

    def conv_layout_to_dense_int(self):
        result = 0
        for num in self.state:
            result *= 10
            result += num
        return result

    def availableMoves(self):
        """Return a list of available moves (order is UDLR)"""
        result = []
        indexOfBlankSpace = self.state.index(0)  # find location of blank space
        # first look to see whether we can move up
        if indexOfBlankSpace >= self.boardWidth:
            result.append("Up")
        # next look to see whether we can move down
        if indexOfBlankSpace < (self.boardWidth * (self.boardHeight - 1)):
            result.append("Down")
        # then look to see whether we can move left
        if (indexOfBlankSpace % self.boardWidth) > 0:
            result.append("Left")
        # then look to see whether we can move right
        if (indexOfBlankSpace % self.boardWidth) < (self.boardWidth - 1):
            result.append("Right")

        return result

    def makeMove(self, move):
        """nodestructively move blank tile"""
        # check whether move is valid
        validMoves = self.availableMoves()
        if move not in validMoves:
            raise Exception("Invalid move!")
        # so, it's safe to move, so clone a copy of the board to make the move on
        newBoard = list(self.state)
        to_idx = from_idx = newBoard.index(0)  # find location of blank space
        if move == "Up":
            to_idx= from_idx - self.boardWidth
        if move == "Down":
            to_idx = from_idx + self.boardWidth
        if move == "Left":
            to_idx = from_idx - 1
        if move == "Right":
            to_idx = from_idx + 1

        newBoard[from_idx],newBoard[to_idx] = newBoard[to_idx],newBoard[from_idx]
        # swap_list_elements(newBoard, from_idx, to_idx)
        result = BoardLayout(newBoard)
        return result

    def layout_is_acceptable(self):
        return self._layout_hash == 12345678
        # return all(self.state[i] <= self.state[i + 1] for i in range(len(self.state) - 1))

    def __hash__(self):
        return self._layout_hash

    def __eq__(self, other):
        return self._layout_hash == other._layout_hash

class StateSpaceElement():
    def __init__(self, board_layout, parent_state_space_element, action):
        self.board_layout = board_layout
        self.parent_layout = parent_state_space_element
        self.originating_action = action
        self.index_key = None

    def board_layout_is_acceptable(self):
        return self.get_board_layout().layout_is_acceptable()

    def get_board_layout(self):
        if self.board_layout is None:
            parentLayout = self.parent_layout.get_board_layout()
            self.board_layout = parentLayout.makeMove(self.originating_action)
        return self.board_layout

    def get_layout_as_string(self):
        if self.index_key is not None:
            return self.index_key
        self.index_key = str(self.board_layout)
        return self.index_key
    @property
    def search_depth(self):
        layers = 1
        x = self.parent_layout
        while x is not None:
            layers += 1
            x = x.parent_layout
        return layers
    def __hash__(self):
        return self.board_layout.__hash__()
    def __eq__(self, other):
        return self.board_layout._layout_hash == other.board_layout._layout_hash

class SearchAlgorithm():
    def __init__(self, fringe, explored):
        self.fringe = fringe
        self.explored = explored
        self.max_fringe_size = len(self.fringe)
        self.max_search_depth = 0

    def success(self, finalState):
        msg = self.solution_as_string(finalState)
        if output_to_console:
            log(msg, 3)
        else:
            f = open('output.txt', 'w')
            f.write(msg)
            f.close()
        return (self, finalState)

    def get_path_to_goal(self, finalState):
        moves = []
        s = finalState
        while s.originating_action is not None:
            moves.append(s.originating_action)
            s = s.parent_layout
        moves.reverse()
        return moves

    def expand_node(self, state):
        board = state.board_layout
        result = [StateSpaceElement(board.makeMove(move), state, move) for move in board.availableMoves()]
        # changing this to not bother generating the new board layout till it is needed, so that expansion does not take
        # place till the item is taken off of the fringe.
        # a value of None for the board layout means generate forward from the nearest progenitor layout that has an
        # explicit layout (which may well be the initial board layout)
        #result = [StateSpaceElement(None, state, move) for move in board.availableMoves()]
        return result

    def failure(self):
        print("rats!")
        return 1

    def solution_as_string(self, final_state):
        path_to_goal = self.get_path_to_goal(final_state)
        return """path_to_goal: %s\ncost_of_path: %d\nnodes_expanded: %d\nfringe_size: %d\nmax_fringe_size: %d\nsearch_depth: %d\nmax_search_depth: %d\nrunning_time: %.8f\nmax_ram_usage: %.8f""" % (
            path_to_goal,
            len(path_to_goal),
            len(self.explored),
            len(self.fringe),
            self.max_fringe_size,
            len(path_to_goal),
            self.max_search_depth,
            (time.time() - start_time),
            resource.getrusage(
                resource.RUSAGE_SELF).ru_maxrss / 1024.0)  # units of max_rss is 1kb for linux (apparently)

    def update_max_fringe_size(self):
        self.max_fringe_size = max(self.max_fringe_size, len(self.fringe))
        if self.max_fringe_size % 500 == 0:
            log(" %d"%self.max_fringe_size, 1)


class BreadthFirstSearch(SearchAlgorithm):
    def __init__(self, starting_board_layout):
        self.start_layout = starting_board_layout
        SearchAlgorithm.__init__(self, deque([]), dict())

    def search(self):
        fr = self.fringe
        app = fr.append
        app(StateSpaceElement(self.start_layout, None, None))
        self.update_max_fringe_size()

        while len(fr) > 0:
            state = fr.popleft()

            if state.board_layout_is_acceptable():
                return self.success(state)

            self.explored[hash(state.board_layout)] = state
            # self.max_search_depth = max(self.max_search_depth, len(self.get_path_to_goal(state)))
            self.max_search_depth = max(self.max_search_depth, state.search_depth)

            for neighbour in self.expand_node(state):
                tmp1 = self.explored.get(hash(neighbour.board_layout), None)
                if neighbour not in fr and tmp1 is None:
                    app(neighbour)

            self.update_max_fringe_size()
        return self.failure()


class DepthFirstSearch(SearchAlgorithm):
    def __init__(self, starting_board_layout):
        """Initialises the runtime state. Uses a list (as a stack) for the fringe, and a set for the explored set."""
        self.start_layout = starting_board_layout
        SearchAlgorithm.__init__(self, [], dict())

    def search(self):
        fr = self.fringe
        app = fr.append
        app(StateSpaceElement(self.start_layout, None, None))
        self.update_max_fringe_size()
        explored_counter = 0
        while len(fr) > 0:
            state = fr.pop()

            if state.board_layout_is_acceptable():
                return self.success(state)

            self.explored[state.board_layout._layout_hash] = state
            explored_counter+=1

            if should_log_progress and (explored_counter % progress_log_granularity) == 0:
                log("explored: %d"%explored_counter, 2)
            self.max_search_depth = max(self.max_search_depth, state.search_depth)

            child_nodes = self.expand_node(state)
            if len(child_nodes) > 0:
                child_nodes.reverse() # for putting onto the stack so dfs semantics are preserved
                for neighbour in child_nodes:
                    tmp1 = self.explored.get(neighbour.board_layout._layout_hash, None)
                    if not contains(neighbour, fr) and tmp1 is None:
                        app(neighbour)

            self.update_max_fringe_size()
        return self.failure()


class AStarSearch(SearchAlgorithm):
    def __init__(self, startingBoardLayout):
        """Initailises the runtime state. Uses a list (as a stack) for the fringe, and a set for the explored set."""
        self.startLayout = startingBoardLayout
        SearchAlgorithm.__init__(self, [], set([]))

    def search(self):
        self.fringe.append(StateSpaceElement(self.startLayout, None, None))
        self.update_max_fringe_size()

        while len(self.fringe) > 0:
            state = self.fringe.pop()

            if state.board_layout_is_acceptable():
                return self.success(state)

            self.explored.add(state)
            self.max_search_depth = max(self.max_search_depth, len(self.get_path_to_goal(state)))

            for neighbour in self.expand_node(state):
                if neighbour not in self.fringe and neighbour not in self.explored:
                    self.fringe.append(neighbour)

            self.update_max_fringe_size()
        return self.failure()


class IDAStarSearch(SearchAlgorithm):
    def __init__(self, startingBoardLayout):
        """Initailises the runtime state. Uses a list (as a stack) for the fringe, and a set for the explored set."""
        self.startLayout = startingBoardLayout
        SearchAlgorithm.__init__(self, [], set([]))

    def search(self):
        self.fringe.append(StateSpaceElement(self.startLayout, None, None))
        self.update_max_fringe_size()

        while len(self.fringe) > 0:
            state = self.fringe.pop()

            if state.board_layout_is_acceptable():
                return self.success(state)

            self.explored.add(state)
            self.max_search_depth = max(self.max_search_depth, len(self.get_path_to_goal(state)))

            for neighbour in self.expand_node(state):
                if not contains(neighbour, self.fringe) and not contains(neighbour, self.explored):
                    self.fringe.append(neighbour)

            self.update_max_fringe_size()
        return self.failure()


def main():
    board_layout = parse_layout(sys.argv[2])
    startingBoardLayout = BoardLayout(board_layout)
    return dispatch_command(sys.argv[1], startingBoardLayout)


start_time = time.time()
if __name__ == "__main__":
    main()

# a nice 7 step solution: bfs 1,2,5,0,4,8,3,6,7
# path_to_goal: ['Down', 'Right', 'Right', 'Up', 'Up', 'Left', 'Left']
# cost_of_path: 7
# nodes_expanded: 134
# fringe_size: 102
# max_fringe_size: 103
# search_depth: 7
# max_search_depth: 7
# running_time: 0.01337290
# max_ram_usage: 7920.00000000


class SearchTests(unittest.TestCase):
    def test0_7_step_solution(self):
        layout = parse_layout("1,2,5,0,4,8,3,6,7")
        startingBoardLayout = BoardLayout(layout)
        (searcher, finalState) = dispatch_command("bfs", startingBoardLayout)
        path = searcher.get_path_to_goal(finalState)
        self.assertEqual(path, ['Down', 'Right', 'Right', 'Up', 'Up', 'Left', 'Left'])
        self.assertEqual(searcher.max_fringe_size, 103)
        self.assertEqual(len(searcher.fringe), 102)
        self.assertEqual(len(searcher.explored), 134)

    def test0_simplest_dfs_case_works(self):
        startingBoardLayout = BoardLayout("3,1,2,0,4,5,6,7,8")
        (searcher, finalState) = dispatch_command("dfs", startingBoardLayout)
        path = searcher.get_path_to_goal(finalState)
        self.assertEqual(path, ["Up"])
        self.assertEqual(searcher.max_fringe_size, 3)
        self.assertEqual(len(searcher.fringe), 2)
        self.assertEqual(len(searcher.explored), 1)

    def test1_1_bfs(self):#bfs 1,2,5,3,4,0,6,7,8
        layout = parse_layout("1,2,5,3,4,0,6,7,8")
        startingBoardLayout = BoardLayout(layout)
        (searcher, finalState) = dispatch_command("bfs", startingBoardLayout)
        path = searcher.get_path_to_goal(finalState)
        self.assertEqual(path, ['Up', 'Left', 'Left'])
        self.assertEqual(searcher.max_fringe_size, 12)
        self.assertEqual(len(searcher.fringe), 11)
        self.assertEqual(len(searcher.explored), 10)

    def test1_2_dfs(self):#dfs 1,2,5,3,4,0,6,7,8
        layout = parse_layout("1,2,5,3,4,0,6,7,8")
        startingBoardLayout = BoardLayout(layout)
        (searcher, finalState) = dispatch_command("dfs", startingBoardLayout)
        path = searcher.get_path_to_goal(finalState)
        self.assertEqual(path, ['Up', 'Left', 'Left'])
        self.assertEqual(searcher.max_fringe_size, 42913)
        self.assertEqual(len(searcher.fringe), 2)
        self.assertEqual(len(searcher.explored), 181437)
        self.assertEqual(searcher.max_search_depth, 66125)

