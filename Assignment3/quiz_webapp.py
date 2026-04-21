# quiz_webapp.py
# Name: Graysen Oumi
# Assignment 3 - Flask Quiz Web Application
# Converted from Assignment 1 console quiz game to a Flask web app.

import json
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Custom Jinja2 filter: lets templates do `list|enumerate` just like Python's enumerate()
app.jinja_env.filters['enumerate'] = enumerate

# Secret key required for session management (requirement 1: Persistent User Identification)
# AI suggestion: use a strong random key in production; for dev a fixed string is fine
app.secret_key = "quiz_secret_key_2026"

# ---------------------------------------------------------------------------
# Data loading helpers (converted from Assignment 1's file-reading logic)
# ---------------------------------------------------------------------------

def load_questions():
    """Load questions from questions.json and return as a list of dicts.
    Each dict has: question, options, correct_answer, explanation, hint (optional).
    Generated with AI assistance for JSON loading pattern.
    """
    with open("questions.json", "r") as f:
        return json.load(f)


def load_score_history():
    """Load score history from score_history.json.
    Carries over the requirement from Assignment 1 to persist score history.
    """
    try:
        with open("score_history.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_score_history(history):
    """Persist score history dict keyed by username."""
    with open("score_history.json", "w") as f:
        json.dump(history, f, indent=2)


# ---------------------------------------------------------------------------
# Quiz setup helpers (adapted from Assignment 1's quiz_question class logic)
# ---------------------------------------------------------------------------

def prepare_quiz():
    """Shuffle questions and randomize each question's option order.
    Stores the prepared question list in the session so order is stable per session.
    Satisfies requirement: Randomize both question order and answer options.
    """
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
            "hint": q.get("hint"),  # hint is optional, same as Assignment 1
        })
    return prepared


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    """Home / welcome page.
    Requirement 1: Check cookie/session for returning user; greet them and show history.
    If first visit, ask for their name and save it to the session.
    """
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


@app.route("/start")
def start():
    """Initialize a new quiz session and redirect to the first question.
    Resets quiz-specific session data without clearing the username.
    """
    questions = prepare_quiz()
    session["questions"] = questions
    session["current_index"] = 0
    session["score"] = 0
    session["answers"] = []       # tracks per-question result for review screen
    session["start_time"] = datetime.now().isoformat()
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Quiz page — shows one question at a time.
    GET: Display current question.
    POST: Process submitted answer, store feedback, advance to next question or results.
    Satisfies requirements: Question Display, Answer Submission & Feedback, Score Tracking.
    """
    questions = session.get("questions")
    if not questions:
        return redirect(url_for("home"))

    index = session.get("current_index", 0)

    # All questions answered — go to results
    if index >= len(questions):
        return redirect(url_for("result"))

    current_q = questions[index]
    feedback = None  # shown after the user submits an answer

    if request.method == "POST":
        action = request.form.get("action")

        # --- Hint request ---
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

        # --- Answer submission ---
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

        # Store result for the end-of-quiz review screen (requirement 9)
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

        return render_template(
            "question_result.html",
            feedback=feedback,
            index=index,
            total=len(questions),
            next_index=index + 1,
        )

    # GET — display the question
    return render_template(
        "quiz.html",
        question=current_q,
        index=index,
        total=len(questions),
    )


@app.route("/result")
def result():
    """Results page.
    Displays final score, time taken, and review of all answers.
    Saves score history for the user (Requirement 1 / Assignment 1 carryover).
    """
    questions = session.get("questions")
    if not questions:
        return redirect(url_for("home"))

    score = session.get("score", 0)
    total = len(questions)
    answers = session.get("answers", [])
    username = session.get("username", "Anonymous")

    # Calculate time taken
    start_time_str = session.get("start_time")
    time_taken = None
    if start_time_str:
        start_time = datetime.fromisoformat(start_time_str)
        delta = datetime.now() - start_time
        minutes = int(delta.total_seconds() // 60)
        seconds = int(delta.total_seconds() % 60)
        time_taken = f"{minutes}m {seconds}s"

    # Persist score to user history (carries over Assignment 1 score history requirement)
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


@app.route("/logout")
def logout():
    """Clear the session so a new user can enter their name."""
    session.clear()
    return redirect(url_for("home"))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)