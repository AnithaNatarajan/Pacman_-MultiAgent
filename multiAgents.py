# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        """
        Score is evaluated for the action to be performed based on 3 factors as below in the
        order of priority:
                1. Food Pellets (of the current position)
                2. Ghost position from pacman position
                3. Location of food
        Here, the score boosts up if the pacman is far away from ghosts. At the same time, food position
        is also considered so that pacman does not linger around empty cells for a longer time. Bonus point
        is given if the current position had a food pellet.
        """

        if successorGameState.isWin():
            return float("inf") - 10

        score = 0

        ghostList = currentGameState.getNumAgents() - 1
        for i in range(1,ghostList):
            ghostposition = currentGameState.getGhostPosition(i)
            distfromghost = util.manhattanDistance(ghostposition, newPos)
            score += max(distfromghost, 5)

        score += successorGameState.getScore()

        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 100

        foodlist = newFood.asList()
        minFoodDistance = 100
        for food in foodlist:
            distfromFood = util.manhattanDistance(food,newPos)
            minFoodDistance = min(distfromFood,minFoodDistance)
        score -= 5 * minFoodDistance

        foodPalettes = currentGameState.getCapsules()
        if newPos in foodPalettes:
            score += 300

        if action == Directions.STOP:
            score -= 10

        return score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1


          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        """
        getAction returns the best possible move for pacman using minimax algorithm.
        Here, for all legal moves of a pacman from current position, min_score (for the
        agents/ghosts) and max_score (for the pacman) is computed. The actions are pushed
        into the priority queue with score being the priority factor. Once the evaluation
        of minimax is done, every action is popped from priority queue so that the last
        action from the priority queue is the best move/action.

        max_score - returns the score of the game if either the game is over (win/lose) or
        depth is 0. If not, compute the total legal actions & iterate it over to find the
        max of  min_score value evaluated for the ghosts.
        """
        "*** YOUR CODE HERE ***"
        def max_score(gameState,depth,ghosts):

            if gameState.isWin() or gameState.isLose() or (depth==0):
                return self.evaluationFunction(gameState)

            totalLegalActions = gameState.getLegalActions(0)
            v = -(float("inf"))

            for action in totalLegalActions:
                v = max(v,min_score(gameState.generateSuccessor(0,action),depth, 1, ghosts))
            return v
        """
        max_score - returns the score of the game if either the game is over (win/lose) or
        depth is 0. If not, compute the total legal actions & iterate it over to find the
        min of  max_score value evaluated for the pacman.
        """
        def min_score(gameState, depth, agentNumber, ghosts):

            if gameState.isWin() or gameState.isLose() or (depth==0):
                return self.evaluationFunction(gameState)

            v = (float("inf"))
            totalLegalActions = gameState.getLegalActions(agentNumber)
            if(agentNumber == ghosts):

                for action in totalLegalActions:
                    v = min(v, max_score(gameState.generateSuccessor(agentNumber, action), depth-1, ghosts))
            else:
                for action in totalLegalActions:
                    v = min(v, min_score(gameState.generateSuccessor(agentNumber, action), depth, agentNumber+1, ghosts))
            return v

        score = -(float("inf"))

        ghosts = gameState.getNumAgents() -1
        totalLegalActions = gameState.getLegalActions(0)
        priorityQueue = util.PriorityQueue()

        bestAction = Directions.STOP

        for action in totalLegalActions:
            successor = gameState.generateSuccessor(0,action)
            score = min_score(successor, self.depth, 1, ghosts)
            priorityQueue.push(action,score)

        while not priorityQueue.isEmpty():
            bestAction = priorityQueue.pop()
        return bestAction

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        """
        AlphaBetaAgent's getAction is same as Minimax's getAction but with a difference
        in computation of max_score and min_score function to avoid from visiting all
        the nodes.

        @:parameter :- alpha - Max's best option on path to root
                       beta  - Min's best option on path to root
                       v     - value of the node thatt is being explored

        max_score - returns the score of the game if either the game is over (win/lose) or
        depth is 0. If not, compute the total legal actions & iterate it over to find the
        max of  v and min_score value evaluated for the ghosts. Here, further nodes are
        not explored whenever v is greater than beta.
        """
        def max_score(gameState, alpha, beta, depth, ghosts):

            if gameState.isWin() or gameState.isLose() or (depth==0):
                return self.evaluationFunction(gameState)

            totalLegalActions = gameState.getLegalActions(0)
            v = -(float("inf"))

            for action in totalLegalActions:
                v = max(v,min_score(gameState.generateSuccessor(0,action), alpha, beta, depth, 1, ghosts))
                if v > beta:
                    return v
                alpha = max(alpha,v)

            return v
        """
        min_score - returns the score of the game if either the game is over (win/lose) or
        depth is 0. If not, compute the total legal actions & iterate it over to find the
        min of  v and max_score value evaluated for the ghosts.Here, further nodes are
        not explored whenever v is lesser than alpha.
        """
        def min_score(gameState, alpha, beta, depth, agentNumber, ghosts):

            if gameState.isWin() or gameState.isLose() or (depth==0):
                return self.evaluationFunction(gameState)

            v = (float("inf"))
            totalLegalActions = gameState.getLegalActions(agentNumber)
            if(agentNumber == ghosts):

                for action in totalLegalActions:
                    v = min(v, max_score(gameState.generateSuccessor(agentNumber, action), alpha, beta, depth-1, ghosts))
                    if v < alpha:
                        return v
                    beta = min(beta,v)
            else:
                for action in totalLegalActions:
                    v = min(v, min_score(gameState.generateSuccessor(agentNumber, action), alpha, beta, depth, agentNumber+1, ghosts))
                    if v< alpha:
                        return v
                    beta = min(beta,v)
            return v

        score = -(float("inf"))

        ghosts = gameState.getNumAgents() -1
        totalLegalActions = gameState.getLegalActions(0)
        priorityQueue = util.PriorityQueue()

        bestAction = Directions.STOP
        alpha = -(float("inf"))
        beta = float("inf")

        for action in totalLegalActions:
            successor = gameState.generateSuccessor(0,action)
            score_to_beat = score
            score = min_score(successor, alpha, beta, self.depth, 1, ghosts)
            if score > score_to_beat:
                bestAction = action
            if score > beta:
                return bestAction
            alpha = max(alpha, score)
            priorityQueue.push(action,score)

        while not priorityQueue.isEmpty():
            bestAction = priorityQueue.pop()
        return bestAction

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        """
        ExpectiMaxAgent's getAction is same as AlphaBetaAgent's getAction but with a
        difference in computation of max_score and min_score function to avoid from
        visiting all the nodes.

        @:parameter :- v - value of the node that is being explored

        max_score - returns the score of the game if either the game is over (win/lose) or
        depth is 0. If not, compute the total legal actions & iterate it over to find the
        max of  v and expected_score value evaluated for the ghosts.
        """

        def max_score(gameState,depth,ghosts):

            if gameState.isWin() or gameState.isLose() or (depth==0):
                return self.evaluationFunction(gameState)

            totalLegalActions = gameState.getLegalActions(0)
            v = -(float("inf"))

            for action in totalLegalActions:
                v = max(v,expected_score(gameState.generateSuccessor(0,action),depth, 1, ghosts))
            return v

        """
        expected_score - returns the score of the game if either the game is over (win/lose) or
        depth is 0. This assumes that the opponent can either be optimal or non-optimal. Hence
        average of the scores of all the successors is considered.
        """
        def expected_score(gameState, depth, agentNumber, ghosts):

            if gameState.isWin() or gameState.isLose() or (depth==0):
                return self.evaluationFunction(gameState)

            v = 0
            totalLegalActions = gameState.getLegalActions(agentNumber)
            for action in totalLegalActions:
                if(agentNumber == ghosts):
                    v += max_score(gameState.generateSuccessor(agentNumber, action), depth-1, ghosts)
                else:
                    v += expected_score(gameState.generateSuccessor(agentNumber, action), depth, agentNumber+1, ghosts)
            return (v/len(totalLegalActions))

        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        score = -(float("inf"))

        ghosts = gameState.getNumAgents() -1
        totalLegalActions = gameState.getLegalActions(0)
        priorityQueue = util.PriorityQueue()

        bestAction = Directions.STOP

        for action in totalLegalActions:
            successor = gameState.generateSuccessor(0,action)
            score = expected_score(successor, self.depth, 1, ghosts)
            priorityQueue.push(action,score)

        while not priorityQueue.isEmpty():
            bestAction = priorityQueue.pop()
        return bestAction

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """
    Here, score is evaluated for the current position of pacman based on 3 factors as below
    in the order of priority:
                1. Food Pellets
                2. Location of food
                3. Ghost position from pacman position
    Here, the score boosts up if the pacman is far away from ghosts. At the same time, food position
    is also considered so that pacman does not linger around empty cells for a longer time. Bonus point
    is given if the current position had a food pellet.

    BetterEvaluationFunction considers the food position for scoring a little more than the EvaluationFunction.
    Also, it does not add the successor's score to the overall score as it is evaluated for the current position.
    Rest all remains the same as EvaluationFunction.
    """
    currentPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()

    if currentGameState.isWin():
        return float("inf") - 10
    elif currentGameState.isLose():
        return -float("inf")+10

    score = currentGameState.getScore()

    ghostList = currentGameState.getNumAgents() - 1
    for i in range(1, ghostList):
        ghostposition = currentGameState.getGhostPosition(i)
        distfromghost = util.manhattanDistance(ghostposition, currentPos)
        score += max(distfromghost, 5)

    foodlist = newFood.asList()
    minFoodDistance = 100
    for food in foodlist:
        distfromFood = util.manhattanDistance(food, currentPos)
        minFoodDistance = min(distfromFood, minFoodDistance)
    score -= 2 * minFoodDistance

    foodPalettes = currentGameState.getCapsules()
    if currentPos in foodPalettes:
        score += 300
    score -= 10 * len(foodPalettes)

    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

