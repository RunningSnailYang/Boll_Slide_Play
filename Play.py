#!/usr/bin/env python
import sys
from game import Boll_slide
def main():
    game_state = Boll_slide.GameState('start')
    while True:
        game_state.frame_step()

if __name__ == "__main__":
    main()
    
