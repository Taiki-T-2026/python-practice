h=180
print(h)
h=29
print(h)
print(h+48)
k=64
print(h+k)
#変数定義　変数はいくらでも作れて、いくらでも再定義可能

k=k+90
print(k)
#変数の再定義のために再定義する変数を用いることもできる

k-=54
#累積代入文　k=k-54と同義　+でも同様

def BMI(height,weight):
    return weight/(height/100)**2
print(BMI(170,65))
#関数　引数の後の:を忘れずに　BMI=体重（Kg)÷身長（mの2乗）

def M(cm):
    return cm/100
print(M(7639))
#センチメートルをメートルに換算する関数

def seiseki(kokugo,sansu,eigo):
    goukei=kokugo+sansu+eigo
    print(goukei)
    heikin=goukei/3
    return heikin

print(seiseki(80,68,89))
#ローカル変数　関数の中で変数を作った場合、その変数はその関数のみで適応される
#関数の外でgoukeiやheikinを使っても、外で定義していない限り未定義のエラーが出る。
#この関数の中で使う、その関数の中だけで適応される変数をローカル変数という

def add(x,y): #引数x,yを足す関数add
    return x+y
print(add(6,7))

def rectangle_area(height,width): #引数高さと幅で長方形の面積を出す関数
    return height*width
print('長方形の面積は',rectangle_area(6,9))

def greet(name): #名前を入れると「○○さんこんにちわ」と返す関数
    print(name,'さんこんにちわ')

print(greet('田中'))

def double_sum(x,y):
    total=x+y
    return total*2
print(double_sum(5,6))

tax_rate=0.1

def add_tax(price): #引数「価格」を入れたら10％の税込み価格に変換する関数
    return price+(price*tax_rate)
print(add_tax(300))

grand_total=0

def add_total(price,quantity):
    subtotal=price*quantity
    return subtotal
print(add_total(800,9))

