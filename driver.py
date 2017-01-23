import sys

class State():
    """An implementation of some key search algorithms. For edX AI week 2"""
        
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

def dispatchCommand(command, state):
    print ("dispatching ", command, " with ", state.asString())
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

def displayState(blah):
    print (blah.asString())

startState = State(sys.argv[2])
dispatchCommand(sys.argv[1],startState)