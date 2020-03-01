import position
import os
import wave
from keyboard_map import map_all

def init_for_DTOA():
    return map_all()

key_dic = init_for_DTOA()
def Find_position(wave):
    # the function for position
    global key_dic
    angle = position.give_angle(wave)[0]
    angle = position.angle_normalized(angle)
    return position.find_top5_key(key_dic,angle)

for i in range(1,21):
    # name = '..\\data\\key_P\\key_'+str(i)+'.wav'
    name = '.\\double-blind\\key_'+str(i)+'.wav'
    print(name)
    print('这个文件是否存在：'+str(os.path.exists(name)))
    [_,wave,_] = position.wavread(name)

    probility = Find_position(wave)
    print('key_'+str(i))
    position_set = position.set_return(probility)
    print('----------')