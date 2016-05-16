from flask import Flask, request
app = Flask(__name__)

def main(num, minterms):
    minterms = [i for i in minterms]
    rrange = [0 for i in range(len(minterms))]
    rrange[0] = len(minterms)
    f = [[[0 for k in range(num + 1)] for j in range(pow(2, pow(num, 2)))] for i in range(num + 1)]
    for i in range(len(minterms)):
        for j in range(num):
            f[0][i][num - 1 - j] = minterms[i] % 2
            minterms[i] /= 2
    for i in range(1, len(minterms)):
        count = 0
        for j in range(rrange[i - 1]):
            for k in range(rrange[i - 1]):
                if f[i - 1][j].count(1) + 1 == f[i - 1][k].count(1):
                    difference = 0
                    for x, y in zip(f[i - 1][j][:-1], f[i - 1][k][:-1]):
                        if x != y:
                            difference += 1
                    if difference > 1:
                        continue
                    f[i - 1][j][-1], f[i - 1][k][-1] = 2, 2
                    for l in range(num):
                        if f[i - 1][j][l] != f[i - 1][k][l]:
                            f[i][count][l] = 2
                        else:
                            f[i][count][l] = f[i - 1][j][l]
                    count += 1
        rrange[i] = count
    llen = 0
    result = [[0 for j in range(num + 1)] for i in range(pow(2, pow(num, 2)))]
    for i in range(num):
        for j in range(rrange[i]):
            if f[i][j][-1] != 2:
                if f[i][j] in result:
                    continue
                for k in range(num):
                    result[llen][k] = f[i][j][k]
                llen += 1
    str = 'f = '
    c = 0
    for i in range(llen):
        if result[i][-1] != 2:
            if c != 0:
                str += ' + '
            for j in range(num):
                if result[i][j] == 0:
                    str += '%s\'' % chr(j + 65)
                elif result[i][j] == 1:
                    str += '%s' % chr(j + 65)
            c += 1
    return str

@app.route('/<num>/<minterms>')
def function(num, minterms):
    minterms = [int(i) for i in minterms.encode('utf8').split(',')]
    return main(int(num.encode('utf8')), tuple(minterms))


@app.route("/")
def usage():
    str = """<xmp>
    Usage:
        /num/minterms

        num stands for literals ( A, B, C, ......)
    Example:
        /2/1,2,3
        the result should be "f = A + B"
    </xmp>"""
    return str

if __name__ == "__main__":
    app.run()