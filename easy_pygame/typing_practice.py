"""
Created on Wed Oct 30 14:24:16 2019

@author: DataAnt(董轶)
"""
from pathlib import Path
import sys
from collections import deque

import pygame
from pygame.sprite import Sprite, Group
from pygame.color import THECOLORS as COLORS
from pygame.locals import (
    QUIT,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    USEREVENT,
    K_BACKSPACE
)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
ROOT_PATH = Path(__file__).parent
FPS = 60

class Passage:
    def __init__(self, source: Path):
        self.source = source
        self.texts = []
        self.input_text = ''
        self.output_index = 3
        self.read_passage()
        # 前面几段文本累积得分
        self.previous_score = 0

    def read_passage(self):
        with open(self.source, 'r') as f:
            texts = f.readlines()
        # 去掉末尾的换行符
        texts = [t[:-1] for t in texts if t[-1] == '\n']
        self.texts = [t for t in texts if len(t) > 0]

    @property
    def output_text(self):
        return self.texts[self.output_index]

    @property
    def score(self):
        _input = self.input_text.split(' ')
        _output = self.output_text.split(' ')
        _score = self.previous_score
        for wi, wo in zip(_input, _output):
            if wi == wo:
                _score += 1
        return _score

    def is_input_over(self):
        return len(self.input_text) >= len(self.output_text)

    def update(self):
        if self.is_input_over():
            self.previous_score = self.score
            self.output_index += 1
            self.input_text = '' 
            return True
        return False


class SpeedCompute:
    def __init__(self):
        self.keydown_count = 0

    def count_add(self):
        self.keydown_count += 1

    @property
    def speed(self):
        """
        平均每分钟按键次数
        """
        t = pygame.time.get_ticks() / 1000 / 60
        return self.keydown_count / t

    @property
    def color_rgb(self):
        speed = self.speed
        # print(speed)
        # 正规化速度到0-255之间的数字
        color_value = min(int(speed / 255 * 255), 255)
        return (255 - color_value, color_value, 0)


class Display:
    def __init__(self, width, height, title):
        self.screen = pygame.display.set_mode((width, height))
        self.chars_width = {}
        pygame.display.set_caption(title)
        pygame.key.set_repeat(200)
        self.cursor_init()

    def cursor_init(self):
        # 光标位置(列， 行)
        self.cursor_cr = 0, 0
        # 光标坐标（x, y）
        self.cursor_xy = self.get_text_width('', self.fonts['1']) + 555, 5

    @property
    def fonts(self):
        _fonts = pygame.font.get_fonts()
        Font = pygame.font.Font

        def f(_id: int):
            return pygame.font.match_font(_fonts[_id])
        return {
            '1': Font(f(0), 24),
            '2': Font(f(1), 28),
            '3': Font(f(1), 18)
        }

    def show_time(self, _time: int):
        im_1 = self.fonts['2'].render('Time', True, COLORS['black'])
        im_2 = self.fonts['2'].render(str(_time), True, COLORS['black'])
        self.blit(im_1, (460, 200))
        self.blit(im_2, (480, 240))

    def show_score(self, score):
        # surface = self.screen.subsurface(rect)
        im_1 = self.fonts['2'].render('Score', True, COLORS['black'])
        im_2 = self.fonts['2'].render(str(score), True, COLORS['black'])
        self.blit(im_1, (455, 340))
        self.blit(im_2, (480, 380))
        # self.screen.blit(surface, )

    def show_passage(self, output_text, input_text):
        """显示短文，并用不同颜色标记用户输入文本的正误
        :param output_text: 程序输出的参考文本
        :parma input_text: 用户输入的文本
        :return: 
        """
        self.render_text(self.fonts['1'], 10, 10, output_text, COLORS['white'])

    def render_char(self, surface, font, x, y, char, color):
        im = font.render(char, True, color)
        surface.blit(im, (x, y))

    def blit_output_surface(self, width, height, font, o_text, color=COLORS['white']):
        surface = pygame.Surface((width, height))
        # surface.fill((0, 0, 0))
        surface.set_colorkey((0, 0, 0))
        # surface.convert_alpha()
        # surface.set_alpha(20)
        lines = self.composing(o_text, width - 20, font)
        for row, line in enumerate(lines):
            im = font.render(line, True, color)
            surface.blit(im, (0, row * 30))
        self.screen.blit(surface, (0, 0))

    def blit_input_surface(self, width, height, font, i_text, color=COLORS['white']):
        surface = self.input_surface = pygame.Surface((width, height))
        surface.set_colorkey((0, 0, 0))
        lines = self.composing(i_text, width - 20, font)
        # 方便计算光标位置时调用
        self.input_lines = lines
        for row, line in enumerate(lines):
            im = font.render(line, True, color)
            surface.blit(im, (0, row * 30))
        self.screen.blit(surface, (550, 0))

    def get_char_width(self, char, font):
        try:
            w = self.chars_width[char]
        except KeyError:
            im = font.render(char, False, (0, 0, 0))
            self.chars_width[char] = w = im.get_width()
        return w

    def get_text_width(self, text, font):
        # width = 0
        # for char in text:
        #     width += self.get_char_width(char, font)
        im = font.render(text, False, (0, 0, 0))
        width = im.get_width() + 5
        return width

    def composing(self, text: str, max_width: int, font: pygame.font.Font) -> list:
        """根据文本宽度，将文本拆分成多行，每行文本作为一个元素存入list
        :param text: 要排版的文本
        :param max_width: 每行文本的最大宽度
        :return: 储存文本的列表
        """
        width = 0
        lines = []
        while text:
            for i, char in enumerate(text):
                if width > max_width:
                    width = 0
                    if text[i: i + 1] in ('.', ',', ';', ':', ' ', '"'):
                        i += 1
                    else:
                        while text[i: i + 1].isalpha() or text[i: i + 1].isdecimal():
                            i -= 1
                        i += 1
                    lines.append(text[: i])
                    # 最后一行只有一个字符时，i=0会导致text永远为一个字符，进入死循环
                    text = text[i:] if i > 0 else ''
                    break
                width += self.get_char_width(char, font)
            else:
                # 最后一行，不满最大宽度
                lines.append(text)
                text = ''
        if len(lines) == 0:
            lines = ['']
        return lines

    def move_cursor(self, direction: str):
        lines = self.input_lines
        c, r = self.cursor_cr
        if direction == 'left':
            if c <= 0:
                r = r - 1 if r > 0 else 0
                c = len(lines[r]) - 2
            else:
                c -= 1
        elif direction == 'right':
            if c > len(lines[r]):
                r += 1
                c = 1
            else:
                c += 1
        else:
            raise Exception('不存在的方向')

        x = self.get_text_width(lines[r][: c + 1], self.fonts['1']) + 555
        y = r * 30 + 5
        self.cursor_cr = c, r
        self.cursor_xy = x, y

    def __getattr__(self, item):
        if item in ('fill', 'blit'):
            return getattr(self.screen, item)
        raise AttributeError("'Display' object has no attribute '%s'" % item)


class Cursor(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._init()
        self.image = self.ims[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame_i = 0

    def _init(self):
        im_1 = pygame.Surface((1, 21))
        im_1.fill(COLORS['white'])
        im_2 = pygame.Surface((1, 21))
        im_2.fill(COLORS['black'])
        self.ims = [im_1, im_2]

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # 造型切换
        self.frame_i += 1
        if self.frame_i >= len(self.ims):
            self.frame_i = 0
        self.image = self.ims[self.frame_i]


class RestartButton(pygame.surface.Surface):
    def __init__(self, rect: pygame.Rect, screen: pygame.surface.Surface, font: pygame.font.Font):
        self.rect = pygame.Rect(rect)
        super().__init__((self.rect.width, self.rect.height))
        self.fill(COLORS['cyan'])
        self.caption(font)
        self.screen = screen
    
    def caption(self, font: pygame.font.Font):
        im = font.render('Restart', True, COLORS['white'])
        self.blit(im, (3, 0))

    def mouse_button_down(self, func):
        button_pressed_1, _, _ = pygame.mouse.get_pressed()
        if button_pressed_1:
            x, y = pygame.mouse.get_pos()
            if all((x > self.rect.left, x < self.rect.right, y < self.rect.bottom, y > self.rect.top)):
                func()

    def update(self):
        self.screen.blit(self, (self.rect.x, self.rect.y))



class Game:
    def __init__(self, passage_source: Path):
        self._init()
        self.passage = Passage(passage_source)
        self.time = 60
        self.fps_clock = pygame.time.Clock()
        self.display = Display(SCREEN_WIDTH, SCREEN_HEIGHT, '打字练习')
        # 速度计算器实例
        self.compute = SpeedCompute()
        # 光标精灵
        self.cursor = Cursor(*self.display.cursor_xy)
        # 光标精灵组
        self.cursor_group = self.set_cursor_group()
        self.restart_button = RestartButton((460, 100, 80, 30), self.display.screen, self.display.fonts['3'])

    def restart(self):
        self.time = 60
        self.passage.previous_score = 0
        self.passage.input_text = ''
        self.passage.source = 0
        self.display = Display(SCREEN_WIDTH, SCREEN_HEIGHT, '打字练习')
        self.cursor.move(*self.display.cursor_xy)
        self.compute = SpeedCompute()

    def _init(self):
        # 初始化游戏
        pygame.init()
        # 根据打字速度更新背景颜色
        pygame.time.set_timer(USEREVENT + 1, 500)
        # 倒计时
        pygame.time.set_timer(USEREVENT + 2, 1000)

    def set_cursor_group(self):
        cursor_group = Group()
        cursor_group.add(self.cursor)
        return cursor_group

    def keydown(self, event):
        if self.time <= 0:
            return 
        if event.key == K_BACKSPACE:
            self.passage.input_text = self.passage.input_text[:-1]
            self.display.move_cursor('left')
        else:
            if len(event.unicode) > 0:
                self.passage.input_text += event.unicode
                game.display.move_cursor('right')
        
        game.cursor.move(*game.display.cursor_xy)

    def update(self):
        self.restart_button.update()
        passage = self.passage
        display = self.display
        # 绘制输出文本
        display.blit_output_surface(
            450, 600, display.fonts['1'], passage.output_text)
        # 绘制输入文本
        display.blit_input_surface(
            450, 600, display.fonts['1'], passage.input_text)
        # 绘制分数
        display.show_score(passage.score)
        # 绘制时间
        display.show_time(self.time)
        # 切换输出短文
        if passage.update() and self.time > 0:
            display.cursor_init()
            game.cursor.move(*game.display.cursor_xy)
        # 更新光标位置
        self.cursor_group.draw(display.screen)
        self.cursor_group.update()
        # 控制帧率
        self.fps_clock.tick(FPS)
        pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    # 短文实例
    passage_source = ROOT_PATH / 'passage.txt'
    game = Game(passage_source)

    # 游戏主循环
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game.quit()
            elif event.type == KEYDOWN:
                game.compute.count_add()
                game.keydown(event)
            elif event.type == MOUSEBUTTONDOWN:
                game.restart_button.mouse_button_down(game.restart)
            elif event.type == USEREVENT + 1:
                game.display.fill(game.compute.color_rgb)
                pygame.draw.rect(game.display.screen,
                                 COLORS['skyblue'], (450, 0, 100, 600))
            elif event.type == USEREVENT + 2:
                t = game.time
                game.time = t - 1 if t > 0 else t

        game.update()
