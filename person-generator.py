# Author: Timothy Pham
# Description: Person Generator Program

import csv
import random
import argparse
from tkinter import *
import os
import subprocess

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
        self.board_var = IntVar(self)
        self.board_game_list = []

        self.create_board_games()

        self.state_keys = list(states.keys())
        self.option_var = StringVar(self)
        self.create_states()

        self.create_streets()

        self.create_generate_button()
        self.create_content_button()


    def create_board_games(self):
        """creates checkbox label for year"""
        board_game = Label(self, text="Add favorite board game? ")
        board_game.grid(column=1, row=1, sticky='', **self.paddings)

        self.button_checkbox = Checkbutton(self, variable=self.board_var).grid(column=2, row=1, sticky='', **self.paddings)

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
                                 command=lambda: self.create_output_gui(self.option_var.get(), self.int_var.get(), self.board_var.get()))
        button_generate.grid(column=2, row=4, sticky='', **self.paddings)

    def create_content_button(self):
        button_content = Button(self,
                                text="Call Content-Generator",
                                command=lambda: self.create_content_output())
        button_content.grid(column=1, row=4, sticky='', **self.paddings)

    def create_content_output(self):
        """creates input.csv, calls content-generator and generate output window of top ten items"""

        board_input = self.board_var.get()

        self.listbox.delete(0, END)

        if board_input != 1:
            self.listbox.insert(1, "Please check game option to request content-generator")
            self.listbox.grid(column=1, row=5, columnspan=4, sticky='EW', **self.paddings)
            return

        content_request()

        with open('life_generator_output.csv', 'r') as infile:
            header = next(csv.reader(infile))
            for x, row in enumerate(csv.reader(infile)):
                self.board_game_list.append(row[3])
                self.listbox.insert(x, row[3])
                self.listbox.grid(column=1, row=5, columnspan=3, sticky='EW', **self.paddings)

    def check_state_and_people(self, state_input, number_input):
        if state_input == "" or number_input == 0:
            self.listbox.insert(1, "Please fill all appropriate inputs")
            self.listbox.grid(column=1, row=5, columnspan=3, sticky='EW', **self.paddings)
            return

    def count_lines_state_csv(self, state_input):
        with open(states[state_input], 'r') as infile:
            lines = sum(1 for line in infile)
        return lines

    def create_street_address(self, state_input, infile_row):
        print(infile_row)
        new_street = list(infile_row)
        new_street = [x.lower().title() for x in new_street]
        new_street[1] = " " + new_street[1]
        new_street[2] = ", " + new_street[2]
        new_street[3] = ", " + states[state_input].strip(".csv").upper() + ", " + new_street[3]
        street_string = "".join(new_street)
        return  street_string

    def get_random_sorted_list(self, number_input, lines):
        random_numbers = [random.randint(1, lines) for x in range(number_input)]
        random_numbers.sort()
        return random_numbers

    def make_header_output_list(self, board_input):
        if len(self.board_game_list) > 0 and board_input == 1:
            header_list = ["input_state", "input_number_to_generate",
                          "output_content_type", "output_content_value", "favorite_board_game"]
        else:
            header_list = ["input_state", "input_number_to_generate",
                          "output_content_type", "output_content_value"]
        return header_list

    def write_output_file(self, state_input, number_input, board_input):
        """creates an output csv with information and return output list"""
        if len(self.board_game_list) == 0:
            self.create_content_output()

        self.check_state_and_people(state_input, number_input)
        lines = self.count_lines_state_csv(state_input)

        with open(states[state_input], 'r') as infile, open('output.csv', 'w') as outfile:
            random_numbers = self.get_random_sorted_list(number_input, lines)

            writer = csv.writer(outfile)
            writer.writerow(self.make_header_output_list(board_input))

            output_list = []
            new_street = None
            index = 0
            random_board_game = ""
            for line_number, row in enumerate(csv.reader(infile)):
                if index < number_input:
                    if line_number == random_numbers[index]:
                        street_string = self.create_street_address(state_input, row)
                        if len(self.board_game_list) > 0 and board_input == 1:
                            random_board_game = random.choice(tuple(self.board_game_list))
                            writer.writerow([state_input, number_input, "street address", street_string, random_board_game])
                        else:
                            writer.writerow([state_input, number_input, "street address", street_string])

                        output_list.append(street_string + " | " + random_board_game)
                        index += 1
                else:
                    break
        return output_list

    def create_output_gui(self, state_input, number_input, board_input):
        """reads output_list and create GUI element for output"""
        output_list = self.write_output_file(state_input, number_input, board_input)

        self.listbox.delete(0, END)
        for x, y in enumerate(output_list):
            self.listbox.insert(x+1, y)
        self.listbox.grid(column=0, row=5, columnspan=4, sticky='EW', **self.paddings)


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
            if index < len(random_numbers):
                while line_number == random_numbers[index]:
                    new_street = list(row)
                    new_street = [x.lower().title() for x in new_street]
                    new_street[1] = " " + new_street[1]
                    new_street[2] = ", " + new_street[2]
                    new_street[3] = ", " + states[state_input].strip(".csv").upper() + ", " + new_street[3]
                    street_string = "".join(new_street)
                    writer.writerow([state_input, number_input, "street address", street_string])

                    index += 1

                    if index >= len(random_numbers):
                        break

            else:
                break
    return

def content_request():
    subprocess.run(['python3', 'content-generator.py', 'input.csv'])
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
