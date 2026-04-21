#Assignment 3
#Name: Graysen Oumi
#Date: April 21, 2026

#This is a Flask web app version of the quiz game from Assignment 1, converted from a console app to run in the browser

#Extra requirements
#1. Use cookies or sessions to check if a user has already visited the quiz game. If so, welcome them back and show them their score history. If it’s their first visit, ask them for their name and save it in a cookie/session which will be used to identify them in subsequent visits. Use sessions and cookies to track the user’s quiz score history.
#8. Include a progress bar to visually represent quiz completion status. The bar should fill as the user answers each question.

#I used Claude to help me convert the Assignment 1 console quiz into a Flask web app with the prompt
#"Convert my Assignment 1 Python quiz game into a Flask web app that uses sessions to track state between requests and fulfills the following requirements"
#I made sure I understood all the Flask routing and session logic before using it, I also edited all of the comments to explain
#my understanding and also iterated on the original code because a bunch of it didn't make sense to me.

import json
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

#Need to add enumerate as a Jinja2 filter so the templates can use it the same way python does
app.jinja_env.filters['enumerate'] = enumerate

#Flask requires a secret key to use sessions, this is what encrypts the session cookie
app.secret_key = "quiz_secret_key_2026"


#This loads all the questions from the JSON file and returns them as a list, same idea as reading from the txt file in Assignment 1
def load_questions():
    with open("questions.json", "r") as f:
        return json.load(f)


#This loads the score history from a JSON file so we can show returning users their past scores (requirement 1)
#Returns an empty dict if the file doesnt exist yet so the first run doesnt crash
def load_score_history():
    try:
        with open("score_history.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


#This saves the updated score history back to the file after every quiz (requirement 1)
def save_score_history(history):
    with open("score_history.json", "w") as f:
        json.dump(history, f, indent=2)


#This shuffles the question order and randomizes the answer options for each question before a quiz starts
#I wanted to keep the same randomization behavior from Assignment 1 but now it needs to live in the session so the order stays stable across page loads
def prepare_quiz():
    questions = load_questions()
    random.shuffle(questions)

    prepared = []
    for q in questions:
        options = q["options"][:]
        random.shuffle(options)
        prepared.append({
            "question": q["question"],
            "options": options,
            "correct_answer": q["correct_answer"],
            "explanation": q["explanation"],
            "hint": q.get("hint"),  
            #hint is optional
        })
    return prepared


#Home page route — checks if the user already has a session and greets them if so, otherwise asks for their name (requirement 1)
@app.route("/", methods=["GET", "POST"])
def home():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            error = "Please enter your name to continue."
        else:
            session["username"] = name
            return redirect(url_for("home"))

    username = session.get("username")
    score_history = []

    if username:
        all_history = load_score_history()
        score_history = all_history.get(username, [])

    return render_template("index.html", username=username, score_history=score_history, error=error)


#This route sets up a fresh quiz by loading and shuffling the questions and storing them in the session
#I reset score and answer tracking here so replaying doesn't carry over the old results
@app.route("/start")
def start():
    questions = prepare_quiz()
    session["questions"] = questions
    session["current_index"] = 0
    session["score"] = 0
    session["answers"] = []
    session["start_time"] = datetime.now().isoformat()
    return redirect(url_for("quiz"))


#This is the main quiz route that handles showing questions and processing answers one at a time
#GET shows the current question and POST handles the submitted answer, then redirects to a feedback page before moving on
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = session.get("questions")
    if not questions:
        return redirect(url_for("home"))

    index = session.get("current_index", 0)

    #If all questions have been answered, send the user to results
    if index >= len(questions):
        return redirect(url_for("result"))

    current_q = questions[index]
    feedback = None

    if request.method == "POST":
        action = request.form.get("action")

        #If the user asked for a hint, show the question again with the hint shown (requirement 6)
        if action == "hint":
            hint_text = current_q.get("hint", "No hint available.")
            return render_template(
                "quiz.html",
                question=current_q,
                index=index,
                total=len(questions),
                hint=hint_text,
                show_hint=True,
            )

        selected = request.form.get("answer")
        if not selected:
            return render_template(
                "quiz.html",
                question=current_q,
                index=index,
                total=len(questions),
                error="Please select an answer before submitting.",
            )

        is_correct = selected == current_q["correct_answer"]

        if is_correct:
            session["score"] = session.get("score", 0) + 1

        #Store each answer result so we can show the full review at the end (requirement 9)
        answers = session.get("answers", [])
        answers.append({
            "question": current_q["question"],
            "selected": selected,
            "correct_answer": current_q["correct_answer"],
            "explanation": current_q["explanation"],
            "is_correct": is_correct,
        })
        session["answers"] = answers
        session["current_index"] = index + 1
        session.modified = True

        feedback = {
            "is_correct": is_correct,
            "selected": selected,
            "correct_answer": current_q["correct_answer"],
            "explanation": current_q["explanation"],
        }

        #Show the answer feedback page with the explanation before letting the user move on (requirement 7)
        return render_template(
            "question_result.html",
            feedback=feedback,
            index=index,
            total=len(questions),
            next_index=index + 1,
        )

    return render_template(
        "quiz.html",
        question=current_q,
        index=index,
        total=len(questions),
    )


#Results page that shows the final score, how long it took, and a review of every question (requirements 7 and 9)
#Also saves the score to the user's history so they can see it next time they visit (requirement 1)
@app.route("/result")
def result():
    questions = session.get("questions")
    if not questions:
        return redirect(url_for("home"))

    score = session.get("score", 0)
    total = len(questions)
    answers = session.get("answers", [])
    username = session.get("username", "Anonymous")

    #Calculate how long the quiz took using the start time we saved at the beginning
    start_time_str = session.get("start_time")
    time_taken = None
    if start_time_str:
        start_time = datetime.fromisoformat(start_time_str)
        delta = datetime.now() - start_time
        minutes = int(delta.total_seconds() // 60)
        seconds = int(delta.total_seconds() % 60)
        time_taken = f"{minutes}m {seconds}s"

    #Append this quiz result to the user's score history and save it to the file
    all_history = load_score_history()
    user_history = all_history.get(username, [])
    user_history.append({
        "score": score,
        "total": total,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    all_history[username] = user_history
    save_score_history(all_history)

    return render_template(
        "result.html",
        score=score,
        total=total,
        answers=answers,
        username=username,
        time_taken=time_taken,
    )


#Logout just clears the session so a different user can enter their name
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
