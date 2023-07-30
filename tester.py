import pygame, sys
from button import Button

pygame.init()

# SCREEN = pygame.display.set_mode((450, 550))
pygame.display.set_caption("Menu")

# Constants
GRID_SIZE = 6
CELL_SIZE = 75
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
SCOREBOARD_HEIGHT = 100
WIN_LENGTH = 5

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

BG = pygame.image.load("assets/Background.png")
# Create the game window
screen = pygame.display.set_mode((450, 550))
pygame.display.set_caption("Longest Line Game")

# Game variables
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
game_over = False
winning_line = []
winner = None
player_score = 0
ai_score = 0

#Music
music = pygame.mixer.music.load('Battle Results.mp3')
pygame.mixer.music.play(-1)
pop_sound = pygame.mixer.Sound("pop.wav")


# Fonts
font = pygame.font.Font(None, 40)

class Button():
        
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False
        

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = WHITE
            if grid[y][x] == 1:
                color = RED
            elif grid[y][x] == 2:
                color = BLUE
            elif (x, y) in winning_line:
                color = GREEN
            pygame.draw.rect(screen, color, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_scoreboard(player_score, ai_score):
    scoreboard_rect = pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, SCOREBOARD_HEIGHT)
    pygame.draw.rect(screen, BLACK, scoreboard_rect)

    player_score_text = font.render(f"Player: {player_score}", True, RED)
    ai_score_text = font.render(f"AI: {ai_score}", True, BLUE)
    reset_text = font.render("Reset", True, WHITE)
    main_menu_text = font.render("Main Menu", True, WHITE)
    

    screen.blit(player_score_text, (10, WINDOW_SIZE + 10))
    screen.blit(ai_score_text, (WINDOW_SIZE - 10 - ai_score_text.get_width(), WINDOW_SIZE + 10))
    screen.blit(reset_text, (WINDOW_SIZE // 2 - reset_text.get_width() // 2, WINDOW_SIZE + 10))
    screen.blit(main_menu_text, (WINDOW_SIZE // 2 - main_menu_text.get_width() // 2, WINDOW_SIZE + 50))

def draw_win_screen():
    win_text = font.render(f"{winner} wins!", True, WHITE)
    win_rect = pygame.Rect(WINDOW_SIZE // 2 - win_text.get_width() // 2, WINDOW_SIZE // 2 - win_text.get_height() // 2, win_text.get_width(), win_text.get_height())
    pygame.draw.rect(screen, BLACK, win_rect)
    screen.blit(win_text, (WINDOW_SIZE // 2 - win_text.get_width() // 2, WINDOW_SIZE // 2 - win_text.get_height() // 2))

def reset_game():
    global grid, game_over, winning_line, winner, player_score, ai_score
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    winning_line = []
    winner = None
    player_score, ai_score = 0, 0


def count_longest_line(player, x, y, score_count):
    longest_line = score_count
    winning_line_candidate = []
    print("Player is : " , player)
    print(grid[y][x])
    print(x, "-", y)

    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
        line_length = 0
        line = [(x, y)]
        nx, ny = x + dx, y + dy
        print(nx, ny, "CHECK")
        if grid[y][x] == player:
            line_length += 1
        while 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] == player:
            print("(", ny, nx, ")")
            print("BABABA: ", grid[ny][nx])

            line_length += 1
            print("player", player, " - ", line_length, "max")
            line.append((nx, ny))
            nx += dx
            ny += dy
        if line_length > longest_line:
            longest_line = line_length
            winning_line_candidate = line
        print(winning_line_candidate)

    return longest_line, winning_line_candidate


     

def ai_move():
    global ai_score
    count = 0
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 0 and count == 0:
                grid[y][x] = 2
                print("AI MOVE")
                print(grid[y][x])
                ai_score, _ = count_longest_line(2, x, y, ai_score)
                count = 1
                print("AI STOP")

def check_win(player, score_count):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == player:
                
                line_length, line = count_longest_line(player, x, y, score_count)
                if line_length == WIN_LENGTH:
                
            
                    return True, line
    return False, []

def play():
    global game_over, winning_line, winner
    running = True
    while running:
        global player_score, ai_score
        screen.fill(WHITE)
        draw_grid()
        draw_scoreboard(player_score, ai_score)

        if game_over:
            draw_win_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pop_sound.play()
                print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\n")
                print("YOU CLICK", player_score, ai_score,  "Ha")
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if y < WINDOW_SIZE and grid[grid_y][grid_x] == 0:
                    grid[grid_y][grid_x] = 1
                    player_score, _ = (count_longest_line(1, grid_x, grid_y, player_score))
                    game_over, winning_line = check_win(1, player_score)
                    if game_over:
                        winner = "Player"
                    else:
                        print("--------------------------------")
                        ai_move()
                        print("+++++++++++++++++++++++++++++++++++")
                        game_over, winning_line = check_win(2, ai_score)
                        if game_over:
                            winner = "AI"

                if y >= WINDOW_SIZE and y <= WINDOW_SIZE + 35 and x >= 180 and x <= 260:
                    reset_game()
                # if y >= WINDOW_SIZE + ... and y <= WINDOW_SIZE + SCOREBOARD_HEIGHT + ....:
                #     main_menu
        pygame.display.flip()

    pygame.quit()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        
        screen.fill("purple")

        #Options Text Information Title
        OPTIONS_TEXT = get_font(17).render("Welcome to Bots and Doxes", True, "Gold")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(225, 60))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        #Further Information
        OPTIONS_TEXT = get_font(15).render("First to 5 Wins!", True, "Yellow")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(225, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        #Options Text Edit for "Back" Button
        OPTIONS_BACK = Button(image=None, pos=(225, 400), 
                            text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")
                            
        #Indicator of pressing "Back" Button
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pop_sound.play()
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                    pop_sound.play()
                    

        pygame.display.update()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        

        #Title for Menu
        MENU_TEXT = get_font(30).render("Bots and Doxes", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(225, 50))

        # Set the size for the image
        DEFAULT_IMAGE_SIZE = (150, 50)
        
        # Scale the image to  needed size
        play_image = pygame.transform.scale(pygame.image.load("assets/Play Rect.png"), DEFAULT_IMAGE_SIZE)
        options_image = pygame.transform.scale(pygame.image.load("assets/Options Rect.png"), DEFAULT_IMAGE_SIZE)
        quit_image = pygame.transform.scale(pygame.image.load("assets/Quit Rect.png"), DEFAULT_IMAGE_SIZE)

        PLAY_BUTTON = Button(play_image, pos=(225, 150), 
                            text_input="PLAY", font=get_font(25), base_color="#d7fcd4", hovering_color="Green")
        OPTIONS_BUTTON = Button(options_image, pos=(225, 275), 
                            text_input="OPTIONS", font=get_font(25), base_color="#d7fcd4", hovering_color="Yellow")
        QUIT_BUTTON = Button(quit_image, pos=(225, 400), 
                            text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="Red")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                pop_sound.play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                    pop_sound.play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    pop_sound.play()
           

        pygame.display.update()

main_menu()