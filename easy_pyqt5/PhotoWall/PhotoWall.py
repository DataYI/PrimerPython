from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
import sys
from itertools import cycle
from pathlib import Path
from typing import Union, List, Tuple


FIVE = [
    (0, 0), (0, 1), (0, 2), (0, 3),
    (1, 0), 
    (2, 0), 
    (3, 0), (3, 1), (3, 2), (3, 3), 
    (4, 3), 
    (5, 3), 
    (6, 0), (6, 1), (6, 2), (6, 3)
]
TWO = [
    (0, 0), (0, 1), (0, 2), (0, 3),
    (1, 3), 
    (2, 3), 
    (3, 0), (3, 1), (3, 2), (3, 3), 
    (4, 0), 
    (5, 0), 
    (6, 0), (6, 1), (6, 2), (6, 3)
]
ZERO= [
    (0, 0), (0, 1), (0, 2), (0, 3),
    (1, 0), (1, 3),
    (2, 0), (2, 3),
    (3, 0), (3, 3),
    (4, 0), (4, 3),
    (5, 0), (5, 3),
    (6, 0), (6, 1), (6, 2), (6, 3)
]


class ImagePath:
    def __init__(self, path: Union[Path, str]):
        if isinstance(path, str):
            path = Path(path)
        self.image_paths = cycle(path.iterdir())

    def next(self):
        return next(self.image_paths)


class ImageLabel(QLabel):
    _signal = pyqtSignal(str)
    def __init__(self, master: QWidget, image_path: str):
        super().__init__(master)
        self.setStyleSheet('border-style:solid;border-color:rgb(0,0,0);border-width:1px;')
        self.image_path = image_path
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(50, 50)
        self.setPixmap(pixmap)
        self.installEventFilter(self)
    
    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            # 发送鼠标所在位置的图片路径信号
            self._signal.emit(object.image_path)
            return True
        elif event.type() == QEvent.Leave:
            return True
        return False
    

class DigitWidget(QWidget):
    image_paths = ImagePath('images')
    _signal = pyqtSignal(str)
    def __init__(self, digit: str):
        super().__init__()
        self.glayout = QGridLayout()
        self.glayout.setHorizontalSpacing(1)
        self.glayout.setVerticalSpacing(1)
        self.setLayout(self.glayout)
        digit_pos = DigitPos.get(digit)
        self.layout(digit_pos)
    
    def layout(self, digit_pos: List[Tuple[int, int]]):
        '''
        随机选择图片组合数字组件
        '''
        for pos in digit_pos:
            img_path = self.image_paths.next()
            label = ImageLabel(self, str(img_path))
            # 图片标签发送的图片路径信号绑定到数字组件的信号上
            label._signal.connect(self._signal)
            self.glayout.addWidget(label, *pos)


class DigitPos:
    pos_dict = {
        '5': FIVE,
        '2': TWO,
        '0': ZERO
    }
    @staticmethod
    def get(digit: str, offset=(0, 0)):
        digit_pos = DigitPos.pos_dict[digit]
        r_o, c_o = offset
        pos_offset = [(r + r_o, c + c_o) for r, c in digit_pos]
        return pos_offset


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('520')
        self.setWindowIcon(QIcon('logo.png'))
        # 窗口布局，水平布局
        self.wlayout = QHBoxLayout()
        self.setLayout(self.wlayout)
        # 添加字符组件520
        self.add_digits('520')
        # 添加大图显示标签
        self.top_label = QLabel(self)
        self.top_label.setAlignment(Qt.AlignCenter)
        self.wlayout.addWidget(self.top_label)
    
    def add_digits(self, text: str):
        '''
        在窗口布局中添加字符组件
        '''
        for c in text:
            digit = DigitWidget(c)
            digit._signal.connect(self.set_hover_label)
            self.wlayout.addWidget(digit)

    def set_hover_label(self, image_path: str):
        '''
        根据图片路径改变大图显示标签中的图片
        '''
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(200, 200)
        self.top_label.setPixmap(pixmap)
        self.top_label.raise_()
        self.top_label.show()
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())