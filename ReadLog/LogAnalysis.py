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
       self.colorlist = ['black','red','blue','ivory2','gold2','light cyan']
       self.backgroundcolor = self.colorlist[3]
       self.textcolor = self.colorlist[0]
       self.root = tk.Tk()
       self.root.title(u"Log解析")
       self.root.geometry("1000x820")
       self.root.resizable(width=False, height=False)
       self.root.configure(bg=self.backgroundcolor)

    def MainGUI(self):
        # ログ表示ウインドウ
        self.ShowLogWindowModule()
        
        # ログファイル選択ボタン
        self.SelectLogFileModule() 

        # 計測開始stepと計測終了stepの表示
        self.ShowSelectStepModule()
        
        # 経過時間算出
        self.CalcElapsedTimeModule()

        # 選択コマンド間の経過時間をすべて算出
        self.SelectAndCalcElapsedTimeAllModule()
        
        # csv出力
        self.SaveFileModule()

        # ×ボタン押すと終了
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
        self.Frame1.configure(bg=self.backgroundcolor)

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
        self.Frame2.configure(bg=self.backgroundcolor)

        # ボタン1:ログファイル選択
        self.Button1 = tk.Button(self.Frame2, text=u'Logファイル選択', width=130, relief='raised')
        self.Button1.bind("<Button-1>",self.SelectLogFile)
        self.Button1.pack(side='top', fill='x')

    def ShowSelectStepModule(self):
        # フレームの作成
        self.Frame3 = tk.Frame(self.root, width=900, height=80, relief = tk.SUNKEN, bd=0)
        self.Frame3.pack(side='top', fill='x', pady=10)
        self.Frame3.configure(bg=self.backgroundcolor)
        
        # ラベル1
        FontStyle1 = tkFont.Font(family="Lucida Grande", size=12)
        self.Static1 = tk.Label(self.Frame3, text=u'開始STEP', font=FontStyle1, width=20, fg=self.textcolor)
        self.Static1.configure(bg=self.backgroundcolor)
        self.Static1.pack(side='left')
        
        # ボックス1
        self.EditBox1 = tk.Entry(self.Frame3, width=130)
        self.EditBox1.pack()

        # フレームの作成
        self.Frame3_5 = tk.Frame(self.root, width=900, height=80, relief = tk.SUNKEN, bd=0)
        self.Frame3_5.pack(side='top', fill='x')
        self.Frame3_5.configure(bg=self.backgroundcolor)

        # ラベル2
        FontStyle2 = tkFont.Font(family="Lucida Grande", size=12)
        self.Static2 = tk.Label(self.Frame3_5, text=u'終了STEP', font=FontStyle2, width=20, fg=self.textcolor)
        self.Static2.configure(bg=self.backgroundcolor)
        self.Static2.pack(side='left')
        # ボックス2
        self.EditBox2 = tk.Entry(self.Frame3_5, width=130)
        self.EditBox2.pack()

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
            tk.messagebox.showinfo('Warning!','.logまたは.txtファイルを選択して下さい')
            return "break"
        else:
            try:
                # ログファイル表示を削除
                self.Listbox.delete(0,len(self.lines))
                # 選択済ステップを削除
                self.EditBox1.delete(0, tk.END)
                self.EditBox2.delete(0, tk.END)
                # 一括算出表示を削除
                self.Listbox2.delete(0, len(self.lines))
                self.Listbox3.delete(0, len(self.lines))
                self.Listbox4.delete(0, len(self.lines))
                self.EditBox4.delete(0, tk.END)
                # 選択済みインデックスを削除
                self.startIdx = []
                self.endIdx = []
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
            self.lines[i] = '['+str(i)+'] '+self.lines[i]
            self.Listbox.insert(END,self.lines[i])

    def CalcElapsedTimeModule(self):
        # フレームの作成
        self.Frame4 = tk.Frame(self.root, width=900, height=80, relief = tk.SUNKEN, bd=0)
        self.Frame4.pack(side='top', fill='x', pady=15)
        self.Frame4.configure(bg=self.backgroundcolor)

        # ボタン2:計算開始
        FontStyle3 = tkFont.Font(family="Lucida Grande", size=10)
        self.Button2 = tk.Button(self.Frame4, text=u'経過時間算出', font=FontStyle3, width=20, relief='raised')
        self.Button2.bind("<Button-1>",self.CalcStart)
        self.Button2.pack(side='left', padx=17)
        # ボックス3
        self.EditBox3 = tk.Entry(self.Frame4, width=130)
        self.EditBox3.pack(padx=0)

    def CalcStart(self,event):
        str_start = self.EditBox1.get();
        str_end   = self.EditBox2.get();
        try:
            idx1 = int(str_start.find('] ')) + 2 #2021の先頭の位置の位置分スライドさせる
            t_start = dt.datetime(int(str_start[idx1+0:idx1+4]), int(str_start[idx1+5:idx1+7]),\
                                  int(str_start[idx1+7:idx1+9]), int(str_start[idx1+10:idx1+12]),\
                                  int(str_start[idx1+13:idx1+15]), int(str_start[idx1+16:idx1+18]),\
                                  int(str_start[idx1+19:idx1+22]+'000'))
        except:
            tk.messagebox.showinfo('Warning!','開始STEPが間違っています')
            self.EditBox3.delete(0, tk.END)
            return "break"
        try:
            idx2 = int(str_end.find('] ')) + 2 #2021の先頭の位置分スライドさせる
            t_end   = dt.datetime(int(str_end[idx2+0:idx2+4]), int(str_end[idx2+5:idx2+7]),\
                                  int(str_end[idx2+7:idx2+9]), int(str_end[idx2+10:idx2+12]),\
                                  int(str_end[idx2+13:idx2+15]), int(str_end[idx2+16:idx2+18]),\
                                  int(str_end[idx2+19:idx2+22]+'000'))
        except:
            tk.messagebox.showinfo('Warning!','終了STEPが間違っています')
            self.EditBox3.delete(0, tk.END)
            return "break"

        td = t_end-t_start
        self.EditBox3.delete(0, tk.END)
        self.EditBox3.insert(0, str(td.total_seconds())+'[s]')
        
    def SelectAndCalcElapsedTimeAllModule(self):
        # 大フレーム
        self.FrameBig = tk.Frame(self.root, width=900, height=300, relief = 'groove', bd=2)
        self.FrameBig.pack(side='top', fill='x', padx=10, pady=10)
        self.FrameBig.configure(bg=self.backgroundcolor)
        
        # Frame5
        self.Frame5 = tk.Frame(self.FrameBig, width=900, height=20, relief = 'flat', bd=0)
        self.Frame5.pack(side='top', fill='x', padx=10, pady=15)
        self.Frame5.configure(bg=self.backgroundcolor)
        
        # ボタン3：一括計算開始ボタン
        FontStyle5 = tkFont.Font(family="Lucida Grande", size=10)
        self.Button3 = tk.Button(self.Frame5, text=u'実行', font=FontStyle5, width=20, relief='raised')
        self.Button3.bind("<Button-1>",self.CalcElapsedTimeAll)
        self.Button3.grid(row=0, column=0, padx=50)

        # 開始コマンド選択
        barlabel1 = ['PathPlan START', 'CAPUTURE START', 'python START']
        self.v = tk.StringVar()
        self.Combobox1 = ttk.Combobox(self.Frame5, textvariable=self.v, values=barlabel1, width=20)
        self.Combobox1.bind(
            '<<ComboboxSelected>>', 
            self.ShowStartStep)
        self.Combobox1.grid(row=0, column=1)

        # ラベル3
        FontStyle3 = tkFont.Font(family="Lucida Grande", size=12)
        self.Static3 = tk.Label(self.Frame5, text=u'から', font=FontStyle3, width=10, fg=self.textcolor)
        self.Static3.configure(bg=self.backgroundcolor)
        self.Static3.grid(row=0, column=2)

        # 終了コマンド選択
        barlabel2 = ['PathPlan END', 'CAPUTURE END', 'python END']
        self.v = tk.StringVar()
        self.Combobox2 = ttk.Combobox(self.Frame5, textvariable=self.v, values=barlabel2, width=20)
        self.Combobox2.bind(
            '<<ComboboxSelected>>', 
            self.ShowEndStep)
        self.Combobox2.grid(row=0, column=3)

        # ラベル4
        FontStyle4 = tkFont.Font(family="Lucida Grande", size=12)
        self.Static4 = tk.Label(self.Frame5, text=u'までの経過時間を一括算出', font=FontStyle4, width=30, fg=self.textcolor)
        self.Static4.configure(bg=self.backgroundcolor)
        self.Static4.grid(row=0, column=4)

        ###############################################################################################
        # Frame6
        self.Frame6 = tk.Frame(self.FrameBig, width=900, height=200, relief = 'flat', bd=0)
        self.Frame6.pack(side='top', fill='x', padx=10, pady=10)
        self.Frame6.configure(bg=self.backgroundcolor)

        # Listボックスとスクロールバー:検索結果表示用(start)
        self.lists_init = tk.StringVar(value=[])
        # Listボックスの作成
        self.Listbox2 = tk.Listbox(self.Frame6, listvariable=self.lists_init, height=10, width=55)
        # スクロールバーの作成
        scrollbar2 = tk.Scrollbar(self.Frame6, orient=tk.VERTICAL, command=self.Listbox2.yview)
        # スクロールバーをListboxに反映
        self.Listbox2["yscrollcommand"] = scrollbar2.set
        # 各種ウィジェットの設置
        self.Listbox2.grid(row=1, column=0, columnspan=3, pady=0)
        scrollbar2.grid(row=1, column=3, pady=0, sticky=(tk.N, tk.S))

        # Listボックスとスクロールバー:検索結果表示用(end)
        self.lists_init = tk.StringVar(value=[])
        # Listボックスの作成
        self.Listbox3 = tk.Listbox(self.Frame6, listvariable=self.lists_init, height=10, width=55)
        # スクロールバーの作成
        scrollbar3 = tk.Scrollbar(self.Frame6, orient=tk.VERTICAL, command=self.Listbox3.yview)
        # スクロールバーをListboxに反映
        self.Listbox3["yscrollcommand"] = scrollbar3.set
        # 各種ウィジェットの設置
        self.Listbox3.grid(row=1, column=4, columnspan=3, pady=0)
        scrollbar3.grid(row=1, column=7, pady=0, sticky=(tk.N, tk.S))

        # Listボックスとスクロールバー:計算結果表示用
        self.lists_init = tk.StringVar(value=[])
        # Listボックスの作成
        self.Listbox4 = tk.Listbox(self.Frame6, listvariable=self.lists_init, height=10, width=38)
        # スクロールバーの作成
        scrollbar4 = tk.Scrollbar(self.Frame6, orient=tk.VERTICAL, command=self.Listbox4.yview)
        # スクロールバーをListboxに反映
        self.Listbox4["yscrollcommand"] = scrollbar4.set
        # 各種ウィジェットの設置
        self.Listbox4.grid(row=1, column=8, pady=0)
        scrollbar4.grid(row=1, column=9, pady=0, sticky=(tk.N, tk.S))

        # ListボックスにSTEP削除機能を追加
        # 右クリックメニュー->計測開始・終了STEPを選択
        self.popup_menu2 = tk.Menu(self.Listbox2, tearoff=0)
        self.popup_menu2.add_command(label="STEPを削除",
                                    command=self.DeleteStep1)
        self.popup_menu3 = tk.Menu(self.Listbox3, tearoff=0)
        self.popup_menu3.add_command(label="STEPを削除",
                                    command=self.DeleteStep2)
        self.Listbox2.bind("<Button-3>", self.Popup2) 
        self.Listbox3.bind("<Button-3>", self.Popup3) 

        # 平均値算出
        # Frame7
        self.Frame7 = tk.Frame(self.FrameBig, width=900, height=50, relief = 'flat', bd=0)
        self.Frame7.pack(side='top', fill='x', padx=10, pady=10)
        self.Frame7.configure(bg=self.backgroundcolor)
        # ボックス4
        self.EditBox4 = tk.Entry(self.Frame7, width=30)
        self.EditBox4.pack(side='right', padx=20)
        # ラベル5
        FontStyle5 = tkFont.Font(family="Lucida Grande", size=12)
        self.Static5 = tk.Label(self.Frame7, text=u'平均値', font=FontStyle5, width=10)
        self.Static5.configure(bg=self.backgroundcolor)
        self.Static5.pack(side='right')

    def DeleteStep1(self):
        if tk.messagebox.askokcancel("Information", "選択STEPを削除しますか?"):
            try:
                delIdx = self.Listbox2.curselection()[0]
                self.Listbox2.delete(delIdx);
                del self.startIdx[delIdx]
            except:
                tk.messagebox.showinfo('Warning!','削除に失敗しました')

    def DeleteStep2(self):
        if tk.messagebox.askokcancel("Information", "選択STEPを削除しますか?"):
            try:
                delIdx = self.Listbox3.curselection()[0]
                self.Listbox3.delete(delIdx);
                del self.endIdx[delIdx]
            except:
                tk.messagebox.showinfo('Warning!','削除に失敗しました')

    def Popup2(self, event):
        try:
            self.popup_menu2.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu2.grab_release()

    def Popup3(self, event):
        try:
            self.popup_menu3.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu3.grab_release()

    def CalcElapsedTimeAll(self, event):
        self.Listbox4.delete(0, tk.END)
        self.EditBox4.delete(0, tk.END)
        self.elapsedTimeAll = []
        try:
            for i in range(min(len(self.startIdx),len(self.endIdx))):
                str_start = self.lines[self.startIdx[i]];
                str_end   = self.lines[self.endIdx[i]];
                idx1 = int(str_start.find('] ')) + 2 #2021の先頭の位置分スライドさせる
                t_start = dt.datetime(int(str_start[idx1+0:idx1+4]), int(str_start[idx1+5:idx1+7]),\
                                    int(str_start[idx1+7:idx1+9]), int(str_start[idx1+10:idx1+12]),\
                                    int(str_start[idx1+13:idx1+15]), int(str_start[idx1+16:idx1+18]),\
                                    int(str_start[idx1+19:idx1+22]+'000'))
                idx2 = int(str_end.find('] ')) + 2 #2021の先頭の位置分スライドさせる
                t_end   = dt.datetime(int(str_end[idx2+0:idx2+4]), int(str_end[idx2+5:idx2+7]),\
                                    int(str_end[idx2+7:idx2+9]), int(str_end[idx2+10:idx2+12]),\
                                    int(str_end[idx2+13:idx2+15]), int(str_end[idx2+16:idx2+18]),\
                                    int(str_end[idx2+19:idx2+22]+'000'))
                elampsedTime = t_end - t_start
                self.elapsedTimeAll = self.elapsedTimeAll + [str(elampsedTime.total_seconds())]
                self.Listbox4.insert(0, str(elampsedTime.total_seconds())+'[s]')
        except:
            tk.messagebox.showinfo('Warning!','一括計算に失敗しました')
            self.Listbox2.delete(0, tk.END)
            self.Listbox3.delete(0, tk.END)
            self.Listbox4.delete(0, tk.END)
            return "break"
        
        # 一括計算が成功したら,平均値(小数点以下3桁)の算出
        elapsedTimeAllfloat = [float(s) for s in self.elapsedTimeAll]
        try:
            self.elapsedTimeMean = round(sum(elapsedTimeAllfloat)/len(elapsedTimeAllfloat), 3)
        except:
            return "break"
        self.EditBox4.insert(0, str(self.elapsedTimeMean)+'[s]')

    def ShowStartStep(self, event):
        self.startIdx = []
        self.Listbox2.delete(0, tk.END)
        try:
            for i in range(len(self.lines)):
                if self.Combobox1.get() in self.lines[i]: 
                    self.startIdx = self.startIdx + [i]
                    self.Listbox2.insert(END, self.lines[i])
        except:
            tk.messagebox.showinfo('Warning!','Logファイルが選択されていません')
            return "break"

    def ShowEndStep(self, event):
        self.endIdx = []
        self.Listbox3.delete(0, tk.END)
        try:
            for i in range(len(self.lines)):
                if self.Combobox2.get() in self.lines[i]: 
                    self.endIdx = self.endIdx + [i]
                    self.Listbox3.insert(END, self.lines[i])
        except:
            tk.messagebox.showinfo('Warning!','Logファイルが選択されていません')
            return "break"

    def SaveFileModule(self):
        # Frame8
        self.Frame8 = tk.Frame(self.FrameBig, width=900, height=50, relief = 'flat', bd=0)
        self.Frame8.pack(side='top', fill='x', padx=15, pady=10)
        self.Frame8.configure(bg=self.backgroundcolor)
        # ボタン4：保存ボタン
        FontStyle6 = tkFont.Font(family="Lucida Grande", size=12)
        self.Button4 = tk.Button(self.Frame8, text=u'csv出力', font=FontStyle6, width=15, relief='raised')
        self.Button4.bind("<Button-1>",self.SaveFile)
        self.Button4.pack(side='right')

    def SaveFile(self, event):
        try:
            f_type = [('csv file','*.csv'), ('text file','*.txt')]
            ret = tk.filedialog.asksaveasfile(defaultextension='csv' ,filetypes=f_type, title='名前を付けて保存')
            if ret==None:
                return "break"
            # リストの結合
            elapsedTimeList = []
            for i in range(min(len(self.startIdx),len(self.endIdx))):
                elapsedTimeList = elapsedTimeList + [self.Listbox4.get(i).replace('[s]', '')]
            # ファイルに書き込み
            with open(ret.name, 'w') as f:
                f.write(','.join(elapsedTimeList))
            return "break"
        except:
            tk.messagebox.showinfo('Warning!','算出結果の保存に失敗しました')
            return "break"

if __name__ == "__main__":
    # execute only if run as a script
    app = LogAnalysis();
    app.MainGUI();