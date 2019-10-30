"""
1. Letter 类用于从文件夹中读取素材图片，并通过 ImageTk 转换为 
   tkinter 支持的格式，最终将所以素材图片存储为dict；
2. MainCanvas 类用于绘制图片和文本；
3. 通过 Letter 生成的随机字符，MainCanvas 可以从 Letter 存储
   图片的字典中取出字符图片，并在画布上创建图片对象（以字符作为
   tags），要切换切图片时，通过 tags 删除字符图片，同时重复之前
   的操作生成新的字符图片
"""

from tkinter import Tk, Canvas
from PIL import ImageTk
from pathlib import Path
import random


class Letter:
    def __init__(self):
        self.ims = {}
        self.load_im()
    
    def load_im(self):
        """
        加载本地的字母图片
        """
        p = Path(__file__).parent / 'letter'
        for f in p.iterdir():
            key = f.name[0].upper()
            f = p / f
            # 读取图片的操作必须在Tk实例化之后执行
            im = ImageTk.PhotoImage(file=f)
            self.ims[key] = im
    
    def choice(self):
        """
        随机返回A-Z中的一个字母
        """
        code = random.randint(65, 90)
        return chr(code)


class MainCanvas(Canvas):
    def __init__(self, root):
        super().__init__(root)
        self.current_char = None
        self.letter = Letter()
        self.setup()
        self.show_letter()
        self.event_bind()
    
    def setup(self):
        self.config(
            width=600,
            height=400
        )

    def event_bind(self):
        self.bind('<Key>', self.eliminate_letter)

    def show_letter(self):
        self.current_char = self.letter.choice()
        im = self.letter.ims[self.current_char]
        self.create_image(
            int(int(self.cget('width')) / 2), 
            int(int(self.cget('height')) / 2), 
            image=im, 
            tags=self.current_char
        )
    
    def eliminate_letter(self, event):
        """
        绑定键盘事件的函数，用于删除当前显示的字母图片，同时
        显示一个新的字母图片
        """
        if event.char.upper() == self.current_char:
            self.delete(self.current_char)
            self.show_letter()


root = Tk()
root.geometry('600x400+10+10')
cv = MainCanvas(root)
cv.place(x=0, y=0)
# 使cv获得焦点，否则按键时不会激活cv的键盘事件
cv.focus_set()

root.mainloop()
