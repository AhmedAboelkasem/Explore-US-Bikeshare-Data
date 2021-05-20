import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def check (f_input, type):
    """check user input validation"""
    while True:
        ch_input = input(f_input).lower()
        try:
            if ch_input in ["chicago", "new york city", "washington"] and type == 201:
                break
            elif ch_input in ["january", "february", "march", "april", "may", "june","all"] and type == 202:
                break
            elif ch_input in ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"] and type == 203:
                break
            else:
                if type == 201:
                    print("Please,you should enter one of these cities : Chicago, New york city, Washington")
                if type == 202:
                    print("Please,you should enter the month from january to june or all [january, february, march, april, may, june]")
                if type == 203:
                    print("Please,you should enter the day or all [saturday, sunday, monday, tuesday, wednesday, thursday, friday]")
        except ValueError:
            print("sorry, you entered invalid input")
    return ch_input
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check("Enter one of these cities: chicago, new york city, washington :", 201)
    # TO DO: get user input for month (all, january, february, ... , june)
    month = check("Enter the month from january to june or all :", 202)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = check("Enter the day or all :", 203)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: {}'.format(common_month))
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is: {}'.format(common_day))
    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('The most common hour is: {}'.format(common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common Start Station is: {}'.format(common_start_station))
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common End Station is: {}'.format(popular_end_station))
    # display most frequent combination of start station and end station trip
    group_field = df.groupby(['Start Station', 'End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print("most frequent combination of start station and end station : {}".format(popular_combination_station))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is:', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Count of user types:\n{0}\n{1}\n{0}\n".format('-' * 20, user_types.to_string()))
    if 'Gender' in df:
        user_genders = df['Gender'].value_counts()
        print("Count of gender:\n{0}\n{1}\n{0}\n".format('-' * 20, user_genders.to_string()))
    else:
        print("There is no Gender data to display for chosen city")
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_year = df['Birth Year']
        earliest_year_of_birth = int(birth_year.min())
        mostrecent_year_of_birth = int(birth_year.max())
        common_year_of_birth = int(birth_year.mode()[0])
        # year data was collected to calculate age
        data_collection_year = 2017
        print("Earliest year of birth:    {} ( eldest user was {} )".format(earliest_year_of_birth, data_collection_year - earliest_year_of_birth))
        print("Most recent year of birth: {} ( youngest user was {} )".format(mostrecent_year_of_birth, data_collection_year - mostrecent_year_of_birth))
        print("Most common year of birth: {} ( most common age {} )".format(common_year_of_birth, data_collection_year - common_year_of_birth))
    else:
        print("There no Birth Year data to display for chosen city")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)



def display_raw_data(df):
    """Displays raw data in batch of 5 upon user request."""
    row = 0
    reviewanswer = input('\nWould you like to see sample raw data ? (y)es or anything else for no.\n')
    while reviewanswer.lower() == 'yes' or reviewanswer.lower() == 'y':
        dfslice = df.iloc[row:row + 5]
        # check if end of data is reached, if so,  exit the loop
        if dfslice.empty:
            print('no more data to display!')
            break
        else:
            print(dfslice)
            morereview = input('\nType (y)es if you would you like to see more sample raw data or type anything else for no \n')
            if morereview.lower() != 'y' and morereview.lower() != 'yes':
                break
            else:
                row += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

