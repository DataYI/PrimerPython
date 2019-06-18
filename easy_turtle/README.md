# easy_turtle

## turtle.cfg
* 说明
    配置文件，放在当前运行脚本的同一路径下，用来设置screen和turtle，详情见[官网](https://docs.python.org/3.3/library/turtle.html?highlight=turtle#how-to-configure-screen-and-turtles)
    
## turtle_assist.py
* 说明
    一些辅助功能，帮助使用turtle
* 方法
    1. `grid`
        增加背景网格
        ```py
        import turtle as t
        from turtle_assist import Assist

        screen = t.Screen()
        assist = Assist(screen)
        assist.grid()
        assist.printpos(True)

        t1 = t.Turtle()
        t.done()
        ```
    2. `printpos`
        开启/关闭打印坐标的功能，如果为True，鼠标点击screen时，会在命令行输出点击位置的坐标
        ```py
        assist.printpos(True)
        ```