"""
1. 画出棋盘
2. 鼠标左键落黑子
3. 鼠标右键落白子
4. 当状态栏显示黑方回合时，白方无法落子，反之亦然
5. 判断鼠标点击处是否已存在棋子，如果存在拒绝落子
6. 增加后台的信息反馈
7. 增加控制面板
8. 棋盘增加判断棋局是否已经开始的方法
9. 棋盘增加下棋记录和悔棋的方法
10. 重构控制面板的按钮设置方法
"""

from tkinter import (
    Tk,
    Canvas,
    Frame,
    Button,
    Label,
    StringVar
)
from pathlib import Path

class ChessBoard(Canvas):
    def __init__(self, root):
        super().__init__(root)
        self.side_len = 480
        # 棋盘横向或纵向的线条数
        self.line_count = 15
        # 棋盘网格边长
        self.mesh_side_len = int(self.side_len / (self.line_count + 1))
        # # 初始化落子记录
        # self.records = Records()
        # 初始设置
        self.setup()
        # 事件绑定
        self.event_bind()

    @property
    def is_started(self):
        """
        判断棋局是否已经开始
        """
        return len(self.find_all()) > 35


    def setup(self):
        # 清空画布
        self.delete('all')
        # 清空记录
        self.records = Records()
        self.config(
            width=self.side_len, 
            height=self.side_len,
            background='burlywood'
        )
        self.draw_mesh()
        # 游戏开始第一回合为黑方回合
        self.black_round = True
        print('黑方回合开始')
    
    def event_bind(self):
        self.bind('<Button-1>', self.move_black)
        self.bind('<Button-3>', self.move_white)

    def move_black(self, event):
        """黑方落子"""
        if not self.black_round:
            return None
        if self.draw_pieces_by_xy(event.x, event.y, 'black'):
            self.black_round = False
            print('黑方回合结束，白方回合开始')
        

    def move_white(self, event):
        """
        白方落子
        """
        if self.black_round:
            return None
        if self.draw_pieces_by_xy(event.x, event.y, 'white'):
            self.black_round = True
            print('白方回合结束，黑方回合开始')

    def draw_mesh(self):
        sl = self.side_len
        msl = self.mesh_side_len
        for c in range(msl, sl, msl):
            # 画纵向的线
            self.create_line(c, msl, c, sl - msl)
            # 画横向的线
            self.create_line(msl, c, sl - msl, c)
        # 画标志点
        for i, j in [(4, 4), (12, 4), (8, 8), (4, 12), (12, 12)]:
            self.draw_sign(i * msl, j * msl)

    def draw_sign(self, x, y):
        # 画棋盘中的某个固定标志点，即以(x, y)为圆心画一个实心小圆
        # 半径为3
        r = 3
        return self.create_oval(x - r, y - r, x + r, y + r, fill='black')  

    def draw_pieces_by_cr(self, column, row, color):
        """
        基于列标各行标画棋子
        """
        # 画棋子，半径为12
        r = 12
        if column is None or column < 0 or column >= self.line_count:
            return None
        if row is None or row < 0 or row >= self.line_count:
            return None 
        x = self.cr_to_xy(column)
        y = self.cr_to_xy(row)
        # 根据棋子的标签来确定当前位置是否存在棋子
        shapes = self.find_withtag('(%s,%s)' % (column, row))
        if len(shapes) != 0:
            print('列%s行%s处的棋子已存在！' % (column, row))
            return None
        # 添加落子记录
        self.records.append(column, row, color)
        return self.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill=color,
            tags='(%s,%s)' % (column, row)
        )
    
    def draw_pieces_by_xy(self, x, y, color):
        """
        基于坐标画棋子
        """
        column = self.xy_to_cr(x)
        row = self.xy_to_cr(y)
        return self.draw_pieces_by_cr(column, row, color)

    def cr_to_xy(self, c_or_r):
        """列标或行标转为坐标"""
        return (c_or_r + 1) * self.mesh_side_len
    
    def xy_to_cr(self, x_or_y):
        """坐标转为列标或行标"""
        c_or_r = x_or_y / self.mesh_side_len - 1
        if c_or_r < 0:
            return None
        integer_part = int(c_or_r)
        decimal_part = c_or_r - integer_part
        if decimal_part < 0.3:
            return integer_part
        elif decimal_part > 0.7:
            return integer_part + 1
        return None
    
    def undo(self):
        """
        悔棋功能，即删除最后一条记录的同时删除记录标签对应的棋子
        """
        tags = self.records.pop()
        if tags:
            self.delete('(%s,%s)' % tags[:-1])
    
    def save(self):
        """
        保存落子记录
        """
        if len(self.records.steps) > 0:
            self.records.save()
            print('保存落子记录...')
        else:
            print('棋盘无棋子')
    
    def resuming(self):
        """
        复盘
        """
        steps = self.records.read()
        for step in steps:
            self.draw_pieces_by_cr(*step)
        # 判断复盘后棋局的先手方
        if step[2] == 'black':
            self.black_round = False
        else:
            self.black_round = True

       
class ShowCoordsMixIn:
    def show(self, event):
        print(event.x, event.y)
    
    def init_mixin(self):
        self.bind('<Button-1>', self.show)


class ControlPanel(Frame, ShowCoordsMixIn):
    def __init__(self, root, aco):
        super().__init__(root)
        super().init_mixin()
        # aco(access-control object)即访问控制对象
        self.aco = aco
        # 显示回合的文本
        self.str_round = StringVar()
        self.font_1 = ('黑体', 20, 'bold')
        self.setup()

    def setup(self):
        self.config(
            width=480,
            height=120,
            background='burlywood'
        )
        self.set_widget()
    
    def set_widget(self):
        # 重新开始按钮
        self.b_restart = self.new_button('重新开始', self.aco.setup, 200, 5)
        # 悔棋按钮
        self.b_undo = self.new_button('悔棋', self.aco.undo, 10, 10)
        # 保存记录按钮
        self.b_save = self.new_button('保存', self.aco.save, 400, 10)
        # 复盘记录按钮
        self.b_resuming = self.new_button('复盘', self.aco.resuming, 400, 50)
        # 回合状态标签
        self.l_status = Label(
            self, 
            textvariable=self.str_round,
            font=self.font_1,
            background='#CDC0B0'
        )
        self.l_status.place(x=180, y=50, width=130, height=30)
    
    def new_button(self, text, command, x, y):
        button = Button(
            self,
            text=text,
            background='#CDC0B0',
            command=command
        )
        button.place(x=x, y=y)
        return button


class Records:
    def __init__(self):
        self.steps = []
        self.work_dir = Path(__file__).parent
        self.file = self.work_dir / 'records.txt'
    
    def append(self, column, row, color):
        self.steps.append((column, row, color))

    def pop(self):
        if len(self.steps) > 0:
            return self.steps.pop()
        return None

    def save(self):
        print(self.steps)
        with open(self.file, 'w') as f:
            for step in self.steps:
                f.write('%s,%s,%s\n' % step)
    
    def read(self):
        """
        读取记录，并返回一个记录的列表
        并不会改变 self.steps，
        因为所有的记录都是由chess_board的draw_pieces_by_cr功能添加的
        """
        steps = []
        with open(self.file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            t = line[:-1].split(',')
            t = (int(t[0]), int(t[1]), t[2])
            steps.append(t)
        return steps


root = Tk()
root.title('五子棋')
root.geometry('480x600+100+10')
root.resizable(False, False)

chess_board = ChessBoard(root)
chess_board.pack()
control_panel = ControlPanel(root, chess_board)
control_panel.pack()


def run():
    # 回合状态显示
    if chess_board.black_round:
        control_panel.str_round.set('黑方回合')
    else:
        control_panel.str_round.set('白方回合')
    # 开始按钮状态控制
    if chess_board.is_started:
        control_panel.b_restart.config(state='normal')
        control_panel.b_resuming.config(state='disabled')
    else:
        control_panel.b_restart.config(state='disabled')
        control_panel.b_resuming.config(state='normal')
    # 悔棋按钮状态控制
    if len(chess_board.records.steps) > 0:
        control_panel.b_undo.config(state='normal')
    else:
        control_panel.b_undo.config(state='disabled')
    root.after(100, run)

run()
root.mainloop()
