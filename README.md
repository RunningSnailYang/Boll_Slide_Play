# Boll_Slide_Play
This is a mini-game written by python
## Prerequisite
* python2.7

## Python dependencies

```
pip install pygame
```
## Run the game
```
python Play.py
```
## Generate stand-alone executables
### Introduction
By generating executables, you can distribute the bundle as a folder or file to other people, and they can execute your program. To your users, the app is self-contained. They do not need to install any particular version of Python or any modules. They do not need to have Python installed at all.
### Prerequisite
* pyinstaller

It should be noticed that pyinstaller v4 is not suitable for python2.7, so we can install version 3.5 as instead.
```
pip install pyinstaller==3.5
```

### Generate stand-alone executables
```
pyinstaller Play.py \
--add-data 'assets/sprites/title.png:assets/sprites' \ 
--add-data 'assets/sprites/Boll1.png:assets/sprites' \
--add-data 'assets/sprites/platform11.png:assets/sprites' \
--add-data 'assets/sprites/platform21.png:assets/sprites' \
--add-data 'assets/sprites/stab1.png:assets/sprites' \
--add-data 'assets/sprites/up.png:assets/sprites' \
--add-data 'assets/sprites/down.png:assets/sprites' \
--add-data 'assets/sprites/background1.jpg:assets/sprites'
```