#-*- coding: UTF-8-*-
from datetime import datetime
import datetime as Datetime
from zhdate import ZhDate
tian_gan="甲乙丙丁戊己庚辛壬癸"
di_zhi="子丑寅卯辰巳午未申酉戌亥"
from skyfield import api
ts = api.load.timescale()
eph = api.load('de405.bsp')
#eph = api.load('https://github.com/skyfielders/python-skyfield/tree/master/ci/de405.bsp')
from skyfield import almanac
from skyfield import almanac_east_asia as almanac_ea
format='%Y-%m-%d %H:'

def get_jieqi(year,jieqi=None):
    
    t0 = ts.utc(year, 1, 1)
    t1 = ts.utc(year, 12, 31)
    t, tm = almanac.find_discrete(t0, t1, almanac_ea.solar_terms(eph))

    match={}
    for tmi, ti in zip(tm, t):
        match[almanac_ea.SOLAR_TERMS_ZHS[tmi]]=datetime.strptime(ti.utc_iso(' ')[0:14],format)+Datetime.timedelta(hours=8)
        #print(tmi, almanac_ea.SOLAR_TERMS_ZHS[tmi], ti.utc_iso(' '))
    #print(match)
    if jieqi==None:
        return match
    else:
        return match[jieqi]

def convert_date(input_date:datetime,output_type="char"):
    global tian_gan
    global di_zhi
    year,month,date=ZhDate.from_datetime(input_date).lunar_year,\
        ZhDate.from_datetime(input_date).lunar_month,\
        ZhDate.from_datetime(input_date).lunar_day
    day=datetime(year,month,date)
    jieqi=get_jieqi(year)
    lichun=jieqi["立春"]
    #lichun=ZhDate.from_datetime(lichun)
    if input_date<lichun:
        year-=1
    

    month_tmp=((year-4)*12+2+month)%60
    
   
    cent=input_date.year%100-1
    month_base=[0,31,-1,30,0,31,1,32,3,33,4,34]
    day_tmp=cent//4*6+5*(cent//4*3+cent%4)+month_base[input_date.month-1]+input_date.day
    if (year%4==0 and year%100!=0) or (year%400==0):
        day_tmp+=1
    
    
    hour=input_date.hour
    hour_tmp1=round((hour / 2) + 0.1) % 12
    hour_tmp2=(day_tmp%10*2+hour_tmp1-2)%10

    if output_type=="char":
        year_res=tian_gan[(year-4)%10]+di_zhi[(year-4)%12]
        month_res=tian_gan[(month_tmp%10-1)%10]+di_zhi[(month_tmp%12-1)%12]
        day_res=tian_gan[(day_tmp%10-1)%10]+di_zhi[(day_tmp%12-1)%12]
        hour_res=tian_gan[hour_tmp2]+di_zhi[hour_tmp1]
    else:
        year_res=[(year-4)%10,(year-4)%12]        
        month_res=[(month_tmp%10-1)%10,(month_tmp%12-1)%12]
        day_res=[(day_tmp%10-1)%10,(day_tmp%12-1)%12]
        hour_res=[hour_tmp2,hour_tmp1]

    return year_res,month_res,day_res,hour_res
    
if __name__=="__main__":
    date=datetime(2023,11,11,11,10)
    zh_date=ZhDate.from_datetime(date)
    print(zh_date)
    print(convert_date(date))