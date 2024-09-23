import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

Data = pd.read_csv('LifeTrack White Stork Tunisia.csv')
Data = Data[['event-id', 'timestamp', 'location-long', 'location-lat', 'ground-speed', 'tag-local-identifier']]

Tags = pd.unique(Data['tag-local-identifier'])

Data = Data[~np.isnan(Data['location-long'])]
Data = Data[~np.isnan(Data['location-lat'])]


def PlotMeanSpeeds():
    OneDay = dt.timedelta(days=1)
    Timestamps = [dt.datetime.strptime(time[:-4], '%Y-%m-%d %H:%M:%S') for time in Data['timestamp']]

    TimeDifference = [time - Timestamps[0] for time in Timestamps] # The time since the first timestamp
    Days = [int(time / OneDay) for time in TimeDifference] # Days passed since the first timestamp
    Data['Day'] = Days

    plt.figure(figsize=(40, 40))
    for j, tag in enumerate(Tags):
        TagData = Data[Data['tag-local-identifier'] == tag]

        TagData = TagData[~np.isnan(TagData['ground-speed'])]
        
        Day = 1
        Index = []
        DailyMeanSpeed = []
        for i in range(len(TagData)):
            if TagData.iloc[i]['Day'] < Day:
                Index.append(i)
            else:
                DailyMeanSpeed.append(np.mean(TagData['ground-speed'].iloc[Index]))
                Index = [i]
                Day += 1

        plt.subplot(3, 3, j+1)
        plt.plot(DailyMeanSpeed)
        plt.xlabel('Days')
        plt.ylabel('Mean Speed')
        plt.title('Daily Mean Speeds of ' + str(tag))
        plt.grid()

    plt.savefig('Daily Mean Speed White Stork.pdf')


def PlotMigration():
    proj = ccrs.Mercator()
    plt.figure()
    ax = plt.axes(projection=proj)
    ax.set_extent((-10.0, 40.0, 0.0, 40.0))
    # Adding land, oceans, borders and coastlines to the map
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    for i, tag in enumerate(Tags): 
        TagData = Data[Data['tag-local-identifier'] == tag]
        x = TagData['location-long']
        y = TagData['location-lat']
        ax.plot(x, y, '.', transform=ccrs.Geodetic(), label=tag)

    plt.title("Migration Map")
    plt.legend()
    plt.savefig('White Stork Migration.pdf')
