# 🎮 Dungeon Escape – by Efran457

Welcome to my Python + Pygame project! 🚀  
This is a tile-based dungeon game where you collect keys 🔑, avoid enemies 👾, and reach the door 🚪 to win!

> *info: __ONLY__ works with python and pygame!
For more infos __Scrol Down__*

---

## 🧠 About The Game

- 🧍 Player movement with WASD / Arrow Keys  
- 🔑 Collect all keys to unlock the door  
- 👾 Smart enemies that chase the player  
- 🚪 Win by reaching the door after collecting all keys  
- 💀 Game over if an enemy catches you  
- 📦 JSON-based level system  
- 📷 Camera movement system  


---

## 🚀 How To Run

### *if on windows check __[DungeonRPG - Releases](https://github.com/Efran457/DungeonRPG-python/releases)__ the __exe__ schould be there*

### Step 0 - *installing the RPG*

vvv Download at Zip here vvv 

[![Download](https://img.shields.io/badge/Download-ZIP-blue?style=for-the-badge&logo=github)](https://github.com/Efran457/DungeonRPG-python/archive/refs/heads/main.zip)

*then unzip it*
### Step 1 - *installing Python*🤓
Install python *(>3.10)* from [python.org - Downloads](https://www.python.org/downloads/)

to check if installed run this comand in the Comand Promt/Powershell
```bash
python --version
```
or if that does not work
```bash
python3 --version
```

### Step 2 - *installing pygame*🎮
Open the Comand Promt/Powershell and type
```bash
pip install pygame
```
Wait for installation

### Last Step's - Run/Play the Game👾
*Multiple Comand are needed here* 
- ```bash
    cd Path/to/DungeonRPG-Folder/
- ```bash
    python dungeon.py
    ```
    if it fails run:
  ```bash
    python3 dungeon.py
#### Now have Fun playing😊

---

## 🛠 Built With

- 🐍 Python
- 🎮 Pygame
- 📄 JSON (for level data)

---

## 🎮 Controls

| Key | Action |
|------|--------|
| W / ↑ | Move Up |
| S / ↓ | Move Down |
| A / ← | Move Left |
| D / → | Move Right |
| R | Restart After Game Over |
| Enter | Next Level |

---

## 📂 Project Structure
> ⚠️ Structure may change in future
```
assets/
├── images/
│   ├── door.png
│   ├── enemy.png
│   ├── floor_tile1.png
│   ├── icon.png
│   ├── key.png
│   ├── player.png
│   ├── wall.png
│   └── ...
├── levels/
│   ├── All Levels in JSON.json
│   ├── lvl1.json
│   ├── lvl2.json
│   └── ...
├── font/
│   └── A Custom Pixel Font.ttf
├── dungeon.py       ← main entry point
└── README.md        ← you are here
```

## Credits
- font by NF Pixel *[NFPixel font - Github](https://github.com/sgigou/NF-Pixels)*
- Game made by me *(Efran457)*