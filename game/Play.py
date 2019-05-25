#!/usr/bin/env python
import pygame
import Boll_slide as game
def main():
    game_state = game.GameState()
    while True:
        game_state.frame_step()

if __name__ == "__main__":
    main()
    
