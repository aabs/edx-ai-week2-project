import sys

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

class StateRenderer():
    """render the current state in some way"""

    def __init__(self):
        """open a file and start writing the output to it"""

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

startingBoardLayout = BoardLayout(sys.argv[2])
dispatchCommand(sys.argv[1],startingBoardLayout)