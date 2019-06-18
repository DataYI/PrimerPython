"""
一个辅助turtle画图的类
grid 增加网格背景
printpos 鼠标点击screen时，打印出鼠标点击的位置坐标
"""
import turtle


class Assist(turtle.Turtle):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
    
    def mygoto(self, x, y):
        self.up()
        self.goto(x, y)
        self.down()

    def grid(self):
        self.screen.tracer(0, 0)
        self.hideturtle()
        self.pencolor('#DCDCDC')
        self.setheading(-90)
        for x in range(-610, 620, 100):
            self.mygoto(x, 460)
            self.goto(x, -460)

        self.setheading(0)
        for y in range(-460, 470, 100):
            self.mygoto(-610, y)
            self.goto(610, y)

        self.screen.tracer(None, None)

    def __print(self, x, y):
        print(x, y)
        
    def printpos(self, on=True):
        if on:
            self.screen.onscreenclick(self.__print)   
        else:
            self.screen.onscreenclick(None)
        self.screen.listen()

if __name__ == '__main__':
    screen = turtle.Screen()
    assist = Assist(screen)
    assist.printpos()
    t = turtle.Turtle()
    turtle.done()
