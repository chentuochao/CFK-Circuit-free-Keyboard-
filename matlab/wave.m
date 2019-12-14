myfft = [];
mypeak = [];
mypeak2 = [];
thersold = 2;
low = 6000;
up = 10000;

%--------------------------------W-----------------------------------------
[wav,Fs]=audioread('WW.wav');%读出信号，采样率和采样位数。
y=wav(:,1);%我这里假设你的声音是双声道，我只取单声道作分析，如果你想分析另外一个声道，请改成y=y(:,2)
sigLength=length(y);
%{
figure(1)
subplot(211)
t=(0:sigLength-1)/Fs;
plot(t,y);xlabel('Time(s)');

Y = fft(y,sigLength);
Pyy = Y.* conj(Y) / sigLength;
halflength=floor(sigLength/2);
subplot(212)
f=Fs*(0:halflength)/sigLength;
plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');
%}
figure(2)
%bound = [147300,168800 , 191000, 211300, 232300 ]; %Q
bound = [  84700, 105000, 125350, 145750, 214000 ]; %W233300, 64600,
%bound = [ 83900, 103900, 123600, 164500, 205500 ]; %E
%bound = [ 97500, 117500, 136500, 175500, 193500 ]; %rctrl
for i = 1 : 5
    %y = wav(bound(i)+low : bound(i) + 8800); %5000
    y = wav(bound(i)+200 : bound(i) + 5200);
    sigLength=length(y);
    subplot(5,2,2 * i - 1)
    t=(0:sigLength-1)/Fs;
   
    plot(t,y);xlabel('Time(s)');
    axis([0 0.25 -0.2 0.2]);
    Y = fft(y,sigLength);   
    Pyy = Y.* conj(Y) / sigLength;
    halflength=floor(sigLength/2);
    subplot(5,2,2*i)
    f=Fs*(0:halflength)/sigLength;
    x1 = round(low * sigLength / Fs);
    x2 = round(up * sigLength / Fs);
    myfft = [myfft, Pyy(x1:x2)];
    Py1 = Pyy(x1:x2) / mean(Pyy(x1:x2));
    [maxv,maxl]=findpeaks(Py1, 'minpeakheight',thersold);
    Py2 = zeros(x2-x1+1,1);
    Py3 = zeros(x2-x1+1,1);
    
    for j = 1 : length(maxl)
        Py2(maxl(j)) = maxv(j);
        Py3(maxl(j)) = 1;
    end
    mypeak = [mypeak, Py3];
    mypeak2 = [mypeak2, Py2];
    
    stem(f(x1 + maxl - 1),maxv, 'Marker', 'none');xlabel('Frequency(Hz)');
    hold on;
    %plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');
    axis([low up 0 10]);
    hold off;
end
%-------------------------W end---------------------------
%--------------------------------Q-----------------------------------------
[wav,Fs]=audioread('QQ.wav');%读出信号，采样率和采样位数。
y=wav(:,1);%我这里假设你的声音是双声道，我只取单声道作分析，如果你想分析另外一个声道，请改成y=y(:,2)
sigLength=length(y);
%{
figure(1)
subplot(211)
t=(0:sigLength-1)/Fs;
plot(t,y);xlabel('Time(s)');

Y = fft(y,sigLength);
Pyy = Y.* conj(Y) / sigLength;
halflength=floor(sigLength/2);
subplot(212)
f=Fs*(0:halflength)/sigLength;
plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');
%}
figure(3)
bound = [147300,168800 , 191000, 211300, 232300 ]; %Q
%bound = [  84700, 105000, 125350, 145750, 214000 ]; %W233300, 64600,
%bound = [ 83900, 103900, 123600, 164500, 205500 ]; %E
%bound = [ 97500, 117500, 136500, 175500, 193500 ]; %rctrl
for i = 1 : 5
    %y = wav(bound(i)+low : bound(i) + 8800); %5000
    y = wav(bound(i)+200 : bound(i) + 5200);
    sigLength=length(y);
    subplot(5,2,2 * i - 1)
    t=(0:sigLength-1)/Fs;
   
    plot(t,y);xlabel('Time(s)');
    axis([0 0.25 -0.2 0.2]);
    Y = fft(y,sigLength);   
    Pyy = Y.* conj(Y) / sigLength;
    halflength=floor(sigLength/2);
    subplot(5,2,2*i)
    f=Fs*(0:halflength)/sigLength;
    x1 = round(low * sigLength / Fs);
    x2 = round(up * sigLength / Fs);
    myfft = [myfft, Pyy(x1:x2)];
    Py1 = Pyy(x1:x2) / mean(Pyy(x1:x2));
    [maxv,maxl]=findpeaks(Py1, 'minpeakheight',thersold);
    Py2 = zeros(x2-x1+1,1);
    Py3 = zeros(x2-x1+1,1);
    
    for j = 1 : length(maxl)
        Py2(maxl(j)) = maxv(j);
        Py3(maxl(j)) = 1;
    end
    mypeak = [mypeak, Py3];
    mypeak2 = [mypeak2, Py2];
    stem(f(x1 + maxl - 1),maxv, 'Marker', 'none');xlabel('Frequency(Hz)');
    hold on;
    %plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');
    axis([low up 0 10]);
    hold off;
end
%-------------------------Q end---------------------------

%--------------------------------E-----------------------------------------
[wav,Fs]=audioread('EE.wav');%读出信号，采样率和采样位数。
y=wav(:,1);%我这里假设你的声音是双声道，我只取单声道作分析，如果你想分析另外一个声道，请改成y=y(:,2)
sigLength=length(y);
%{
figure(1)
subplot(211)
t=(0:sigLength-1)/Fs;
plot(t,y);xlabel('Time(s)');

Y = fft(y,sigLength);
Pyy = Y.* conj(Y) / sigLength;
halflength=floor(sigLength/2);
subplot(212)
f=Fs*(0:halflength)/sigLength;
plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');
%}
figure(4)
%bound = [147300,168800 , 191000, 211300, 232300 ]; %Q
%bound = [  84700, 105000, 125350, 145750, 214000 ]; %W233300, 64600,
bound = [ 64500, 103900, 123600, 164500, 205500 ]; %E
%bound = [ 97500, 117500, 136500, 175500, 193500 ]; %rctrl
for i = 1 : 5
    %y = wav(bound(i)+low : bound(i) + 8800); %5000
    y = wav(bound(i)+200 : bound(i) + 5200);
    sigLength=length(y);
    subplot(5,2,2 * i - 1)
    t=(0:sigLength-1)/Fs;
   
    plot(t,y);xlabel('Time(s)');
    axis([0 0.25 -0.2 0.2]);
    Y = fft(y,sigLength);   
    Pyy = Y.* conj(Y) / sigLength;
    halflength=floor(sigLength/2);
    subplot(5,2,2*i)
    f=Fs*(0:halflength)/sigLength;
    x1 = round(low * sigLength / Fs);
    x2 = round(up * sigLength / Fs);
    myfft = [myfft, Pyy(x1:x2)];
    Py1 = Pyy(x1:x2) / mean(Pyy(x1:x2));
    [maxv,maxl]=findpeaks(Py1, 'minpeakheight',thersold);
    Py2 = zeros(x2-x1+1,1);
    Py3 = zeros(x2-x1+1,1);
    
    for j = 1 : length(maxl)
        Py2(maxl(j)) = maxv(j);
        Py3(maxl(j)) = 1;
    end
    mypeak = [mypeak, Py3];
    mypeak2 = [mypeak2, Py2];
    stem(f(x1 + maxl - 1),maxv, 'Marker', 'none');xlabel('Frequency(Hz)');
    hold on;
    %plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');
    axis([low up 0 10]);
    hold off;
end
%-------------------------E end---------------------------

%--------------------------------ctrl-----------------------------------------
[wav,Fs]=audioread('lCtrl.wav');%读出信号，采样率和采样位数。
y=wav(:,1);%我这里假设你的声音是双声道，我只取单声道作分析，如果你想分析另外一个声道，请改成y=y(:,2)
sigLength=length(y);
%{
figure(1)
subplot(211)
t=(0:sigLength-1)/Fs;
plot(t,y);xlabel('Time(s)');

Y = fft(y,sigLength);
Pyy = Y.* conj(Y) / sigLength;
halflength=floor(sigLength/2);
subplot(212)
f=Fs*(0:halflength)/sigLength;
plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');
%}
figure(8)
%bound = [147300,168800 , 191000, 211300, 232300 ]; %Q
%bound = [  84700, 105000, 125350, 145750, 214000 ]; %W233300, 64600,
%bound = [ 64500, 103900, 123600, 164500, 205500 ]; %E
bound = [ 97400, 41500, 78400, 175500, 59300 ]; %lctrl
for i = 1 : 5
    %y = wav(bound(i)+low : bound(i) + 8800); %5000
    y = wav(bound(i)+100 : bound(i) + 5100);
    sigLength=length(y);
    subplot(5,2,2 * i - 1)
    t=(0:sigLength-1)/Fs;
   
    plot(t,y);xlabel('Time(s)');
    axis([0 0.25 -0.2 0.2]);
    Y = fft(y,sigLength);   
    Pyy = Y.* conj(Y) / sigLength;
    halflength=floor(sigLength/2);
    subplot(5,2,2*i)
    f=Fs*(0:halflength)/sigLength;
    x1 = round(low * sigLength / Fs);
    x2 = round(up * sigLength / Fs);
    myfft = [myfft, Pyy(x1:x2)];
    Py1 = Pyy(x1:x2) / mean(Pyy(x1:x2));
    [maxv,maxl]=findpeaks(Py1, 'minpeakheight',thersold+1);
    Py2 = zeros(x2-x1+1,1);
    Py3 = zeros(x2-x1+1,1);
    
    for j = 1 : length(maxl)
        Py2(maxl(j)) = maxv(j);
        Py3(maxl(j)) = 1;
    end
    mypeak = [mypeak, Py3];
    mypeak2 = [mypeak2, Py2];
    stem(f(x1 + maxl - 1),maxv, 'Marker', 'none');xlabel('Frequency(Hz)');
    hold on;
    %plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');
    axis([low up 0 10]);
    hold off;
end
%-------------------------ctrl---------------------------


figure(5)
r1 = abs(corrcoef(myfft));
imagesc(r1);
colormap(gray)


peak_size = size(mypeak, 2);
r2 = zeros(peak_size, peak_size);
for i = 1:peak_size
    for j = 1:peak_size
        r2(i,j) = mymatch(mypeak(:,i), mypeak(:,j));
    end
end
figure(6)
imagesc(r2);
colormap(gray)

figure(7)
r3 = abs(corrcoef(mypeak2));
imagesc(r3);
colormap(gray)
colorbar

