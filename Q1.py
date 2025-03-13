"""Part 5 Tutorial Questions

The following are based on the Australian Tourism Dataset used in:

Hyndman, Rob J., Roman A. Ahmed, George Athanasopoulos, and Han Lin Shang. 2011. “Optimal Combination Forecasts for Hierarchical Time Series.” Computational Statistics & Data Analysis 55 (9): 2579–89..
Hollyman, Ross, Fotios Petropoulos, and Michael E. Tipping. 2021. “Understanding Forecast Reconciliation.” European Journal of Operational Research 294 (1): 149–60.

Amongst several others papers.

The data represent the number of overnight stays for domestic travel in Australia at monthly frequency.

1.	Open the dataset in excel and note carefully the format of the file
2.	Load the data into a Pandas DataFrame called 'oztour'
3.	Introduce a new date based index for the 'oztour' DataFrame:
    - This will require a few steps... it is good practice to work out what these are...
    (hint: check out the keyword arguments to the pd.Series.fillna(), then use pd.to_datetime)
    Convert the existing date information into a pandas period index (which represents the whole month rather than just a point in time)
    Set the dataframe index to take these values
4.	The column names indicate Geographic States, Zones and Regions of Australia (first three letters respectively)
    and the purpose of travel. Using the pd.groupby() command:
    a.	Report a DataFrame 'PoT' showing the data summed by purpose of travel, assign the resulting DataFrame
    b.	Report a DataFrame 'State' showing the data summed by state
    c.	Report a DataFrame 'PoT_State' showing summed by state and purpose of travel
5.	Report a DataFrame 'corr_mat' containing the correlation matrix of the data series summed by state and purpose of travel, rounded to 2 decimal places.
    (hint Pandas has commands for both steps)
6.	Report a DataFrame 'PoT_State_By_Year' containing the data summed by state and purpose of travel, as above,
    then further aggregated by Calendar Year.
7.	An alternative approach is to aggregate the data over time using the pd.resample() command.
    a.	Plot the monthly data summed by purpose of travel using df.plot() (more on this next week!)
    b.	Reseample the data to Quarterly and Yearly frequency using df.resample(‘Q’) and df.resample(‘Y’) commands. Plot both charts.
    c.	Which chart makes the trends (as opposed to the seasonality) in the data easier to see?"""


import pandas as pd
import matplotlib.pyplot as plt


file_path = "TourismData_v3.csv"  
oztour = pd.read_csv(file_path)


oztour['Year'] = oztour['Year'].ffill()



list_comp = [oztour['Month'][i] + '-' + str(int(oztour['Year'][i])) for i in oztour.index]
di = pd.to_datetime(list_comp).to_period('M')
oztour.set_index(di,inplace=True)
oztour.drop(['Year','Month'],axis=1,inplace=True)



grouper = [i[3:] for i in oztour.columns]
PoT = oztour.T.groupby(grouper).sum().T
State = oztour.T.groupby([i[0] for i in oztour.columns]).sum().T
PoT_State = oztour.T.groupby([i[1] + i[3:] for i in oztour.columns]).sum().T


print(PoT_State)



state_pot = oztour.groupby([i[1]+i[3:] for i in oztour.columns],axis=1).sum()
corr_mat = PoT_State.corr().round(2)
print(corr_mat)


PoT_State_By_Year = state_pot.groupby(state_pot.index.year,axis=0).sum()
print(PoT_State_By_Year)


