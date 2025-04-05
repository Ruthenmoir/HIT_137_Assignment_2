import csv
import urllib.request
from io import StringIO

"""Aim: Calculate the average temperatures for each season across all years. Save the result to file 'average_temp.txt'"""

def find_season(month_name):
    if month_name in ['December', 'January', 'February']:
        return "Summer"
    elif month_name in ['March', 'April', 'May']:
        return "Autumn"
    elif month_name in ['June', 'July', 'August']:
        return "Winter"
    elif month_name in ['September', 'October', 'November']:
        return "Spring"
    else:
        return None


def process_temperature_data(file_urls):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    seasonal_data = {
        "Summer": {"sum_of_temp": 0, "count": 0},
        "Autumn": {"sum_of_temp": 0, "count": 0},
        "Winter": {"sum_of_temp": 0, "count": 0},
        "Spring": {"sum_of_temp": 0, "count": 0}
    }

    for url in file_urls:
        try:
            # Fetch the file using urllib.request
            with urllib.request.urlopen(url) as response:
                file_content = response.read().decode('utf-8')  # Decode bytes to string
                file = StringIO(file_content)
                reader = csv.DictReader(file)

                for row in reader:
                    for month in months:
                        try:
                            temp = float(row[month])
                            season = find_season(month)
                            if season:
                                seasonal_data[season]["sum_of_temp"] += temp
                                seasonal_data[season]["count"] += 1
                            else:
                                print(f"Invalid month '{month}' in {url}")
                        except (ValueError, KeyError) as e:
                            print(f"Error processing {month} in {url}: {e}")
                            continue

        except urllib.error.URLError as e:
            print(f"Failed to fetch {url}: {e}")
            continue

    season_average = {}
    for season in seasonal_data:
        if seasonal_data[season]["count"] > 0:
            season_average[season] = (seasonal_data[season]["sum_of_temp"] / seasonal_data[season]["count"])
        else:
            season_average[season] = 0
            print(f"No data available for {season}")

    return season_average


def results(averages, output_file):
    with open(output_file, 'w') as f:
        f.write("Average Season Temperatures for all stations between 1986 and 2005\n")
        for season, avg_temp in averages.items():
            f.write(f"{season}: {avg_temp:.1f}°C\n")


def main():
    output_file = "average_temp.txt"

    # Replace these with the actual filenames from your GitHub folder
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
        seasonal_averages = process_temperature_data(file_urls)
        if seasonal_averages:
            results(seasonal_averages, output_file)
            print(f"Results saved to {output_file}")
        else:
            print("No data processed.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
