import math
from datetime import datetime
import tkinter as tk
from GUI import HistogramApp
#import MultiCSVProcessor


FILE_EXTENSION = ".csv"
vehicle_hour_hanley = {}
vehicle_hour_elm = {}


#prompt to user to enter the valid date
def validate_date_input():
    while True:
        user_input = (input("Please enter the day of the survey in the format dd: "))
        if user_input.isdigit():
            dd = int(user_input)
            if 1 <= dd <= 31:
                return user_input
            else:
                print("Out of range - values must be in the range 1 to 31.")
                continue
        else:
            print("Integer required")
            continue


#prompt to user to enter the valid month
def validate_month_input():
    while True:
        user_input = (input("Please enter the month of the survey in the format mm : "))
        if user_input.isdigit():
            mm = int(user_input)
            if 1 <= mm <= 12:
                return user_input
            else:
                print("Out of range - values must be in the range 1 to 12.")
                continue
        else:
            print("Integer required")
            continue


#prompt to user to enter the valid year
def validate_year_input():
    while True:
        user_input = (input("Please enter the year of the survey in the format YY: "))
        if user_input.isdigit():
            yy = int(user_input)
            if 2000 <= yy <= 2024:
                return user_input
            else:
                print("Out of range - values must be in the range 2000 to 2024.")
                continue
        else:
            print("Integer required")
            continue



"""date=validate_date_input()
print(date)

month=validate_month_input()
print(month)

year=validate_year_input()
print(year)"""


#open and read the csv file
def process_csv_data(file_name):
    global vehicle_hour_hanley,vehicle_hour_elm
    file_path = file_name + FILE_EXTENSION
#Read the csv file
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Data file does not exist for the given date! Try again with a different date")
        return None

#Extract the headers and  data
    header = lines[0].strip().split(',')                 #Extract the column names
    data = []

    for line in lines[1:]:                               #header row skipping
        data.append(line.strip().split(','))


#column names to their indices
    vehicle_type_index = header.index('VehicleType')
    electric_hybrid_index = header.index('elctricHybrid')
    junction_name_index = header.index('JunctionName')
    travel_direction_out_index = header.index('travel_Direction_out')
    travel_direction_in_index = header.index('travel_Direction_in')
    time_of_day_index = header.index('timeOfDay')
    juction_speed_limit_index = header.index('JunctionSpeedLimit')
    vehicle_speed_index = header.index('VehicleSpeed')
    weather_index = header.index('Weather_Conditions')


#Initialize variables for counts 
    total_number_of_vehicle = len(data)
    total_number_of_trucks = 0
    total_number_of_electricvehicles = 0
    two_wheeled_vehicles = 0
    total_number_of_busses_leavin_north = 0
    total_number_of_vehicles_without_turning = 0
    times = []
    number_bikes = 0
    the_total_number_of_vehicles_speed_limit = 0
    number_vehicles_elm_rec = 0
    number_vehicles_hanley_rec = 0
    number_Scooter_through_elm = 0


#Extra structures for Hanley Highway/Westway

    vehicle_hour_hanley = {}


#when it was raining store hours
    rain_hours = set()



#count trucks 
    for row in data:
        if row[vehicle_type_index] == 'Truck':
            total_number_of_trucks += 1


#count electric hybrid vehicle

        if row[electric_hybrid_index].lower() == 'true':
            total_number_of_electricvehicles += 1



#count two wheeled vehicles

        if row[vehicle_type_index] in ["Motorcycle", "Bicycle", "Scooter"]:
            two_wheeled_vehicles += 1


# count buses leaving Elm Avenue heading North
        if row[junction_name_index] == 'Elm Avenue/Rabbit Road' and row[travel_direction_out_index] == "N" and row[
            vehicle_type_index] == 'Buss':
            total_number_of_busses_leavin_north += 1


#  not turning vehiles count
        if row[travel_direction_in_index] == row[travel_direction_out_index]:
            total_number_of_vehicles_without_turning += 1

#count times
        time = (datetime.strptime(row[time_of_day_index], '%H:%M:%S'))
        times.append(time)

#count number of bikes
        if row[vehicle_type_index] == 'Bicycle':
            number_bikes += 1

#count vehicle over the speed limit

        if int(row[juction_speed_limit_index]) < float(row[vehicle_speed_index]):
            the_total_number_of_vehicles_speed_limit += 1


#count vehicles through Elm Avenue/Rabbit Road junctions
        if row[junction_name_index] == 'Elm Avenue/Rabbit Road':
            number_vehicles_elm_rec +=  1
            hour = time.hour
            if hour not in vehicle_hour_elm:
                vehicle_hour_elm[hour] = 0
            vehicle_hour_elm[hour] += 1


#count vehicles Hanley Highway/Westway
        elif row[junction_name_index] == 'Hanley Highway/Westway':
            #number_vehicles_hanley_rec += 1
            hour = time.hour
            if hour not in vehicle_hour_hanley:
                vehicle_hour_hanley[hour] = 0
            vehicle_hour_hanley[hour] +=1

        if row[junction_name_index] == 'Elm Avenue/Rabbit Road' and row[vehicle_type_index] == 'Scooter':
            number_Scooter_through_elm += 1


        if "rain" in row[weather_index].lower():
            rain_hours.add(time.hour)
        
# Count scooters through Elm
            # if (row[junction_name_index] == 'Elm Avenue/Rabbit Road' and
            #         row[vehicle_type_index] == 'Scooter'):
            #     print("inside if scooo")
            #     # number_scooters_through_elm += 1

#calculate percentage of trucks

    if total_number_of_vehicle > 0:
        percentage_trucks = (total_number_of_trucks / total_number_of_vehicle * 100)
    else:
        percentage_trucks = 0


#calculate  total hour
    if times:
        total_hour = ((max(times) - min(times)).total_seconds() / 3600)
    else:
        total_hour = 0

#calculate average bikes per hour
    if total_hour > 0:
        avg_bikes = round(number_bikes / total_hour)
    else:
        avg_bikes = 0

#calculate percentage of scooter
    if number_vehicles_elm_rec > 0:
        percentage_scooters = (number_Scooter_through_elm / number_vehicles_elm_rec * 100)
    else:
        percentage_scooters = 0


#calculate vehicle hour hanley highway/westway
    if vehicle_hour_hanley:
        max_hour = max(vehicle_hour_hanley, key=vehicle_hour_hanley.get)

        max_count = vehicle_hour_hanley[max_hour]
        max_hour = "{}:00 and {}:00".format(max_hour, max_hour + 1)
    else:
        max_hour = None
        max_count = 0
            
#calculate the number of rain hour
    
    count_rain_hours = len(rain_hours)

    print("************************")

    print("data file selected is traffic_data15062024.csv")
    

    print("************************")


    return {
       
        'Total number of vehicle {} ': total_number_of_vehicle,

        'Total number of Trucks   {} ': total_number_of_trucks,

        'total number of electricvehicles  {} ': total_number_of_electricvehicles,

        'Number two wheels  {} ': two_wheeled_vehicles,

        'The total number of busses leaving Elm Avenue/Rabbit Road junction heading north  {}': total_number_of_busses_leavin_north,

        'The total number of vehicles passing through both junctions without turning left or right  {}': total_number_of_vehicles_without_turning,

        'The percentage of all vehicles recorded that are Trucks for the selected date  {}': round(percentage_trucks),

        'The average number Bicycles per hour for the selected date  {}': avg_bikes,

        'The total number of vehicles recorded as over the speed limit for this date is  {}': the_total_number_of_vehicles_speed_limit,

        'The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is   {}': number_vehicles_elm_rec,

        'The total number of vehicles recorded through Hanley Highway/Westway junction is {}': number_vehicles_hanley_rec,

        '{}%  of vehicles recorded through Elm Avenue/Rabbit Road are scooters.': round(percentage_scooters),

        'The highest number of vehicles in an hour on Hanley Highway/Westway is  {}': max_count,

        'The most vehicles through Hanley Highway/Westway were recorded between  {}': max_hour,

        'The number of hours of rain for date is  {}': count_rain_hours

        }


#Function to display outcomes   
def collect_outcomes(outcomes):

#Iterates the outcomes dictionary and prints formatted results
    for key, value in outcomes.items():
        print(key.format(value))


#funtion to save result file
def save_results_to_file(outcomes,file_name="results.txt"):
    with open(file_name,"a")as file:
#write a new line
        for key,value in outcomes.items():
            file.write(key.format(value)+"\n")
        file.write("\n****************************")
    print()
    print("Text has been appended to file")



#clear data vehicle count dictionaries
def clear_counts_vehicle():
    global vehicle_hour_hanley,vehicle_hour_elm
    vehicle_hour_hanley.clear()
    vehicle_hour_elm.clear()
    print("Vehicle counts of data cleared.")

"""data = process_csv_data("traffic_data15062024.csv")
collect_outcomes(data)"""

# day = "15"
# month = "06"
# year = "2024"
#
# csv_file_name = "traffic_data" + day + month + year

# file_01 = "traffic_data15062024"
# csv_data = process_csv_data(file_01)
# display_outcomes(csv_data)
# save_results_to_file(csv_data)


# file_02 = "traffic_data16062024"
# csv_data = process_csv_data(file_02)
# display_outcomes(csv_data)
# save_results_to_file(csv_data)
#
#
# file_03 = "traffic_data21062024"
# csv_data = process_csv_data(file_03)
# display_outcomes(csv_data)
# save_results_to_file(csv_data)



while True:
#prompt user to enter day,month,year for traffic data file

    day = validate_date_input()
    month = validate_month_input()
    year = validate_year_input()
#create csv file name for user input
    csv_file_name = "traffic_data" + day + month+ year
#process csv file
    csv_data = process_csv_data(csv_file_name)


    if csv_data is None:
        continue
#collect outcomes from proceed data
    collect_outcomes(csv_data)
#save the result file
    save_results_to_file(csv_data)

    #Initialize the GUI   
    window = tk.Tk()                                                     #create main window
    formatted_day = "{}/{}/{}".format(day,month,year)
    app = HistogramApp (window,vehicle_hour_elm,vehicle_hour_hanley,formatted_day)
    window.mainloop()                                                     #run GUI loop
    


    #is_running = prompt_user_input()
    
    prompt_user_input = input("Do you want to select another data file for a different date? Y/N > ").lower()

    if prompt_user_input == "y":
        continue   
    elif prompt_user_input == "n":
        print("End of the run")
        break
    else:
        print("Invalid input. Please enter 'Y' or 'N'")


#clear data vehicle count dictionaries and call
clear_counts_vehicle()









    




    



        
    