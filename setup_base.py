from datetime import datetime
import datetime as Datetime
from zhdate import ZhDate
from math import gcd
from gan_zhi import convert_date,get_jieqi
tian_gan="甲乙丙丁戊己庚辛壬癸"
di_zhi="子丑寅卯辰巳午未申酉戌亥"
yuan=list("子午卯酉寅申巳亥辰戌丑未")
jieqi_table=[ '立冬', '小雪', '大雪', '冬至','小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降']
gua="乾坎艮震巽离坤兑"
base_table=[693,582,471,174,285,396,852,963,174,396,417,528,417,528,639,936,825,714,258,147,936,714,693,582]


def bringup(input_date:datetime):
    jieqi=get_jieqi(input_date.year)
    zh_date=datetime(ZhDate.from_datetime(input_date).lunar_year,\
        ZhDate.from_datetime(input_date).lunar_month,\
        ZhDate.from_datetime(input_date).lunar_day)

    res=convert_date(input_date,"nums")

    #符头
    header=res[2][0]*res[2][1]//gcd(res[2][0],res[2][1])-(res[2][0]*res[2][1]//gcd(res[2][0],res[2][1]))%5
    #header_char=tian_gan[header%10]+di_zhi[header%12]


    ls1=list(jieqi.values())
    ls2=list(jieqi.keys())
    base_indx0=-1
    for i in range(0,len(ls1)-1):
        if ls1[i]<input_date and ls1[i+1]>input_date:
            base_indx0=i
            break
    base_char=ls2[base_indx0]
    base_indx=jieqi_table.index(base_char)
    my_gua=gua[base_indx//3]
    tmp_base=base_table[base_indx]
    num=[tmp_base//100,tmp_base//10-10*(tmp_base//100),tmp_base%10]
    num_indx=yuan.index(di_zhi[header%12])
    num_chosn=num[num_indx//4]
    yin_yang=(input_date>jieqi["夏至"])#False=阳 True=阴
    #地盘完成
    tmp=gcd(res[3][0],res[3][1])
    xun_shou=[int(res[3][0]*res[3][1]/gcd(res[3][0],res[3][1])//10)*10,\
        int(res[3][0]*res[3][1]/gcd(res[3][0],res[3][1])//10)+4] #旬首
    #xunshou_char=tian_gan[xun_shou[0]%10]+di_zhi[xun_shou[0]%12]+tian_gan[xun_shou[1]]
    

    return 0

if __name__=="__main__":
    date=datetime(2020,5,27,11,21)
    #('癸卯', '壬戌', '癸酉', '戊午')
    bringup(date)