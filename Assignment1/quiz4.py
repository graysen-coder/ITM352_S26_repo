#Quiz game. Second version
#Name: Graysen Oumi
#Date: February 24, 2026
#Make QUESTIONS a dictionary, to include answer options and the correct choice

QUESTIONS = {
     "What is the airspeed of an unladen swallow in miles/hr": [
          "12",
          "8",
          "11",
          "15"
     ],
     "What is the capital of Texas": [
          "Austin",
          "San Antonio",
          "Dallas",
          "Waco"
     ],
     "The Last Supper was painted by which artist": [
          "Da Vinci",
          "Rembrandt",
          "Picasso",
          "Michelangelo"
     ]
}

for question, options in QUESTIONS.items():
    correct_answer = options[0]  # First option is correct
    sorted_options = sorted(options)
    print(question)
    for label, alternative in enumerate(sorted_options, start=1):
        print(f"  - {label}: {alternative}")

    answer_label = int(input(question + ":"))

    answer = sorted_options[answer_label-1]

    if answer == correct_answer:
        print("Correct!")
    else:
        print(f"The answer is '{correct_answer}'. Not '{answer}'.")