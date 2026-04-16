# Shooting Plane Game --- COMP2116 Final Project
Shooting Plane Game is a simple 2D arcade-style shooting game developed in Python.
Players control a fighter plane, shoot down enemies, and try to achieve the highest score while avoiding collisions.

### How to Install?

1. Go to the github Release:
<img width="2559" height="1194" alt="未命名設計" src="https://github.com/user-attachments/assets/c29be48e-8f65-4a97-965e-f8c420042992" />
2. Click **ShootingGame-demo-verison-v0.6.zip** to download and extract it:
<img width="2559" height="1194" alt="Download the zip file" src="https://github.com/user-attachments/assets/d8e29e62-2b89-4f5d-ae4c-578d0213b7d8" />
3. After extract the folder you can find two file:
<img width="924" height="612" alt="螢幕擷取畫面 2026-04-16 144510" src="https://github.com/user-attachments/assets/3905e13c-d784-4341-94b7-292aadc1a78a" />
4. Click .exe file to play:
<img width="1110" height="770" alt="image" src="https://github.com/user-attachments/assets/9ba78ea5-cc7f-45cd-b613-533566085128" />



# 1. Graphical Abstract

### HOME:
<img width="792" height="626" alt="螢幕擷取畫面 2026-04-15 235210" src="https://github.com/user-attachments/assets/5737da7e-6e5a-4ba5-8b41-18e2bcda9725" />

### IN GAME:
<img width="797" height="628" alt="螢幕擷取畫面 2026-04-15 235225" src="https://github.com/user-attachments/assets/4ead0b96-88a2-484f-8316-212b271ed2a9" />

### GAME OVER:
<img width="793" height="626" alt="螢幕擷取畫面 2026-04-15 235235" src="https://github.com/user-attachments/assets/fb4f4441-88fa-48d0-9ea9-7bc8c15318e4" />




# 2. Project Purpose

### Software Development Process Applied:
The development of the Shooting Plane Game follows the Agile Development Methodology. This project utilizes an incremental and iterative approach, where the software is developed as a series of versions (v0.1 to v0.3). Each iteration focuses on delivering working code quickly—from basic player movement to the integration of complex systems like collision, scoring, and multimedia elements.

### Why Agile?
We chose the Agile approach over the Waterfall model for several strategic reasons:
- Response to Change: Unlike the Waterfall model’s inflexible partitioning , Agile allows us to embrace changes in game requirements or mechanics (such as adding W/S keys or background music) based on testing feedback.
- Rapid Delivery: Agile focuses on delivering a functional product early. As seen in our schedule, we released a demo (v0.1) within 10 days, allowing for early validation of core gameplay.
- Efficiency for Small Teams: For a Python-based arcade game, Agile minimizes documentation overhead and maximizes focus on code and working software.
- Strategic Fit: Given the dynamic nature of game development, Agile provides a better "Time-to-Market" advantage and fits our need for flexibility in the design of "Fun & Joy" elements.


### Possible usage of your software (Target Market)

The Shooting Plane Game is designed for:
- Casual Gamers: The primary target market includes users seeking quick, arcade-style entertainment and stress relief through simple, engaging mechanics.
- Educational Purpose: The project serves as an open-source reference for students and developers learning Python and game physics (e.g., using the Pygame library).
- Indie Game Developers: It provides a modular foundation for developers looking to build upon a functional 2D shooting engine for more complex arcade titles.

# 3. Project Development Plan

### Development Process:
### Software Development Process (Agile Methodology)
Our team adopted the Agile Development methodology to develop the "Shooting Plane Game.", we prioritized iterative development, rapid prototyping, and continuous refinement to ensure the software evolved based on testing and validation.

1. Agile Framework: Iterative & Incremental
Instead of a rigid linear process, we organized our development into three focused Sprints. This allowed us to maintain a "Minimum Viable Product" (v0.1) and progressively add features (Audio, GUI) through software evolution.

2. Software Process Activities within Sprints
In each iteration, we integrated the four core activities:

  - Specification: Defining gameplay requirements and user interactions.

  - Design & Implementation: Building the game logic, graphics, and sound systems.

  - Validation: Constant debugging and playtesting to identify collision or scoring issues.

  - Evolution: Refining player movement (W/S keys) and adding immersive elements (BGM) based on previous version performance.

3. Sprint Cycles & Milestones

| Sprint | Date | Focus | Key Deliverables / Activities |
| --- | --- | --- | --- |
| Sprint 1: Core Engine | 15/03 - 23/03 | Fundamental Mechanics | - Project setup & Environment configuration- Player movement & Shooting mechanics- Enemy AI system & Collision detection |
| Sprint 2: Alpha Release | 24/03 - 25/03 | Stability & First Demo | - Integrated testing & bug fixing- Release Demo Version v0.1 (Core Gameplay) |
| Sprint 3: Enhancement | 30/03 - 01/04 | User Experience (UX) | - Added GUI & Shooting sound effects- Refined Player Movement (W/S keys)- Release Demo Version v0.2 |
| Final Sprint: Polish | 02/04 | Final Delivery | - Integrated BGM & In-game music- Final bug squashing- Release Demo Version v0.3 |


4. Coping with Change
In accordance with Agile principles, we embraced changes during the process. For instance, the transition from v0.1 to v0.2 involved re-evaluating the player controls and adding GUI feedback, ensuring the software evolved to meet a higher quality standard as defined in our validation phase.



### Members:

## Roles & Responsibilities & Portion

| Name           | Role                                      | Responsibilities                                                                                                   | Portion (%)   |
|:---------------|:------------------------------------------|:-------------------------------------------------------------------------------------------------------------------|:--------------|
| LAM CHON HIN | Lead Software Architect & Project Manager | Project initialization, software evolution (Focus/Health Mode), core logic implementation, and release management. | 20%           |
| KOU CHON HANG       | Backend Developer & Graphics Integration  | Bug fixing, environment configuration (VS Code), enemy sprite integration, and audio management (Game Over).       | 20%           |
| LAM CHEOK IN      | GUI & Audio Engineer                      | User Interface (GUI) design, background music synchronization, and sound effect implementation.                    | 20%           |
| LENG WAI IP       | Technical Writer & Algorithm Designer     | Documentation (README.md), algorithm specification, and software declarations.                                     | 20%           |
| LAI U HIN       | Visual Designer & Media Producer          | Player asset creation, visual implementation in VS Code, and demo video production for validation.                 | 20%  


### Schedule
(Top to Bottom)
- 15/3/2026: Project setup  
- 20/3/2026: Player movement  
- 21/3/2026: Enemy system  
- 22/3/2026: Shooting system  
- 23/3/2026: Collision and scoring  
- 24/3/2026: Testing and debugging  
- 25/3/2026: Packaging and release demo verison-v0.1
- 30/3/2026 Added shooting sound, GUI, player movement(W/S) 
- 1/4/2026: Release demo-verison-v0.2
- 2/4/2026: Added background music and ingame music, fix some bugs, release demo-verison-v0.3
- 3/4/2026: Added Elite Emeny airplane and shooting bullet
- 11/4/2026 Managing the structure of the code
- 12/4/2026 Create a icon of the game, and added new sound effect, gameover bgm, release demo-verison-v0.4
- 13/4/2026 Added icon, and release demo-verison-v0.5
- 14/4/2026 Added Focus Mode and update Emeny system, added health system
- 15/4/2026 Release demo-verison-v0.6 (beta verison)
  
### Algorithm
Finite State Machine (FSM)
This program uses a finite state machine algorithm to manage the entire game flow and separate different game logics.

Core States
-menu: Main menu interface
-game: In-game playing logic
-pause: Paused state
-game_over: Game over interface
How it works
-The game uses current_state to control which logic runs.
-Different states have independent input handling, updates, and rendering.
-It prevents messy code and decouples menu, gameplay, pause, and game-over systems.
  
Key code
if state["current_state"] == "menu":
    # run main menu
elif state["current_state"] == "game":
    # run game logic
elif state["current_state"] == "pause":
    # show pause menu
elif state["current_state"] == "game_over":
    # show game over interface
    
Core value: 
-Decouples logic across different game stages
-It separates menu, gameplay, pause, and game-over logic so they do not interfere with each other, making the code cleaner, more stable, and easier to maintain.

Cooldown / Timer Algorithm
This program uses cooldown and timer algorithms to control shooting frequency and prevent unlimited firing, ensuring game balance.
Key Implementations
1.Player shooting cooldown (frame counting)
- Check if player can shoot
def can_shoot(self):
    return self.cooldown == 0  

-Shoot and set cooldown
def shoot(self):
    self.cooldown = 12  # Lock shooting for 12 frames
    return Bullet(...)  

- Update cooldown every frame
if self.cooldown > 0:
    self.cooldown -= 1
    
2.Elite enemy shooting (timestamp method)

def shoot(self, now_ms):
    - Check if enough time has passed since last shot
    if now_ms - self.last_shot_time >= ELITE_ENEMY_SHOOT_DELAY_MS:
        self.last_shot_time = now_ms  # Reset timer
        return EliteBullet(...)
Core Value
-Stabilizes firing rate and avoids overly fast shooting.
-Improves game balance and difficulty control.

Object Pool / List Management Algorithm

This program uses list-based object management to handle the lifecycle of bullets, enemies, and elite bullets.
It dynamically updates, checks, and removes objects to keep the game efficient and stable.
Key Code 

- Manage bullets: update and remove off-screen bullets
for bullet in state["bullets"][:]:
    bullet.update()
    if bullet.rect.bottom < 0:
        state["bullets"].remove(bullet)

- Manage enemies: update and remove off-screen enemies
for enemy in state["enemies"][:]:
    enemy.update()
    if enemy.rect.top > HEIGHT:
        state["enemies"].remove(enemy)

- Manage elite bullets: update and remove invalid ones
for eb in state["elite_bullets"][:]:
    eb.update()
    if eb.rect.top > HEIGHT:
        state["elite_bullets"].remove(eb)
Core Value
-Maintains object lifecycle safely
-Prevents memory waste
-Avoids errors when deleting objects during iteration
-Decouples object logic and keeps the game efficient

### Current Status
The Shooting Plane Game is currently in a demo version (v0.6) beta verison.

As of April 15, 2026, the project has successfully reached Demo Version v0.6 (beta verison). Following the Agile iterative process, we have transitioned from a basic prototype to a feature-rich pilot version. The current status includes:
- **Core Mechanics:** Fully functional player movement (including W/S keys), shooting system, and a dynamic enemy system featuring both standard and newly added Elite Enemy airplanes with their own projectile logic.
- **Gameplay Systems:** Integration of a Health System and a specialized Focus Mode to enhance player experience and tactical depth.
- **Multimedia & UI:** Implementation of a complete GUI, customized game icons, and a layered audio system (Background Music, In-game SFX, and Game Over BGM).
- **Code Quality:** Conducted significant Code Restructuring (Refactoring) on April 11 to improve maintainability and scalability, ensuring the architecture can support further incremental updates as per Agile principles.
- **Stability:** Basic collision detection and scoring logic are verified, with initial debugging phases completed to ensure a playable demo experience.


  
### Future Plan
In alignment with the Incremental Delivery strategy outlined in our software process, the following features and improvements are planned for upcoming sprints:
- **Iteration 7** (Level & Difficulty Scaling): Implementation of a stage-based system where enemy spawn rates and speed increase over time to provide a progressive challenge.
- **Iteration 8** (Power-up System): Introduction of collectible items (e.g., triple-shot, shields, or health kits) to add variety to the core gameplay loop.
- **Iteration 9** (Boss Encounter): Development of a "Boss" enemy with complex attack patterns and higher health points to serve as a milestone for each level.
- **User Feedback Integration:** As an Agile project, we plan to conduct user testing sessions to gather feedback on the "Focus Mode" and "Elite Enemy" balance, which will inform the requirements for version v1.0.

## Demo (YoutubeURL)


## Environments of the software development and running
### Development Environment:
- Programming Language: Python 3.11+
- Game Framework: Pygame 2.5+
- IDE Recommended: VS Code (Visual Studio Code)
- Language: Python 3.11

### Minimum Hardware Requirements:
- **CPU:** Dual-core processor (2.0 GHz or higher)  
- **RAM:** 2 GB  
- **GPU:** Integrated graphics (OpenGL support)  
- **Storage:** At least 200 MB free space  
- **Display:** 1280x720 resolution
  
### Minimum Software Requirements:
- **Operating System:** Windows 10
- **Python:** Version 3.11  
- **Pygame:** Version 2.5.2 or later  
- **Editor:** Visual Studio Code (recommended)


## Declaration

- BGM: https://opengameart.org/content/magic-space by CodeManu
- INGAME BGM: https://youtu.be/mRN_T6JkH-c?si=0t8uFVJOn-cOpBqP 
- SOUND EFFECTS: laser-https://opengameart.org/content/laser-fire by dklon 
- GAMEOVER BGM: https://www.youtube.com/watch?v=Fy0gYzKIv1g&list=RDFy0gYzKIv1g&start_radio=1

1. Core Dependencies (External Packages)
Library/Package	Purpose	License	Source
Python	Programming language runtime	PSF License	https://www.python.org/
Pygame	Game engine (graphics, input, audio)	LGPL-2.1	https://www.pygame.org/
PyInstaller	Build executable (optional)	GPL-2.0	https://pyinstaller.org/

2. Python Standard Libraries (Built-in)
These libraries are part of the official Python distribution and not developed by our team:
-sys
-math
-random
-ctypes
-pathlib

4. Game Assets (Images & Sounds)
All image and audio resources are third‑party open‑source / royalty‑free assets (CC0 / CC BY) and not created by our team:
-Player plane image
-Enemy aircraft images
-Game icons
-Shooting sound effects
-Explosion sound effects
-Background music (menu & in-game)

5. Copyright & Ownership
-Custom game logic code (all .py files): Developed and owned by our team.
-Third-party frameworks & assets: Used under their respective open‑source licenses.
-No part of this project violates any open‑source license terms.
