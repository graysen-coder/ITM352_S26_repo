#Assignment 1
#Name: Graysen Oumi
#Date: February 27, 2026

#This is a quiz game that asks the user a series of questions

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

        answer = input("Choice? ").lower()

        if self.hint and answer.lower == "hint":
            print(f"Hint: {self.hint}")

            answer = input("Choice? ").lower()

        #Keep prompting the user for input until they enter a valid letter corresponding to one of the options

        while(len(answer) == 0 or not answer.isascii() or answer not in ascii_lowercase[:len(self.optionsList)]):

            if self.hint:
                print("Please enter a letter corresponding to one of the options. Type 'hint' for a hint.\n")

            else:
                print("Invalid input. Please enter a letter corresponding to one of the options.\n")

            answer = input("Choice? ").lower()

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
        

#This is the actual quiz game implementation, writing the program here so it can read the questions from a file and create a list of questions to ask

with open("questions.txt", "r") as question_file:

    #Create a list of quiz_question objects to represent the questions in the quiz

    questions = []

    for line in question_file:

        parts = line.strip().split("|")

        #I used copilot to help generate this file parsing code to get the questions and the parts to put into the quiz_question objects

        #This checks if the line has 5 parts (meaning it has a hint) or 4 parts meaning it has no hint and create the quiz question going from there

        if len(parts) == 5:
            question_text, options_str, correct_answer, explanation, hint = parts

            #need to convert the options into a list of strings by splitting on the commas and then create the quiz_question object and append it to the list of questions
            #This list comprehension takes each option in the string and strips any leading or trailing whitespace and creates a list of options to pass to the quiz_question constructor
            options = [opt.strip() for opt in options_str.split(",")]

            #This appends it to the questions list
            questions.append(quiz_question(question_text, options, correct_answer.strip(), explanation, hint))

        elif len(parts) == 4:

            question_text, options_str, correct_answer, explanation = parts

            options = [opt.strip() for opt in options_str.split(",")]

            questions.append(quiz_question(question_text, options, correct_answer.strip(), explanation, None))

#Using this variable to track if the user wants to quit at the end
play_again = 1

#Quiz starts here
while(play_again == 1):


    num_correct = 0

    #Loop through each question and ask it to the user, keeping track of how many they get correct
    print(f"Welcome to the quiz! There are {len(questions)} questions. Please answer the following questions:")

    for question in questions:

        print("____________________________________________________________")

        if question.ask_question() == True:

            num_correct += 1

    #At the end of the quiz, print the user's score and append it to the file storing score history (requirement 1)
    print(f"You got {num_correct} out of {len(questions)} correct.")

    exit_or_play_again = 0

    while(exit_or_play_again == 0):

        print("Type A to exit or B to play again.")

        choice = input("Choice? ").lower()

        if choice == "a":
            exit_or_play_again = 1
            play_again = 0

        elif choice == "b":

            exit_or_play_again = 2

        else:

            print("Invalid input. Please enter A to exit or B to play again.\n")

    #Append users score to the file every time they play
    with open("score_history.txt", "a") as score_history_file:

        score_history_file.write(f"Score: {num_correct}/{len(questions)}\n")




score_history_file.close()

