import os
import tkinter as tk
from tkinter.constants import END, NW
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font as tkFont
from tkinter import ttk
import datetime as dt


class LogAnalysis:
    def __init__(self):
       self.gui_size = 0;
       self.color = 'ivory2'

    def MainGUI(self):
        self.root = tk.Tk()
        self.root.title(u"Log Analysis")
        self.root.geometry("1000x800")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg=self.color)
        
        # ログ表示ウインドウ
        self.ShowLogWindowModule()
        
        # ログファイル選択ボタン
        self.SelectLogFileModule() 

        # 計測開始stepと計測終了stepの表示
        self.ShowSelectStepModule()
        
        # 経過時間計算
        self.CalcElapsedTimeModule()

        # self.Frame2()

        # # コンボボックス1
        # self.ComboBox1()

        # # ラベル3
        # self.Label3()
        
        # ×ボタン
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def quit(self):
           self.root.destroy()
           self.root.quit()

    def on_closing(self):
        if tk.messagebox.askokcancel("Information", "アプリを終了しますか?"):
            self.quit();

    def ShowLogWindowModule(self):
        # LogWindow用フレームの作成
        self.Frame1 = tk.Frame(self.root, width=1000, height=300, relief = tk.SUNKEN, bd=0, bg='gray')
        self.Frame1.pack(side='top', fill='x')
        self.Frame1.configure(bg=self.color)

        # Listボックスとスクロールバー
        self.lists_init = tk.StringVar(value=[])
        # 各種ウィジェットの作成
        self.Listbox = tk.Listbox(self.Frame1, listvariable=self.lists_init, height=20, width=163)
        
        # スクロールバーの作成
        scrollbar = tk.Scrollbar(self.Frame1, orient=tk.VERTICAL, command=self.Listbox.yview)
        # スクロールバーをListboxに反映
        self.Listbox["yscrollcommand"] = scrollbar.set
        # 各種ウィジェットの設置
        self.Listbox.pack(side='left', fill='x')
        scrollbar.pack(side='right', fill='y')

        # 右クリックメニュー->計測開始・終了STEPを選択
        self.popup_menu = tk.Menu(self.Listbox, tearoff=0)
        self.popup_menu.add_command(label="開始STEPに設定",
                                    command=self.SelectStartStep)
        self.popup_menu.add_command(label="終了STEPに設定",
                                    command=self.SelectEndStep)
        self.Listbox.bind("<Button-3>", self.Popup) # Button-2 on Aqua

    def Popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
        
    def SelectStartStep(self):
        try:
            self.EditBox1.delete(0, tk.END)
            self.EditBox1.insert(0, self.Listbox.get(self.Listbox.curselection()[0]))
        except:
            tk.messagebox.showinfo('Warning!','STEPが選択されていません.')
    def SelectEndStep(self):
        try:
            self.EditBox2.delete(0, tk.END)
            self.EditBox2.insert(0, self.Listbox.get(self.Listbox.curselection()[0]))
        except:
            tk.messagebox.showinfo('Warning!','STEPが選択されていません.')

    def SelectLogFileModule(self):
        # LogWindow用フレームの作成
        self.Frame2 = tk.Frame(self.root, width=900, height=10, relief = tk.SUNKEN, bd=0)
        self.Frame2.pack(side='top', fill='x')
        self.Frame2.configure(bg=self.color)

        # ボタン1:ログファイル選択
        self.Button1 = tk.Button(self.Frame2, text=u'Logファイル選択', width=130, relief='raised')
        self.Button1.bind("<Button-1>",self.SelectLogFile)
        self.Button1.pack(side='top', fill='x')

    def ShowSelectStepModule(self):
        # フレームの作成
        self.Frame3 = tk.Frame(self.root, width=900, height=80, relief = tk.SUNKEN, bd=0)
        self.Frame3.pack(side='top', fill='x', pady=10)
        self.Frame3.configure(bg=self.color)
        
        # ラベル1
        FontStyle1 = tkFont.Font(family="Lucida Grande", size=12)
        self.Static1 = tk.Label(self.Frame3, text=u'開始STEP', font=FontStyle1, width=20)
        self.Static1.configure(bg=self.color)
        self.Static1.pack(side='left')
        
        # ボックス1
        self.EditBox1 = tk.Entry(self.Frame3, width=130)
        self.EditBox1.pack()

        # フレームの作成
        self.Frame3_5 = tk.Frame(self.root, width=900, height=80, relief = tk.SUNKEN, bd=0)
        self.Frame3_5.pack(side='top', fill='x')
        self.Frame3_5.configure(bg=self.color)

        # ラベル2
        FontStyle2 = tkFont.Font(family="Lucida Grande", size=12)
        self.Static2 = tk.Label(self.Frame3_5, text=u'終了STEP', font=FontStyle1, width=20)
        self.Static2.configure(bg=self.color)
        self.Static2.pack(side='left')
        # ボックス2
        self.EditBox2 = tk.Entry(self.Frame3_5, width=130)
        self.EditBox2.pack()

    def CalcElapsedTimeModule(self):
        # フレームの作成
        self.Frame4 = tk.Frame(self.root, width=900, height=80, relief = tk.SUNKEN, bd=0)
        self.Frame4.pack(side='top', fill='x', pady=15)
        self.Frame4.configure(bg=self.color)

        # ボタン2:計算開始
        FontStyle3 = tkFont.Font(family="Lucida Grande", size=10)
        self.Button2 = tk.Button(self.Frame4, text=u'経過時間計算', font=FontStyle3, width=20, relief='raised')
        self.Button2.bind("<Button-1>",self.CalcStart)
        self.Button2.pack(side='left', padx=17)
        # ボックス3
        self.EditBox3 = tk.Entry(self.Frame4, width=130)
        self.EditBox3.pack(padx=0)

    def CalcStart(self,event):
        str_start = self.EditBox1.get();
        str_end   = self.EditBox2.get();
        try:
            t_start = dt.datetime(int(str_start[0:4]), int(str_start[5:7]), int(str_start[7:9]),\
                                int(str_start[10:12]), int(str_start[13:15]), int(str_start[16:18]), int(str_start[19:22]+'000'))
        except:
            tk.messagebox.showinfo('Warning!','開始STEPが間違っています')
            self.EditBox3.delete(0, tk.END)
            return "break"
        try:
            t_end   = dt.datetime(int(str_end[0:4]), int(str_end[5:7]), int(str_end[7:9]),\
                                int(str_end[10:12]), int(str_end[13:15]), int(str_end[16:18]), int(str_end[19:22]+'000'))
        except:
            tk.messagebox.showinfo('Warning!','終了STEPが間違っています')
            self.EditBox3.delete(0, tk.END)
            return "break"

        td = t_end-t_start
        self.EditBox3.delete(0, tk.END)
        self.EditBox3.insert(0, str(td.total_seconds())+'[s]')
        
    def ComboBox1(self):
        # コンボボックス
        # Frame
        frame = ttk.Frame(self.Frame2, padding=10, width=20)
        frame.grid(row=4, column=0, padx=10, sticky=tk.W)

        # Combobox
        barlabel = ['PathPlan START', 'CAPUTURE START', 'python START']
        self.v = tk.StringVar()
        self.cb1 = ttk.Combobox(frame, textvariable=self.v, values=barlabel, width=20)
        self.cb1.set(barlabel[0])
        self.cb1.bind(
            '<<ComboboxSelected>>', 
            lambda e: print('v=%s' % self.v.get()))
        self.cb1.grid()

    def SelectLogFile(self,event):
        # ファイル選択ダイアログの表示
        root = tk.Tk()
        root.withdraw()
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.LogFileDir = tk.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

        root, ext = os.path.splitext(self.LogFileDir)

        # 処理ファイル名の出力
        if not self.LogFileDir:
            return "break"
        if ext != '.log' and ext != '.txt':
            tk.messagebox.showinfo('Warning!','.logまたは.txtを選択して下さい')
            return "break"
        else:
            try:
                # ログファイル表示を削除
                self.Listbox.delete(0,len(self.lines))
                # 選択済ステップを削除
                self.EditBox1.delete(0, tk.END)
                self.EditBox2.delete(0, tk.END)
                self.ReadLogFile()
            except:
                self.ReadLogFile()
            return "break"

    def ReadLogFile(self):
        try:
            self.LogFile = open(self.LogFileDir, 'r')
        except:
            tk.messagebox.showinfo('Warning!','Logファイル読み込みに失敗しました.')
            return
        self.lines = self.LogFile.readlines()
        for i in range(len(self.lines)):
            self.Listbox.insert(END,self.lines[i])
        