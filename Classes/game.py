import pygame
from .data import Data

class Game:
    def __init__(self, win):
        self.win = win
        self.data = Data(win)

    def update(self):
        pygame.display.update()
    def gameCycle():
        playerArray = self.updatePlayers();
        self.deal();
        gamePhase = 0
        while(gameInProgress == True)
        {
            while(allplayerscall = False)
            {
                PlayerWhoRaised = -1;
                for (i = 0; i< playerArray.length; i++)
                {
                    if(PlayerWhoRaised == i)
                    {
                        break;
                    }
                    playerBet = self.playerTurn(i);
                    if (playerBet == currentbet)
                    {
                        #call
                    }
                    else if (playerBet > currentbet)
                    {
                        #raise
                        PlayerWhoRaised = i;
                        currentbet = playerBet;
                    }
                    else if (playerBet < currentbet)
                    {
                        #fold
                    } 
                    
                }

                allplayerscall = true;
                for (i = 0; i< playerArray.length; i++)
                {
                    if (playerArray[i].bet != currentbet)
                    {
                        allplayerscall = false;
                    }
                }
                
            }
            
            
            if (gamePhase == 0)
            {
                #doflop
            }
            else if(gamePhase == 1)
            {
                #flipnext card
            }
            else if(gamePhase == 2)
            {
                #flipnext card
            }
            else if(gamePhase == 3)
            {
                #decide winner
                #gameInProgress = false;
            }
            gamePhase++
        }
        
    def deal():
        #give each player 2 cards

    def updatePlayers():
        #check if any players are wating in queue
        #check if any players want to leave
        #return player array

    def playerTurn(playerNumber):
        {
            currPlayer = playerArray[i];
            currPlayer
        }