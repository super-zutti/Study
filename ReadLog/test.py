import glob
import os
import csv





# 2018年7月1日のログから抽出
DATA_DIR = ('main_log')
# /log/20180701の配下に保存されているテキストファイルを変数「files」に入れる
files = glob.glob(os.path.join(DATA_DIR, ‘*.txt’))

 

# 「files」から１ファイルずつOpenしていく
for file in files:
with open(file) as f:
        # openしたファイルから１行ずつ読み込んでいく
lines = f.readlines()
lines_strip = [line.strip() for line in lines]

        # ログ取得時間の取得
        # 「Time source is user configuration」という文字が含まれている行を抜き出して
        # 変数「l_time」に代入する
l_time = [line for line in lines_strip if ‘Time source is user configuration’ in line]
        # 「l_time」の中に保存された１行を空白セルで区切る
        # 例）「Time source is user configuration, 00:00:00.963 UTC Sun Jul 1 2018」
time_sp = str(l_time).split(‘ ‘)
        # 空白セルで区切られた１行から6月番目だけを抽出し、「time」に代入する
time = time_sp[5::6]

        #Outputデータ量の取得
        # 「5 minute output rate」という文字が含まれている行を抜き出して
        # 変数「l_opt」に代入する
l_opt = [line for line in lines_strip if ‘5 minute output rate’ in line]
        # 「l_opt」の中に保存された１行を空白セルで区切る
        # 例）「5 minute output rate 2367 bits/sec, 21 packets/sec」
opt_sp = str(l_opt).split(‘ ‘)
        # 空白セルで区切られた１行から5月番目だけを抽出し、「opt」に代入する
opt = opt_sp[4::5]

i = 0
for tm in time:
            # 先程抽出した、変数「time」と変数「opt」を組み合わせて「table」に代入していく
            # 間に「,」を入れることでcsv化した時に列を分割させる
table = (tm, ‘,’, opt[i])
            # 日付入りのCSVファイルを作成する
            # オプションで「a」を選択することで上書きモードでオープン
f_log = open(days + ‘_log_data.csv’, ‘a’)
            # csvファイルに先程の「table」を書き込む
f_log.writelines(table)
            # 「’\n’」を入れることで改行させる
f_log.writelines(‘\n‘)
            # 次のデータに進む
i += 1
        # csvファイルを閉じる
f_log.close()