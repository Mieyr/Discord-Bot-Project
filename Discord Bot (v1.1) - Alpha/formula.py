import random

def truncate(n, decimals = 0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

Search_base = 20
Search_multiplier = truncate(random.uniform(1, 1.5), 0)

def Number_translate(Number):
    Number = str(Number) # Turn into str in order for len() to work
    if len(Number) > 3: # Wont do shit if its only 3 digit and under
        New_Number = ""
        First_Group_Counter = len(Number) % 3
        Triplet_Counter = 0
        Triplet_Comma = ((len(Number) - First_Group_Counter) / 3) - 1 # Number of comma in between 0s, -1 since 1 comma already used
        Triplet_Comma_Counter = 0

        # First-Group is a set of number(s) that comes before the first comma, E.g. 12,000,000 (12 is a First-Group)

        for Numerator in Number:
            if First_Group_Counter > 0: # Will only happen as long as there's a member of the First-Group
                New_Number = New_Number + Numerator # Add those First-Group into New_Number from Numerator
                First_Group_Counter -= 1
                if First_Group_Counter == 0:
                    New_Number = New_Number + ","
            else: # Won't happen if there's still a member of the First-Group
                Triplet_Counter += 1 # Counts the number 0s to 3
                New_Number = New_Number + Numerator
                if Triplet_Comma_Counter < Triplet_Comma and Triplet_Counter == 3: 
                    New_Number = New_Number + ","
                    Triplet_Counter = 0 # Reset the counter
                    Triplet_Comma_Counter += 1
        return New_Number
    else:
        return Number