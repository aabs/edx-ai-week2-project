import sys



def dispatchCommand(command, boardLayout):
    print ("dispatching ", command, " with ", boardLayout.asString())
    if command == "bfs":
        doBfs(boardLayout)
    elif command == "dfs":
        doDfs(boardLayout)
    elif command == "ast":
        doAst(boardLayout)
    elif command == "ida":
        doIda(boardLayout)
    else:
        displayUsage(command)
        

        
def doBfs(boardLayout):
    """comment"""
    print("doBfs")

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



class RuntimeState():
    """This class is responsible for keeping track of the various aspects of runtime performance"""
    
    def __init__(self):
        """initialise with default characters"""
        self.path_to_goal = []
        self.cost_of_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 0
        self.max_fringe_size = 0
        self.search_depth = 0
        self.max_search_depth = 0
        self.running_time = 0.0
        self.max_ram_usage = 0.0
        
    def asString(self):
        return """
path_to_goal: %s
cost_of_path: %d
nodes_expanded: %d
fringe_size: %d
max_fringe_size: %d
search_depth: %d
max_search_depth: %d
running_time: %.8f
max_ram_usage: %.8f"""%(
            self.path_to_goal,
            self.cost_of_path,
            self.nodes_expanded,
            self.fringe_size,
            self.max_fringe_size,
            self.search_depth,
            self.max_search_depth,
            self.running_time,
            self.max_ram_usage )

class BoardLayout():
    """a class representing an instance of a configuration of the board"""
        
    def parseLayoutToVector(self, layout):
        """convert a comma separated list of chars into a vector"""
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
        self.boardWidth = 3
        self.boardHeight = 3
    
    def findBlankSpace(self):
        return self.state.index(0)

    def availableMoves(self):
        """Return a list of available moves (order is UDLR)"""
        result = []
        indexOfBlankSpace = self.state.index(0)
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

def main():
    runtimeStateTracker = RuntimeState()
    startingBoardLayout = BoardLayout(sys.argv[2])
    dispatchCommand(sys.argv[1],startingBoardLayout)
    print("available moves %s" % startingBoardLayout.availableMoves())
    print(runtimeStateTracker.asString())


if __name__ == "__main__":
    main()
