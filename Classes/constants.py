import pygame

# desmos link: https://www.desmos.com/calculator/tibq5mmg3q
# The desmos link makes it easier to know where to place draw things on screen. In pygame, y value gets higher so need to do Height - y to get the y value
# Also I didn't inlcude the offset initially. Just add offset to the x coordiate

WIDTH, HEIGHT = 1400, 800
BOARD_RADIUS = 350
INNER_BORDER_RADIUS = BOARD_RADIUS // 2
CHIP_SIZE = 25
INFO_BOX_WIDTH, INFO_BOX_HEIGHT = 235, 300
GAP = 10
# Other than the info and button box, OFFSET is used to push over the table along with eveything on the table over. Center table by making offset = 0.
# Offset should only be used with x coordinates
OFFSET = 150
CARD_WIDTH, CARD_HEIGHT = 50, 90 #50, 90 100, 150
MAG_CARD_WIDTH, MAG_CARD_HEIGHT = 100, 180
INFO_BOX_X, INFO_BOX_Y = 150, 50
BOARD_CARD_BOX_X, BOARD_CARD_BOX_Y = 279, 105
SMALL_CARD_FONT_SIZE = 25
BIG_CARD_FONT_SIZE = 35

HEART = pygame.transform.scale(pygame.image.load('Pictures/Card_heart.png'), (17,13))
DIAMOND = pygame.transform.scale(pygame.image.load('Pictures/Card_diamond.png'), (17,13))
CLUB = pygame.transform.scale(pygame.image.load('Pictures/Card_club.png'), (17,13))
SPADE = pygame.transform.scale(pygame.image.load('Pictures/Card_spade.png'), (17,13))
BACK = pygame.transform.scale(pygame.image.load('Pictures/Card_back.jpg'), (CARD_WIDTH,CARD_HEIGHT))

'''
HEART = pygame.transform.scale(pygame.image.load('Pictures/Card_heart.png'), (36,28))
DIAMOND = pygame.transform.scale(pygame.image.load('Pictures/Card_diamond.png'), (36,28))
CLUB = pygame.transform.scale(pygame.image.load('Pictures/Card_club.png'), (36,28))
SPADE = pygame.transform.scale(pygame.image.load('Pictures/Card_spade.png'), (36,28))
'''

BACKGROUND_COLOR = pygame.Color("#373737")
BOARD_COLOR = pygame.Color("#114636")
BOARD_CARDS_BOX_COLOR = pygame.Color("#2f4f4f")
RAILING_COLOR = (111, 78, 55)

#Poker values
START_STACK = 1000
SM_BLIND = 5
BIG_BLIND = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TOKEN_FONT_SIZE = 25

CARDW = 100
CARDH = 150
OUTLINEBUFF = 5
NUMBUFF = 10


PLAYER_NAMES = ["Daniel Negreanu", "Bryn Kenney", "Phil Ivey", "Justin Bonomo",
                "Erik Seidel", "Dan Smith", "Stephen Chidwick", "Tom Dwan"]
SUITS = ['♣','♦','♠','♥']
HANDS = ['High Card', 'Pair', 'Two Pair', 'Three of a kind',
        'Straight', 'Flush', 'Full House', 'Four of a kind',
        'Straight Flush', 'Royal Flush']
