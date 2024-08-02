import random

def generate_multiplier():
    return round(random.uniform(1, 1.5), 1) # (uniform(min value, max value), decimal point)

def number_translate(number):
    # Convert the number to a string
    number_str = str(number)

    # Check if the length is greater than 3
    if len(number_str) > 3:
        # Use Python's string formatting to add commas
        formatted_number = "{:,}".format(number)
        return formatted_number
    else:
        return number_str