import csv

#Calculate the average temperatures for each season across all years. Save the result to file “average_temp.txt”

def find_season(month_name):    #seasons based off months listed in cvs table
    if month_name in ['December', 'January', 'February']:
        return "Summer"
    elif month_name in ['March', 'April', 'May']:
        return "Autumn"
    elif month_name in ['June','July','August']:
        return "Winter"
    elif month_name in ['September','October', 'November']:
        return "Spring"
    else: 
        return None   #incase invalid month entered

def process_temperature_data(filenames):

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November','December']

    seasonal_data = {                                 #sum and tally for finding averages
        "Summer": {"sum_of_temp": 0, "count": 0},
        "Autumn": {"sum_of_temp": 0, "count": 0},
        "Winter": {"sum_of_temp": 0, "count": 0},
        "Spring": {"sum_of_temp": 0, "count": 0}
    }

    for filename in filenames:
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    for month in months:
                        try:
                            temp = float(row[month])   #return the temp values for each month
                            season = find_season(month)

                            if season:
                                seasonal_data[season]["sum_of_temp"] += temp    #combine temps for the months in the season
                                seasonal_data[season]["count"] += 1      #increase count for every month in season so it can be divided later for the average

                            else:
                                print(f"Invalid month '{month}' in {filename}")
                        except (ValueError, KeyError) as e:
                            print(f"Error processing{month} in {filename}: {e}")
                            continue

        except FileNotFoundError:
            print(f"File not found: {filename}")
            continue


    season_average = {}                                                       # calculate averages
    for season in seasonal_data:
        season_average[season] = (seasonal_data[season]["sum_of_temp"] / seasonal_data[season]["count"])
    return season_average




def results(averages, output_file):                                        #saving results to text file
    with open(output_file, 'w') as f:
        f.write("Average Season Temperatures for Australia \n")
        for season, avg_temp in averages.items():
            f.write(f"{season}: {avg_temp:.1f}°C\n")

        
def main():
    output_file = "average_temp.txt"

    filenames = [
        "stations_group_1988.csv",
        "stations_group_1989.csv"
    ]
    try:
        seasonal_averages = process_temperature_data(filenames)
        results(seasonal_averages, output_file)
        print(f"Results saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
                              



