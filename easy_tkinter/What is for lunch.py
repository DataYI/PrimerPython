from tkinter import (
    Tk, 
    Label, 
    Button,
    StringVar
)
import random
import itertools

root = Tk()
root.title('中午吃什么')
root.geometry('210x190')
root.resizable(False, False)

flag = False
font = ('宋体', 10)


def run():
    global flag
    if flag:
        flag = False
        label_2.config(font=('宋体', 20, 'bold'), fg='blue')
        button_run.config(text='开始', fg='green')
    else:
        flag = True
        label_2.config(font=font, fg='black')
        button_run.config(text='停止', fg='red')


button_run = Button(root, text='开始', font=('宋体', 16, 'bold'), fg='green', command=run)
button_run.place(x=60, y=10, width=80, height=30)

str_1 = StringVar()
label_1 = Label(root, textvariable=str_1, font=font)
label_1.place(x=40, y=50, width=120, height=30)
str_2 = StringVar()
label_2 = Label(root, textvariable=str_2, font=font)
label_2.place(x=40, y=85, width=120, height=30)
str_3 = StringVar()
label_3 = Label(root, textvariable=str_3, font=font)
label_3.place(x=40, y=120, width=120, height=30)

food = ['木桶饭', '土豆粉', '重庆小面', '麻辣烫', '砂锅粥', '自助快餐', '百包铺']
shuffle_food = food[:]
# 随机打乱food顺序
random.shuffle(shuffle_food)
# 无限循环生成器
shuffle_food = itertools.cycle(shuffle_food)


def roll():
    if flag:
        new_candidate = next(shuffle_food)
        str_1.set(str_2.get())
        str_2.set(str_3.get())
        str_3.set(new_candidate)
    root.after(200, roll)
    

roll()
root.mainloop()