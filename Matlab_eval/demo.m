myfft = [];
mypeak = [];
mypeak2 = [];
thersold = 1;
low = 100; 
up =10000;


test = 'ABCDEFGHJKLMNOPQRSVWXYZ123';

for index = 1:length(test)
    for i = 1 : 5 
        %figure(index)
        [wav, Fs] = audioread(['./test/key_', test(index),'/key_',num2str(i),'.wav' ]);
        y = wav(:, 2);
        sigLength=length(y);
        %subplot(5,2,2 * i - 1)
        t=(0:sigLength-1)/Fs;

        %plot(t,y);xlabel('Time(s)');
        Y = fft(y,sigLength);   
        Pyy = Y.* conj(Y) / sigLength;
        halflength=floor(sigLength/2);
        %subplot(5,2,2*i)
        f=Fs*(0:halflength)/sigLength;
        x1 = round(low * sigLength / Fs);
        if x1 < 1
            x1 = 1;
        end
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

        %stem(f(x1 + maxl - 1),maxv, 'Marker', 'none');xlabel('Frequency(Hz)');
        %hold on;
        %plot(f,Pyy(1:halflength+1));xlabel('Frequency(Hz)');
        %set(gca,'XLim',[low up]);%X轴的数据显示范围
        %axis([low up]);
        %hold off;
    end
end
height = size(myfft,2);
%{
figure(50)
r1 = abs(corrcoef(myfft));
imagesc(r1);
colormap(gray)
colorbar
axis off

peak_size = size(mypeak, 2);
r2 = zeros(peak_size, peak_size);
for i = 1:peak_size
    for j = 1:peak_size
        r2(i,j) = mymatch(mypeak(:,i), mypeak(:,j));
    end
end
figure(60)
imagesc(r2);
colormap(gray)

figure(70)
r3 = abs(corrcoef(mypeak2));
imagesc(r3);
colormap(gray)
colorbar
%}

mycolor = 'rgb';
area = {'QAZWSXEDRC','FTGVYHBUJN','PLOKMIJN'};
eval = 'YPMZO';
figure(1)
hold on
for index = 1:length(eval)
    %myarea = area{index};
    emyfft = [];
    emypeak = [];
    emypeak2 = [];
    CDF = [0,0,0,0,0,0,0,0];
    CDF2 = [0,0,0,0,0,0,0,0];
    for i = 1 : 20
        %figure(index)
        [wav, Fs] = audioread(['./eval/key_', eval(index),'/key_',num2str(i),'.wav' ]);
        y = wav(:, 2);
        sigLength=length(y);
        t=(0:sigLength-1)/Fs;

        %plot(t,y);xlabel('Time(s)');
        Y = fft(y,sigLength);   
        Pyy = Y.* conj(Y) / sigLength;
        halflength=floor(sigLength/2);
        %subplot(5,2,2*i)
        f=Fs*(0:halflength)/sigLength;
        x1 = round(low * sigLength / Fs);
        if x1 < 1
            x1 = 1;
        end
        x2 = round(up * sigLength / Fs);
        emyfft = Pyy(x1:x2);
        Py1 = Pyy(x1:x2) / mean(Pyy(x1:x2));
        [maxv,maxl]=findpeaks(Py1, 'minpeakheight',thersold);
        Py2 = zeros(x2-x1+1,1);
        Py3 = zeros(x2-x1+1,1);
        
        for j = 1 : length(maxl)
            Py2(maxl(j)) = maxv(j);
            Py3(maxl(j)) = 1;
        end
        emypeak = Py3;
        emypeak2 = Py2;
        %{
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
        %}
        corr = [];
        for j = 1: height
            temp = [emyfft, myfft(:, j)];
            %temp = [emypeak, mypeak(:, j)];
            r1 = abs(corrcoef(temp));
            corr = [corr, r1(1,2)];
        end
        [max_corr, max_index] = sort(corr,2);
        max_corr = fliplr(max_corr);
        max_index = fliplr(max_index);
        %disp(max_corr(1:5))
        result = [];
        for j = 1:8
            result = [result, test(floor((max_index(j)-1)/5) + 1)];
        end
        %{
        result2 = [];
        num = 0;
        for j = 1:length(max_corr)
            tmp = test(floor((max_index(j)-1)/5)+1);
            if ~isempty(strfind(myarea,tmp))
                result2 = [result2,tmp];
                num = num + 1;
                if num == 8
                    break
                end
            end
        end
        %disp(eval(index))
        %disp(result)
        %disp(result2)
        %disp('-----------------------')
        %}
        for j = 1:8
            if result(j) == eval(index)
                CDF(j) = CDF(j)+ 1; 
                break
            end
        end
        %for j = 1:8
        %    if result2(j) == eval(index)
        %        CDF2(j) = CDF2(j)+ 1; 
        %        break
       %     end
       % end
    end
    sum_CDF = [0 0 0 0 0 0 0 0 0 ];
    sum_CDF2 = [0 0 0 0 0 0 0 0 0 ];
    for j = 1 : 8
        sum_CDF(j + 1) = sum_CDF(j) + CDF(j)/20;
        sum_CDF2(j + 1) = sum_CDF2(j) + CDF2(j)/20;
    end
    %sum_CDF
    plot([1,1:8], sum_CDF,  '-o', 'LineWidth',1.5);
    %plot([1,1:8], sum_CDF2, [ '--o',mycolor(index)], 'LineWidth',1.5);
    axis([1 5 0 1])  
end
ylabel('CDF%')
set(gca,'XTick',1:5);%给坐标加标签 
set(gca,'XTickLabel',{'top1','top2','top3','top4','top5'});%给坐标加标签 
legend('Y','P','M','Z','O')
%legend('R without positioning','R with positioning','N without positioning','N with positioning','O without positioning','O with positioning')
hold off



