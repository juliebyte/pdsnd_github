import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all' ]             

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs        
    while True:
        city = input('Please enter Chicago, New York, or Washington:\n')
        city = city.lower()
        if city in CITIES:
           break

    # get user input for month (all, january, february, ... , june)       
    while True:
        month = input('\nPlease enter a month from this list, or "all" to get all months.\n January, February, March, April, May, June, or all: \n')
        month = month.lower()
        if month in MONTHS:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nPlease enter a day of the week, or "all" to get all days.\n Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or all: \n')
        day = day.lower()
        if day in DAYS:
           break

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
    # load data file into a dataframe using the city as the key to get the file name 
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if a month was specified
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # filter by day if one was specified 
    if day != 'all':
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Bikeshare Use...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month for bike use is: ", most_common_month)

    # display the most common day of week
    # Found on https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmax.html
    most_common_day = df['day_of_week'].value_counts().idxmax()
    print("The most common day of the week for bike use is: ", most_common_day)

    # display the most common start hour
    # Found on https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmax.html
    most_common_hour = df['hour'].value_counts().idxmax()
    print("The most common hour for bike use is: ", most_common_hour)

    # How long the calculation took
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # find most common station for starting the bike trip
    # Found on https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmax.html
    most_common_begin_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used station to start a bike trip: ", most_common_begin_station)

    # find most commnon station to end using a bike
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used station to end a bike trip: ", most_common_end_station)

    # find most common combination of start station and end station 
    most_common_begin_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start and end station: {}, {}"\
            .format(most_common_begin_end_station[0], most_common_begin_end_station[1]))

    # Print how long the calculation took
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time: ", total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean (average) travel time: ", mean_travel)  

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Find how many users of different types
    print("How many users of various types: \n")
    user_value_counts = df['User Type'].value_counts()
    for index, user_count in enumerate(user_value_counts):
        print("  {}: {}".format(user_value_counts.index[index], user_count))
    
    print()


    # How many of each gender
    if 'Gender' in df.columns:
        count_gender(df)

    # Display earliest, most recent, and most frequently occurring year of birth
    if 'Birth Year' in df.columns:
        count_birth_year(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def count_gender(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Count how many users of each gender
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()

    for index,gender_count   in enumerate(gender_counts):
        print("  {}: {}".format(gender_counts.index[index], gender_count))
    
    print()
    

def count_birth_year(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""
    
    birth_year = df['Birth Year']
    # The most common birth year
    most_common_year = birth_year.value_counts().idxmax()
    print("The most frequently occurring birth year:", most_common_year)
    # The most recent birth year
    most_recent_year = birth_year.max()
    print("The most recent birth year (youngest users):", most_recent_year)
    # The earliest birth year
    earliest_year = birth_year.min()
    print("The earliest birth year (oldest users):", earliest_year)



def display_raw_rows(df):
    """Displays some rows of raw bikeshare data as requested."""

    rowIndex = 0

    showRaw = input("\n Would you like to see a sample of the raw data? Type yes or no: \n").lower()
    while True:
        if showRaw == 'yes':        
            print(df[rowIndex: rowIndex + 5])
            rowIndex = rowIndex + 5
            showRaw = input("\n Would you like to see more raw data? Type yes or no: \n").lower()
        else:
            return


def main():
    """Program mainline."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
