#Quiz game. Second version
#Name: Graysen Oumi
#Date: February 24, 2026
#Make QUESTIONS a dictionary, to include answer options and the correct choice

from string import ascii_lowercase

#remove line breaks from this dictionary
QUESTIONS = {"What is the airspeed of an unladen swallow in miles/hr": ["12","8","11","15"], 
             "What is the capital of Texas": ["Austin","San Antonio","Dallas","Waco"],
             "The Last Supper was painted by which artist": ["Da Vinci","Rembrandt","Picasso", "Michelangelo"]
}
num_correct = 0
for num, (question, options) in enumerate(QUESTIONS.items(), start=1):
    print(f"Question {num}:")
    print(f"{question}")
    correct_answer = options[0]  # First option is correct
    labeled_alternatives = dict(zip(ascii_lowercase, sorted(options)))
    for label, alternative in labeled_alternatives.items():
        print(f"  - {label}: {alternative}")

    answer_label = input("Choice? ")
    answer = labeled_alternatives.get(answer_label)

    if answer == correct_answer:
        print("Correct!")
        num_correct += 1
    else:
        print(f"The answer is '{correct_answer}'. Not '{answer}'.")