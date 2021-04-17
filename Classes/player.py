from . data import *
from . constants import *
from . button import *
import time
from . card import Card
import gc
import pygame
import sys

class Player:
    def __init__(self, win, player_name, player_num, start_amt):
        self.win = win
        self.player_name = player_name
        self.player_num = player_num
        self.stack = start_amt
        self.hand = []
        self.board_cards = []
        self.buttons = []
        self.curr_hand = None
        self.playing = True
        self.chip_pos = self.get_chip_pos()
        self.card_pos = self.get_card_pos()
        self.font = pygame.font.SysFont('Arial', SMALL_CARD_FONT_SIZE)

    # If needing to print out a player object, will return name and player number. To use in main: print(player)
    def __str__(self):
        return "Player Name: " + self.player_name + " --- " + "Player Number: " + str(self.player_num)

    # @return - How much the player is paying for the blind (Not sure if the self.stack is suppose to be manipulated)
    def blind(self, blind_amt):  
        ###same as in bet, determine if the player has that much money left
        ###if it doesn't then return the maxium amt it cant(subtracting so that self.stack = 0) and the data class will handle
        copy_stack = self.stack
        copy_stack -= blind_amt
        # ? return the amount player added to blind ?
        if copy_stack < 0:
            print(str(self.stack) + ' - ' + str(blind_amt) + " = " + str(copy_stack))
            new_blind_amt = self.stack
            self.stack = 0
            return new_blind_amt
        else:
            self.stack -= blind_amt
            return blind_amt

    # @description - Gets a list of (number, suit), converts into Card object, stores Card objects into the self.hand list
    # @param - A list of cards that will be the objects hand
    # @return - nothing
    def receive_hand(self, hand):
        ###With that poker module, the cards are actually already in a built-in class(maybe it would have been easier to just implement with numbers idk)
        ### but it will come in a Card object. To get the rank and suit, they can be accessed with card.suit and card.rank
        ###  these will return strings for the rank(2-9 or T,J,Q,K,A) and suit. The suits are special characters. I have these in the constants in data.py
        ### and have added them to this branch
        i = 0
        for card in hand:
            if i % 2 == 0:
                print("[player.py] " + self.player_name + " receiving cards:")
            self.hand.append(card)
            print(f'\t [player.py] Added to hand: {self.hand[i]}')
            i += 1

    # @description - Gets a list of (number, suit), converts into Card object, stores Card objects into the self.hand list
    # @param - A list of numbers that will be the board cards
    # @return - nothing
    def receive_board_cards(self, cards):  # list of cards. WILL be duplicates
        ###Same thing as above, it will come in as Card objects that can be accessed with Card.rank and card.suit
        ###Can Not just use append. Check if the card already exists in self.board_cards before using append
        ### the entire board will be sent each time so there will be duplicates
        print(f'[player.py] {self.player_name} has access to the board cards:')
        self.board_cards.append(cards)
        for i in range(len(self.board_cards)):
            print(f'\t [player.py] {self.board_cards[0][i]}')

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

    def take_turn(self, cur_bet, prev_bet):
        # Might need some help with this method. Played poker like 5 times but have no clue how to play.
        ###This will be an input loop similar to what happens in main. We will await input from the user in terms of buttons
        self.draw_board()
        self.info()
        self.button_area()
        i = 0
        for i in range(len(self.buttons)):
            print(i)
        print(f'Total buttons = {i + 1}')
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if pos[0] >= 95 and pos[0] <= 187:
                        if pos[1] >= 370 and pos[1] <= 414:
                            print('FOLD button clicked')
                            self.fold()
                            return 0
                        elif pos[1] >= 423 and pos[1] <= 467:
                            print('CALL button pressed')
                            return 1
                        elif pos[1] >= 480 and pos[1] <= 520:
                            print('CHECK button pressed')
                            return 2
                        elif pos[1] >= 535 and pos[1] <= 577:
                            print('RAISE button pressed')
                            turn_finished = False
                            raise_amt = 0
                            while not turn_finished:
                                raise_amt = int(input('How much to raise?'))
                                if self.stack >= raise_amt:
                                    self.stack -= raise_amt
                                    # add to pot?
                                    turn_finished = True
                                else:
                                    print("Can't raise that amount. Not enough in stack")
                            print(f'Amount raise: {raise_amt}')
                            return 3
                        elif pos[1] >= 591 and pos[1] <= 633:
                            print('CONFIRM button pressed')
                            return 4
                        elif pos[1] >= 647 and pos[1] <= 689:
                            print('QUIT button pressed')
                            pygame.quit()
                            # return -1
                        else:
                            print('No button was pressed')
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()

        ### for btn in self.btns:
        ###     btn.activate will make it appear, otherwise it will be hidden
        ### while not input:
        ###
        ###     for event in pygame.event.get():
        ###         if event.type == pygame.MOUSEBUTTONDONW
        ###             check if it hit a button in self.btns - these will include FOLD, CALL, CHECK, RAISE, CONFIRM or
        ###                                                     something that can do those functions. The reason for confirm
        ###                                                     would be so that a person could click raise several times
        ###             if it should do something, FOLD, CALL, CHECK, etc then do it
        ###             and end the loop
        ###
        ###ACTUALLY, JUST GET RID OF BET() AND JUST DO TAKE_TURN

        ###Add drawing of the board and player symbols, etc.

    # @description - Draws each card from current players hand
    # @param - nothing
    # @return - nothing
    def draw_cards(self):
        # each card is an object from card class
        print(f'[player.py] Drawing cards on screen for player {self.player_name}')
        self.hand[0].draw(self.win, self.card_pos[0], self.card_pos[1])
        self.hand[1].draw(self.win, self.card_pos[0] + CARD_WIDTH + GAP, self.card_pos[1])

    # @description - Draws the board cards
    # @param - nothing
    # @return - nothing
    def draw_board_cards(self):
        print(f'[player.py] Drawing board cards on screen for player {self.player_name}')
        board_card_box = pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (560 + OFFSET, 365, BOARD_CARD_BOX_X, BOARD_CARD_BOX_Y))
        board_card_1 = self.board_cards[0][0].draw(self.win, 560 + 5 * 1 + OFFSET, 365 + 15 // 2)
        board_card_2 = self.board_cards[0][1].draw(self.win, 560 + 5 * 2 + 1 * CARD_WIDTH + OFFSET, 365 + 15 // 2)
        board_card_3 = self.board_cards[0][2].draw(self.win, 560 + 5 * 3 + 2 * CARD_WIDTH + OFFSET, 365 + 15 // 2)
        try:
            board_card_4 =self.board_cards[0][3].draw(self.win, 560 + 5 * 4 + 3 * CARD_WIDTH + OFFSET, 365 + 15 // 2)
        except:
            print('[player.py] There are current only 3 board cards. Drawing 2 blank cards')
            board_card_4 = pygame.draw.rect(self.win, WHITE, (560 + 5 * 4 + 3 * CARD_WIDTH + OFFSET, 365 + 15 // 2, CARD_WIDTH, CARD_HEIGHT))
        try:
            board_card_5 =self.board_cards[0][4].draw(self.win, 560 + 5 * 5 + 4 * CARD_WIDTH + OFFSET, 365 + 15 // 2)
        except:
            print('[player.py] There are current only 4 board cards. Drawing 1 blank cards')
            board_card_5 = pygame.draw.rect(self.win, WHITE, (560 + 5 * 5 + 4 * CARD_WIDTH + OFFSET, 365 + 15 // 2, CARD_WIDTH, CARD_HEIGHT))

    # @description - Draws all the other players cards
    # @param - nothing
    # @return - nothing
    def draw_opponents(self):
        print(f'[player.py] Drawing card/hands of other players')
        for i in range(8):
            if i != self.player_num:
                other_player_card_x, other_player_card_y = self.get_other_player_card_pos(i)
                card_1 = pygame.draw.rect(self.win, WHITE, (other_player_card_x, other_player_card_y, CARD_WIDTH, CARD_HEIGHT))
                card_2 = pygame.draw.rect(self.win, WHITE, (other_player_card_x + CARD_WIDTH + GAP, other_player_card_y, CARD_WIDTH, CARD_HEIGHT))

    def draw_board(self):
        self.win.fill(BACKGROUND_COLOR)
        railing = pygame.draw.circle(self.win, RAILING_COLOR, (WIDTH // 2 + OFFSET, HEIGHT // 2), BOARD_RADIUS * 1.1)
        board = pygame.draw.circle(self.win, BOARD_COLOR, (WIDTH // 2 + OFFSET, HEIGHT // 2), BOARD_RADIUS)
        inner_circle = pygame.draw.circle(self.win, WHITE, (WIDTH // 2 + OFFSET, HEIGHT // 2), INNER_BORDER_RADIUS, width=1)

        # self.draw_chips()       # Won't need if for loop works
        # self.draw_board_cards()
        # self.info()
        # self.button_area()
        # self.draw_cards()
        # self.draw_opponents()

    def draw_chips(self):
        pygame.draw.circle(self.win, WHITE, (self.chip_pos[0] + OFFSET, self.chip_pos[1]), CHIP_SIZE)
        self.win.blit(self.font.render(str(self.stack), True, BLACK), (self.chip_pos[0] - (TOKEN_FONT_SIZE // 2) + OFFSET, self.chip_pos[1] - (TOKEN_FONT_SIZE // 2)))
        print(f'[player.py] Chip coordinates for {self.player_name}: {self.chip_pos}')

    def info(self):
        pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (25, 25, INFO_BOX_WIDTH, HEIGHT - 60))
        # drawing blank don't use the next 2 lines in actual code. Instead use the line 3 and 4 after this line.
        pygame.draw.rect(self.win, WHITE, (35, 35, MAG_CARD_WIDTH, MAG_CARD_HEIGHT))
        pygame.draw.rect(self.win, WHITE, (35 + MAG_CARD_WIDTH + 15, 35, MAG_CARD_WIDTH, MAG_CARD_HEIGHT))
        # self.hand[0].draw_big(self.win, 35, 35)
        # self.hand[1].draw_big(self.win, 35 + MAG_CARD_WIDTH + 15, 35)
        self.win.blit(self.font.render(f'{self.player_name.split()[0].upper()} STACK = {self.stack}', True, BLACK), (25, 15 + MAG_CARD_HEIGHT + 30))
        self.win.blit(self.font.render(f'POT = '.upper(), True, BLACK), (25, 15 + MAG_CARD_HEIGHT + 30 + TOKEN_FONT_SIZE))

    def button_area(self):
        # pygame.draw.rect(self.win, BOARD_CARDS_BOX_COLOR, (25, HEIGHT - INFO_BOX_HEIGHT, 115, INFO_BOX_HEIGHT - 100))
        fold_button = Button(self.win, 90, HEIGHT - INFO_BOX_HEIGHT + 15 - 150)
        fold_button.draw('FOLD')
        self.buttons.append(fold_button)
        call_button = Button(self.win, 90, HEIGHT - INFO_BOX_HEIGHT + 15 * 2 + 40 * 1 - 150)
        call_button.draw('CALL')
        self.buttons.append(call_button)
        check_button = Button(self.win, 90, HEIGHT - INFO_BOX_HEIGHT + 15 * 3 + 40 * 2 - 150)
        check_button.draw('CHECK')
        self.buttons.append(check_button)
        raise_button = Button(self.win, 90, HEIGHT - INFO_BOX_HEIGHT + 15 * 4 + 40 * 3 - 150)
        raise_button.draw('RAISE')
        self.buttons.append(raise_button)
        confirm_button = Button(self.win, 90, HEIGHT - INFO_BOX_HEIGHT + 15 * 5 + 40 * 4 - 150)
        confirm_button.draw('CONFIRM')
        self.buttons.append(confirm_button)
        quit_button = Button(self.win, 90, HEIGHT - INFO_BOX_HEIGHT + 15 * 6 + 40 * 5 - 150)
        quit_button.draw('QUIT')
        self.buttons.append(quit_button)


    def get_chip_pos(self):
        if self.player_num == 0:
            return (437.5, 400)
        elif self.player_num == 1:
            return (525, 575)
        elif self.player_num == 2:
            return (700, 662.5)
        elif self.player_num == 3:
            return (875, 575)
        elif self.player_num == 4:
            return (962.5, 400)
        elif self.player_num == 5:
            return (875, 225)
        elif self.player_num == 6:
            return (700, 137.5)
        elif self.player_num == 7:
            return (525, 225)
        else:
            return "Error in get_chip_pos()"

    def get_card_pos(self):
        if self.player_num == 0:
            return (475 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif self.player_num == 1:
            return (582 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif self.player_num == 2:
            return (850 - CARD_WIDTH, 775 - CARD_WIDTH - 30)
        elif self.player_num == 3:
            return (1117 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif self.player_num == 4:
            return (1225 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif self.player_num == 5:
            return (1112 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        elif self.player_num == 6:
            return (850 - CARD_WIDTH, 25 - (CARD_WIDTH // 2) + 10)
        elif self.player_num == 7:
            return (582 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        else:
            return "Error in get_card_pos()"

    def get_other_player_card_pos(self, player_num):
        if player_num == 0:
            return (475 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif player_num == 1:
            return (582 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif player_num == 2:
            return (850 - CARD_WIDTH, 775 - CARD_WIDTH - 30)
        elif player_num == 3:
            return (1117 - CARD_WIDTH, 663 - (CARD_WIDTH // 2))
        elif player_num == 4:
            return (1225 - CARD_WIDTH, 400 - (CARD_WIDTH // 2))
        elif player_num == 5:
            return (1112 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        elif player_num == 6:
            return (850 - CARD_WIDTH, 25 - (CARD_WIDTH // 2) + 10)
        elif player_num == 7:
            return (582 - CARD_WIDTH, 133 - (CARD_WIDTH // 2))
        else:
            return "Error in get_card_pos()"

    def bet(self, curr_bet, prev_bet):
        ### This was for testing for me, so change this to be based on user input
        ### self.take_turn()
        ### keep track of what they do. If they end up calling fold() then return -1, if they bet the same as the current bet, then
        ### return curr_bet - prev_bet
        ### if they raise, then return the value they raised, etc
        if curr_bet == 0:
            self.stack -= (10 + prev_bet)
            return 10 - prev_bet
        self.stack -= (curr_bet + prev_bet)
        return curr_bet - prev_bet
        # return 0 for check, curr_bet for call, higher value for raise, -1 for fold
        # reduce player stack by bet amount then return it




