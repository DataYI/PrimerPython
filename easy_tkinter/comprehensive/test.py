from tkinter import Tk, Frame, Menu


root = Tk()
root.geometry('300x300+10+10')

def hello():
    print("hello!")

frame = Frame(root, width=300, height=30, bg='red')
# frame.grid(row=3, column=0)
frame.place(x=0, y=100)

# 创建一个顶级菜单
menubar = Menu(frame)
menubar.add_command(label="Hello!", command=hello)
menubar.add_command(label="Quit!", command=root.quit)
root.config(menu=menubar)


root.mainloop()