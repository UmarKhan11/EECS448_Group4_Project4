import random 
from . data import *
from . constants import *
from . button import *
import time
from . card import Card
import gc
import pygame
import sys

FPS = 60

class Player:
    def __init__(self, win, player_name, player_num, start_amt):
        self.win = win
        self.player_name = player_name
        self.player_num = player_num
        self.stack = start_amt
        self.deck_img = Card(5)
        self.hand = []
        self.board_cards = []
        self.buttons = []
        self.curr_hand = None
        self.playing = True
        self.hand_num = 0
        self.high_card = 0
        self.init_buttons()
        self.chip_pos = self.get_chip_pos()
        self.card_pos = self.get_card_pos(self.player_num)
        self.font = pygame.font.SysFont('Arial', SMALL_CARD_FONT_SIZE)
        self.playAgain = True
        self.raising = False
        self.pot = 0
     ################################################################# Added test from line 34 to 146
        self.test = []
        self.testPlayerList = []

    def create_test_players(self):
        for i in range(8):
            self.testPlayerList.append(Player(self.win, PLAYER_NAMES[i], i, 1000))
            # print(self.testPlayerList[i])
        print('\n')

    def check_test_array(self, test_number, array, messageP, messageF):
        state = True
        for i in range(len(array)):
            if array[i] == False:
                state = False
                break
        if state:
            print(f'Test ({test_number}) PASSED')
            print(f'\t {messageP}')
        else:
            print(f'Test ({test_number}) FAILED')
            print(f'\t {messageF}')
        return

    def test_blind(self):
        test_number = 1
        self.create_test_players()
        test_array = [False, False, False, False, False, False, False, False]
        messageP = "Blind did not affect other players stacks."
        messageF = "Blind affected other players."

        for i in range(8):
            i_player = self.testPlayerList[i]
            i_player.blind(100)
            for j in range(8):
                if j == i:
                    pass
                elif i_player.stack == self.testPlayerList[j].stack:
                    test_array[i] = False
                else:
                    test_array[i] = True
            self.testPlayerList[i].stack = 1000
        self.check_test_array(test_number, test_array, messageP, messageF)

    def test_receive_winnings(self):
        test_number = 2
        self.create_test_players()
        test_array = [False, False, False, False, False, False, False, False]
        messageP = "Only winner received winner money"
        messageF = "Losers also received money"

        for i in range(8):
            i_player = self.testPlayerList[i]
            i_player.receive_winnings(100)
            for j in range(8):
                if j == i:
                    pass
                elif i_player.stack == self.testPlayerList[j].stack:
                    test_array[i] = False
                else:
                    test_array[i] = True
            self.testPlayerList[i].stack = 1000
        self.check_test_array(test_number, test_array, messageP, messageF)

    def test_takeATurn_check(self):
        test_number = 3
        self.create_test_players()
        test_array = [False, False, False, False, False, False, False, False]
        passed = []
        all_pass = True
        messageP = "All turns logic was executed correctly"
        messageF = "A turn was executed incorrectly"

        for i in range(8):
            if (self.testPlayerList[i].test_helper_takeATurn(0) and
                self.testPlayerList[i].test_helper_takeATurn(1) and
                self.testPlayerList[i].test_helper_takeATurn(2) and
                self.testPlayerList[i].test_helper_takeATurn(3) and
                self.testPlayerList[i].test_helper_takeATurn(4) and
                    self.testPlayerList[i].test_helper_takeATurn(6)):
                test_array[i] = True

        self.check_test_array(test_number, test_array, messageP, messageF)


    def test_helper_takeATurn(self, i):
        cur_bet = 100
        prev_bet = 100
        raiseValue = 5

        if i == 0:  # check
            if (cur_bet - prev_bet) == 0:
                self.raising = False
            return True
        elif i == 1:  # call
            self.update_stack(cur_bet - prev_bet)
            self.raising = False
            return True
        elif i == 2:  # raise
            raiseValue += 10
            return True
        elif i == 3:  # fold
            self.playing = False
            self.raising = False
            return True
        elif i == 4:  # confirm raise
            self.update_stack(raiseValue - prev_bet)
            return True
        elif i == 6:  # All in
            temp = self.stack
            self.update_stack(self.stack)
            return True
    ################################################################# Added TEST

    # If needing to print out a player object, will return name and player number. To use in main: print(player)
    def __str__(self):
        return "Player Name: " + self.player_name + " --- " + "Player Number: " + str(self.player_num)

    def receive_winnings(self, amt):
        self.stack += amt

    def receive_top_hand_and_card(self, hand_num, high_card): #both int
        self.hand_num = hand_num
        self.high_card = high_card

    # @return - How much the player is paying for the blind (Not sure if the self.stack is suppose to be manipulated)
    def blind(self, blind_amt):  
        ###same as in bet, determine if the player has that much money left
        ###if it doesn't then return the maxium amt it cant(subtracting so that self.stack = 0) and the data class will handle
        copy_stack = self.stack
        copy_stack -= blind_amt
        # ? return the amount player added to blind ?
        '''
        if copy_stack < 0:
            print(str(self.stack) + ' - ' + str(blind_amt) + " = " + str(copy_stack))
            new_blind_amt = self.stack
            self.stack = 0
            return new_blind_amt
        else:
        '''
        self.stack -= blind_amt
        return blind_amt

    # @description - Gets a list of (number, suit), converts into Card object, stores Card objects into the self.hand list
    # @param - A list of cards that will be the objects hand
    # @return - nothing
    def receive_hand(self, hand):
        for card in hand:
            self.hand.append(card)
    
    # @description - changes relevant cards to be null 
    # @param - None
    # @return - None
    def reset(self):
        self.board_cards = []
        self.hand = []
        self.hand_num = 0
        self.playing = True
        self.high_card = 0


    # @description - Gets a list of (number, suit), converts into Card object, stores Card objects into the self.hand list
    # @param - A list of numbers that will be the board cards
    # @return - nothing
    def receive_board_cards(self, cards, str):  
        for card in cards:
            self.board_cards.append(card)

    # @description - Adds money to the current players stack of money
    # @param - money that will be added to current players stack of money
    # @return - nothing
    def receive_money(self, money):
        self.stack += money

    # @description - Current player has folded. Players hand is empty
    # @param - nothing
    # @return - nothing
    def fold(self):
        self.playing = False
        self.hand = []

    def get_x_y(self, pos):
        x = pos[0]
        y= pos[1]
        return x,y 

    def draw_current_player_turn_indicator(self, x, y):
        border_thickness = 3
        width = border_thickness* 2 + CARD_WIDTH * 2 + GAP
        height = border_thickness* 2 + CARD_HEIGHT
        #card.draw(self.win, self.card_pos[0] + i*CARD_WIDTH + i*GAP, self.card_pos[1], front)
        pygame.draw.rect(self.win, (0, 255, 0), (x, y, width, height), border_thickness)

    def takeATurn(self, cur_bet, prev_bet):
        clock = pygame.time.Clock()
        running = True
        x,y = -1, -1
        
        if(self.raising == False):
            betText = "Current bet: " + str(cur_bet)                            #draw current bet
            font = pygame.font.SysFont('Arial',17)                      
            text = font.render(betText, 1, (0, 0, 0))
            self.win.blit(text,(147, HEIGHT - INFO_BOX_HEIGHT + 17 + 12))
            self.raising = True
        
        raiseValue = cur_bet

        while running:
            clock.tick(FPS)
            self.draw_current_player_turn_indicator(self.card_pos[0] - 3, self.card_pos[1] - 3)        

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x,y = self.get_x_y(pos)
            ## (Check, Call, Raise, Fold)
            if x != -1 and y != -1:
                for i,button in enumerate(self.buttons):
                    if (button.x <= x < (button.x + button.width)) and (button.y < y < (button.y + button.height)):
                        if button.clickable:

                            if i == 0: #check
                                self.buttons[4].hidden = True
                                if (cur_bet - prev_bet) == 0:
                                    self.raising = False                                    
                                    return 0
                            elif i == 1: #call
                                self.buttons[4].hidden = True
                                self.update_stack(cur_bet-prev_bet)
                                self.raising = False
                                return cur_bet - prev_bet
                                
                            elif i == 2: #raise
                                self.buttons[4].hidden = False  
                                self.buttons[4].clickable = True
                                self.buttons[4].draw()                                              
                                raiseValue += 10
                                raiseText = "Current raise: " + str(raiseValue)
                                font = pygame.font.SysFont('Arial',17)                      #draw current raise
                                text = font.render(raiseText, 1, (0, 0, 0))
                                pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (147, HEIGHT - INFO_BOX_HEIGHT + 17 * 2 + 40 * 1 + 12, 125, 20))#BOARD_CARDS_BOX_COLOR
                                self.win.blit(text,(147, HEIGHT - INFO_BOX_HEIGHT + 17 * 2 + 40 * 1 + 12))                                     

                            elif i == 3: #fold
                                self.buttons[4].hidden = True
                                self.playing = False
                                self.raising = False
                                return -1
                            elif i == 4: #confirm raise
                                self.buttons[2].clickable = True
                                self.buttons[4].hidden = True
                                self.buttons[4].clickable = False
                                self.raising = False
                                self.update_stack(raiseValue - prev_bet)
                                return raiseValue
                            elif i == 5: #leave game
                                pygame.quit()
                                running = False
                                #self.playAgain = False
                                #self.playing = False
                                #self.raising = False
                                #return -1
                            elif i == 6: #All in
                                temp = self.stack
                                self.update_stack(self.stack)
                                return temp
                            
                            x = -1
                            y = -1
            else:
                pass #waiting for input
            pygame.display.update()


    # @description - Draws each card from current players hand
    # @param - front True if drawing front false if back
    # @return - nothing
    def draw_cards(self, front):
        if self.playing:
            for i, card in enumerate(self.hand):
                card.draw(self.win, self.card_pos[0] + i*CARD_WIDTH + i*GAP, self.card_pos[1], front)

    def draw_player_name(self, x, y, name):
        self.win.blit(self.font.render(name, True, BLACK), (x - (TOKEN_FONT_SIZE // 2) + OFFSET, y - (TOKEN_FONT_SIZE // 2)))

    # @description - Draws the board cards
    # @param - nothing
    # @return - nothing
    def draw_board_cards(self):
        for i, card in enumerate(self.board_cards):
            card.draw(self.win, 560 + 5 *(i+1) + OFFSET + i* CARD_WIDTH, 365 + 15 // 2, True)

    # @description - Draws the user interface
    # @param - other_players -- > list of players other than the current player
    # @return - nothing
    def draw(self, other_players, front, curr_player, dealer_num): 
        self.other_players = other_players
        self.draw_board(dealer_num)
        self.draw_chips() 
        self.draw_board_cards()
        self.draw_cards(True)
        self.draw_player_name(self.chip_pos[0] - 3* len(self.player_name), self.chip_pos[1] + 50, self.player_name)
        self.draw_buttons()
        self.draw_deck()
        self.draw_opponents(other_players, front)
        self.drawPot()
        if curr_player != None:
            if curr_player != 0:
                curr_player = 8 + curr_player
            pos = self.get_card_pos(curr_player)
            self.draw_current_player_turn_indicator(pos[0] - 3, pos[1] - 3)
        pygame.display.update()

    # @description - draws the deck
    # @param - None
    # @return - nothing
    def draw_deck(self): 
        self.deck_img.draw_deck(self.win)

    def recievePotValue(self, pot):
        self.pot = pot      

    def drawPot(self):
        potText = "Pot: " + str(self.pot)                       #draw current pot
        font = pygame.font.SysFont('Arial',17)                      
        text = font.render(potText, 1, (0, 0, 0))
        pygame.draw.circle(self.win, (255,255,255), (930, 310), 30)
        self.win.blit(text,(910, 300))

    # @description - Draws all the other players cards
    # @param - nothing
    # @return - nothing
    def draw_opponents(self, other_players, front):
        for player in other_players:
            if player.playing:
                player.draw_cards(front) #boolean for which side to draw            
            player.draw_chips()
            sign = 1
            if player.chip_pos[1] < HEIGHT//2:
                sign = -1
            str_length = len(player.player_name)
            player.draw_player_name(player.chip_pos[0]-3 * str_length , player.chip_pos[1] - 50* sign, player.player_name)

    def draw_board(self, dealer_num):
        self.win.fill(BACKGROUND_COLOR)
        pygame.draw.circle(self.win, BROWN, (WIDTH // 2 + OFFSET, HEIGHT // 2), BOARD_RADIUS + 140)
        board = pygame.draw.circle(self.win, BOARD_COLOR, (WIDTH // 2 + OFFSET, HEIGHT // 2), BOARD_RADIUS + 80)
        inner_circle = pygame.draw.circle(self.win, WHITE, (WIDTH // 2 + OFFSET, HEIGHT // 2), INNER_BORDER_RADIUS, width=1)
        for i in range(8):
            pos = self.get_card_pos(i)
            border_thickness = 3
            width = border_thickness* 2 + CARD_WIDTH * 2 + GAP
            height = border_thickness* 2 + CARD_HEIGHT
            pygame.draw.rect(self.win, (255, 0, 0), (pos[0] - 3, pos[1] - 3, width, height), border_thickness)
        
        #drawing the dealer, big blind, and small blind
        self.draw_markers(abs(dealer_num))
        
    
    def draw_markers(self, dealer_num):
        spots = [   [645, 400],
                    [735, 225],
                    [905, 135],
                    [965, 225],
                    [1060, 400],
                    [965, 575],
                    [800, 663],
                    [735, 575]]

        small = (dealer_num + 1) % 8
        big = (dealer_num + 2) % 8

        pygame.draw.circle(self.win, (128,0,0), (spots[dealer_num][0],spots[dealer_num][1]), 20)       #Dealer Chip
        dealText = "Dealer"                       
        font = pygame.font.SysFont('Arial',15)                      
        text = font.render(dealText, 1, (0, 0, 0))
        self.win.blit(text,(spots[dealer_num][0] - text.get_width() // 2, spots[dealer_num][1] - text.get_height() // 2))

        pygame.draw.circle(self.win, (69,88,255), (spots[small][0],spots[small][1]), 20)                    #Small Blind
        smallText1 = "Small"                       
        font = pygame.font.SysFont('Arial',15)                      
        text = font.render(smallText1, 1, (0, 0, 0))
        self.win.blit(text,(spots[small][0] - text.get_width() // 2, spots[small][1] - text.get_height()))
        smallText2 = "Blind"                       
        font = pygame.font.SysFont('Arial',15)                      
        text = font.render(smallText2, 1, (0, 0, 0))
        self.win.blit(text,(spots[small][0] - text.get_width() // 2, spots[small][1]))

        pygame.draw.circle(self.win, (255,255,0), (spots[big][0],spots[big][1]), 20)                    #Big Blind
        bigText1 = "Big"                       
        font = pygame.font.SysFont('Arial',15)                      
        text = font.render(bigText1, 1, (0, 0, 0))
        self.win.blit(text,(spots[big][0] - text.get_width() // 2, spots[big][1] - text.get_height()))
        bigText2 = "Blind"                       
        font = pygame.font.SysFont('Arial',15)                      
        text = font.render(bigText2, 1, (0, 0, 0))
        self.win.blit(text,(spots[big][0] - text.get_width() // 2, spots[big][1]))

    def draw_chips(self):
        pygame.draw.circle(self.win, WHITE, (self.chip_pos[0] + OFFSET, self.chip_pos[1]), CHIP_SIZE)
        self.win.blit(self.font.render(str(self.stack), True, BLACK), (self.chip_pos[0] - (TOKEN_FONT_SIZE // 2) + OFFSET, self.chip_pos[1] - (TOKEN_FONT_SIZE // 2)))

    def info(self):
        pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (25, 25, INFO_BOX_WIDTH, INFO_BOX_HEIGHT))
        self.hand[0].draw_big(self.win, 35, 35)
        self.hand[1].draw_big(self.win, 35 + MAG_CARD_WIDTH + 15, 35)
        self.win.blit(self.font.render(f'{self.player_name} Stack = {self.stack}', True, BLACK), (25, 15 + MAG_CARD_HEIGHT + 30))
        self.win.blit(self.font.render(f'Idk what other info', True, BLACK), (25, 15 + MAG_CARD_HEIGHT + 30 + TOKEN_FONT_SIZE))

    def init_buttons(self):
        self.buttons.append(Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17, f'Check') )
        self.buttons.append(Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17 * 2 + 40 * 1, f'Call'))
        self.buttons.append(Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17 * 3 + 40 * 2, f'Raise'))
        self.buttons.append(Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17 * 4 + 40 * 3, f'Fold'))
        self.buttons.append(Button(self.win, 147, HEIGHT - INFO_BOX_HEIGHT + 17 * 3 + 40 * 2, f'Confirm Raise'))
        self.buttons.append(Button(self.win, 1250, HEIGHT - INFO_BOX_HEIGHT + 17 * 4 + 40 * 3, f'Leave Game'))
        self.buttons.append(Button(self.win, 147, HEIGHT - INFO_BOX_HEIGHT + 17 * 4 + 40 * 3, f'All In'))
        self.buttons[4].hidden = True                                                                          ###Might not want this
        self.buttons[4].clickable = False
    
    def draw_buttons(self):
        pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (25, HEIGHT - INFO_BOX_HEIGHT, 115, INFO_BOX_HEIGHT - 50))
        pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (140, HEIGHT - INFO_BOX_HEIGHT, 133, INFO_BOX_HEIGHT - 50))#############
        for button in self.buttons:
            button.draw()

    def get_chip_pos(self):
        if self.player_num % 8 == 0:
            return (437.5, 400)
        elif self.player_num % 8 == 1:
            return (525, 575)
        elif self.player_num % 8 == 2:
            return (700, 662.5)
        elif self.player_num % 8 == 3:
            return (875, 575)
        elif self.player_num % 8 == 4:
            return (962.5, 400)
        elif self.player_num % 8 == 5:
            return (875, 225)
        elif self.player_num % 8 == 6:
            return (700, 137.5)
        elif self.player_num % 8 == 7:
            return (525, 225)
        else:
            return "Error in get_chip_pos()"

    def get_card_pos(self, player_num):
        if player_num % 8 == 0:
            return (475 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif player_num % 8 == 1:
            return (582 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif player_num % 8 == 2:
            return (850 - CARD_WIDTH, 775 - CARD_WIDTH - 30)
        elif player_num % 8 == 3:
            return (1117 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif player_num % 8 == 4:
            return (1225 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif player_num % 8 == 5:
            return (1112 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        elif player_num % 8 == 6:
            return (850 - CARD_WIDTH, 25 - (CARD_WIDTH // 2) + 10)
        elif player_num % 8 == 7:
            return (582 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        else:
            return "Error in get_card_pos()"

    def update_stack(self, amt):
        self.stack -= amt

    def bet(self, curr_bet, prev_bet):
        if curr_bet == 0:
            self.stack -= (10 - prev_bet)
            return 10 - prev_bet
        self.stack -= (curr_bet - prev_bet)
        return curr_bet - prev_bet
        # return 0 for check, curr_bet for call, higher value for raise, -1 for fold
        # reduce player stack by bet amount then return it
    
    def playAgainQuery(self):
        buttonyes = Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17, f'yes')
        buttonyes.draw()
        buttonno = Button(self.win, 30, HEIGHT - INFO_BOX_HEIGHT + 17, f'no')
        buttonno.draw()

    '''
        def bet(self, curr_bet, prev_bet):
        if curr_bet == 0:
            bet = int(random.random() * 100)
            self.stack -= bet
            return bet
        elif curr_bet > (self.stack + prev_bet):
            bet = self.stack
            self.stack = 0
            return bet
        else:
            bet = curr_bet - prev_bet
            self.stack -= bet
            return bet
        #return 0 for check, curr_bet for call, higher value for raise, -1 for fold
        #reduce player stack by bet amount then return it
    '''
    def draw_winners(self, message):
        print("it made it to winners")
        font = pygame.font.SysFont('Arial', 25)
        myRender = font.render(message, True, (0,200,0))
        self.win.blit(myRender,(0,0))
        print(message)
        pygame.display.update()
        time.sleep(1.5)
    
    def draw_losers(self, message, offset):
        print("it made it to losers")
        font = pygame.font.SysFont('Arial', 20)
        myRender = font.render(message, True, BLACK)
        self.win.blit(myRender,(0,100+offset))
        print(message)
        pygame.display.update()
        time.sleep(1.5)
        
             
