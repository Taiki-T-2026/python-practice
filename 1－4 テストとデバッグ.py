x=7
assert x>0

def square(x):
    x=3
    assert square==9,"squareの計算が間違っています"
    return x*x
#間違い　下のコードが正解
#assert square==9のsquareは関数そのものを指す。square(3)のように呼び出して初めて計算結果(9)が得られるのであって、square単体では9と比較しても意味がない。
#↑常にFalseになり、この関数を呼び出すたびに即座にエラーになる。
#assertが関数の中にある。「関数を定義すること」と「その関数の動きを確認すること」は別の場所で行う必要がある。

def square(x):
    return x*x
assert square(3)==9,"squareの計算が間違っています"

