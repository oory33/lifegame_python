import tkinter as tk
import math
import copy
from tkinter.constants import TRUE
import numpy as np

# rootクラスの設定（ウィンドウの設定）


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Life Game")
        self.root.resizable(width=True, height=True)
        self.root.geometry("720x800")

    def run(self):
        self.root.mainloop()

# Frameクラスの設定


class Frame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        # インスタンス変数の設定
        self.toggle = False  # マウスのクリックを受け取ったかどうか
        self.running = False  # ループを実行しているかどうか
        self.state = True  # !=self.runningと同義

        # キャンバス（実際に描画されるエリア）の設定
        self.canvassize = 720
        self.rowcells = 19
        self.fps = 12
        self.milisec = int(1000 / self.fps)

        self.width = self.canvassize / self.rowcells
        self.canvas = tk.Canvas(
            self, width=self.canvassize, heigh=self.canvassize, bg="#bcd7ff")
        self.canvas.grid()

        # 初期状態の設定
        self.galaxyinit = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        self.inil = np.random.randint(0, 2, (self.rowcells ** 2))

        self.cell = copy.copy(self.inil)

        # ボタンを配置
        self.b = tk.Button(self, text="Start Game",
                           font=("", 14), command=self.start)
        self.b.grid(row=1, column=0)
        self.b = tk.Button(self, text="Restart Game",
                           font=("", 14), command=self.restart)
        self.b.grid(row=1, column=1)
        self.b = tk.Button(self, text="Galaxy", font=(
            "", 14), command=self.galaxy)
        self.b.grid(row=1, column=2)

        # クリックした時にself.click関数を読む
        self.canvas.bind('<Button-1>', self.click)

    # 盤面の描画
    def draw(self):
        self.canvas.delete("all")  # 盤面の初期化
        m = 0
        w = self.width
        if self.toggle:
            x = self.mouseposition[0]
            y = self.mouseposition[1]
            i = self.xytoIndex(x, y)  # マウスの座標から通し番を取得
            self.cell[i] = not self.cell[i]
            self.toggle = False
        if self.running or self.state:
            for i in self.cell:
                p = self.Indextoxy(m)  # 通し番号からセルの座標（枚数）を取得
                x = p[0] * w
                y = p[1] * w  # 座標系を枚数からピクセルへ変換
                if i == 1:
                    self.canvas.create_rectangle(
                        x, y, x + w, y + w, fill="#2d5bff")
                    self.canvas.grid(columnspan=3)  # セルが生存なら描画
                m = m + 1
        if self.running:  # ループが実行中なら次世代を計算し再度描画
            self.next()
        self.after(self.milisec, self.draw)

    # 次の世代の作成
    def next(self):
        self.state = False
        q = 0
        self.newcell = copy.copy(self.cell)  # 次世代用に盤面をコピー
        for u in self.cell:
            p = self.Indextoxy(q)
            # 通し番号から枚数座標に変換し周囲の生きているセルの数を取得
            live = self.livesaround(p[0], p[1])
            if u == 1:  # セルが生きている場合
                if live == 2 or live == 3:  # 周囲に2つか3つ生きたセルがあれば残存
                    self.newcell[q] = 1
                elif not live == 2 or live == 3:
                    self.newcell[q] = 0
            elif u == 0:  # セルが死んでいる場合
                if live == 3:  # 周囲に3つ生きたセルがあれば誕生
                    self.newcell[q] = 1
                elif live != 3:
                    self.newcell[q] = 0
            q += 1
        if self.toggle:  # マウスがクリックされた時の処理
            x = self.mouseposition[0]
            y = self.mouseposition[1]
            i = self.xytoIndex(x, y)  # マウスの座標から通し番を取得
            self.newcell[i] = 1
            self.toggle = False
        self.cell = copy.copy(self.newcell)  # 次世代を反映

    def livesaround(self, x, y):  # 周囲の生きたセルをカウントする関数
        a = x - 1
        L = 0
        while a <= x+1:
            b = y - 1
            while b <= y+1:
                i = self.xytoIndex(a, b)
                if self.cell[i] == 1 and i != -1:  # セルが生存しかつ、通し番が盤面の中ならカウント
                    L += 1
                b += 1
            a += 1
        this = self.xytoIndex(x, y)
        t = self.cell[this]
        if t == 1:
            L = L - 1  # そのセル自身が生きていれば引く
        return L

    def xytoIndex(self, x, y):
        w = self.rowcells
        if x < 0 or x >= w or y < 0 or y >= w:
            return -1
        else:
            return y * w + x

    def Indextoxy(self, i):
        x = i % self.rowcells
        y = math.floor(i / self.rowcells)
        return [x, y]

    def click(self, event):
        x = int(event.x)
        y = int(event.y)
        x = math.floor(x / self.width)
        y = math.floor(y / self.width)
        self.toggle = True
        self.mouseposition = [x, y]

    def restart(self):
        self.running = False
        self.state = True
        self.cell = copy.copy(self.inil)

    def start(self):
        self.running = True

    def galaxy(self):
        self.running = False
        self.state = True
        self.cell = copy.copy(self.galaxyinit)


app = App()
f = Frame()
f.draw()
app.run()
