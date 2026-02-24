#Quiz game. Second version
#Name: Graysen Oumi
#Date: February 24, 2026
#Make a list with the questions and correct answers

QUESTIONS = [
    ("What is the airspeed of an unladen swallow in miles per hour?", "12"),
    ("What is the capital of Texas?", "Austin"),
    ("The last supper was painted by which artist?", "Da Vinci")
]

for question, correct_answer in QUESTIONS:
    answer = input(question + " ")
    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}'. Not '{answer}'.")