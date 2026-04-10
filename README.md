# Shooting Plane Game --- COMP2116 Final Project
Shooting Plane Game is a simple 2D arcade-style shooting game developed in Python.
Players control a fighter plane, shoot down enemies, and try to achieve the highest score while avoiding collisions.


# 1. Graphical Abstract





# 2. Project Purpose
### Development Methodology:
This project follows an Agile development process.

### Why Agile?
Agile was chosen over the Waterfall model because it allows for incremental development and continuous improvement.

During the development of the Shooting Plane Game, features were implemented step by step (e.g., player movement, enemies, shooting system), and each component was tested immediately after completion. This made it easier to:

- Identify and fix bugs early
- Adjust game mechanics quickly
- Improve gameplay based on testing

Compared to Waterfall, which requires all requirements to be defined upfront, Agile provides more flexibility, which is suitable for game development where ideas often evolve during the process.

### Target Market / Usage:

The Shooting Plane Game is designed for:
- Casual players who enjoy simple arcade-style games
- Students and beginners learning game development concepts
- Anyone looking for a lightweight and easy-to-play shooting game

The game can be used for:
- Entertainment and casual gaming
- Educational purposes (learning basic game mechanics and programming)
- Demonstration of fundamental game development techniques



# 3. Project Development Plan

### Development Process:
### Software Development Process (Agile Methodology)
Our team adopted the Agile Development methodology to develop the "Shooting Plane Game." Following the principles outlined in the COMP2116 course materials, we prioritized iterative development, rapid prototyping, and continuous refinement to ensure the software evolved based on testing and validation.

1. Agile Framework: Iterative & Incremental
Instead of a rigid linear process, we organized our development into three focused Sprints. This allowed us to maintain a "Minimum Viable Product" (v0.1) and progressively add features (Audio, GUI) through software evolution.

2. Software Process Activities within Sprints
In each iteration, we integrated the four core activities:

- Specification: Defining gameplay requirements and user interactions.

- Design & Implementation: Building the game logic, graphics, and sound systems.

- Validation: Constant debugging and playtesting to identify collision or scoring issues.

- Evolution: Refining player movement (W/S keys) and adding immersive elements (BGM) based on previous version performance.

# Project Documentation

  ------------------------------------------------------------------------------------
  Sprint        Date      Focus         Key Deliverables / Activities
  ------------- --------- ------------- ----------------------------------------------
  Sprint 1:     15/03 -   Fundamental   \- Project setup & Environment configuration-
  Core Engine   23/03     Mechanics     Player movement & Shooting mechanics- Enemy AI
                                        system & Collision detection

  Sprint 2:     24/03 -   Stability &   \- Integrated testing & bug fixing- Release
  Alpha Release 25/03     First Demo    Demo Version v0.1 (Core Gameplay)

  Sprint 3:     30/03 -   User          \- Added GUI & Shooting sound effects- Refined
  Enhancement   01/04     Experience    Player Movement (W/S keys)- Release Demo
                          (UX)          Version v0.2

  Final Sprint: 02/04     Final         \- Integrated BGM & In-game music- Final bug
  Polish                  Delivery      squashing- Release Demo Version v0.3 (Final)
  ------------------------------------------------------------------------------------

4. Coping with Change
In accordance with Agile principles, we embraced changes during the process. For instance, the transition from v0.1 to v0.2 involved re-evaluating the player controls and adding GUI feedback, ensuring the software evolved to meet a higher quality standard as defined in our validation phase.



### Members:

| Role | Member Name | Member Student ID | Responsibilities	|
|----------|----------|----------|----------|


### Schedule:
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

### Algorithm:
Algorithms Used to Optimize Games
1.Spatial partitioning algorithms (Quadtree, Octree, BVH)
  Reduce unnecessary rendering, collision checks, and physics calculations by organizing game objects spatially.
2.Frustum culling
  Skips drawing objects outside the camera view to improve FPS and GPU performance.
3.LOD (Level of Detail)
  Uses lower-polygon models and simpler textures for distant objects to lower rendering cost.
4.A pathfinding & NavMesh*
  Optimize NPC and enemy movement; NavMesh precomputes walkable areas for faster AI navigation.
5.FSMs & Behavior Trees
  Structure AI logic efficiently, making NPC behavior predictable and CPU-friendly.
6.Collision optimization algorithms (GJK, EPA, Sweep and Prune)
  Speed up physics detection and reduce unnecessary physical computations.
7. Object pooling
  Reuses game objects instead of frequent creation/destruction, reducing memory overhead and lag.

### Current Status:

The Shooting Plane Game is currently in a demo version (v0.3).

✅ Completed Features:
- Player-controlled airplane with left/right movement
- Enemy airplane system
- Shooting (bullet) functionality
- Score tracking system
- Collision detection (game over on impact)
- Restart functionality (press R to restart) 
- Player movement (W/S/A/D)
- Shooting sound (bullet)
- Menu (GUI)
- Background Music
- Ingame Music

### Future Plan:
- Enhanced enemy behaviors and difficulty scaling (TBD)
- Improved graphics and visual effects (TBD)
- Background music (Added)
- User interface enhancements (menus, HUD) (Added)
- Performance optimization and bug fixes (TBD)
- Setting round (Boss) (TBD)
- Improve shooting system (TBD)

## Demo (YoutubeURL): 


## Environments of the software development and running:


## Declaration:
### Tools Used: 
- Language: Python 3.11
- Library: Pygame
- Documentation: Markdown (README.md)

