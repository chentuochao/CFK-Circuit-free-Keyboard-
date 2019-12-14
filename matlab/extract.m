function extract()
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明
[wav,Fs]=audioread('output.wav');%读出信号，采样率和采样位数。
size(wav)
Fs
for i = 1 : 6
    subplot(2,3,i)
    plot(wav(2000:2500,i))
    
%{
y=wav(40000:100000,1);%我这里假设你的声音是双声道，我只取单声道作分析，如果你想分析另外一个声道，请改成y=y(:,2)
sigLength=length(y);

figure(1)
subplot(311)
t=(0:sigLength-1)/Fs;
plot(t,y);xlabel('Time(s)');

Y = fft(y,sigLength);
Pyy = Y.* conj(Y) / sigLength;
halflength=floor(sigLength/2);
subplot(312)
f=Fs*(0:halflength)/sigLength;
plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');

for i = 1: sigLength-1
   %if(abs(y(i+1) -y(i)) > 0.04) 
   if(abs(y(i)) > 0.2) 
        subplot(313)
        t=(i-1000:i+8000)/Fs;
        plot(t,y(i-1000:i+8000));xlabel('Time(s)');
        break;
    end
end

%}
end

