# 問題1
# # 変数 num が定義されている。num を2で割った余りが0であれば「偶数です」、
# そうでなければ「奇数です」と表示するプログラムを書きなさい。
num = 7
 
#解答
if num % 2 == 0:
    print("偶数です")
else:
    print("奇数です")
 
# 問題2
# 変数 age と has_ticket が定義されている。
# age が18以上 かつ has_ticket が True の場合にのみ「入場できます」と表示する
# プログラムを、if文を入れ子（ネスト）にして書きなさい（and演算子は使わないこと）。
age = 20
has_ticket = True
 
#解答
if age >= 18:
    if has_ticket = True:
        print("入場できます")

#正解
if age >= 18:
    if has_ticket:  # has_ticket == True と同義
        print("入場できます")
#「=」は代入。条件式の中で代入はできない。


 
# 問題3
# 変数 score（0〜100の整数）が定義されている。以下の基準で評定を判定し、
# 変数 grade に代入するプログラムを if・elif・else を使って書きなさい。
# 90点以上: 'S'　80点以上90点未満: 'A'　60点以上80点未満: 'B'　60点未満: 'C'
score = 85
 
#解答
if score >= 90:
    print('S')
elif 90 > score >= 80:
    print('A')
elif 80 > score >= 60:
    print('B')
else:
    print('C')

#正解
if score >= 90:
    grade = 'S'
elif score >= 80:
    grade = 'A'
elif score >= 60:
    grade = 'B'
else:
    grade = 'C'

print(grade)
#問題文は「変数gradeに代入する」ことを求めている
#「A」「B」に関して、直前のSのFalseの時点で90点未満が、AのFalseの時点で80点未満が確定しているため、90 > score >= 80:の90 >と80 > score >= 60:の80 >は冗長であり、不要。バグではない。

# 問題4
# 変数 num が定義されている。以下の条件を if・elif・else を使って書きなさい。
# num が0より大きければ「numは正の数です」と表示する。
# num が0より小さければ「numは負の数です。0に修正します」と表示したうえで、
#   num を 0 に修正する。
# それ以外（numが0）の場合は「numは0です」と表示する。
# 最後に num の値を表示しなさい。
# num = -3 として実行した場合、「numは0です」というメッセージは表示されるかどうか、
# 理由もあわせて考えてみましょう。
num = -3
 
#解答
if num > 0:
    print('numは正の数です')
elif num < 0:
    print('numは負の数です。0に修正します')
    num = 0
print(num)

#正解
num = -3

if num > 0:
    print('numは正の数です')
elif num < 0:
    print('numは負の数です。0に修正します')
    num = 0
else:
    print('numは0です')

print(num)
#3つ目の分岐であるelseがない。

 
# 問題5
# 変数 x（値10）と y（値3）が定義されている。del x により x を未定義にしたあと、
# 条件式 "x > 5 or y > 5" を持つ if 文を書き、条件が真であれば
# 「条件を満たしました」と表示するプログラムを書きなさい。
# このプログラムを実行するとエラーになるか、ならないか、理由も含めて考えてみましょう。
x = 10
y = 3
del x
 
#解答
if x > 5 or y > 5:
    print('条件を満たしました')
#エラーなる。x > 5という未定義のxを使った式が先に来ており、yに到達する前にxを先に処理するため、xが未定義であることに対してエラーを返して実行は終了する。
 
# 問題6
# 変数 x が定義されている（値は0）。
# 「x が 0 でなく、かつ 10 を x で割った値が 3 より大きい」場合に
# 「条件を満たします」と表示するプログラムを、and の短絡評価を利用して
# ゼロ除算エラーが起きないように書きなさい。
x = 0
 
#解答
if x != 0 and 10/x > 3:
    print('条件を満たします') 
 
# 問題7
# 変数 num が定義されている。num が0以上であれば 'non-negative' を、
# そうでなければ 'negative' を変数 result に代入するプログラムを、
# 三項演算子（条件式）を使って1行で書きなさい。
num = -5
 
#解答
result = 'non-negative' if num >=0 else 'negative'
print(result)