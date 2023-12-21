from Finchbot.BirdBrain import Finch
from time import sleep
from enum import Enum

DELAY_VALUE:float = 0.001 #of a second=1 millisecond

Directions = list[bool]

finch:Finch = Finch()

defaultSpeed:float = 20 #TODO: Change this/measure this

WALL_THRESHOLD:float = 10 #TODO: check if this is enough?

finch.setMotors(0,0)

class Turns(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    OPPOSITE = '180˚Turn'

def turnFinch(turn:Turns):
    TURN_WAIT_TIME:float = 0.5 #TODO: check if this is enough?

    if(turn == Turns.LEFT):
        finch.setTurn('L', 90, 100) #face left
    elif(turn == Turns.RIGHT):
        finch.setTurn('R', 90, 100) #face right
    elif(turn == Turns.OPPOSITE):
        finch.setTurn('R', 90, 100)

        finch.setTurn('L', 20, 100)
        finch.setMove('B', 5, 20)
        finch.setTurn('R', 40, 100)
        finch.setMove('F', 5, 20)
        finch.setTurn('L', 20, 100)

        finch.setTurn('R', 90, 100)

    sleep(TURN_WAIT_TIME) #sleep for 100 ms to allow the turn

def turnAndDetectWalls() -> Directions:

    finch.setMotors(0,0) #stop the finchbot

    turnFinch(Turns.LEFT)
    leftObjectDist:int = finch.getDistance()

    wallPresentDirections:Directions = [False, False]

    if(leftObjectDist <= WALL_THRESHOLD): #wall to this side
        print('Wall to left side')
        wallPresentDirections = [True, False]

    turnFinch(Turns.OPPOSITE) #180˚ turn to make it face right from already left facing direction
    rightObjectDist:int = finch.getDistance()

    if(rightObjectDist <= WALL_THRESHOLD): #wall to this side
        print('Wall to right side')
        wallPresentDirections[1] = True

    if(wallPresentDirections[0] == False and wallPresentDirections[1] == False): #no wall on both sides!
        if(leftObjectDist>rightObjectDist):
            print('Wall dist greater to the LEFT')
            wallPresentDirections.append(False) #go towards left
        else:
            print('Wall dist greater to the RIGHT')
            wallPresentDirections.append(True) #go towards right. Also if both dists are equal

    turnFinch(Turns.LEFT)#come back to original pos

    return wallPresentDirections


def traversePath(directions:Directions, firstTime:bool = False):
    PERIODIC_WALL_CHECK_TIME:float = 1.8  #TODO: check this time

    leftOrRightTurn:int = 0 #0=left, 1=right

    if(firstTime):
        finch.setMotors(defaultSpeed, defaultSpeed)
    
    if(directions[0] == False and directions[1] == False):
        print('Deciding on left or right bigger, as no wall on both sides')
        if(directions[2]): #turn right if True, which means right distance is greater
            turnFinch(Turns.RIGHT)
            leftOrRightTurn = 1
            print('Turning right as wall dist is greater to the right')
        else:
            turnFinch(Turns.LEFT)
            leftOrRightTurn = 0
            print('Turning left as wall dist is greater to the left')
    elif(directions[0] and directions[1]==False):
        turnFinch(Turns.RIGHT)
        leftOrRightTurn = 1
        print('Turning right as there is a wall to the left')
    elif(directions[1] and directions[0]==False):
        turnFinch(Turns.LEFT)
        leftOrRightTurn = 0
        print('Turning left as there is a wall to the right')
    elif(directions[0] and directions[1]):
        print('Wall to both sides. Move forward')

    forwardDistance:float = finch.getDistance()

    while(True):
        if(finch.getButton('A') == True or finch.getButton('B') == True):
            finch.setMotors(0,0)
            break

        finch.setMotors(defaultSpeed, defaultSpeed)
        sleep(PERIODIC_WALL_CHECK_TIME)
        detectedWallDirections:Directions = turnAndDetectWalls()

        firstTime=False

        if(detectedWallDirections[0] and detectedWallDirections[1]):
            if(forwardDistance<=WALL_THRESHOLD):
                print('Wall on all three sides, backtrack')
                break #will happen if that path is a dead end
            else:
                if(firstTime==False):
                    finch.setTurn('R', 20, 100)
                    finch.setMove('B', 5, 20)
                    finch.setTurn('L', 40, 100)
                    finch.setMove('F', 5, 20)
                    finch.setTurn('R', 20, 100)
                else:
                    firstTime=False
                print('Wall to both sides. Move forward')
        else:
            traversePath(detectedWallDirections, firstTime=False)
            print('Dead end detected while following this path, so backtrack') 
            break #will happen if that path is a dead end
    
    while(True):
        if(finch.getButton('A') == True or finch.getButton('B') == True):
            finch.setMotors(0,0)
            break

        if(directions[0] == False and directions[1]==False and firstTime == False):
            newDirection:Directions = [False, False]
            if(leftOrRightTurn == 0):
                newDirection[1] = True
            if(leftOrRightTurn == 1):
                newDirection[0] = True

            traversePath(firstTime=False, directions=newDirection)
        if(forwardDistance>WALL_THRESHOLD):#can go to front
            traversePath(firstTime=False, directions=[True, True])
            break

        finch.setMotors(-defaultSpeed, -defaultSpeed) #go back/start reversing
        sleep(PERIODIC_WALL_CHECK_TIME)
        detectedWallDirections:Directions = turnAndDetectWalls()

        if(detectedWallDirections[0] and detectedWallDirections[1]):
            if(forwardDistance<=WALL_THRESHOLD):
                print('Wall on all three sides WHILE backtrack, this shouldnt have happened')
            else:
                print('Wall to both sides. Move backwards while backtracking')
        else:
            if(leftOrRightTurn == 0): #prev turn was left
                print('Backtracking with right turn')
                turnFinch(Turns.RIGHT)
                break
            elif(leftOrRightTurn == 1):
                print('Backtracking with left turn')
                turnFinch(Turns.LEFT)
                break

    return #backtracking done and front tracking done

    
while(True):
    if(finch.getButton('A') == True or finch.getButton('B') == True):
        finch.setMotors(0,0)
        break
     
    traversePath(firstTime=True, directions=[True, True])

    sleep(DELAY_VALUE)

finch.setMotors(0,0)