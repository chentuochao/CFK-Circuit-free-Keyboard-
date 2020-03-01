#-------------------将键盘上的按键转换为对应于麦克风的坐标------------------------
from parameter import XCORRECT
from parameter import YCORRECT
from parameter import CONSIDER_NUMBER_OR_NOT

def keyboard_coordinate_read(): #读取当前键盘的按键分布位置文件
    keyboard_map = []
    f = open('.\\keyboard.txt','r')
    line = f.readline()
    while line:
        line = line.strip('\n')
        line = line.split(' ')
        keyboard_map.append(line)
        line = f.readline()
    # print(keyboard_map)
    f.close()
    # print(len(keyboard_map))
    return keyboard_map

def get_keyboard_order():
    if CONSIDER_NUMBER_OR_NOT == 1:
        print("---使用带数字按键的识别---")
        order = ' 1234567890    qwertyuiop    asdfghjkl    zxcvbnm' #暂时把不用的都标记为空格了，之后可以标记为别的
    else:
        print('---使用没有数字按键的识别---')
        order = '               qwertyuiop    asdfghjkl    zxcvbnm'
    use = []
    for i in order:
        use.append(i)
    # print(len(use))
    return use

def map_all():  #把字母和字母位置匹配起来
    order = get_keyboard_order()
    position = keyboard_coordinate_read()
    dic = {}
    for i in range(0,len(order)):
        position_correct = [float(position[i][0])+XCORRECT,float(position[i][1])+YCORRECT]  #根据给出的原点对字母位置进行修正
        dic[order[i]] = position_correct
    return dic