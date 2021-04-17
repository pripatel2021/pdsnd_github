import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

month_name = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

day_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    try:
        city = input(
            " which city analysis you would like to do? - chicago, new york city, washington\n").lower()
        while city not in CITY_DATA:
            print(
                "City you selected is not correct. Please  select one of the citities in the list -  chicago, new york city, washington")
            city = input(
                " please enter one of the city names in list to analyze bikeshare data - chicago, new york city, washington\n").lower()

        print('You selected city: ', city)

        # get user input for month (all, january, february, ... , june)
        month = input(
            "please enter one of the months in the list to analyze bikeshare data- all, january, february, march, april, may, june\n").lower()
        while month not in month_name:
            print(
                "month you selected is not valid. Please select one in the list - all, january, february, march, april, may, june")
            month = input(
                "please enter one of the months in the list to analyze bikeshare data- all, january, february, march, april, may, june\n").lower()
        print('You selected month: ', month)

        day = input(
            'Please enter day you would like to analyze bikeshare data - all, monday, tuesday, wednesday, thursday, friday, saturday, sunday\n').lower()
        while day not in day_of_week:
            print(
                'Day you entered is not valid. Please enter day in the list - - all, monday, tuesday, wednesday, thursday, friday, saturday, sunday')
            day = input(
                'Please enter day you would like to analyze bikeshare data - all, monday, tuesday, wednesday, thursday, friday, saturday, sunday\n').lower()

        print('your selected day: ', day)

        return city, month, day

    except Exception as e:
        print('There was error with your input values: {}'.format(e))
    print('-' * 40)


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
    try:
        df = pd.read_csv(CITY_DATA[city])

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()
        df['hour'] = df['Start Time'].dt.hour

        # filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = month_name.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
        return df
    except Exception as e:
        print('Error occured while loading file: {}'.format(e))


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    try:
        start_time = time.time()

        # display the most common month
        common_month = df['month'].mode()[0]
        print('common Month:', common_month)

        # display the most common day of week
        common_day_of_week = df['day_of_week'].mode()[0]
        print('common Day Of Week:', common_day_of_week)

        # display the most common start hour
        common_start_hour = df['hour'].mode()[0]
        print('Most Common Start Hour:', common_start_hour)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
    except Exception as e:
        print("error getting time stats for bikeshare data {}".format(e))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    try:
        start_time = time.time()

        # display most commonly used start station
        common_start_station = df['Start Station'].mode()[0]
        print('Common Start Station:', common_start_station)

        # display most commonly used end station
        common_end_station = df['End Station'].mode()[0]
        print('Common End Station:', common_end_station)

        # display most frequent combination of start station and end station trip
        frequent_trip = df.loc[:, 'Start Station':'End Station'].mode()[0:]
        print('most frequent combination of start and end station trip - ', frequent_trip)

        frequent_trip_duration = df.groupby(["Start Station", "End Station"]).size().max()
        print('most frequent duration trip - ', frequent_trip_duration)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
    except Exception as e:
        print("Error getting station stats for the bikeshare data {}".format(e))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    try:
        start_time = time.time()

        # display total travel time
        total_travel_time = df['Trip Duration'].sum()
        print('Total Travel Time:', total_travel_time)

        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print('Mean Travel Time:', mean_travel_time)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)
    except Exception as e:
        print("Error getting trip duration for bikeshare data {}".format(e))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    try:
        start_time = time.time()

        # Display counts of user types

        user_types = df['User Type'].value_counts()
        print('User Type count: ', user_types)
    except Exception as e:
        print("\nNo data available for user stats for the bikeshare data {}".format(e))

    # Display counts of gender

    try:
        gender_types = df['Gender'].value_counts()
        print('Gender Type Count: ', gender_types)
    except Exception as e:
        print("\nNo data available for gender types {}".format(e))

    # Display earliest, most recent, and most common year of birth

    try:
        earliest_birth_year = df['Birth Year'].min()
        print('\nearliest Year of birth:', earliest_birth_year)
    except Exception as e:
        print("\nNo data available for earliest birth date {}".format(e))

    try:
        recent_birth_Year = df['Birth Year'].max()
        print('\nRecent birth year:', recent_birth_Year)
    except Exception as e:
        print("\nNo data available for recent birth year {}".format(e))

    try:
        most_common_year = df['Birth Year'].mode()[0]
        print('\nMost Common Birth Year:', most_common_year)
    except Exception as e:
        print("\nNo data available for most common year {}".format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    index = 0
    try:
        user_input = input('would you like to display 5 rows of raw data? Enter yes or no\n').lower()
        while user_input in ['yes', 'y', 'yep', 'yea', 'yup'] and index + 5 < df.shape[0]:
            print(df.iloc[index:index + 5])
            index += 5
            break
        user_input = input('would you like to display 5 rows of raw data? Enter yes or no\n ').lower()

        return
    except Exception as e:
        print('There was error displaying data: {}'.format(e))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
