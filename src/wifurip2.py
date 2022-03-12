import argparse
import time
from os import mkdir, path, getcwd
import re

def main(i: str, out: str):
    # out = 'D:\\Games\\[ScrewThisNoise] HoneySelect 2 DX BetterRepack\\UserData\\chara\\female\\export'
    out = getcwd() + '\\Export'

    if not path.exists(out):
        mkdir(out)

    with open(i, 'rb') as f:
        binStr = f.read()
    sceneHex = binStr.hex()

    # start 640000000fe380904149535f4368617261e3
    # end 313694ca00000000ca00000000ca00000000ca3f800000ca00000000ca0000000090
    ls = sceneHex.split('640000000fe380904149535f4368617261e3')
    ls = ls[1:]
    lsLen = len(ls)
    if lsLen < 1:
        return
    last = ls[lsLen -1]
    
    res = re.search(r'803f0000803f01000000010[\d]000000', last)

    ls[lsLen - 1] = last[:res.regs[0][1]]

    for chara in ls:
        chara = '640000000fe380904149535f4368617261e3' + chara
        res = re.search(r'7365780([01])', chara)
        sex = 0
        if res:
            sex = int(res.groups(1)[0])
        if sex == 0:
            continue

        sex = ['male', 'female'][sex]

        exportFilename = sex + '_' + str(round(time.time() * 1000)) + '.png'

        with open(out + '\\' + exportFilename, 'wb') as ef:
            bs = bytes.fromhex(chara)
            ef.write(bs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='选择场景文件,*.png', type=str, default='')
    # parser.add_argument('-outDir', help='选择输出目录', type=str,  default='')
    args = parser.parse_args()

    # if not path.exists(args.i):
    #     raise FileNotFoundError(args.i)
    # elif not args.i.endswith('.png'):
    #     raise NotImplementedError('不支持的文件格式')
    #
    main('D:\\Games\\[ScrewThisNoise] HoneySelect 2 DX BetterRepack\\UserData\\Studio\\scene\\Mine\\2021_0601_1438_08_850.png', '')