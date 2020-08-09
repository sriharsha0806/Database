import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city = ['chicago', 'new york city', 'washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
    
    while True:
        CITY = input('\n Enter the name of the city you want to analyze?\n {}, \n'.format(' '.join(city)))
        if CITY.lower() in city:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('\n Enter the month\n {}, \n'.format(' '.join(months)))
        if month.lower().strip() in months:
            break
           

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)    
    while True:
        day = input('\n Enter the days\n {}, \n'.format(' '.join(days)))
        if day.lower().strip() in days:
            break

    print('-'*40)
    return CITY, month, day


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int        
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

    # TO DO: display the most common month
    most_common_month_index = df['Start Time'].dt.month.mode()[0]
    most_common_month = months[most_common_month_index-1].title()
    print('The most common month is', most_common_month)
    

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('The most popular weekday is', most_common_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common start hour', most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station", common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station", common_end_station)


    # TO DO: display most frequent combination of start station and end station trip
    Combination = df['Start Station']+"  --->  "+df['End Station']
    print("The most frequently start and stop stations in a trip", Combination.mode()[0], "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    
    duration = df['End Time'] - df['Start Time']
    duration_in_secs = duration.apply(lambda x:x.total_seconds())
    print("The total Travel Time amounts to", sum(duration_in_secs), "seconds\n")

    # TO DO: display mean travel time
    print("The Mean Travel Time amounts to", np.mean(duration_in_secs), "Seconds \n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The types of users are", df['User Type'].value_counts(), "\n")
    # TO DO: Display counts of gender
    # All stations does not provide gender information
    try: 
        print("Info regarding the Gender\n", df['Gender'].value_counts(), "\n")
    except:
        print("Info regarding Gender not available for this city")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print("The person with earliest Birth Year was born on", min(df['Birth Year']), "\n")
        print("The person with most recent Birth Year was born on", max(df['Birth Year']), "\n")
        print("The Most Common Year the people were born corresponds to", df['Birth Year'].mode()[0], "\n")
    except:
        print("Information regarding the Birth not available", "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print(city)
        df = load_data(city, month, day)
        original_data = input("would you like to see original data? Enter yes or no. \n").lower().strip()
        start = 0
        end = 5
        while(original_data == "yes"):
            print(df.iloc[start:end])
            start += 5
            end += 5
            original_data = input("Would you like to see original data? Enter yes or no. \n").lower().strip()
            
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
      
            
        if restart.lower().strip() != 'yes':
            break


if __name__ == "__main__":
	main()
