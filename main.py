"""
Shinchan Jungle Run - Educational Game
Created for learning Pygame development
Fan-made project - Not for commercial use
All Shinchan characters belong to their respective copyright owners and ai features
"""

import pygame
import random
import sys
import math
import os
import traceback
from pygame import mixer

def safe_init():
    """Safely initialize pygame with error handling"""
    try:
        pygame.init()
        mixer.init()
        print("Pygame initialized successfully")
        return True
    except Exception as e:
        print(f"Pygame initialization failed: {e}")
        return False

def load_image_safe(path, default_size=(100, 100), default_color=(200, 150, 150), description=""):
    """Safely load image or create placeholder"""
    try:
        if os.path.exists(path):
            image = pygame.image.load(path)
            return pygame.transform.scale(image, default_size)
        else:
            # Create a colored rectangle as placeholder
            surface = pygame.Surface(default_size, pygame.SRCALPHA)
            pygame.draw.rect(surface, default_color, (0, 0, default_size[0], default_size[1]))
            # Add text to identify the placeholder
            if description:
                font = pygame.font.SysFont('Arial', 12)
                text = font.render(description, True, (255, 255, 255))
                text_rect = text.get_rect(center=(default_size[0]//2, default_size[1]//2))
                surface.blit(text, text_rect)
            return surface
    except Exception as e:
        # Emergency fallback
        surface = pygame.Surface(default_size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0), (0, 0, default_size[0], default_size[1]))
        return surface

def load_sound_safe(path):
    """Safely load sound or return silent sound"""
    try:
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        else:
            return pygame.mixer.Sound(buffer=bytearray([]))  # Silent sound
    except Exception as e:
        return pygame.mixer.Sound(buffer=bytearray([]))  # Silent sound

def draw_button(screen, text, x, y, width, height, inactive_color, active_color, text_color=(255, 255, 255), action=None):
    """Draw a button with hover effect"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    button_rect = pygame.Rect(x, y, width, height)
    
    # Check if mouse is over button
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, active_color, button_rect, border_radius=12)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, button_rect, border_radius=12)
    
    # Add button border
    pygame.draw.rect(screen, (50, 50, 50), button_rect, 2, border_radius=12)
    
    # Button text
    font = pygame.font.SysFont('Arial', 30)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    
    return button_rect

def main():
    """Main game function with comprehensive error handling"""
    try:
        # Initialize pygame
        if not safe_init():
            input("Press Enter to exit...")
            return

        # Screen setup
        WIDTH, HEIGHT = 800, 400
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shinchan's Jungle Run")
        clock = pygame.time.Clock()

        # Colors
        LIGHT_GREEN = (200, 240, 200)
        GREEN = (100, 180, 100)
        DARK_GREEN = (70, 120, 70)
        BRIGHT_GREEN = (120, 220, 120)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        BLUE = (0, 100, 255)
        YELLOW = (255, 255, 0)
        GOLD = (255, 215, 0)

        # Load assets safely
        # Images
        bg_img = load_image_safe("assets/shinchan_files/jungle_bg.png", (WIDTH, HEIGHT), (100, 150, 100), "BG")
        home_bg = load_image_safe("assets/shinchan_files/home_bg.png", (WIDTH, HEIGHT), (150, 200, 150), "HOME")
        player_img = load_image_safe("assets/shinchan_files/shinchan.png", (80, 80), (255, 150, 150), "SHINCHAN")
        choco_img = load_image_safe("assets/shinchan_files/chocobee.png", (50, 50), (255, 215, 0), "CHOCO")
        pudding_img = load_image_safe("assets/shinchan_files/pudding.png", (50, 50), (150, 100, 200), "PUDDING")
        obstacle_img = load_image_safe("assets/shinchan_files/obstacle.png", (100, 100), (120, 80, 60), "OBSTACLE")
        parents_img = load_image_safe("assets/shinchan_files/parents.png", (100, 180), (200, 150, 150), "PARENTS")

        # Sounds
        jump_sound = load_sound_safe("assets/sounds/jump.mp3")
        collect_sound = load_sound_safe("assets/sounds/collect.mp3")
        win_sound = load_sound_safe("assets/sounds/win.mp3")
        crash_sound = load_sound_safe("assets/sounds/crash.mp3")
        double_jump_sound = load_sound_safe("assets/sounds/double_jump.mp3")
        button_sound = load_sound_safe("assets/sounds/button.mp3")

        # Try to load background music
        try:
            if os.path.exists("assets/sounds/bg_music.mp3"):
                pygame.mixer.music.load("assets/sounds/bg_music.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
        except:
            pass

        # Font function
        def get_font(size):
            return pygame.font.SysFont('Arial', size)

        # Draw text function
        def draw_text(text, x, y, size=30, color=BLACK, center=False):
            font = get_font(size)
            text_surface = font.render(text, True, color)
            if center:
                text_rect = text_surface.get_rect(center=(x, y))
            else:
                text_rect = text_surface.get_rect(topleft=(x, y))
            screen.blit(text_surface, text_rect)
            return text_rect

        # Game state variables
        class GameState:
            def __init__(self):
                self.reset()
            
            def reset(self):
                self.player_x = 100
                self.player_y = 300
                self.player_velocity = 0
                self.gravity = 1
                self.is_jumping = False
                self.jump_count = 0  # Track jumps for double jump
                self.can_double_jump = False  # Can perform double jump
                self.score = 0
                self.choco_count = 0
                self.pudding_count = 0
                self.distance = 0
                self.game_speed = 5
                self.game_over = False
                self.game_won = False
                self.items = []  # Collectible items
                self.obstacles = []  # Obstacles to avoid
                self.parents_x = WIDTH + 2000  # Parents at the end
                self.parents_spawned = False
                self.bg_x = 0  # Background scroll position
                self.last_jump_time = 0  # For double jump timing

        game = GameState()

        # Button actions
        def start_game():
            button_sound.play()
            return False  # Exit home screen

        def restart_game():
            button_sound.play()
            game.reset()

        def quit_game():
            pygame.quit()
            sys.exit()

        # Simple home screen
        home_screen_active = True
        while home_screen_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        home_screen_active = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
            
            # Draw home screen
            screen.blit(home_bg, (0, 0))
            
            # Title and instructions in YELLOW
            draw_text("SHINCHAN JUNGLE RUN", WIDTH//2, 80, 50, YELLOW, center=True)
            draw_text("Collect Chocobees & Puddings!", WIDTH//2, 130, 25, YELLOW, center=True)
            draw_text("Avoid obstacles and find your parents!", WIDTH//2, 160, 25, YELLOW, center=True)
            draw_text("SPACE: Jump | Double SPACE: Double Jump", WIDTH//2, 190, 20, YELLOW, center=True)
            
            # Draw start button
            start_button = draw_button(
                screen, 
                "START GAME", 
                WIDTH//2 - 100, 
                250, 
                200, 
                60, 
                GREEN, 
                BRIGHT_GREEN, 
                WHITE, 
                start_game
            )
            
            # Draw quit button
            quit_button = draw_button(
                screen,
                "QUIT",
                WIDTH//2 - 100,
                330,
                200,
                50,
                DARK_GREEN,
                GREEN,
                WHITE,
                quit_game
            )
            
            # Handle button clicks
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            
            if start_button.collidepoint(mouse_pos) and mouse_click[0]:
                home_screen_active = start_game()
            elif quit_button.collidepoint(mouse_pos) and mouse_click[0]:
                quit_game()
            
            pygame.display.flip()
            clock.tick(60)

        # Timers for spawning objects
        item_spawn_timer = 0
        obstacle_spawn_timer = 0

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not game.game_over and not game.game_won:
                        current_time = pygame.time.get_ticks()
                        
                        # First jump (on ground)
                        if not game.is_jumping:
                            game.player_velocity = -18  # First jump force
                            game.is_jumping = True
                            game.jump_count = 1
                            game.can_double_jump = True
                            jump_sound.play()
                        
                        # Double jump (in air, within time window)
                        elif game.is_jumping and game.can_double_jump and game.jump_count < 2:
                            # Check if we're within double jump window (300ms after first jump)
                            if current_time - game.last_jump_time < 300:
                                game.player_velocity = -16  # Slightly less force for double jump
                                game.jump_count = 2
                                game.can_double_jump = False  # Can't triple jump
                                if double_jump_sound.get_length() > 0:  # Only play if sound exists
                                    double_jump_sound.play()
                            else:
                                # Too late for double jump
                                game.can_double_jump = False
                        
                        game.last_jump_time = current_time
                        
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if not game.game_over and not game.game_won:
                # Apply gravity
                game.player_velocity += game.gravity
                game.player_y += game.player_velocity

                # Ground collision
                if game.player_y >= 300:
                    game.player_y = 300
                    game.player_velocity = 0
                    game.is_jumping = False
                    game.jump_count = 0
                    game.can_double_jump = False

                # Update distance and speed
                game.distance += game.game_speed
                if game.distance % 500 == 0:  # Increase speed every 500 units
                    game.game_speed += 0.5

                # Scroll background
                game.bg_x -= game.game_speed
                if game.bg_x <= -WIDTH:
                    game.bg_x = 0

                # Spawn collectible items
                item_spawn_timer += 1
                if item_spawn_timer > 60:  # Spawn every 60 frames
                    item_type = random.choice(['choco', 'pudding'])
                    item_img = choco_img if item_type == 'choco' else pudding_img
                    item_y = random.randint(200, 280)  # Random height
                    game.items.append({
                        'type': item_type,
                        'img': item_img,
                        'rect': pygame.Rect(WIDTH, item_y, 40, 40),
                        'collected': False
                    })
                    item_spawn_timer = 0

                # Spawn obstacles
                obstacle_spawn_timer += 1
                if obstacle_spawn_timer > 90:  # Spawn every 90 frames
                    game.obstacles.append({
                        'img': obstacle_img,
                        'rect': pygame.Rect(WIDTH, 320, 60, 60)
                    })
                    obstacle_spawn_timer = 0

                # Update items
                for item in game.items[:]:
                    item['rect'].x -= game.game_speed
                    
                    # Check collection
                    player_rect = pygame.Rect(game.player_x, game.player_y, 60, 60)
                    if player_rect.colliderect(item['rect']) and not item['collected']:
                        item['collected'] = True
                        collect_sound.play()
                        game.score += 1
                        if item['type'] == 'choco':
                            game.choco_count += 1
                        else:
                            game.pudding_count += 1
                            game.score += 2  # Extra points for pudding
                        game.items.remove(item)
                    elif item['rect'].right < 0:
                        game.items.remove(item)

                # Update obstacles
                for obstacle in game.obstacles[:]:
                    obstacle['rect'].x -= game.game_speed
                    
                    # Check collision
                    player_rect = pygame.Rect(game.player_x, game.player_y, 60, 60)
                    if player_rect.colliderect(obstacle['rect']):
                        game.game_over = True
                        crash_sound.play()
                    elif obstacle['rect'].right < 0:
                        game.obstacles.remove(obstacle)

                # Check if parents should appear
                if game.distance >= 1500 and not game.parents_spawned:
                    game.parents_spawned = True

                # Update parents position
                if game.parents_spawned:
                    game.parents_x -= game.game_speed
                    
                    # Check if reached parents
                    player_rect = pygame.Rect(game.player_x, game.player_y, 60, 60)
                    parents_rect = pygame.Rect(game.parents_x, 220, 80, 160)
                    if player_rect.colliderect(parents_rect):
                        game.game_won = True
                        win_sound.play()

            # Draw everything
            screen.fill(LIGHT_GREEN)
            
            # Draw scrolling background
            screen.blit(bg_img, (game.bg_x, 0))
            screen.blit(bg_img, (game.bg_x + WIDTH, 0))
            
            # Draw collectible items
            for item in game.items:
                screen.blit(item['img'], item['rect'])
            
            # Draw obstacles
            for obstacle in game.obstacles:
                screen.blit(obstacle['img'], obstacle['rect'])
            
            # Draw parents if spawned
            if game.parents_spawned:
                screen.blit(parents_img, (game.parents_x, 220))
            
            # Draw player
            screen.blit(player_img, (game.player_x, game.player_y))
            
            # Draw jump indicator
            if game.is_jumping and game.can_double_jump and game.jump_count == 1:
                # Show double jump available indicator
                indicator_color = BLUE
                pygame.draw.circle(screen, indicator_color, (game.player_x + 40, game.player_y - 20), 8)

            # Draw UI
            draw_text(f"Score: {game.score}", 20, 20, 25, BLACK)
            draw_text(f"Chocobees: {game.choco_count}", 20, 50, 20, BLACK)
            draw_text(f"Puddings: {game.pudding_count}", 20, 75, 20, BLACK)
            draw_text(f"Distance: {min(game.distance, 2000)}/2000", 20, 100, 20, BLACK)
            
            # Draw jump status
            if game.jump_count == 1:
                draw_text("Jump: 1/2", WIDTH - 80, 20, 18, BLUE)
            elif game.jump_count == 2:
                draw_text("Jump: 2/2", WIDTH - 80, 20, 18, RED)
            else:
                draw_text("Jump: 0/2", WIDTH - 80, 20, 18, BLACK)
            
            # Draw instructions
            if not game.game_over and not game.game_won:
                draw_text("SPACE: Jump", WIDTH - 100, 45, 16, BLACK)
                draw_text("Double SPACE: Double Jump", WIDTH - 130, 65, 16, BLACK)
            
            # Game over screen
            if game.game_over:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                
                draw_text("GAME OVER", WIDTH//2, HEIGHT//2 - 80, 60, RED, center=True)
                draw_text(f"Final Score: {game.score}", WIDTH//2, HEIGHT//2 - 30, 30, WHITE, center=True)
                
                # Restart button
                restart_button = draw_button(
                    screen,
                    "PLAY AGAIN",
                    WIDTH//2 - 100,
                    HEIGHT//2 + 20,
                    200,
                    50,
                    GREEN,
                    BRIGHT_GREEN,
                    WHITE,
                    restart_game
                )
                
                # Quit button
                menu_button = draw_button(
                    screen,
                    "MAIN MENU",
                    WIDTH//2 - 100,
                    HEIGHT//2 + 90,
                    200,
                    50,
                    DARK_GREEN,
                    GREEN,
                    WHITE,
                    lambda: [restart_game(), setattr(game, 'game_over', False), setattr(game, 'game_won', False)]
                )
                
                # Handle button clicks
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()
                
                if restart_button.collidepoint(mouse_pos) and mouse_click[0]:
                    restart_game()
                elif menu_button.collidepoint(mouse_pos) and mouse_click[0]:
                    restart_game()
                    game.game_over = False
                    game.game_won = False
                    # Return to home screen would need additional logic
            
            # Game won screen
            if game.game_won:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 100, 0, 150))
                screen.blit(overlay, (0, 0))
                
                draw_text("YOU WIN!", WIDTH//2, HEIGHT//2 - 80, 60, GOLD, center=True)
                draw_text("You found your parents!", WIDTH//2, HEIGHT//2 - 30, 30, WHITE, center=True)
                draw_text(f"Final Score: {game.score}", WIDTH//2, HEIGHT//2 + 10, 30, WHITE, center=True)
                
                # Restart button
                restart_button = draw_button(
                    screen,
                    "PLAY AGAIN",
                    WIDTH//2 - 100,
                    HEIGHT//2 + 50,
                    200,
                    50,
                    GREEN,
                    BRIGHT_GREEN,
                    WHITE,
                    restart_game
                )
                
                # Menu button
                menu_button = draw_button(
                    screen,
                    "MAIN MENU",
                    WIDTH//2 - 100,
                    HEIGHT//2 + 120,
                    200,
                    50,
                    DARK_GREEN,
                    GREEN,
                    WHITE,
                    lambda: [restart_game(), setattr(game, 'game_over', False), setattr(game, 'game_won', False)]
                )
                
                # Handle button clicks
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()
                
                if restart_button.collidepoint(mouse_pos) and mouse_click[0]:
                    restart_game()
                elif menu_button.collidepoint(mouse_pos) and mouse_click[0]:
                    restart_game()
                    game.game_over = False
                    game.game_won = False
            
            pygame.display.flip()
            clock.tick(60)

        print("Game ended normally")
        
    except Exception as e:
        print(f"Game crashed with error: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
