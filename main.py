import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)  # Light blue for title screen background

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math-Fall-Blast!")

# Fonts
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player properties
player_width = 100
player_height = 20
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - 50

# ** Customize player speed here **
player_speed = 9  # Change this value to increase or decrease player speed

# Falling numbers properties
numbers = []
fall_speed = 5   # ** Customize falling number speed here **
spawn_delay = 1000

# Game variables
score = 0
high_score = 0
answer = 0
num1, num2 = 0, 0
operation = "+"
time_last_spawn = pygame.time.get_ticks()
game_over = False
level = 1
timer_limit = 40  
timer_start = None   # Start time will be set when game starts

# Load resources (images and sounds)
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
catch_sound = pygame.mixer.Sound("catch.wav")

# Function to generate a new math problem
def generate_problem():
    global num1, num2, answer, operation
    num1 = random.randint(1 + level - 1, 9 + level - 1)  
    num2 = random.randint(1 + level - 1, 9 + level - 1)
    operation = random.choice(["+", "-", "*", "/"])

    if operation == "+":
        answer = num1 + num2
    elif operation == "-":
        answer = num1 - num2  
    elif operation == "*":
        answer = num1 * num2
    elif operation == "/":
        answer = num1 // num2 if num2 != 0 else random.randint(1, num1)

def create_falling_number():
    is_correct_answer = random.random() < 0.5
    value = answer if is_correct_answer else random.randint(-10, answer + level * 10)  
    x_position = random.randint(0, SCREEN_WIDTH - 50)
    rect = pygame.Rect(x_position, -50, 50, 50)
    return {"value": value, "rect": rect}

def draw_player():
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

def draw_numbers():
    for num in numbers:
        pygame.draw.rect(screen, GREEN, num["rect"])
        text = font_small.render(str(num["value"]), True, BLACK)
        screen.blit(text, (num["rect"].x + 10, num["rect"].y + 10))

def draw_hud():
    problem_text = font_large.render(f"{num1} {operation} {num2} =", True, BLACK)
    score_text = font_small.render(f"Score: {score}", True, BLACK)
    high_score_text = font_small.render(f"High Score: {high_score}", True, BLACK)
    
    # Display timer based on whether the game has started.
    timer_text_value = max(0, (timer_limit - (pygame.time.get_ticks() - timer_start) // 1000)) if timer_start else timer_limit 
    timer_text = font_small.render(f"Time: {timer_text_value}", True, BLACK)

    screen.blit(problem_text, (20, 20))
    screen.blit(score_text, (20, 100))
    screen.blit(high_score_text, (20, 140))
    screen.blit(timer_text,(20 ,180))

def draw_game_over():
    game_over_text = font_large.render("Game Over!", True , RED)
    restart_text=font_small.render("Press SPACE to Restart", True , BLACK)
    screen.blit(game_over_text,(SCREEN_WIDTH //2 -150 , SCREEN_HEIGHT //2 -50))
    screen.blit(restart_text,(SCREEN_WIDTH//2-150 , SCREEN_HEIGHT//2+20))

def draw_title_screen():
    # Fill background with light blue color for title screen.
    screen.fill(LIGHT_BLUE)

    title_text=font_large.render("Math-Fall-Blast!", True , BLACK)
    start_text=font_small.render("Press ENTER to Start", True , BLACK)

    # Draw title and start text on the background.
    screen.blit(title_text,(SCREEN_WIDTH //2 - title_text.get_width() //2 , SCREEN_HEIGHT //4))
    screen.blit(start_text,(SCREEN_WIDTH //2 - start_text.get_width() //2 , SCREEN_HEIGHT //2))

def restart_game():
    global score , fall_speed , numbers , player_x , game_over , level , timer_start , spawn_delay , high_score , timer_limit
    
    if score > high_score:
        high_score=score
        
    score=0 
    fall_speed=5   # Reset falling speed on restart; customize this value as needed.
    
    numbers=[] 
    player_x=SCREEN_WIDTH//2-player_width//2 
    game_over=False 
    level=1 
    
    timer_limit=40   
    timer_start=pygame.time.get_ticks()  

    spawn_delay=1000 
    generate_problem()

def main():
    global player_x , score , time_last_spawn , numbers , fall_speed , game_over , high_score , spawn_delay , timer_start , timer_limit , level 

    generate_problem()

    running=True
    in_title_screen=True

    while running:
        if in_title_screen:
            draw_title_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  
                        in_title_screen=False  
                        timer_start=pygame.time.get_ticks()   # Start the timer when entering gameplay.

        else:
            # Draw background image for gameplay.
            screen.blit(background_image,(0 ,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False

            # Game logic when not game over.
            if not game_over:
                keys=pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and player_x>0:
                    player_x-=player_speed 
                if keys[pygame.K_RIGHT] and player_x<SCREEN_WIDTH-player_width:
                    player_x+=player_speed 

                current_time=pygame.time.get_ticks()
                if current_time-time_last_spawn>spawn_delay:
                    numbers.append(create_falling_number())
                    time_last_spawn=current_time

                for num in numbers[:]:
                    num["rect"].y+=fall_speed

                    if num["rect"].y>SCREEN_HEIGHT:  
                        print(f"Missed number: {num['value']}")
                        numbers.remove(num)

                    if player_x<num["rect"].x+num["rect"].width and \
                       player_x+player_width>num["rect"].x and \
                       player_y<num["rect"].y+num["rect"].height and \
                       player_y+player_height>num["rect"].y:
                        if num["value"]==answer:  
                            print("Correct answer caught!")
                            catch_sound.play()
                            score+=1 
                            fall_speed+=0.1   # Increase falling speed slightly with each correct answer.
                            timer_limit += 2   
                            generate_problem()  
                        else:  
                            print("Incorrect answer caught!")
                            game_over=True  

                        numbers.remove(num)

                if timer_start is not None:
                    elapsed_time=(pygame.time.get_ticks()-timer_start)//1000
                else:
                    elapsed_time=0

                if elapsed_time>=timer_limit:
                    print(f"Time's up! Final Score: {score}")
                    game_over=True  

                draw_hud()
                draw_player()
                draw_numbers()
            else:
                draw_game_over()
                keys=pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:  
                    restart_game()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()