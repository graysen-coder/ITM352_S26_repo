### **Web Application Assignment: Building a Quiz Game**

In this assignment, you’ll transform your console-based quiz game from Assignment 1 into an interactive web application. This exercise will introduce you to web development concepts in Python using a framework, such as Flask, and front-end techniques to create a responsive, user-friendly quiz game. Your application should display randomized questions, capture user responses, and provide feedback on correct answers, just like the original game.

### **Assignment Objectives**

* **Convert** the provided quiz game to a Flask web application.  
* **Enhance UI/UX** using HTML, CSS, Flask templates with Jinja, and basic JavaScript (if needed).  
* **Rapid** self-learning of Python packages (Flask), HTML, CSS, and browser JavaScript  
* **Understanding and Designing** a web application  
* **Effective** use of generative AI to support web application development

### **Functional Requirements:**

1. **User Interface Requirements**  
   * Design a clean and intuitive UI with HTML, CSS, and JavaScript (as needed).  
   * Create dynamic elements that respond to user actions, including question display, answer options, and submission feedback.  
2. **Question Display Requirements**  
   * Load questions dynamically from a JSON file containing all questions and answer options (i.e. not “hard-coded” into the page or program).  
   * Randomize both question order and answer options for each session to ensure variety.  
3. **Answer Submission and Feedback**  
   * Provide users with real-time feedback on their answer selections.  
   * Implement score tracking that updates based on correct/incorrect answers.  
4. **Data Management Requirements**  
   * Store questions, answer choices, and user score data in JSON format or a simple data file.  
   * Use server-side Python code to handle data storage and retrieval.  
5. **Backend Requirements**  
   * Use a framework like Flask to serve the web application.  
   * Implement RESTful APIs for retrieving questions and storing user scores.  
6. **Score Tracking and Feedback**  
   * Calculate and display the user’s final score upon quiz completion.  
   * Show detailed feedback, such as the number of correct/incorrect answers, time taken, and areas for improvement.  
7. **Error Handling and Validations**  
   * Ensure input validation for text fields, login, and registration.  
   * Display user-friendly error messages when validation fails or data loading issues occur.

### **Non-Functional Requirements:**

8. **User-Friendliness**  
   * The application should be easy to use, intuitive, and accessible for all types of users. This means a clear layout, responsive navigation, and helpful feedback for user actions.  
9. **Documentation**  
   * Clear and thorough documentation must accompany the code. This includes setup instructions, usage guides, comments in code, and explanations of design choices.  
10. **Performance**  
    * The web application should load quickly and respond promptly to user inputs. Efficient data handling and minimal lag in question display or answer feedback are required.  
11. **Quality Assurance**  
    * You must test your application to ensure it is free of bugs and errors. This includes unit tests, integration tests, and user acceptance testing to guarantee reliability.  
12. **Maintainability**  
    * The application's codebase should be structured and commented in a way that makes future updates and debugging easy. Use modular design, meaningful variable/function names, and clear organization so others can maintain or expand the project efficiently.

These core requirements ensure the web application’s functionality, user-friendliness, and accessibility while incorporating best practices in backend data handling and security**.** 

**IMPORTANT: You must document in an easy to understand and recognize way that all the core requirements have been satisfied. This may be a simple as a document listing the requirements and a discussion on how they have been satisfied (e.g. “The ExerciseAPI\_test.py verifies that all the Quiz Game routes are accessible from the Flask server”)** 

**AI Tips:**

- Use AI to write a detailed “use of AI” document based on your chat history  
- Use AI to generate **test code** and **documentation**. You will likely have to adjust the tests and documentation. It may be better to ask for specific tests one at a time rather then everything at once.  
- Use AI to check if your code conforms to conventions  
- If your AI generated code uses package you are unfamiliar with, ask AI to explain it to you or direct it to rewrite the code in way you do understand e.g. “rewrite the get\_page\_info() function using BeutifulSoup”  
- If you do not understand some part of your AI generate code, direct your AI to explain it what it does and why it’s there. If it’s superfluous (not needed), ask it to remove it. If you think it’s needed but still do not understand it or you think it’s doing more than what’s needed, direct the AI to do what is needed in a different way that you do understand e.g. “Rewrite the file load function to just load the CSV data from data\_file\_url into a Panda dataframe and check for necessary columns. Do not have it try to load alternative files in the event the data\_file\_url does not work.”  
- Use AI to help write your documentation such as requirements satisfaction. Take care to edit the output as it will likely produce more than needed or give overlay verbose documentation.

**Individual Requirements:**  
Your requirement numbers will be the same as for your previous assignments. You must implement **both** of your assignment requirements. Then, you may choose to do some of the other requirements for extra credit.

1. **Persistent User Identification and History**  
   Use cookies or sessions to check if a user has already visited the quiz game. If so, welcome them back and show them their score history. If it’s their first visit, ask them for their name and save it in a cookie/session which will be used to identify them in subsequent visits. Use sessions and cookies to track the user’s quiz score history.  
2. **Leaderboard System**  
   After completing the quiz, ask the user for their name. Implement a global leaderboard to rank users based on their quiz scores. Display the top 10 high scores and allow users to view their ranking.  
3. **Timer-Based Challenge Mode**  
   Include a timed quiz mode where each question must be answered within a certain time. Display a countdown timer and end the quiz if the timer reaches zero.  
4. **Difficulty Levels**  
   Enable users to select a difficulty level (e.g., Easy, Medium, Hard) before starting. Add difficulty level to the questions.  Offer questions based on the difficulty level selected, adjusting the scoring for each level.  
5. **Hint System**  
   Add a hint system where users can request a hint on a question. For balance, deduct points when hints are used, or limit hints to one per quiz.  
6. **Randomized Quiz Categories**  
   Divide questions into categories, such as Science, History, and Sports. Allow users to select a category for the quiz and provide a score summary per category.  
7. **Interactive Visual Feedback**  
   Implement animations or visual effects for correct and incorrect answers. For example, correct answers could turn green, while incorrect answers turn red with an explanation.  
8. **Progress Bar**  
   Include a progress bar to visually represent quiz completion status. The bar should fill as the user answers each question.  
9. **Question Review and Explanation**  
   After each question, show a brief explanation of the correct answer. At the end, provide a review screen for users to revisit questions they missed with explanations.  
10. **Responsive Design for Mobile**  
    Design the application to be fully responsive, ensuring it works seamlessly on both desktop and mobile devices (consider using a framework such a Bootstrap). Test across multiple screen sizes to enhance accessibility.

**Use of AI:**   
You are encouraged to use AI to help you with this assignment (Claude is a good choice). If you use AI-generated code, you are required to do the following:

- You must **specify where and how you used AI** in your code comments e.g. “This function was generated using ChatGPT with the prompt …”  
- You must provide **adequate comments** in the code. AI-generated code tends to provide too detailed comments about what specific code does and not what the code does for the overall application.  
- You must ensure that the code you use **meets the requirements for the assignment**.   
- **Never** not use generated code that you **do not fully understand**. AI may utilize more advanced programming concepts and things we did not discuss in class. Using code you don’t understand will quickly lead to a system that you will have difficulty adapting and evolving to your particular requirements. Either adapt the code to what you fully understand or **don’t use it.**

There is no penalty for using AI. However, failing to follow the above guidelines will result in point deductions. If you use AI just for reference and examples you do not need to do the above. You are discouraged from using AI to build the entire application. You are likely to get better results if you use AI to help with small parts and put these parts together.