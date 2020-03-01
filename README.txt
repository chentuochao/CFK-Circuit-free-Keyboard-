1. CV_measure_key用于用CV来测量各个按键之间的间距
2. data用于存储原始数据，包括长段录音和单个keystroke
3. demo用于实时识别按键，其中主要算法包括（按键检测+定位+特征匹配）
4. Front_end是基于python+js的网页前端打字输入和录音
5. Machine_learning 包括训练神经网络的整个框架（数据预处理+网络结构+训练+模型保存和导入+测试和评估+可视化）
6. Matlab_eval用于CDF的evaluation
7. Record_with_C用C和底层的库SDL来进行录音，有更好的实时性


当前的任务列表
1. 完成python 上的FFT相关算法
2. 完成更加流畅的前端使用界面（并不着急）
3. 更新对于流数据的事件识别和分割算法（梁博）
4. 更新硬件设备，PCM186x可能是比较合适的声卡