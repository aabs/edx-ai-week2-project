import sys
import math
from collections import deque
import time
import resource

def dispatchCommand(command, boardLayout):
    if command == "bfs":
        bfs = BreadthFirstSearch(boardLayout)
        return bfs.search()
    elif command == "dfs":
        doDfs(boardLayout)
    elif command == "ast":
        doAst(boardLayout)
    elif command == "ida":
        doIda(boardLayout)
    else:
        displayUsage(command)
        
def doDfs(boardLayout):
    """comment"""
    print("doDfs")

def doAst(boardLayout):
    """comment"""
    print("doAst")

def doIda(boardLayout):
    """comment"""
    print("doIda")

def displayUsage(command):
    """comment"""
    print("dont understand ", command)

def displayState(blah):
    print (blah.asString())

def swapListElements(l, fromIdx, toIdx):
    tmp = l[toIdx]
    l[toIdx] = 0
    l[fromIdx] = tmp
    
def contains(target, seq1):
    for item in seq1:
        if target.boardLayout.asString() == item.boardLayout.asString():
            return True
    return False
    
class BoardLayout():
    """a class representing an instance of a configuration of the board"""
        
    def parseLayoutToVector(self, layout):
        """convert a comma separated list of chars into a vector"""
        # check if list is already a list of integers (in which case just return a cloned copy of it)
        if all(isinstance(x, int) for x in layout):
            return list(layout)
            
        listOfStrings = layout.split(",")
        result =[]
        for s in listOfStrings:
            result.append(int(s))
            # TODO: write code...
        return result
    
    def asString(self):
        return ", ".join('%d'%x for x in self.state)
        
    def __init__(self, layout):
        """initialise from a comma separated list of characters"""
        self.state = self.parseLayoutToVector(layout)
        x = math.trunc(math.sqrt(len(self.state)))
        # see whether the board is square
        if (x * x) != len(self.state):
            raise Exception("board is not square!")
        self.boardWidth = x
        self.boardHeight = x
    
    def availableMoves(self):
        """Return a list of available moves (order is UDLR)"""
        result = []
        indexOfBlankSpace = self.state.index(0)  # find location of blank space
        # first look to see whether we can move up
        if indexOfBlankSpace >= self.boardWidth:
            result.append("Up")
        # next look to see whether we can move down
        if indexOfBlankSpace < (self.boardWidth * (self.boardHeight-1)):
            result.append("Down")
        # then look to see whether we can move left
        if (indexOfBlankSpace % self.boardWidth) > 0:
            result.append("Left")
        # then look to see whether we can move right
        if (indexOfBlankSpace % self.boardWidth) < (self.boardWidth-1):
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
        indexOfBlankSpace = newBoard.index(0)  # find location of blank space
        if move == "Up":
            swapListElements(newBoard, indexOfBlankSpace, indexOfBlankSpace-self.boardWidth)
        if move == "Down":
            swapListElements(newBoard, indexOfBlankSpace, indexOfBlankSpace+self.boardWidth)
        if move == "Left":
            swapListElements(newBoard, indexOfBlankSpace, indexOfBlankSpace-1)
        if move == "Right":
            swapListElements(newBoard, indexOfBlankSpace, indexOfBlankSpace+1)
        
        return BoardLayout(newBoard)
        
    def layoutIsAcceptable(self):
        return all(self.state[i] <= self.state[i+1] for i in range(len(self.state)-1))
      
class StateSpaceElement():
    def __init__(self, boardLayout, progenitorStateSpaceElement, action):
        self.boardLayout = boardLayout
        self.progenitorLayout = progenitorStateSpaceElement
        self.originatingAction = action
     

class BreadthFirstSearch():
    def __init__(self, startingBoardLayout):
        self.startLayout = startingBoardLayout
        self.fringe = deque([])
        self.explored = set([])
        self.max_fringe_size = len(self.fringe)
        self.max_search_depth = 0

    def search(self):
        self.fringe.append(StateSpaceElement(self.startLayout, None, None))
        self.max_fringe_size = max(self.max_fringe_size, len(self.fringe))
        
        while len(self.fringe) > 0:
            state = self.fringe.popleft()
            
            if state.boardLayout.layoutIsAcceptable():
                return self.Success(state)
                
            self.explored.add(state)
            self.max_search_depth = max(self.max_search_depth, len(self.getPathToGoal(state)))
            
            for neighbour in self.expandNode(state):
                if not contains(neighbour, self.fringe) and not contains(neighbour, self.explored):
                    self.fringe.append(neighbour)
            
            self.max_fringe_size = max(self.max_fringe_size, len(self.fringe))
        return self.Failure()
        
    def solutionAsString(self, finalState):
        path_to_goal = self.getPathToGoal(finalState)
        return """path_to_goal: %s\ncost_of_path: %d\nnodes_expanded: %d\nfringe_size: %d\nmax_fringe_size: %d\nsearch_depth: %d\nmax_search_depth: %d\nrunning_time: %.8f\nmax_ram_usage: %.8f"""%(
            path_to_goal,
            len(path_to_goal),
            len(self.explored),
            len(self.fringe),
            self.max_fringe_size,
            len(path_to_goal),
            self.max_search_depth,
            (time.time() - start_time),
            resource.getrusage(resource.RUSAGE_SELF).ru_maxrss /1024.0) # units of max_rss is 1kb for linux (apparently)
      
    def Success(self, finalState):
        f = open('output.txt', 'w')
        f.write(self.solutionAsString(finalState))
        f.close()
        return 0
    
    def getPathToGoal(self, finalState):
        moves = []
        s = finalState
        while s.originatingAction != None:
            moves.append(s.originatingAction)
            s = s.progenitorLayout
        moves.reverse() 
        return moves
        
    def expandNode(self, state):
        board = state.boardLayout
        result = [StateSpaceElement(board.makeMove(move), state, move) for move in board.availableMoves()]
        return result
        
    def Failure(self):
        print("rats!")
        return 1
def main():
    startingBoardLayout = BoardLayout(sys.argv[2])
    return dispatchCommand(sys.argv[1],startingBoardLayout)

start_time = time.time()
if __name__ == "__main__":
    main()
