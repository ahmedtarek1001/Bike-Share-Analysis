import time
import pandas as pd

# Define constants for city data file paths
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Valid options for months and days to ensure consistent input
VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
VALID_DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def validate_input(prompt, valid_options):
    """
    Prompts the user for input and validates it against a list of valid options.

    Args:
        prompt (str): The message displayed to the user.
        valid_options (list): A list of valid inputs.

    Returns:
        str: Validated user input.
    """
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please choose from: {', '.join(valid_options)}")

def get_filters():
    """
    Prompts the user to specify a city, month, and day for filtering the data.

    Returns:
        str: Selected city.
        str: Selected month.
        str: Selected day.
    """
    print("Welcome! Let's explore US Bikeshare data!")
    # Prompt user to choose a city from the available options
    city = validate_input("Choose a city (chicago, new york city, washington): ", CITY_DATA.keys())
    # Prompt user to choose a month to filter by, or "all" for no filter
    month = validate_input("Choose a month (january to june) or 'all': ", VALID_MONTHS)
    # Prompt user to choose a day of the week to filter by, or "all" for no filter
    day = validate_input("Choose a day (sunday to saturday) or 'all': ", VALID_DAYS)
    return city, month, day

def load_data(city, month, day):
    """
    Loads bikeshare data for the specified city and applies month and day filters.

    Args:
        city (str): Selected city.
        month (str): Selected month.
        day (str): Selected day of the week.

    Returns:
        DataFrame: Filtered dataset.
    """
    # Read the dataset for the selected city
    df = pd.read_csv(CITY_DATA[city])
    # Convert 'Start Time' column to datetime for easier analysis
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract month, day of week, and hour from 'Start Time'
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Filter dataset by month if a specific month is chosen
    if month != 'all':
        df = df[df['month'] == month]
    # Filter dataset by day if a specific day is chosen
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def display_time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df (DataFrame): Filtered dataset.
    """
    print("\nCalculating the most frequent times of travel...\n")
    start_time = time.time()
    # Find and display the most common month of travel
    print("Most Common Month:", df['month'].mode()[0])
    # Find and display the most common day of travel
    print("Most Common Day of Week:", df['day_of_week'].mode()[0])
    # Find and display the most common hour of travel
    print("Most Common Start Hour:", df['hour'].mode()[0])
    print(f"\nThis took {time.time() - start_time:.2f} seconds.\n{'-' * 40}")

def display_station_stats(df):
    """
    Displays statistics on the most popular stations and trips.

    Args:
        df (DataFrame): Filtered dataset.
    """
    print("\nCalculating the most popular stations and trips...\n")
    start_time = time.time()
    # Find and display the most commonly used start station
    print("Most Common Start Station:", df['Start Station'].mode()[0])
    # Find and display the most commonly used end station
    print("Most Common End Station:", df['End Station'].mode()[0])
    # Find and display the most frequent combination of start and end stations
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("Most Frequent Trip:", most_common_trip)
    print(f"\nThis took {time.time() - start_time:.2f} seconds.\n{'-' * 40}")

def display_trip_duration_stats(df):
    """
    Displays statistics on trip durations.

    Args:
        df (DataFrame): Filtered dataset.
    """
    print("\nCalculating trip duration statistics...\n")
    start_time = time.time()
    # Calculate and display the total travel time
    print("Total Travel Time (seconds):", df['Trip Duration'].sum())
    # Calculate and display the average travel time
    print("Average Travel Time (seconds):", df['Trip Duration'].mean())
    print(f"\nThis took {time.time() - start_time:.2f} seconds.\n{'-' * 40}")

def display_user_stats(df, city):
    """
    Displays statistics on bikeshare users.

    Args:
        df (DataFrame): Filtered dataset.
        city (str): Selected city (used to handle missing data for Washington).
    """
    print("\nCalculating user statistics...\n")
    start_time = time.time()
    # Display user type breakdown
    print("User Types:\n", df['User Type'].value_counts())
    # For cities other than Washington, display additional user stats
    if city != 'washington':
        print("Gender Breakdown:\n", df['Gender'].value_counts())
        print("Earliest Birth Year:", int(df['Birth Year'].min()))
        print("Most Recent Birth Year:", int(df['Birth Year'].max()))
        print("Most Common Birth Year:", int(df['Birth Year'].mode()[0]))
    else:
        print("No gender or birth year data available for Washington.")
    print(f"\nThis took {time.time() - start_time:.2f} seconds.\n{'-' * 40}")

def display_raw_data(df):
    """
    Displays raw data rows in chunks of 5 upon user request.

    Args:
        df (DataFrame): Filtered dataset.
    """
    start = 0
    while True:
        # Prompt user if they want to view raw data
        display = validate_input("Would you like to see 5 rows of raw data? (yes/no): ", ['yes', 'no'])
        if display == 'yes':
            # Display 5 rows of raw data at a time
            print(df.iloc[start:start + 5])
            start += 5
        else:
            break

def main():
    """
    Main program loop to execute the bikeshare analysis.
    """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_time_stats(df)
        display_station_stats(df)
        display_trip_duration_stats(df)
        display_user_stats(df, city)
        display_raw_data(df)
        # Prompt user to restart the program
        restart = validate_input("Would you like to restart? (yes/no): ", ['yes', 'no'])
        if restart != 'yes':
            print("Thank you for exploring the data. Goodbye!")
            break

# Run the program only if this script is executed directly
if __name__ == "__main__":
    main()
