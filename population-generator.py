# Joey Punzel
# Software Engineering / CS361
# Winter 2021
# Population Generator

import tkinter as tk
import sys
import requests
import csv
import os

def population_size(year,state):
    state_code = find_state_code(state)
    api_url = "https://api.census.gov/data/" + str(year) + "/acs/acs1?get=NAME,B01003_001E&for=state:" + str(state_code)
    response = requests.get(api_url)
    js = response.json()
    result = js[1][1]
    return result

def find_state_code(state):
    switchme={
        'Alabama': '01',
        'Alaska': '02',
        'Arizona': '04',
        'Arkansas': '05',
        'California': '06',
        'Colorado': '08',
        'Connecticut': '09',
        'Delaware': 10,
        'Florida': 12,
        'Georgia': 13,
        'Hawaii': 15,
        'Idaho': 16,
        'Illinois': 17,
        'Indiana': 18,
        'Iowa': 19,
        'Kansas': 20,
        'Kentucky': 21,
        'Louisiana': 22,
        'Maine': 23,
        'Maryland': 24,
        'Massachusetts': 25,
        'Michigan': 26,
        'Minnesota': 27,
        'Mississippi': 28,
        'Missouri': 29,
        'Montana': 30,
        'Nebraska': 31,
        'Nevada': 32,
        'New Hampshire': 33,
        'New Jersey': 34,
        'New Mexico': 35,
        'New York': 36,
        'North Carolina': 37,
        'North Dakota': 38,
        'Ohio': 39,
        'Oklahoma': 40,
        'Oregon': 41,
        'Pennsylvania': 42,
        'Rhode Island': 44,
        'South Carolina': 45,
        'South Dakota': 46,
        'Tennessee': 47,
        'Texas': 48,
        'Utah': 49,
        'Vermont': 50,
        'Virginia': 51,
        'Washington': 53,
        'West Virginia': 54,
        'Wisconsin': 55,
        'Wyoming': 56
    }
    return switchme.get(state,"Invalid State")

def gui_generate(year,state):
    year = int(year)
    state = str(state)
    population = population_size(year,state)
    generate_statement = "Year: " + str(year) + ", State: " + state + " , Population: " + str(population)
    label = tk.Label(text=generate_statement)
    label.pack()

    # also print result to output.txt file
    output_file = open("output.csv", "a")
    output_file.write("\n")
    output_file.write(str(year) + "," + state + "," + str(population))
    output_file.close()
    return 0

def main():
    print("Running in Command Mode")
    input = sys.argv[1]

    if input == "request_person_generator":
        os.system("cp input_person_generator.csv input.csv")
        os.system("python3 person-generator.py -i")
        os.system("cp input_population_generator.csv input.csv")
        print("Completed calling person-generator - see output file in output.csv")
        return 0

    elif input == "input.csv":
        #os.system("cp input_population_generator.csv input.csv")
        output_file = open("output.csv","w")
        output_file.write("input_year,input_state,output_population_size")
        output_file.close()
        with open(input) as csv_file:
            csv_read = csv.reader(csv_file, delimiter=',')
            lcount = 0
            for row in csv_read:
                if lcount != 0:
                    size = population_size(row[0],row[1])
                    output_file = open("output.csv","a")
                    output_file.write("\n")
                    output_file.write(row[0] + "," + row[1] + "," + size)
                    output_file.close()
                lcount += 1
    else:
        print("Input file not valid. Options: ")
        print("[1] input.csv - listing year,state where population size requested")
        print("[2] request_person_generator input.csv - where looking to feed into person generator microservice with input.csv file")

    return 0

# logic to run script as command (with argument) or gui (without arguments)
if __name__ == '__main__':
    if len(sys.argv) > 1:
        main()
    else:
        print("Running in GUI Mode")
        # start new output file and establish headers
        output_file = open("output.csv", "w")
        output_file.write("input_year,input_state,output_population_size")
        output_file.close()

        window = tk.Tk()
        # gui title
        title_widget = tk.Label(text="Population Generator v1 By Joey Punzel")
        title_widget.pack()

        # drop down for year options
        YEAR_OPTIONS = [
            "2019",
            "2018",
            "2017",
            "2016",
            "2015",
            "2014",
            "2013",
            "2012",
            "2011",
            "2010",
            "2009",
            "2008",
            "2007",
            "2006",
            "2005"
        ]
        year_var = tk.StringVar(window)
        year_var.set(YEAR_OPTIONS[0])  # default value
        year_widget = tk.OptionMenu(window, year_var, *YEAR_OPTIONS)
        year_widget.pack()

        # drop down for state options
        STATE_OPTIONS = [
            "Alabama",
            "Alaska",
            "Arizona",
            "Arkansas",
            "California",
            "Colorado",
            "Connecticut",
            "Delaware",
            "Florida",
            "Georgia",
            "Hawaii",
            "Idaho",
            "Illinois",
            "Indiana",
            "Iowa",
            "Kansas",
            "Kentucky",
            "Louisiana",
            "Maine",
            "Maryland",
            "Massachusetts",
            "Michigan",
            "Minnesota",
            "Mississippi",
            "Missouri",
            "Montana",
            "Nebraska",
            "Nevada",
            "New Hampshire",
            "New Jersey",
            "New Mexico",
            "New York",
            "North Carolina",
            "North Dakota",
            "Ohio",
            "Oklahoma",
            "Oregon",
            "Pennsylvania",
            "Rhode Island",
            "South Carolina",
            "South Dakota",
            "Tennessee",
            "Texas",
            "Utah",
            "Vermont",
            "Virginia",
            "Washington",
            "West Virginia",
            "Wisconsin",
            "Wyoming"
        ]
        state_var = tk.StringVar(window)
        state_var.set(STATE_OPTIONS[0])  # default value
        state_widget = tk.OptionMenu(window, state_var, *STATE_OPTIONS)
        state_widget.pack()

        # button to pull population based on input state/year
        generate_button = tk.Button(window, text="Request Population",
                                    command=lambda: gui_generate(year_var.get(), state_var.get()))
        generate_button.pack()

        # button to quit the gui
        quit_button = tk.Button(window, text="Quit", command=quit)
        quit_button.pack()

        # run loop for gui
        window.mainloop()