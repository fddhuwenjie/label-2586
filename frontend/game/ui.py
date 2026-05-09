# -*- coding: utf-8 -*-
"""
游戏UI组件
包含文本框、选项框、输入框等UI元素
"""

import pygame
from game.config import (
    COLOR_BLACK, COLOR_WHITE, COLOR_GRAY, COLOR_LIGHT_GRAY, COLOR_DARK_GRAY,
    TEXT_BOX_PADDING, OPTION_BOX_HEIGHT, OPTION_BOX_MARGIN,
    INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT
)


class TextBox:
    """文本显示框"""
    
    def __init__(self, x, y, width, height, font):
        """
        初始化文本框
        
        Args:
            x: 左上角x坐标
            y: 左上角y坐标
            width: 宽度
            height: 高度
            font: 字体对象
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.border_color = COLOR_WHITE
        self.bg_color = COLOR_BLACK
        self.text_color = COLOR_WHITE
    
    def set_text(self, text):
        """设置显示文本"""
        self.text = text
    
    def draw(self, screen):
        """绘制文本框"""
        # 绘制背景
        pygame.draw.rect(screen, self.bg_color, self.rect)
        # 绘制边框
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
        # 绘制文本（支持换行）
        lines = self.text.split('\n')
        y_offset = TEXT_BOX_PADDING
        for line in lines:
            if y_offset + self.font.get_height() > self.rect.height - TEXT_BOX_PADDING:
                break
            text_surface = self.font.render(line, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + TEXT_BOX_PADDING, self.rect.y + y_offset))
            y_offset += self.font.get_height() + 5


class OptionBox:
    """选项按钮框"""
    
    def __init__(self, x, y, width, height, font, text="", option_data=None):
        """
        初始化选项框
        
        Args:
            x: 左上角x坐标
            y: 左上角y坐标
            width: 宽度
            height: 高度
            font: 字体对象
            text: 选项文字
            option_data: 选项数据（包含next或ending）
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = text
        self.option_data = option_data
        self.is_hovered = False
        self.border_color = COLOR_WHITE
        self.bg_color = COLOR_BLACK
        self.hover_bg_color = COLOR_DARK_GRAY
        self.text_color = COLOR_WHITE
    
    def update(self, mouse_pos):
        """更新悬停状态"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos, mouse_pressed):
        """检查是否被点击"""
        return self.rect.collidepoint(mouse_pos) and mouse_pressed
    
    def draw(self, screen):
        """绘制选项框"""
        # 根据悬停状态选择背景色
        bg = self.hover_bg_color if self.is_hovered else self.bg_color
        pygame.draw.rect(screen, bg, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
        # 绘制文本（居中）
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class InputBox:
    """文本输入框"""
    
    def __init__(self, x, y, width, height, font):
        """
        初始化输入框
        
        Args:
            x: 左上角x坐标
            y: 左上角y坐标
            width: 宽度
            height: 高度
            font: 字体对象
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        self.border_color = COLOR_WHITE
        self.bg_color = COLOR_BLACK
        self.text_color = COLOR_WHITE
        self.max_length = 20
    
    def handle_event(self, event):
        """
        处理输入事件
        
        Args:
            event: Pygame事件
            
        Returns:
            bool: 如果按下回车返回True
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # 只接受可打印字符
                if len(self.text) < self.max_length and event.unicode.isprintable():
                    self.text += event.unicode
        return False
    
    def update(self, dt):
        """更新光标闪烁"""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # 每500ms切换
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw(self, screen):
        """绘制输入框"""
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
        
        # 绘制文本
        display_text = self.text
        if self.active and self.cursor_visible:
            display_text += "|"
        
        text_surface = self.font.render(display_text, True, self.text_color)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        screen.blit(text_surface, text_rect)
    
    def get_text(self):
        """获取输入的文本"""
        return self.text.strip()
