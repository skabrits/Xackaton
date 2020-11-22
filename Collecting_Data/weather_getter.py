import requests
res = requests.get("https://msk.nuipogoda.ru/апрель-2019")
k = res.text
import requests
yearnow = 2020#сегодняшняя дата
monthnow = 11#сегодняшняя дата
numyear = 2020#начиная с
rain = []#осадки список
temp = []#температура список
url = "http://www.pogodaiklimat.ru/monitor.php?id=27612&month=1&year=2020"# нужно будет убрать, конечно
#Это вычисляет адрес страницы:
while (numyear<=yearnow):
    strnumyear = str(numyear)
    if numyear==yearnow:
        tr = monthnow+1
    else:
        tr = 12
    for i in range(1,tr):
        nummonth = i
        strnummonth = str(nummonth)
        url1 = "&month="+ strnummonth
        url2 = "&year="+ strnumyear
        url = "http://www.pogodaiklimat.ru/monitor.php?id=27612"+url1+url2
        res = requests.get(url)
        #штука для поиска циферок, -, + в строке:
        setnum = set()
        setnum = {'1','2','3','4','5','6','7','8','9','-','+','0'}
        if res.status_code==200:
            k = res.text
            #print(k)
            ind1 = k.find("<td>1</td>")
            ind2 = k.find("</table>",ind1)
            if ind1>=ind2:
                print('error,no data')
            else:
                s = k[ind1:ind2]#строка с мусором и данными
                #print(s)
                ind = 0
                lasso = 0 # счетчик от 0 до 6: число, мин .температура, ср. температура ..., осадки
                data2 = []#осадки
                data1 = []#ср. температура
                indi = 0
                while indi<len(s):
                    if lasso == 6:
                        lasso = 0
                    if (s[indi]=='-'and s[indi+1] in setnum) or (s[indi]!='-' and s[indi] in setnum):
                        lasso+=1
                        num = ''
                        while s[indi]!='<':
                            num = num+s[indi]
                            indi+=1
                        if lasso==3:
                            data1.append(float(num))
                        elif lasso==6:
                            data2.append(float(num))
                    indi+=1
        temp.append(data1)
        rain.append(data2)
    numyear += 1