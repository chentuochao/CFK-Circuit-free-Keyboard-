#include <stdio.h>
#include <SDL.h>
#include <sys/time.h>      //添加头文件
#include <stdlib.h>
#include <math.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <termio.h>
#include <string.h>

#define WAV_MAXLENGTH (48000 * 12 * 360)
#define KEY_MAXLENGTH 100

int64_t past = 0;
int fd;
int recording = 0;
int last_recording = 0;
int64_t begin_time = 0;
int64_t keytime = 0; 

int key_list[KEY_MAXLENGTH] = {0};
int64_t keytime_list[KEY_MAXLENGTH] = {0};
int key_len = 0;
char wav_list[WAV_MAXLENGTH] = {'\0'};
int64_t wav_len = 0;

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
    WAV_MAXLENGTH+36,
    "WAVE",
    "fmt ",
    16,     
    1,    //PCM
    6,    //channels
    48000,  // sample rate
    48000*12,  // byte rate
    12,      // bytes per sample 
    16,      // bits per sample in single channel
    "data",
    WAV_MAXLENGTH  // data size(bytes)
};

int64_t getCurrentTime()      //直接调用这个函数就行了，返回值最好是int64_t，long long应该也可以
{    
    struct timeval tv;    
    gettimeofday(&tv,NULL);    //该函数在sys/time.h头文件中
    return tv.tv_sec * 1000 + tv.tv_usec / 1000;    
}    

void clear_all(){
    memset(key_list,0,KEY_MAXLENGTH * sizeof(int));
    memset(keytime_list,0,KEY_MAXLENGTH * sizeof(int64_t));
    key_len = 0;
    memset(wav_list, '\0', sizeof(wav_list));
    wav_len = 0;
}

int scanKeyboard()
{
    int in;
    struct termios new_settings;
    struct termios stored_settings;
    tcgetattr(0,&stored_settings);
    new_settings = stored_settings;
    new_settings.c_lflag &= (~ICANON);
    new_settings.c_cc[VTIME] = 0;
    tcgetattr(0,&stored_settings);
    new_settings.c_cc[VMIN] = 1;
    tcsetattr(0,TCSANOW,&new_settings);
    
    in = getchar();
    keytime = getCurrentTime();
    tcsetattr(0,TCSANOW,&stored_settings);
    return in;
}


void save_file(){
    char timefile[20] = {'\0'};
    char txt[] = ".txt";
    char wav[] = ".wav";
    char path1[30] = "./raw/";
    
    sprintf(timefile, "%ld", begin_time);
    strcat(path1, timefile);
    strcat(path1, wav);

    char path2[30] = "./raw/";
    strcat(path2, timefile);
    strcat(path2, txt);
    WavInf.total_Len = wav_len + 36;
    WavInf.dwDATALen = wav_len;

    fd = open(path1,O_CREAT|O_RDWR, S_IRWXU);
    if(fd < 0)
    {
        printf("file open error\n");
        return;
    }
    int ret = write(fd,(char *)&WavInf,sizeof(WavInf));
    printf("total : %ld\n", wav_len);
    ret = write(fd, wav_list, wav_len);
    close(fd);

    FILE *fpWrite=fopen(path2,"w");

    if(fpWrite==NULL)
    {
        printf("txt open error!");
        return;
    }
    fprintf(fpWrite, "[");
    for(int i = 0; i < key_len; ++i)
    {
        if (i == (key_len -1)) fprintf(fpWrite, "%d]\n", key_list[i]);
        else fprintf(fpWrite, "%d, ", key_list[i]);
    }

    fprintf(fpWrite, "[");
    for(int i = 0; i < key_len; ++i)
    {
        if (i == (key_len -1)) fprintf(fpWrite, "%ld]\n", keytime_list[i]);
        else fprintf(fpWrite, "%ld, ", keytime_list[i]);
    }

    fclose(fpWrite);
    return;
}

/* Audio Callback
 * The audio function callback takes the following parameters: 
 * stream: A pointer to the audio buffer to be filled 
 * len: The length (in bytes) of the audio buffer 
 * 
*/ 
void fill_audio(void *udata, Uint8 *stream, int len){ 
    if(!recording) return;
    else if(recording && (!last_recording)) {
        begin_time = getCurrentTime();
        last_recording = 1;
        return;
    }
    if(wav_len >= WAV_MAXLENGTH - len) {
        printf("out of range");
        return;
    }
    memcpy((wav_list + wav_len), stream, len);
    wav_len += len;
    //int64_t now = getCurrentTime();
    //printf("remaining time: %ld\n", now - past);
    //past = now;
	//SDL 2.0
} 


int main(int argc, char* argv[])
{
	//Init
    SDL_AudioDeviceID devid;
	if(SDL_Init(SDL_INIT_AUDIO | SDL_INIT_TIMER)) {  
		printf( "Could not initialize SDL - %s\n", SDL_GetError()); 
		return -1;
	}
	//SDL_AudioSpec
	SDL_AudioSpec wanted_spec;
    SDL_memset(&wanted_spec, 0, sizeof(wanted_spec)); 
	wanted_spec.freq = 48000; 
	wanted_spec.format = AUDIO_S16SYS; 
	wanted_spec.channels = 6; 
	wanted_spec.silence = 0; 
	wanted_spec.samples = 1024; 
	wanted_spec.callback = fill_audio; 
    int count = SDL_GetNumAudioDevices(1);
    if(SDL_GetAudioDeviceName(count - 1, 1)==NULL){
        printf("Invalid device index!\n");
        return -1;
    }
    //printf("%ld, %ld\n", sizeof(SDL_GetAudioDeviceName(8, 1)), sizeof(devid)); 
    const char* dev = SDL_GetAudioDeviceName(count - 1, 1);
    //printf("%c， %c ,%c, %c%c\n", dev[0], dev[1], dev[2], dev[3], dev[4]);
    if(dev[0]!='R' || dev[1]!='e' || dev[2] != 'S')
    {
        printf("Please connect microphone!");
        return -1;
    }
    if (SDL_OpenAudioDevice(dev, 1, &wanted_spec, NULL, 0) <= 0){ 
		printf("can't open audio.\n"); 
		return -1; 
	} 
    devid = SDL_OpenAudioDevice(dev, 1, &wanted_spec, NULL, 0);

    SDL_PauseAudioDevice(devid, 0);
    SDL_Delay(500);
    printf("begin typing!\n");
    recording = 1;
    while (1) {
        int button = scanKeyboard();
        //printf(":%d\n",button);
        key_list[key_len] = button;
        keytime_list[key_len] = keytime - begin_time;
        key_len ++;
        if(button == 10){   //Enter
            SDL_Delay(500); 
            recording = 0;
            last_recording = 0;
            save_file();
            clear_all();
            recording = 1;
        }        
    }
    SDL_PauseAudioDevice(devid, 0);
    printf("End recording!\n");
    //SDL_Delay(1000);   
    SDL_PauseAudioDevice(devid, 1);
    SDL_CloseAudioDevice(devid);
    
}