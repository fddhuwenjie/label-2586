# -*- coding: utf-8 -*-
"""
文字冒险游戏 - 主程序入口
基于 Pygame 的黑白文本框风格文字冒险游戏
"""

import pygame
import sys
from game.engine import GameEngine
from game.config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE


def main():
    """游戏主函数"""
    # 初始化 Pygame
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    
    # 创建游戏窗口
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # 创建游戏引擎并运行
    engine = GameEngine(screen)
    engine.run()
    
    # 退出游戏
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
