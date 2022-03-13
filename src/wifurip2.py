import argparse
import time
from os import mkdir, path, getcwd
import re

def main(i: str, d: int):
    # out = 'D:\\Games\\[ScrewThisNoise] HoneySelect 2 DX BetterRepack\\UserData\\chara\\female\\export'
    out = getcwd() + '\\Export'

    if not path.exists(out):
        mkdir(out)

    with open(i, 'rb') as f:
        binStr = f.read()
    sceneHex = binStr.hex()

    # start 640000000fe380904149535f4368617261e3809105312e302e3000000000
    # end 313694ca00000000ca00000000ca00000000ca3f800000ca00000000ca0000000090
    start_str = '640000000fe380904149535f4368617261e3809105312e302e3000000000'
    ls = sceneHex.split(start_str)
    ls = ls[1:]
    lsLen = len(ls)
    if lsLen < 1:
        return

    last = ls[lsLen -1]

    res = re.search(r'803f0000803f0100000001[\d][\d][\d][\d]0000', last)

    if res:
        ls[lsLen - 1] = last[:res.regs[0][1]]

    ls2 = []
    
    for i, chara in enumerate(ls):
        # try:
        #     id = bytes.fromhex(chara[2:chara.find('5e')]).decode('utf8')
        # except Exception as e:
        #     id = bytes.fromhex(chara[2:chara.find('60')]).decode('utf8')

        id = bytes.fromhex(chara[2: 74 * 2]).decode('utf8')

        if d != 0:
            index = next((i for i, v in enumerate(ls2) if v[0] == id), None)
            if index is not None:
                clen = len(chara)
                if clen > ls2[index][2]:
                    ls2[index][1] = chara
                    ls2[index][2] = clen
                continue
        ls2.append([id, chara, len(chara)])
    
    del ls

    for id, chara, l in ls2:
        chara = start_str + chara

        res = re.search(r'7365780([01])', chara)
        sex = 0
        if res:
            sex = int(res.group(1))
        if sex == 0:
            continue

        sex = ['male', 'female'][sex]

        fullname = ''
        res = re.search('66756c6c6e616d65([a-d])([0-9a-f])', chara)
        if res: 
            offset = res.regs[0][1]
            if res.group(1) != 'd':
                multi = {'a':0, 'b':1}[res.group(1)] * 16
                nameLen = (int('0'+res.group(2), 16) + multi) * 2
            else:
                nameLen = chara.find('ab706572', offset) - offset
                offset = offset + 2
            
            fullname = bytes.fromhex(chara[offset: offset + nameLen]).decode('utf8', 'ignore')

        exportFilename = sex + '_' + id + '_' + fullname + '_' + str(round(time.time() * 1000)) + '.png'

        with open(out + '\\' + exportFilename, 'wb') as ef:
            bs = bytes.fromhex(chara)
            ef.write(bs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='选择场景文件,*.png', type=str, default='')
    # parser.add_argument('-outDir', help='选择输出目录', type=str,  default='')
    parser.add_argument('-d', help='是否过滤重复: 0, 1', type=int, default='1')
    args = parser.parse_args()

    if not path.exists(args.i):
        raise FileNotFoundError(args.i)
    elif not args.i.endswith('.png'):
        raise NotImplementedError('不支持的文件格式')
    
    # main('D:\\Games\\[ScrewThisNoise] HoneySelect 2 DX BetterRepack\\UserData\\Studio\\scene\\Mine\\2021_0701_2232_34_825.png', 1)
    main(args.i, args.d)