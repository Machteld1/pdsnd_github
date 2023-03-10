import time
import datetime
import pandas as pd
import numpy as np

valid_cities = ('chicago','new york city','washington')
valid_months = ('january','february','march', 'april', 'may', 'june', 'all')
valid_days = ('monday','tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #mf1
    while True:
        city = input('Pls enter the name of the city you are interested in: ').lower()
        if city in valid_cities:
                break
        else:
                print('That\'s not a valid entry, pls try again!')
    print('City selected: ', city)
   
    while True:
        month = input('Pls enter the month you are interested in or enter "all": ').lower()
        if month in valid_months:
            break
        else:
            print('That\'s not a valid entry, pls try again!')
    print('Month selected: ', month)
    
    while True:
        day = input('Pls enter the day you are interested in or enter "all": ').lower()
        if day in valid_days:
            break
        else:
            print('That\'s not a valid entry, pls try again!')
    print('Day selected: ', day)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    month_name_mapping = {
        1: 'january',
        2: 'february',
        3: 'march',
        4: 'april',
        5: 'may',
        6: 'june'
    }
    day_name_mapping = {
        0: 'monday',
        1: 'tuesday',
        2: 'wednesday',
        3: 'thursday',
        4: 'friday',
        5: 'saturday',
        6: 'sunday'
    }
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    #convert time columns to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    #add column month starting with january equal 1 and june equal 6, map to input values
    df['Start_Month'] = df['Start Time'].dt.month
    df['Start_Month_name'] = df['Start_Month'].map(month_name_mapping)
    
    #add column day_of_week, starting with monday equal 0 and sunday equal 6, map to input values
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['day_of_week_name'] = df['day_of_week'].map(day_name_mapping)
    #print('Example rows:\n', df.head(100))
    #Apply filters for month and date
    if month != 'all':
        df = df[(df['Start_Month_name'] == month)]
    if day != 'all':
        df = df[(df['day_of_week_name'] == day)]

    print(df.head(100))
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df['Start_Month_name'].mode()[0]
    print('Most common month:', common_month)
    
    # display the most common day of week
    
    common_weekday = df['day_of_week_name'].mode()[0]
    print('Most common day of week:', common_weekday)
    
    # display the most common start hour
    
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common start_hour:', common_hour)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common Start Station: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common End Station: ', common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_station_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most Frequent combination of Start and End Station: ', most_frequent_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Travel_Time_s'] = (df['End Time'] - df['Start Time']).dt.total_seconds()
    df['Travel_Time_h'] = (df['End Time'] - df['Start Time']).dt.total_seconds() / 3600
    # display total travel time
    print(f"Total Travel Time: {round(df['Travel_Time_h'].sum(), 2)} h")

    # display mean travel time
    print(f"Average Travel Time: {round(df['Travel_Time_h'].mean(), 2)} h")

    #print(df.describe())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    # Display counts of gender
    # Column 'Gender' missing for Washington!!
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender)
    
    # Display earliest, most recent, and most common year of birth
    # Column 'Birth Year' missing for Washington!!
    if 'Birth Year' in df.columns:
        earliest_yob = int(df['Birth Year'].min())
        print('Earliest year of birth: ',earliest_yob)
        latest_yob = int(df['Birth Year'].max())
        print('Most recent year of birth: ',latest_yob)
        common_yob = int(df['Birth Year'].mode()[0])
        print('Most common year of birth: ',common_yob)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Asks user whether 5 rows of raw data should be displayed. Loop till user answers 'no'"""
    start_loc = 0
    valid_answers = ('yes','no')
    display_rows = ('no')
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if view_data in valid_answers:
                break
        else:
                print('That\'s not a valid entry, pls try again!')

    while True:
        if view_data in display_rows:
            break
        else:
            if start_loc < df.shape[0]:
                print(df.iloc[start_loc:start_loc + 5])
                start_loc += 5
                continue_view = input("Do you wish to continue?: ").lower()
                if continue_view in display_rows:
                    break
                else:
                    print(df.iloc[start_loc:start_loc + 5])
            else:
                break
                
            

                
                
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #mf
        raw_data(df)
        #mf
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
