function r = mymatch( a ,b )
%UNTITLED �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
L= length(a);
match = 0;
for i = 1: L
    if (a(i) == b(i))
        match = match + 1;
    end
end
r = match / L;
end

