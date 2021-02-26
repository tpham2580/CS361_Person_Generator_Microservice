# Author: Timothy Pham
# Description: Person Generator Program

import csv
import random
import argparse
from tkinter import *
import os

"""This program uses preprocessed csv files to extract data from"""

states = {
            "Alaska": "ak.csv",
            "Arizona": "az.csv",
            "California": "ca.csv",
            "Colorado": "co.csv",
            "Hawaii": "hi.csv",
            "Idaho": "id.csv",
            "Montana": "mt.csv",
            "New Mexico": "nm.csv",
            "Nevada": "nv.csv",
            "Oregon": "or.csv",
            "Utah": "ut.csv",
            "Washington": "wa.csv",
            "Wyoming": "wy.csv"
        }


class PersonGenerator(Tk):
    def __init__(self):
        super().__init__()
        self.title("Person Generator")
        self.paddings = {'padx': 5, 'pady': 5}
        self.listbox = Listbox(self)
        self.int_var = IntVar(self)
        self.year_var = IntVar(self)

        self.create_year()

        self.state_keys = list(states.keys())
        self.option_var = StringVar(self)
        self.create_states()

        self.create_streets()

        self.create_generate_button()
        self.create_population_button()

    def create_year(self):
        """creates label for year"""
        label_year = Label(self, text="Input year between 1986 & 2019: ")
        label_year.grid(column=1, row=1, sticky='', **self.paddings)

        year_input = Entry(self, textvariable=self.year_var).grid(column=2, row=1, sticky='', **self.paddings)

    def create_states(self):

        # create label for selecting state
        label_state = Label(self, text="Select a US State in the options: ")
        label_state.grid(column=1, row=2, sticky='', **self.paddings)

        state_options = OptionMenu(
            self,
            self.option_var,
            *self.state_keys
        )

        state_options.grid(column=2, row=2, sticky='', **self.paddings)

    def create_streets(self):

        # create label for inputting number of street addresses
        label_street = Label(self, text="Input number of street addresses: ")
        label_street.grid(column=1, row=3, sticky='', **self.paddings)

        number_state = Entry(self, textvariable=self.int_var).grid(column=2, row=3, sticky='', **self.paddings)

    def create_generate_button(self):
        button_generate = Button(self,
                                 text="Generate Output",
                                 command=lambda: self.create_output_file())
        button_generate.grid(column=2, row=4, sticky='', **self.paddings)

    def create_population_button(self):
        button_pop = Button(self,
                                 text="Call Population-Generator",
                                 command=lambda: self.create_population_output())
        button_pop.grid(column=1, row=4, sticky='', **self.paddings)

    def create_population_output(self):
        """creates input.csv, calls population-generator and generate output window"""

        state_input = self.option_var.get()
        year_input = self.year_var.get()

        if year_input < 1986 or year_input > 2019 or state_input not in states:
            self.listbox.insert(1, "Year or State not properly inputted")
            self.listbox.grid(column=1, row=5, columnspan=3, sticky='EW', **self.paddings)
            return

        with open('input.csv', 'w') as outfile:

            writer = csv.writer(outfile)

            writer.writerow(["input_year", "input_state"])
            writer.writerow([year_input, state_input])

        pop_request()
        with open('output.csv', 'r') as infile:
            header = next(csv.reader(infile))
            row_output = next(csv.reader(infile))
            self.listbox.insert(1, row_output)
            self.listbox.grid(column=1, row=5, columnspan=3, sticky='EW', **self.paddings)
            
    def create_output_file(self):
        """creates output.csv file"""
        state_input = self.option_var.get()
        number_input = self.int_var.get()

        if state_input == "" or number_input == 0:
            self.listbox.insert(1, "Please fill all appropriate inputs")
            self.listbox.grid(column=1, row=5, columnspan=3, sticky='EW', **self.paddings)
            return

        with open(states[state_input], 'r') as infile:
            lines = sum(1 for line in infile)

        with open(states[state_input], 'r') as infile, open('output.csv', 'w') as outfile:
            random_numbers = [random.randint(1, lines) for x in range(number_input)]
            random_numbers.sort()

            writer = csv.writer(outfile)
            writer.writerow(["input_state", "input_number_to_generate",
                             "output_content_type", "output_content_value"])

            output_list = []
            new_street = None
            index = 0
            for line_number, row in enumerate(csv.reader(infile)):
                if index < number_input:
                    if line_number == random_numbers[index]:
                        new_street = list(row)
                        new_street = [x.lower().title() for x in new_street]
                        new_street[1] = " " + new_street[1]
                        new_street[2] = ", " + new_street[2]
                        new_street[3] = ", " + states[state_input].strip(".csv").upper() + ", " + new_street[3]
                        street_string = "".join(new_street)
                        writer.writerow([state_input, number_input, "street address", street_string])

                        index += 1

                        output_list.append(street_string)
                else:
                    break

        for x, y in enumerate(output_list):
            self.listbox.insert(x+1, y)
        self.listbox.grid(column=1, row=4, columnspan=3, sticky='EW', **self.paddings)


def input_to_output():
    """reads input file and outputs to output.csv"""

    with open("input.csv", "r") as infile:
        header = next(csv.reader(infile))
        input_col_index = None
        input_number_col_index = None
        for col_index, col in enumerate(header):
            if col == "input_state":
                input_col_index = col_index
            if col == "input_number_to_generate" or col == "output_population_size":
                input_number_col_index = col_index
        
        if input_col_index == None or input_number_col_index == None:
            print("Unable to read input.csv format")

        row_input = next(csv.reader(infile))
        state_input = row_input[input_col_index]
        number_input = int(row_input[input_number_col_index])
    
    if state_input not in states:
        print(state_input, "is not one of the states covered by the person-generator")
        return

    with open(states[state_input], 'r') as infile:
        lines = sum(1 for line in infile)

    with open(states[state_input], 'r') as infile, open('output.csv', 'w') as outfile:

        random_numbers = [random.randint(1, lines) for x in range(number_input)]
        random_numbers.sort()

        writer = csv.writer(outfile)
        writer.writerow(["input_state", "input_number_to_generate",
                         "output_content_type", "output_content_value"])

        new_street = None
        index = 0
        for line_number, row in enumerate(csv.reader(infile)):
            if index < number_input:
                while line_number == random_numbers[index]:
                    new_street = list(row)
                    new_street = [x.lower().title() for x in new_street]
                    new_street[1] = " " + new_street[1]
                    new_street[2] = ", " + new_street[2]
                    new_street[3] = ", " + states[state_input].strip(".csv").upper() + ", " + new_street[3]
                    street_string = "".join(new_street)
                    writer.writerow([state_input, number_input, "street address", street_string])

                    index += 1

            else:
                break
    return


def pop_request():
    """requests data from population generator"""
    os.system("python3 population-generator.py input.csv")
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action='store_true', help='run program with input.csv')
    parser.add_argument('-p', '--population', action='store_true', help='request data from population generator with input.csv')
    parser.add_argument('-l', '--life', action='store_true', help='run program with input.csv by feeding data to life '
                                                                  'generator')
    args = parser.parse_args()
    if args.input is True:
        input_to_output()
    elif args.input is True:
        pop_input_to_output()
    else:
        person = PersonGenerator()
        person.mainloop()


if __name__ == '__main__':
    main()
