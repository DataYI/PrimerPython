from tkinter import Tk, Frame, Label, StringVar
from datetime import datetime


class TimeLabel(Label):
    def __init__(self, root, x, y, w=80, h=110):
        super().__init__(root)
        self.text = StringVar()
        self.setup()
        self.place(x=x, y=y, width=w, height=h)
    
    def setup(self):
        self.config(
            textvariable=self.text,
            font=('Times', 40, 'bold'), 
            bg='black', 
            fg='green'
        )
        

class ColonLabel(Label):
    def __init__(self, root, x, y, w=10, h=110):
        super().__init__(root)
        self.setup()
        self.place(x=x, y=y, width=w, height=h)
    
    def setup(self):
        self.config(
            text=':',
            font=('Times', 40, 'bold'), 
            bg='black', 
            fg='green'
        )


class MainFrame(Frame):
    # Frame无title属性，这里的设置方便其它程序的调用
    title = 'Digital Clock'
    def __init__(self, root):
        super().__init__(root)
        self.setup()
        self.set_widget()
        self.update_time()
    
    def setup(self):
        self.config(
            width=350,
            height=200,
            bg='black'
        )
    
    def set_widget(self):
        self.label_h = TimeLabel(self, 40, 30)
        self.label_m = TimeLabel(self, 130, 30)
        self.label_s = TimeLabel(self, 220, 30)
        self.label_colon_1 = ColonLabel(self, 120, 30)
        self.label_colon_1 = ColonLabel(self, 210, 30)
    
    def update_time(self):
        today = datetime.today()
        self.label_h.text.set(str(today.hour).zfill(2))
        self.label_m.text.set(str(today.minute).zfill(2))
        self.label_s.text.set(str(today.second).zfill(2))
        self.after(500, self.update_time)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.set_widget()
        self.setup()
   
    def setup(self):
        w = self.frame.cget('width')
        h = self.frame.cget('height')
        self.title(self.frame.title)
        self.geometry('%sx%s+100+100' % (w, h))
    
    def set_widget(self):
        self.frame = MainFrame(self)
        self.frame.place(x=0, y=0)


if __name__ == '__main__':
    app = App()
    app.mainloop()
