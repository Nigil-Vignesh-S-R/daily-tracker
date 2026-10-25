import pandas as pd
import datetime as dt
import bisect
import calendar
from collections import defaultdict
def buildDataFrame(rows):
    df=pd.DataFrame(rows,columns=["habit_id","habit_name","date","completed"])
    df['date']=pd.to_datetime(df['date'])
    return df
def longestStreak(df):
    completed_days=sorted(df[df['completed']]['date'].dt.date.unique())
    if not completed_days:
        return 0,None,None
    best_len,best_start,best_end=1,completed_days[0],completed_days[0]
    cur_len,cur_start=1,completed_days[0]
    for i in range(1,len(completed_days)):
        if (completed_days[i]-completed_days[i-1]).days==1:
            cur_len+=1
        else:
            cur_len,cur_start=1,completed_days[i]
        if cur_len>best_len:
            best_len,best_start,best_end=cur_len,cur_start,completed_days[i]
    return best_len,best_start,best_end
def best_day(df,habits):
    import pandas as pd
    habits_df=pd.DataFrame(habits,columns=["habit_id","habit_name","created_at"])
    habits_df["created_at"]=pd.to_datetime(habits_df["created_at"])
    done=df[df["completed"]].groupby("date").size()
    if done.empty:
        return None,0,0
    results=[]
    for date in done.index:
        total_active=(habits_df["created_at"]<=date).sum()
        results.append((date,done[date],total_active))
    best_date,best_done,best_total=max(results,key=lambda r:(r[1],r[1]/r[2] if r[2] else 0))
    return best_date.date(),int(best_done),int(best_total)
def best_week(df,habits):
    import pandas as pd
    habits_df=pd.DataFrame(habits,columns=["habit_id","habit_name","created_at"])
    habits_df["created_at"]=pd.to_datetime(habits_df["created_at"])
    done=df[df["completed"]].groupby("date").size()
    if done.empty:
        return None,None,0
    full_range=pd.date_range(done.index.min(),done.index.max(),freq="D")
    done=done.reindex(full_range,fill_value=0)
    best_done,best_rate,best_start,best_end=-1,-1,None,None
    for end_date in full_range:
        start_date=end_date-pd.Timedelta(days=6)
        week_done=done[(done.index>=start_date)&(done.index<=end_date)].sum()
        active_per_day=[(habits_df["created_at"]<=d).sum() for d in pd.date_range(start_date,end_date,freq="D")]
        week_total=sum(active_per_day)
        if week_total==0:
            continue
        rate=week_done/week_total
        if (week_done>best_done) or (week_done==best_done and rate>best_rate):
            best_done,best_rate,best_start,best_end=week_done,rate,start_date,end_date
    if best_start is None:
        return None,None,0
    return best_start.date(),best_end.date(),round(best_rate*100)
def longest_streak_by_habit(df):
    results=[]
    for habit_id,habit_df in df.groupby("habit_id"):
        habit_name=habit_df["habit_name"].iloc[0]
        completed_days=sorted(habit_df[habit_df["completed"]]["date"].dt.date.unique())
        total_completed=len(completed_days)
        if not completed_days:
            results.append((habit_name,0,None,None,0))
            continue
        best_len,best_start,best_end=1,completed_days[0],completed_days[0]
        cur_len,cur_start=1,completed_days[0]
        for i in range(1,len(completed_days)):
            if (completed_days[i]-completed_days[i-1]).days==1:
                cur_len+=1
            else:
                cur_len,cur_start=1,completed_days[i]
            if cur_len>best_len:
                best_len,best_start,best_end=cur_len,cur_start,completed_days[i]
        results.append((habit_name,best_len,best_start,best_end,total_completed))
    return sorted(results,key=lambda r:r[1],reverse=True)
def streak_progress_over_time(df):
    completed_days=sorted(df[df["completed"]]["date"].dt.date.unique())
    if not completed_days:
        return [],[]
    full_range=pd.date_range(completed_days[0],completed_days[-1],freq="D").date
    completed_set=set(completed_days)
    streak=0
    xs,ys=[],[]
    for d in full_range:
        if d in completed_set:
            streak+=1
        else:
            streak=0
        xs.append(d)
        ys.append(streak)
    return xs,ys
def compute_stats_page(rows,habits,today):
    created=sorted(h[2] for h in habits)
    def active_on(day):
        return bisect.bisect_right(created,day)

    done_by_day=defaultdict(int)
    habit_days=defaultdict(set)
    for habit_id,_name,day,completed in rows:
        if completed:
            done_by_day[day]+=1
            habit_days[habit_id].add(day)

    # donut: today
    total=active_on(today)
    done=min(done_by_day.get(today,0),total)

    # monthly completion (last 6 months)
    months=[]
    y,m=today.year,today.month
    for _ in range(6):
        months.append((y,m))
        m-=1
        if m==0:
            m=12
            y-=1
    months.reverse()
    month_labels,month_values=[],[]
    for y,m in months:
        first=dt.date(y,m,1)
        last=min(dt.date(y,m,calendar.monthrange(y,m)[1]),today)
        possible=0
        achieved=0
        day=first
        while day<=last:
            possible+=active_on(day)
            achieved+=done_by_day.get(day,0)
            day+=dt.timedelta(days=1)
        month_labels.append(calendar.month_abbr[m])
        month_values.append(round(achieved*100/possible) if possible else 0)

    # last 7 days
    day_labels,day_values=[],[]
    for i in range(6,-1,-1):
        day=today-dt.timedelta(days=i)
        active=active_on(day)
        rate=done_by_day.get(day,0)*100/active if active else 0
        day_labels.append(day.strftime("%d %b"))
        day_values.append(round(min(rate,100)))

    # best habit this month
    month_start=today.replace(day=1)
    best=None
    for habit_id,name,created_at in habits:
        start=max(created_at,month_start)
        days=(today-start).days+1
        if days<=0:
            continue
        d=sum(1 for x in habit_days.get(habit_id,()) if start<=x<=today)
        rate=d/days
        if best is None or (rate,d)>(best[0],best[1]):
            best=(rate,d,name)

    return {"today":today,"total":total,"done":done,
            "month_labels":month_labels,"month_values":month_values,
            "day_labels":day_labels,"day_values":day_values,
            "best":(best[2],round(best[0]*100)) if best else None}