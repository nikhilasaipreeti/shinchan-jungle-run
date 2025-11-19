# Shinchan Jungle Run - Educational Game Project

## 🎮 Project Overview
**Shinchan Jungle Run** is a 2D endless runner game developed from scratch using Python and Pygame. This educational project was created to learn game development fundamentals while building a complete, functional game.

## 🚀 What I Built

### Core Gameplay Features
- **Custom Character Movement**: Implemented smooth running and jumping physics
- **Double Jump System**: Created timing-based double jump mechanics (300ms window)
- **Collectible Items**: Designed Chocobees and Puddings with different point values
- **Obstacle System**: Built collision detection for jungle obstacles
- **Progressive Difficulty**: Game speed increases as player progresses

### Technical Implementation
- **Game Architecture**: Designed custom GameState class and state management
- **Asset Handling**: Created safe loading system with placeholder fallbacks
- **User Interface**: Built complete menu system with buttons and transitions
- **Sound Integration**: Added background music and sound effects

## 🛠️ My Development Process

### Learning Journey
- Started with basic Pygame concepts and built up to complex game mechanics
- Debugged and tested each feature individually
- Implemented error handling for robust performance
- Organized code into modular, maintainable structure

### Key Code I Wrote
```python
# Custom double jump implementation
if game.is_jumping and game.can_double_jump and game.jump_count < 2:
    if current_time - game.last_jump_time < 300:
        game.player_velocity = -16
        game.jump_count = 2
        game.can_double_jump = False

# Custom collision detection system
player_rect = pygame.Rect(game.player_x, game.player_y, 60, 60)
if player_rect.colliderect(item['rect']) and not item['collected']:
    collect_sound.play()
    game.score += 1
```

## 📁 Project Structure
```
shinchan-jungle-run/
├── main.py              # Complete game implementation
├── assets/              # Game resources
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```✨ HERE sample outcome
<img width="489" height="523" alt="image" src="https://github.com/user-attachments/assets/a8ccde9c-0932-4058-9319-b12a846084cb" />
<img width="497" height="525" alt="Screenshot 2025-11-19 195618" src="https://github.com/user-attachments/assets/52226db5-e0c7-4729-902d-c20fe1b8085e" />


## 🎯 What I Learned

### Python Programming Skills
- Object-oriented programming with custom classes
- Event handling and game loop management
- Exception handling and debugging techniques
- Code organization and modular design

### Game Development Concepts
- 2D graphics rendering and animation principles
- Game physics implementation (gravity, velocity)
- Collision detection algorithms
- State management and screen transitions
- User interface design and implementation

### Software Engineering
- Version control with Git and GitHub
- Project documentation
- Asset management best practices
- Problem-solving and debugging strategies

## 🔧 Installation & Setup

### Requirements
- Python 3.8+
- Pygame library

### Quick Start
```bash
# Install Pygame
pip install pygame

# Run the game
python main.py
```

## 🎮 How to Play
- **SPACE**: Jump (double-tap quickly for double jump)
- **Mouse**: Navigate menus and click buttons
- **ESC**: Exit game

**Objective**: Help Shinchan run through the jungle, collect items, avoid obstacles, and reach the goal!

## 🌟 Educational Value
This project demonstrates my understanding of:
- **Game Development Fundamentals**: From concept to implementation
- **Python Programming**: Practical application of programming concepts
- **Problem Solving**: Debugging and optimizing game mechanics
- **Project Management**: Organizing and completing a complex project

## 🔍 Development Notes

### Original Work
- All game mechanics and code logic developed through learning and experimentation
- Visual design choices made for optimal gameplay experience
- Sound and music integration implemented for immersive gameplay
- Complete game architecture designed and built from ground up

### Learning Resources Used
- Pygame official documentation for library reference
- Online programming concepts for game development principles
- AI assistance for conceptual guidance and debugging help
- Personal experimentation and testing for feature implementation

## ⚠️ Educational Purpose
This project was created **exclusively for educational purposes** to learn game development and Python programming. The game represents original implementation work based on learned concepts rather than copied code.

## 🔮 Skills Gained
- Python programming and Pygame library proficiency
- Game design and development principles
- Problem-solving and debugging techniques
- Project planning and execution
- Version control and documentation practices

---

*This project represents my journey learning game development through hands-on implementation and problem-solving and design through my thoughts.*
