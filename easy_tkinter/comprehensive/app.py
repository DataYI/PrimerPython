from tkinter import Tk, Menu, Toplevel
from demo.label import digital_clock, count_down

class Display(Toplevel):
    def __init__(self, root, frame_class):
        super().__init__(root)
        self.frame = frame_class(self)
        self.setup()

    def setup(self):
        self.config(
            width=self.frame.cget('width'),
            height=self.frame.cget('height'),
        )
        self.frame.place(x=0, y=0)
        # 从frame中取出title来设置toplevel的title
        self.title(self.frame.title)


class MenuBar(Menu):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setup()
        self.layout()
    
    def setup(self):
        self.config(

        )

    def layout(self):
        self.sm_label = self.create_sm_label(
            [digital_clock.MainFrame,
            count_down.MainFrame]
        )
        self.add_cascade(label='Label', menu=self.sm_label)


    def create_sm_label(self, frame_classes):
        """
        sm表示submenu，创建label子菜单
        """
        sm = Menu(self, tearoff=0)
        def get_func(frame_class):
            return lambda : Display(self.root, frame_class)
        if not isinstance(frame_classes, list):
            frame_classes = [frame_classes]
        for frame_class in frame_classes:
            func = get_func(frame_class)
            sm.add_command(
                label=frame_class.title, 
                command=func,
                font=('times', 12)
            )
        return sm


class App(Tk):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.title('comprehensive')
        self.geometry('300x400+100+100')
        self.set_widget()
    
    def set_widget(self):
        menubar = MenuBar(self)
        self.config(menu=menubar)


if __name__ == '__main__':
    app = App()
    # d = Display(app, MainFrame)
    app.mainloop()