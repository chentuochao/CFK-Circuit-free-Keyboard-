function r = mymatch( a ,b )
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明
L= length(a);
match = 0;
for i = 1: L
    if (a(i) == b(i))
        match = match + 1;
    end
end
r = match / L;
end

