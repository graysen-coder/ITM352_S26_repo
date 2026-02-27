#Assignment 1
#Name: Graysen Oumi
#Date: February 27, 2026

#Extra requirements
#7. Add explanations for why the correct answer is the correct answer.
#1. Write the history of scores out to a file.  
#6. Allow an option to provide a hint.  

from string import ascii_lowercase

#I wanted to try doing this using a class so the actual quiz game code needs to use less hardcoded indexing and is easier to add and remove questions for the extra requirements
class quiz_question:


    #Each quiz_question object has the question, a list of options, the correct answer, and an explanation for why the correct answer is correct
    #There is also an optional hint with the default value of None if they don't want to provide a hint
    def __init__(self, question, options_list, correct_answer, explanation, hint=None):

        self.question = question

        self.optionsList = options_list

        self.correctAnswer = correct_answer

        self.explanation = explanation

        self.hint = hint

    #This method prints the question then a numbered list of the options and asks user for an answer
    #It then checks if the answer is correct and prints the explanation for the correct answer (requirement 7)
    #If the user is incorrect, the method returns prints the correct answer and explanation and returns false
    def ask_question(self):

        print(f"{self.question}")

        for i, option in zip(ascii_lowercase, self.optionsList):

            print(f"  {i}. {option}")

        #If hint is provided, give user option to type hint to get a hint
        if self.hint:
            print("Type 'hint' for a hint.")

        answer = input("Choice? ")

        if self.hint and answer.lower() == "hint":
            print(f"Hint: {self.hint}")

            answer = input("Choice? ")

        #Keep prompting the user for input until they enter a valid letter corresponding to one of the options

        while(not answer.isascii() or answer not in ascii_lowercase[:len(self.optionsList)]):

            if self.hint:
                print("Please enter a letter corresponding to one of the options. Type 'hint' for a hint.\n")

            else:
                print("Invalid input. Please enter a letter corresponding to one of the options.\n")

            answer = input("Choice? ")

            if self.hint and answer.lower() == "hint":
                print(f"Hint: {self.hint}")

        if ascii_lowercase.index(answer) == self.optionsList.index(self.correctAnswer):

                print("Correct!")

                print(f"Explanation: {self.explanation}\n")

                return True
                    
        else:
        
            print(f"The answer is '{self.correctAnswer}'. Not '{self.optionsList[ascii_lowercase.index(answer)]}'.")

            print(f"Explanation: {self.explanation}")

            return False
        

#take look at this later, need to fix
def get_questions():
    #This function gets the questions for the quiz from a file called questions.txt and returns a list of quiz_question objects

    questions = []

    with open("questions.txt", "r") as questions_file:

        for line in questions_file:

            question_data = line.strip().split(";")

            if len(question_data) >= 4:

                question = question_data[0]

                options_list = question_data[1].split(",")

                correct_answer = question_data[2]

                explanation = question_data[3]

                hint = question_data[4] if len(question_data) > 4 else None

                questions.append(quiz_question(question, options_list, correct_answer, explanation, hint))

    return questions

#This is the actual quiz game implementation

#Create a list of quiz_question objects to represent the questions in the quiz
questions = [
        quiz_question("What is the airspeed of an unladen swallow in miles/hr", ["12", "8", "11", "15"], "12", "The airspeed of an unladen European swallow is approximately 12 miles per hour.", "a"),
        quiz_question("What is the capital of Texas?", ["Austin", "San Antonio", "Dallas", "Waco"], "Austin", "Austin is the capital city of Texas."),
        quiz_question("The Last Supper was painted by which artist?", ["Da Vinci", "Rembrandt", "Picasso", "Michelangelo"], "Da Vinci", "The Last Supper was painted by Leonardo da Vinci."),
    ]

num_correct = 0

#Loop through each question and ask it to the user, keeping track of how many they get correct
print(f"Welcome to the quiz! There are {len(questions)} questions. Please answer the following questions:")

for question in questions:

    print("____________________________________________________________")

    if question.ask_question():

        num_correct += 1

#At the end of the quiz, print the user's score and append it to the file storing score history (requirement 1)
print(f"You got {num_correct} out of {len(questions)} correct.")

with open("score_history.txt", "a") as score_history_file:

    score_history_file.write(f"Score: {num_correct}/{len(questions)}\n")



    

    
