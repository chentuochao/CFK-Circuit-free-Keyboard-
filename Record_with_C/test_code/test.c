#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>


#define sin_t       5
#define sin_hz      1000
#define sin_db 100
#define size_buf    sin_t*100000


unsigned char buf[size_buf*2];


#if 1
typedef struct
{
char chRIFF[4];                 // "RIFF" 标志  
int  total_Len;                 // 文件长度      
char chWAVE[4];                 // "WAVE" 标志  
char chFMT[4];                  // "fmt" 标志 
int  dwFMTLen;                  // 过渡字节（不定）  一般为16
short fmt_pcm;                  // 格式类别  
short  channels;                // 声道数  
int fmt_samplehz;               // 采样率 
int fmt_bytepsec;               // 位速  
short fmt_bytesample;           // 一个采样多声道数据块大小  
short fmt_bitpsample;    // 一个采样占的 bit 数  
char chDATA[4];                 // 数据标记符＂data ＂  
int  dwDATALen;                 // 语音数据的长度，比文件长度小42一般。这个是计算音频播放时长的关键参数~  
}WaveHeader;


WaveHeader WavInf = {
"RIFF",
sin_t*500*2+36,
"WAVE",
"fmt ",
16,
1,
2,
100000,
100000,
1,
8,
"data",
500*sin_t*2
};


#else
//将实际数据转化为内存储存形式
void data2array(unsigned int x,unsigned char a[],unsigned char n)
{ 
    unsigned char i;
for(i=0;i<n;i++)
{ 
        a[i]=x&0xff;
        x=x>>8;
    }
}


//unsigned char WavFileHeader[42] = {0};
unsigned char wav_header[] = {  
'R', 'I', 'F', 'F',      // "RIFF" 标志  
0, 0, 0, 0,              // 文件长度  
'W', 'A', 'V', 'E',      // "WAVE" 标志  
'f', 'm', 't', ' ',      // "fmt" 标志  
16, 0, 0, 0,             // 过渡字节（不定）  
0x01, 0x00,              // 格式类别  
0x01, 0x00,              // 声道数  
0, 0, 0, 0,              // 采样率  
0, 0, 0, 0,              // 位速  
0x01, 0x00,              // 一个采样多声道数据块大小  
0x10, 0x00,              // 一个采样占的 bit 数  
'd', 'a', 't', 'a',      // 数据标记符＂data ＂  
0, 0, 0, 0               // 语音数据的长度，比文件长度小42一般。这个是计算音频播放时长的关键参数~  
};  


void InitWavHeader(void)
{
    unsigned long a = sin_t*100000+36;
    data2array(a,&wav_header[4],4);
    a = 100000;
    data2array(a,&wav_header[24],4);
    data2array(a,&wav_header[28],4);
    a = sin_t*100000;
    data2array(a,&wav_header[40],4);
}
#endif


int main()
{
long i;
    int j = 0;
    int ret;
    //InitWavHeader();
for(i=0;i<size_buf;i++)
{
        buf[j++] = sin((size_buf - i)*(3.14159*2)/100000*sin_hz)*128*sin_db/100+128;
        buf[j++] = 0;
}
int fd;
fd = open("./test.wav",O_CREAT|O_RDWR);
if(fd<0)
{
    printf("open error\n");
    return 0;
}
ret = write(fd,(char *)&WavInf,sizeof(WavInf));
//write(fd,wav_header,44);
ret = write(fd,buf,100000*sin_t*2);
    close(fd);


return 0;
}
