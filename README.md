# alien_force

A 2D action game developed in Python as part of a CSI-22 (Object-Oriented
Programming) project. The game places you at the heart of a military base
under attack following the crash of an alien spaceship. Defend the base
against endless waves of alien invaders in a survival challenge where every
second counts!

---

## Authors

**COMP 27 - Group 1**

- Ângelo de Carvalho Nunes
- Arthur Rocha e Silva
- Artur Dantas Ferreira da Silva
- Gabriel Padilha Leonardo Ferreira
- Guilherme Eiji Moriya

Course: CSI-22 - Object-Oriented Programming  
Professor: Karla D. Fook  
Instituto Tecnológico de Aeronáutica

---

## Requirements

- **Python:** Version 3.11 or higher
- **Libraries:** All the necessary libraries are listed in the
  `requirements.txt` file, available in the project root.
- **Platform:** Compatible with Windows and Linux

---

## How to Run

1. **Clone the Repository:**
    ```bash
    git clone <REPOSITORY_LINK>

2. **Navigate to the project directory:**
    ```bash
   cd alien_force

3. **Install the dependencies:**
    ```bash
   pip3 install -r requirements.txt

4. **Run the Game:**
    ```bash
   export PYTHONPATH=$(pwd)
   python3 src/main.py

---

## Game Review

### Gameplay

#### Objective

Survive as long as possible against continuously increasing waves of alien
enemies. Not only does the number of enemies increase, but their speed also
increases over time.

#### Game mechanics

- Navigate a 2D battlefield using the keyboard.
- Aim with the mouse; the left button fires the primary weapon, while the
  right button activates a special ability.
- Multiple playable characters are available—each with unique weapons and
  abilities.

### Controls

#### Movement

- A: Move left
- D: Move right
- W: Jump

#### Attacks

- Mouse aim: Control the shot direction
- Left Mouse Button: Fire primary weapon
- Right Mouse Button: Fire special ability

#### Menu:

- ESC: Open pause menu
- Menu Navigation: Use the mouse to select menu options

### Playable characters

#### Captain "Cyborg" Kane

- Primary Weapon: Assault rifle with rapid-fire capabilities.

- Special Ability: Plasma accelerator cannon that fires a devastating laser.

- Actions: Run, jump, shoot.

#### Sergeant Jones

- Primary Weapon: Grenade launcher causing area damage (with slower reload).

- Special Ability: Missile Barrage that fires multiple projectiles at once.

- Actions: Run, jump, shoot.

#### Lieutenant Rain

- Primary Weapon: Sniper rifle with slow reload for high damage.

- Special Ability: Survival Mode boosts movement and reload speeds
  temporarily.

- Actions: Run, jump, shoot.

---

## Code Documentation

### Development Documentation

During the development of the game, best practices related to version control
were followed. Thus, for every new feature, a new branch has been created
and, once the feature had been finalized and tested, a Pull Request was opened
and reviewed by another developer. To document the development process, we
added a description to all the Pull Requests, enabling anyone to
view the development details as a timeline by accessing the Pull Requests
tab on GitHub.

In addition, the code has been fully documented using the Python docstring
conventions.

### Code conventions

#### Commit Patterns

The commit message should be structured as follows:

    <type>[optional scope]: <description>

The scope communicates the intent of your modifications. The possible scopes
are:

- `feat`: Adds or removes a feature
- `fix`: Bug fixes
- `refactor`: Code restructuring without changing behavior
    - `perf`: Refactor that improves performance
- `style`: Code style changes (formatting, whitespace, etc.)
- `test`: Adding or correcting tests
- `docs`: Documentation-only changes
- `build`: Changes to build tools, CI, dependencies
- `ops`: Changes related to infrastructure, deployment, recovery
- `chore`: Miscellaneous tasks (e.g., `.gitignore` changes)

#### Code Style

<summary>Click to view code style guidelines</summary>

The project follows a consistent code style to ensure readability and ease of
collaboration. The main conventions are:

- **Encoding:** all files must use **UTF-8**.
- **Maximum line length:** limit lines to **78 characters**.
- **Imports:** always placed at the top of each file.
- **Docstrings:** every function must include a clear and descriptive
  docstring.

To assist with formatting, the repository includes a `code_style.xml` file,
available in the `config` folder. It can be imported into compatible IDEs (
e.g., PyCharm, or VSCode with proper extensions) to apply **automatic
formatting** according to the project's
standards.

#### Naming conventions

| Element                          | Convention             | Example                   |
|----------------------------------|------------------------|---------------------------|
| Classes                          | `CamelCase`            | `PlayerCharacter`         |
| Variables and functions          | `snake_case`           | `update_score()`          |
| Constants and enums              | `SCREAMING_SNAKE_CASE` | `MAX_SPEED = 10`          |
| Directories and non-source files | `snake_case`           | `assets/`, `game_config/` |
| Source files                     | Same as class name     | `PlayerCharacter.py`      |

---

## Credits

- Special Thanks: To Professor Karla D. Fook and the team members for their
  guidance and collaboration.
