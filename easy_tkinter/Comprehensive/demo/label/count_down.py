from tkinter import (
    Tk, 
    Label, 
    Button, 
    IntVar, 
    Entry,
    Frame
)

class NumLabel(Label):
    def __init__(self, master):
        super().__init__(master)
        self.int_var = IntVar()
        self.int_var.set(100)
        self.setup()
        
    def setup(self):
        self.config(
            textvariable=self.int_var,
            font=('Times', 40, 'bold'),
            bg='beige',
            fg='royalblue'
        )
    
    def place(self, x, y):
        super().place(x=x, y=y, width=210, height=100)
    

class ButtonA(Button):
    def __init__(self, master, text, cmd):
        super().__init__(master)
        self.text = text
        self.cmd = cmd
        self.setup()
        
    def setup(self):
        self.config(
            text=self.text,
            bg='beige',
            fg='royalblue',
            command=self.cmd
        )

    def place(self, x, y):
        super().place(x=x, y=y, width=60, height=30)


class MainFrame(Frame):
    title = 'Count Down'
    def __init__(self, master):
        super().__init__(master)
        # 是否开始倒计时
        self.is_on = False
        self.setup()
        self.set_widget()
        self.run()
        
    def setup(self):
        self.config(
            width=350,
            height=200
        )
    
    def set_widget(self):
        self.l_num = NumLabel(self)
        self.l_num.place(70, 20)
        self.b_start = ButtonA(self, '开始', self.start)
        self.b_start.place(30, 140)
        self.b_pause = ButtonA(self, '暂停', self.pause)
        self.b_pause.place(110, 140)
        # 输入秒数的输入框
        self.e_num = Entry(self)
        self.e_num.place(x=260, y=140, width=60, height=30)

    def start(self):
        self.is_on = True
        num = self.e_num.get()
        self.e_num.delete(0, 'end')
        if num.isdigit():
            self.l_num.int_var.set(num)
    
    def pause(self):
        self.is_on = False

    def run(self):
        if self.is_on:
            num = int(self.l_num.int_var.get())
            if num > 0:
                num -= 1
                self.l_num.int_var.set(num)
        self.after(1000, self.run)


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
