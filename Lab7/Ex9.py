celebs = ("Taylor Swift", "Lionel Messi", "The Weeknd", "Keanu Reeves", "Angelina Jolie")
age = (36, 39, 35, 62, 50)

celebs_list = []
ages_list = []

for celeb in celebs:
    celebs_list.append(celeb)

ages_list = [age for age in age]

celebs_dict = {"celebrities":celebs_list, "ages":ages_list}

print(celebs_dict)

#do the above without loops
celebs_dict = {"celebrities": list(celebs), "ages": list(age)}
