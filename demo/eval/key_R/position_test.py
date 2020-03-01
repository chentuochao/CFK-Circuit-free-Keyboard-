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
    return position.find_top8_key(key_dic,angle)

for i in range(1,21):
    name = '.\\eval\\key_E\\key_'+str(i)+'.wav'
    print(name)
    print(os.path.exists(name))
    [_,wave,_] = position.wavread(name)
    print(Find_position(wave))