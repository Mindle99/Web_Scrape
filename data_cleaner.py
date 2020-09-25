import pandas as pd 
import numpy as np 
import re 

df = pd.read_csv('indeed_jobs.csv')

df = df.drop_duplicates()
df.reset_index(drop=True, inplace=True)

df['Salary'] = df['Salary'].apply(lambda x: x.replace('\n','').replace(',','').replace('$',''))

df["salary_period"] = np.nan

df.loc[df["Salary"].str.contains("year"),"salary_period"] = "year"
df.loc[df["Salary"].str.contains("month"),"salary_period"] = "month"
df.loc[df["Salary"].str.contains("week"),"salary_period"] = "week"
df.loc[df["Salary"].str.contains("day"),"salary_period"] = "day"
df.loc[df["Salary"].str.contains("hour"),"salary_period"] = "hour"

# Salary Parsing
df['hourly'] = df['Salary'].apply(lambda x: 1 if 'an hour' in x.lower() else 0)
df['monthly'] = df['Salary'].apply(lambda x: 1 if 'a month' in x.lower() else 0)
df['daily'] = df['Salary'].apply(lambda x: 1 if 'a day' in x.lower() else 0)

#################################################################################
# Replacing the 'None' variables with NaN values

df['Rating'] = df['Rating'].replace(r'None', np.NaN, regex=True)
df['Salary'] = df['Salary'].replace(r'None', np.NaN, regex=True)

#################################################################################

sal_data = df[df["Salary"].notnull()]

year_sal = sal_data[sal_data["Salary"].str.contains("year")]
month_sal = sal_data[sal_data["Salary"].str.contains("month")]
day_sal = sal_data[sal_data["Salary"].str.contains("day")]
hour_sal = sal_data[sal_data["Salary"].str.contains("hour")]

year_sal["Salary"] = year_sal["Salary"].apply(lambda x: x.replace("a year",""))
month_sal["Salary"] = month_sal["Salary"].apply(lambda x: x.replace("a month"," "))
day_sal["Salary"] = day_sal["Salary"].apply(lambda x: x.replace("a day"," "))
hour_sal["Salary"] = hour_sal["Salary"].apply(lambda x: x.replace("an hour"," "))

def format_salary(i):
    try:
        split = i.split("-")
        salary_min = float(split[0])
        salary_max = float(split[1])
        return (salary_min + salary_max)/2
    except:
        return float(i)

def min_sal(i):
    try:
        split = i.split("-")
        salary_min = float(split[0])
        return salary_min
    except:
        return float(i)

def max_sal(i):
    try:
        split = i.split("-")
        salary_max = float(split[1])
        return salary_max
    except:
        return float(i)

# Applying the functions made
year_sal["Average_Salary"] = year_sal["Salary"].apply(format_salary)
year_sal["Min_Salary"] = year_sal["Salary"].apply(min_sal)
year_sal["Max_Salary"] = year_sal["Salary"].apply(max_sal)

month_sal["Average_Salary"] = month_sal["Salary"].apply(format_salary) * 12
month_sal["Min_Salary"] = month_sal["Salary"].apply(min_sal) * 12
month_sal["Max_Salary"] = month_sal["Salary"].apply(max_sal) * 12

day_sal["Average_Salary"] = day_sal["Salary"].apply(format_salary) * 260
day_sal["Min_Salary"] = day_sal["Salary"].apply(min_sal) * 260 
day_sal["Max_SSalary"] = day_sal["Salary"].apply(max_sal) * 260

hour_sal["Average_Salary"] = hour_sal["Salary"].apply(format_salary) * 2080
hour_sal["Min_Salary"] = hour_sal["Salary"].apply(min_sal) * 2080 
hour_sal["Max_Salary"] = hour_sal["Salary"].apply(max_sal) * 2080 

rating = df['Rating']
df['Rating'] = rating.apply(lambda x: float(x))

combined_sal = pd.concat([year_sal, month_sal, day_sal, hour_sal], axis=0)

df = pd.concat([df, combined_sal], axis=0)

df["Description"] = df["Description"].apply(lambda x: x.replace("\n"," "))

#parsing of job description (python, etc.)

#python
df['python_yn'] = df['Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
 
#r studio 
df['R_yn'] = df['Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.R_yn.value_counts()

#spark 
df['spark'] = df['Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()

#aws 
df['aws'] = df['Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()

#excel
df['excel'] = df['Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel.value_counts()

df.to_csv('indeed_salary_data.csv',index = False)