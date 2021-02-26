# CS361_Person_Generator_Microservice

## HOW TO RUN Person-Generator

### Video Walkthrough

![](person-generator-sprint3.gif)

To open GUI for Person-Generator, input in terminal:
  
    $ python3 person-generator.py
  

To run Person Generator in terminal, have a csv file in the same file location as the person-generator python file named "input.csv".
The csv file should have "input_state" and ("input_number_to_generate" or "output_population_size" (From population generator) in each column. 
Additionally, the state should be on the row under input_state and the number of people to generate under "input_number_to_generate" or "output_population_size". 
Finally, input in terminal:

    $ python3 person-generator.py -i
