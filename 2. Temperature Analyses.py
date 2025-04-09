import csv  # Used to read CSV files
import urllib.request  # Used to fetch files from URLs
from io import StringIO  # Used to treat string data as a file-like object

"""Aims:
1. Calculate average temperatures for each season across all years and save to 'average_temp.txt'.
2. Identify station(s) with the largest temperature range using the 'STATION_NAME' column and save to 'largest_temp_range_station.txt'.
3. Find the warmest and coolest stations based on average temperature and save to 'warmest_and_coolest_station.txt'.
"""


def find_season(month_name):
    # Dictionary mapping months to seasons 
    seasons = {
        'December': 'Summer', 'January': 'Summer', 'February': 'Summer',  # Summer months
        'March': 'Autumn', 'April': 'Autumn', 'May': 'Autumn',  # Autumn months
        'June': 'Winter', 'July': 'Winter', 'August': 'Winter',  # Winter months
        'September': 'Spring', 'October': 'Spring', 'November': 'Spring'  # Spring months
    }
    return seasons.get(month_name)  # Returns season or None if month_name not found


def process_temperature_data(file_urls):

    # List of all months to iterate over in each CSV row
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    # Dictionary to store seasonal sums and counts for averaging later with 'sum' (total temp) and 'count' (number of temps)
    seasonal_data = {season: {"sum": 0, "count": 0} for season in ["Summer", "Autumn", "Winter", "Spring"]}

    # Dictionary to track min and max temperatures for each station to calculate range 
    station_temp_ranges = {}

    # Dictionary to track sum and count of temperatures for each station to calculate averages with 'sum' (total temp) and 'count' (number of temps)
    station_averages = {}

    total_files = len(file_urls)  # Total number of files for progress tracking
    for i, url in enumerate(file_urls, 1):  # Loop through each URL with index starting at 1
        print(f"Processing file {i}/{total_files}: {url}")  # Show progress
        try:
            # Fetch the CSV file from the URL
            with urllib.request.urlopen(url) as response:
                file_content = response.read().decode('utf-8')  # Read and decode file content
                file = StringIO(file_content)  # Convert string to file-like object
                reader = csv.DictReader(file)  # Create a CSV reader that treats rows as dictionaries

                # Check if 'STATION_NAME' column exists in the CSV
                if 'STATION_NAME' not in reader.fieldnames:
                    print(f"Warning: 'STATION_NAME' column missing in {url}. Skipping.")
                    continue  # Skip this file if column is missing

                # Process each row in the CSV
                for row in reader:
                    station = row['STATION_NAME'].strip()  # Get station name and remove whitespace
                    if not station:  # Check for empty station names
                        print(f"Warning: Empty station name in {url}. Skipping row.")
                        continue  # Skip this row

                    # Initialize dictionaries for this station if not already present
                    if station not in station_temp_ranges:
                        station_temp_ranges[station] = {"min": float('inf'), "max": float('-inf')}
                    if station not in station_averages:
                        station_averages[station] = {"sum": 0, "count": 0}

                    # Process each month’s temperature in the row
                    for month in months:
                        try:
                            temp = float(row[month])  # Convert temperature to float
                            season = find_season(month)  # Get the season for this month
                            if season:  # If a valid season is returned
                                seasonal_data[season]["sum"] += temp  # Add to season total
                                seasonal_data[season]["count"] += 1  # Increment season count

                            # Update min/max for temperature range
                            station_temp_ranges[station]["min"] = min(station_temp_ranges[station]["min"], temp)
                            station_temp_ranges[station]["max"] = max(station_temp_ranges[station]["max"], temp)

                            # Update sum and count for station average
                            station_averages[station]["sum"] += temp
                            station_averages[station]["count"] += 1

                        except (ValueError, KeyError):
                            continue  # Skip invalid or missing temperature data silently

        except urllib.error.URLError as e:
            print(f"Failed to fetch {url}: {e}")  # Handle URL fetch errors
            continue  # Skip to next file

    # Calculate seasonal averages
    seasonal_averages = {}
    for season, data in seasonal_data.items():
        # If there’s data, compute average; otherwise, set to None
        seasonal_averages[season] = data["sum"] / data["count"] if data["count"] > 0 else None

    # Calculate largest temperature range and corresponding stations
    largest_range = 0  # Initialise largest range found
    stations_with_largest_range = []  # List to store stations with largest range
    for station, temps in station_temp_ranges.items():
        if temps["min"] != float('inf') and temps["max"] != float('-inf'):  # Check for valid data
            temp_range = temps["max"] - temps["min"]  # Calculate range
            if temp_range > largest_range:  # If this range is the largest so far
                largest_range = temp_range
                stations_with_largest_range = [station]  # Reset list with this station
            elif temp_range == largest_range:  # If tied with largest range
                stations_with_largest_range.append(station)  # Add station to list

    # Calculate warmest and coolest stations based on average temperature
    warmest_avg = float('-inf')  # Initialise warmest average as lowest possible value
    coolest_avg = float('inf')  # Initialise coolest average as highest possible value
    warmest_stations = []  # List for stations with highest average temp
    coolest_stations = []  # List for stations with lowest average temp
    for station, data in station_averages.items():
        if data["count"] > 0:  # Ensure there’s data to average
            avg_temp = data["sum"] / data["count"]  # Calculate station’s average temp
            if avg_temp > warmest_avg:  # If this is the warmest so far
                warmest_avg = avg_temp
                warmest_stations = [station]  # Reset list with this station
            elif avg_temp == warmest_avg:  # If tied with warmest
                warmest_stations.append(station)  # Add to list
            if avg_temp < coolest_avg:  # If this is the coolest so far
                coolest_avg = avg_temp
                coolest_stations = [station]  # Reset list with this station
            elif avg_temp == coolest_avg:  # If tied with coolest
                coolest_stations.append(station)  # Add to list

    # Return all computed results as a tuple
    return (seasonal_averages, stations_with_largest_range, largest_range,
            warmest_stations, warmest_avg, coolest_stations, coolest_avg)

#Save all results to their respective text files.
def save_results(averages, stations_range, largest_range, warmest_stations, warmest_avg,
                 coolest_stations, coolest_avg, seasonal_file, range_file, extremes_file):

    # Save seasonal averages to file
    with open(seasonal_file, 'w') as f:
        f.write("Average Season Temperatures for Australia\n")
        for season, avg in averages.items():
            if avg is not None:  # If there’s a valid average
                f.write(f"{season}: {avg:.1f}°C\n")  # Write with 1 decimal place
            else:
                f.write(f"{season}: No data available\n")  # Indicate no data

    # Save largest temperature range stations to file
    with open(range_file, 'w') as f:
        f.write("Station(s) with Largest Temperature Range\n")
        if largest_range > 0:  # If there’s a valid range
            f.write(f"Largest Range: {largest_range:.1f}°C\n")
            for station in stations_range:
                f.write(f"Station: {station}\n")  # List each station
        else:
            f.write("No valid temperature range data available.\n")  # No data case

    # Save warmest and coolest stations to file
    with open(extremes_file, 'w') as f:
        f.write("Warmest and Coolest Stations by Average Temperature\n")
        if warmest_stations:  # If there are warmest stations
            f.write(f"Warmest Average: {warmest_avg:.1f}°C\n")
            for station in warmest_stations:
                f.write(f"Warmest Station: {station}\n")  # List each warmest station
        else:
            f.write("No valid data for warmest station.\n")  # No data case
        if coolest_stations:  # If there are coolest stations
            f.write(f"Coolest Average: {coolest_avg:.1f}°C\n")
            for station in coolest_stations:
                f.write(f"Coolest Station: {station}\n")  # List each coolest station
        else:
            f.write("No valid data for coolest station.\n")  # No data case

#Main function to orchestrate the program execution.
def main():

    # Output file names
    seasonal_file = "average_temp.txt"
    range_file = "largest_temp_range_station.txt"
    extremes_file = "warmest_and_coolest_station.txt"

    # List of URLs for CSV files containing temperature data from team github
    file_urls = [
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1986.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1987.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1988.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1989.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1990.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1991.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1992.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1993.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1994.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1995.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1996.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1997.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1998.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_1999.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_2000.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_2001.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_2002.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_2003.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_2004.csv",
        "https://raw.githubusercontent.com/Ruthenmoir/HIT_137_Assignment_2/refs/heads/main/temperature_data/stations_group_2005.csv",
    ]

    try:
        # Process data and unpack results into variables
        (seasonal_averages, stations_range, largest_range,
         warmest_stations, warmest_avg, coolest_stations, coolest_avg) = process_temperature_data(file_urls)

        # Save all results to files
        save_results(seasonal_averages, stations_range, largest_range,
                     warmest_stations, warmest_avg, coolest_stations, coolest_avg,
                     seasonal_file, range_file, extremes_file)

        # Confirm successful completion
        print(f"Results saved to {seasonal_file}, {range_file}, and {extremes_file}")

    except Exception as e:
        print(f"An error occurred: {e}")  # Handle any top-level errors


if __name__ == "__main__":
    main()  # Run the program if this file is executed directly

