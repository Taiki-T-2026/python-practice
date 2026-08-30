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