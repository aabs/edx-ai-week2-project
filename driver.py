import sys

class State():
    """An implementation of some key search algorithms. For edX AI week 2"""
        
    def parseLayoutToVector(self, layout):
        """convert a comma separated list of chars into a vector"""
        self.state = [0,1,2,3,4,5,6,7,8]
        
    def __init__(self, layout):
        """initialise from a comma separated list of characters"""
        self.state = self.parseLayoutToVector(layout)

    

def dispatchCommand(command, state):
    if command == "bfs":
        doBfs(state)
    elif command == "dfs":
        doDfs(state)
    elif command == "ast":
        doAst(state)
    elif command == "ida":
        doIda(state)
    else:
        displayUsage(command)
        
        
def doBfs(state):
    """comment"""
    print("doBfs")

def doDfs(state):
    """comment"""
    print("doDfs")

def doAst(state):
    """comment"""
    print("doAst")

def doIda(state):
    """comment"""
    print("doIda")

def displayUsage(command):
    """comment"""
    print("dont understand ", command)


startState = State(sys.argv[2])
dispatchCommand(sys.argv[1],startState)