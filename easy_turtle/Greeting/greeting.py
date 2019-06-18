import turtle as t

t.title('surprise')  # 设置标题栏文字
# t.hideturtle()  # 隐藏箭头
t.shape('turtle')
screen = t.getscreen()
screen.bgcolor('pink')  # 背景色
t.color('white', 'red')  # 设置画线颜色、填充颜色
t.pensize(2)  # 笔的大小
t.speed(2)  # 图形绘制的速度,1~10
t.up()  # 移动，不画线
t.goto(0, -180)
t.down()  # 移动，画线
t.begin_fill()  # 开始填充
#t.goto(0, -150)
t.seth(141)
t.fd(225)
t.seth(-39)
t.circle(138.98, -180)
# 画另一边
t.up()  # 移动，不画线
t.goto(0, -180)
t.down()  # 移动，画线
t.seth(39)
t.fd(225)
t.circle(138.98, 180)
t.end_fill()

t.color("black")  # 设置颜色
t.up()
t.goto(0, 300)
t.write("略略略", font=("宋体", 36, "normal"), align="center")
t.goto(200, -250)
t.write('by turtle', font=("宋体", 18, "bold"))
t.goto(220, -200)
t.seth(60)

t.done()
