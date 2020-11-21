import requests
res = requests.get("https://msk.nuipogoda.ru/апрель-2019")
k = res.text
ind1 = k.find("<tbody class=\"tbody-forecast\"><tr>")#выделение строки с данными о месяце
ind2 = k.find("</table></div>",ind1,len(k))
#print(k[ind1:ind2])
data1 = []#гроза, облачно, ...
data2 = []#температура
s = k[ind1:ind2]#строка с данными
i1 = -1
i2 = -1
r = 1
i = 0
while(r==1):
        i1 = s.find("<td time=",i1+1,len(s))
        i2 = s.find("</a></td>",i2+1,len(s))
        if i1!=-1:
            s1 = s[i1:i2]#строка содержащая инфу об одном дне
            #print(s1)
            indata1 = s1.find("title=")
            indata2 = s1.find(">",indata1,len(s1))
            data1.append(s1[indata1+7:indata2-1])
            #print(data1)
        if i1==-1: r = 0
print(data1)