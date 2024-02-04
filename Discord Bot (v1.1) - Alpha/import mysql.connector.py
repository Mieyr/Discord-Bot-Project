import random


counter = 0
tail_counter = 0
head_counter = 0
Flip = ["tail", "head"]
while counter < 100:
    randomizer = random.choice(Flip)
    print(randomizer)
    if randomizer == "tail":
        tail_counter += 1
    else:
        head_counter += 1
    counter += 1
print(tail_counter)
print(head_counter)