# -*- coding: utf-8 -*-
"""
游戏引擎
负责游戏主循环、状态管理和场景切换
"""

import pygame
import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('GameEngine')

from game.config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    COLOR_BLACK, COLOR_WHITE,
    FONT_SIZE_TITLE, FONT_SIZE_LARGE, FONT_SIZE_NORMAL, FONT_SIZE_SMALL,
    TEXT_BOX_MARGIN, OPTION_BOX_HEIGHT, OPTION_BOX_MARGIN,
    INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT,
    STATE_NAME_INPUT, STATE_PLAYING, STATE_GAME_OVER, STATE_VICTORY
)
from game.ui import TextBox, OptionBox, InputBox
from game.story import STORY, ENDINGS


class GameEngine:
    """游戏引擎类"""
    
    def __init__(self, screen):
        """
        初始化游戏引擎
        
        Args:
            screen: Pygame显示表面
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
        logger.info("游戏引擎初始化完成")
        
        # 初始化字体（支持中文）
        self._init_fonts()
        
        # 游戏状态
        self.state = STATE_NAME_INPUT
        self.player_name = ""
        self.current_scene = "start"
        self.empty_name_warning = False
        self.warning_timer = 0
        
        # 初始化UI组件
        self._init_ui()
    
    def _init_fonts(self):
        """初始化字体"""
        # 尝试加载系统中文字体
        font_paths = [
            # Linux
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            # macOS
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            # Windows
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
        ]
        
        font_path = None
        for path in font_paths:
            if os.path.exists(path):
                font_path = path
                break
        
        if font_path:
            logger.info(f"加载中文字体: {font_path}")
            self.font_title = pygame.font.Font(font_path, FONT_SIZE_TITLE)
            self.font_large = pygame.font.Font(font_path, FONT_SIZE_LARGE)
            self.font_normal = pygame.font.Font(font_path, FONT_SIZE_NORMAL)
            self.font_small = pygame.font.Font(font_path, FONT_SIZE_SMALL)
        else:
            # 使用默认字体（可能不支持中文）
            logger.warning("未找到中文字体，使用默认字体（可能无法正确显示中文）")
            self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
            self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
            self.font_normal = pygame.font.Font(None, FONT_SIZE_NORMAL)
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
    
    def _init_ui(self):
        """初始化UI组件"""
        # 故事文本框（留出顶部姓名区域）
        text_box_height = 180
        self.story_box = TextBox(
            TEXT_BOX_MARGIN,
            50,  # 从50开始，给姓名留空间
            WINDOW_WIDTH - TEXT_BOX_MARGIN * 2,
            text_box_height,
            self.font_normal
        )
        
        # 名字输入框
        input_x = (WINDOW_WIDTH - INPUT_BOX_WIDTH) // 2
        input_y = WINDOW_HEIGHT // 2
        self.name_input = InputBox(
            input_x, input_y,
            INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT,
            self.font_normal
        )
        
        # 选项框列表
        self.option_boxes = []
    
    def _create_option_boxes(self, options):
        """
        根据选项数据创建选项框
        
        Args:
            options: 选项列表
        """
        self.option_boxes = []
        start_y = 260  # 文本框下方开始
        box_width = WINDOW_WIDTH - TEXT_BOX_MARGIN * 2
        
        for i, option in enumerate(options):
            box = OptionBox(
                TEXT_BOX_MARGIN,
                start_y + i * (OPTION_BOX_HEIGHT + OPTION_BOX_MARGIN),
                box_width,
                OPTION_BOX_HEIGHT,
                self.font_normal,
                option["text"],
                option
            )
            self.option_boxes.append(box)
    
    def _load_scene(self, scene_id):
        """
        加载场景
        
        Args:
            scene_id: 场景ID
        """
        if scene_id not in STORY:
            logger.error(f"场景不存在: {scene_id}，回退到起始场景")
            scene_id = "start"
        
        scene = STORY[scene_id]
        # 替换玩家名字
        text = scene["text"].replace("{player}", self.player_name)
        self.story_box.set_text(text)
        self._create_option_boxes(scene["options"])
        self.current_scene = scene_id
        logger.info(f"玩家 [{self.player_name}] 进入场景: {scene_id}")
    
    def _show_ending(self, ending_type):
        """
        显示结局
        
        Args:
            ending_type: 结局类型
        """
        if ending_type not in ENDINGS:
            logger.error(f"结局类型不存在: {ending_type}，使用默认结局")
            ending_type = "neutral"
        
        logger.info(f"玩家 [{self.player_name}] 达成结局: {ending_type}")
        if True:  # 保持原有缩进结构
            ending = ENDINGS[ending_type]
            text = f"【{ending['title']}】\n\n{ending['text']}"
            text = text.replace("{player}", self.player_name)
            self.story_box.set_text(text)
            
            # 创建重新开始选项
            self.option_boxes = [
                OptionBox(
                    TEXT_BOX_MARGIN,
                    450,
                    WINDOW_WIDTH - TEXT_BOX_MARGIN * 2,
                    OPTION_BOX_HEIGHT,
                    self.font_normal,
                    "重新开始游戏",
                    {"next": "restart"}
                ),
                OptionBox(
                    TEXT_BOX_MARGIN,
                    450 + OPTION_BOX_HEIGHT + OPTION_BOX_MARGIN,
                    WINDOW_WIDTH - TEXT_BOX_MARGIN * 2,
                    OPTION_BOX_HEIGHT,
                    self.font_normal,
                    "退出游戏",
                    {"next": "quit"}
                )
            ]
            
            if ending_type in ["perfect", "victory", "good"]:
                self.state = STATE_VICTORY
            else:
                self.state = STATE_GAME_OVER
    
    def run(self):
        """游戏主循环"""
        logger.info("游戏启动")
        while self.running:
            dt = self.clock.tick(FPS)
            
            # 处理事件
            self._handle_events()
            
            # 更新
            self._update(dt)
            
            # 渲染
            self._render()
            
            pygame.display.flip()
    
    def _handle_events(self):
        """处理事件"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    mouse_clicked = True
            
            elif event.type == pygame.KEYDOWN:
                if self.state == STATE_NAME_INPUT:
                    if self.name_input.handle_event(event):
                        # 按下回车，开始游戏
                        name = self.name_input.get_text()
                        if name:
                            self.player_name = name
                            self.state = STATE_PLAYING
                            logger.info(f"玩家 [{name}] 开始游戏")
                            self._load_scene("start")
                        else:
                            # 空名字提示
                            self.empty_name_warning = True
                            self.warning_timer = 2000  # 显示2秒
                            logger.warning("玩家尝试使用空名字开始游戏")
        
        # 处理选项点击
        if mouse_clicked and self.state in [STATE_PLAYING, STATE_GAME_OVER, STATE_VICTORY]:
            for box in self.option_boxes:
                if box.is_clicked(mouse_pos, True):
                    self._handle_option_click(box.option_data)
                    break
    
    def _handle_option_click(self, option_data):
        """
        处理选项点击
        
        Args:
            option_data: 选项数据
        """
        logger.info(f"玩家 [{self.player_name}] 选择: {option_data.get('text', option_data)}")
        
        if "ending" in option_data:
            # 显示结局
            self._show_ending(option_data["ending"])
        elif "next" in option_data:
            next_scene = option_data["next"]
            if next_scene == "restart":
                # 重新开始
                self.state = STATE_NAME_INPUT
                self.name_input.text = ""
                self.current_scene = "start"
                self.option_boxes = []
            elif next_scene == "quit":
                # 退出游戏 - 回到首页
                logger.info(f"玩家 [{self.player_name}] 退出游戏")
                self.state = STATE_NAME_INPUT
                self.name_input.text = ""
                self.player_name = ""
                self.current_scene = "start"
                self.option_boxes = []
            else:
                # 加载下一个场景
                self._load_scene(next_scene)
    
    def _update(self, dt):
        """
        更新游戏状态
        
        Args:
            dt: 帧间隔时间（毫秒）
        """
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == STATE_NAME_INPUT:
            self.name_input.update(dt)
            # 更新空名字警告计时器
            if self.empty_name_warning and self.warning_timer > 0:
                self.warning_timer -= dt
                if self.warning_timer <= 0:
                    self.empty_name_warning = False
        else:
            # 更新选项框悬停状态
            for box in self.option_boxes:
                box.update(mouse_pos)
    
    def _render(self):
        """渲染画面"""
        # 清屏
        self.screen.fill(COLOR_BLACK)
        
        if self.state == STATE_NAME_INPUT:
            self._render_name_input()
        else:
            self._render_game()
    
    def _render_name_input(self):
        """渲染名字输入界面"""
        # 标题
        title = self.font_title.render("文字冒险游戏", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(title, title_rect)
        
        # 提示文字
        prompt = self.font_normal.render("请输入你的名字：", True, COLOR_WHITE)
        prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH // 2, 220))
        self.screen.blit(prompt, prompt_rect)
        
        # 输入框位置调整
        self.name_input.rect.centery = 290
        self.name_input.draw(self.screen)
        
        # 提示按回车（输入框下方留足间距）
        hint = self.font_small.render("按 Enter 键开始游戏", True, COLOR_WHITE)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, 360))
        self.screen.blit(hint, hint_rect)
        
        # 空名字警告提示（Enter提示下方）
        if self.empty_name_warning:
            warning = self.font_small.render("请输入名字后再开始游戏", True, (255, 100, 100))
            warning_rect = warning.get_rect(center=(WINDOW_WIDTH // 2, 420))
            self.screen.blit(warning, warning_rect)
    
    def _render_game(self):
        """渲染游戏界面"""
        # 玩家名字
        name_text = self.font_small.render(f"冒险者: {self.player_name}", True, COLOR_WHITE)
        self.screen.blit(name_text, (TEXT_BOX_MARGIN, 15))
        
        # 故事文本框（增加顶部间距）
        self.story_box.rect.y = 50
        self.story_box.draw(self.screen)
        
        # 选项框
        for box in self.option_boxes:
            box.draw(self.screen)
