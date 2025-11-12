import pygame
import sys
import math
import Gomoku1

class Ai:
    def __init__(self,ai_player, difficult):
        self.ai_player = ai_player
        self.score_table = {
            "five": 100000,      # 五连
            "live_four": 10000,  # 活四
            "sleep_four": 1000,  # 冲四
            "live_three": 1000,  # 活三
            "sleep_three": 100,  # 眠三
            "live_two": 100,     # 活二
            "sleep_two": 10,     # 眠二
            "one": 1            # 单子
        }

        self.difficult = difficult

    def Ai_easy(self,who,available_points,mark_points):
        if who == self.ai_player:

