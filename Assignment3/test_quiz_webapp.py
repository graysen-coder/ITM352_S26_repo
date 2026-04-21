# test_quiz_webapp.py
# Assignment 3 - Quiz Web Application Test Suite
# Covers all 7 main functional requirements (FR1-FR7)
# and individual requirements 1 (Persistent User ID) and 8 (Progress Bar).

#I gave Claude the specifications of the assignment specifically the functional requirements and also 
#the individual requirements that I implemented (1 and 8) and asked it to write a test
#case for every combination of possible user inputs in the website. I specified things like the user entering the main page,
#entering a wrong answer and getting the wrong answer message, the user logging into their account and exiting then checcking to see
#if the quiz history was still there using sessions
#To Run from the Assignment3 directory:
#   cd Assignment3
#   pytest test_quiz_webapp.py -v

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quiz_webapp import app

#These are a small set of sample questions I use in place of the real questions.json so the tests dont depend on the actual file
SAMPLE_QUESTIONS = [
    {
        "question": "What is the largest fish?",
        "options": ["Great White Shark", "Whale Shark", "Giant Oarfish", "Bluefin Tuna"],
        "correct_answer": "Whale Shark",
        "explanation": "The whale shark is the largest fish in the ocean.",
        "hint": "Despite its name, it is not a whale.",
    },
    {
        "question": "How many hearts does an octopus have?",
        "options": ["1", "2", "3", "4"],
        "correct_answer": "3",
        "explanation": "Octopuses have three hearts.",
        "hint": "More than you would expect.",
    },
    {
        "question": "Which fish can walk on land?",
        "options": ["Mudskipper", "Flying Fish", "Lungfish", "Archerfish"],
        "correct_answer": "Mudskipper",
        "explanation": "Mudskippers can use their fins to move on land.",
        "hint": "Its name gives it away.",
    },
]

#This stores score history in memory during tests so we dont have to read and write actual files
_history_store: dict = {}


#This fixture runs before and after every test to make sure score history doesnt carry over between tests
@pytest.fixture(autouse=True)
def reset_history():
    _history_store.clear()
    yield
    _history_store.clear()


#This sets up a Flask test client and replaces all the file I/O with in-memory versions so tests dont touch the filesystem
@pytest.fixture
def client(monkeypatch):
    import quiz_webapp

    monkeypatch.setattr(quiz_webapp, "load_questions",
                        lambda: [dict(q) for q in SAMPLE_QUESTIONS])
    monkeypatch.setattr(quiz_webapp, "load_score_history",
                        lambda: dict(_history_store))
    monkeypatch.setattr(quiz_webapp, "save_score_history",
                        lambda h: _update_history(h))

    app.config.update(TESTING=True, SECRET_KEY="test_secret")

    with app.test_client() as c:
        yield c


#Updates the in-memory history store in place so the monkeypatched save function works correctly
def _update_history(h: dict):
    _history_store.clear()
    _history_store.update(h)


#These helper functions simulate what a real user would do so each test doesnt have to repeat the same setup steps

def _session(client):
    with client.session_transaction() as s:
        return dict(s)


def _login(client, name="TestUser"):
    return client.post("/", data={"name": name}, follow_redirects=True)


def _start(client):
    return client.get("/start", follow_redirects=True)


def _answer(client, answer, follow=True):
    return client.post(
        "/quiz",
        data={"answer": answer, "action": "answer"},
        follow_redirects=follow,
    )


#This loops through all the sample questions and answers each one, then returns the results page
def _complete_quiz(client, all_correct=True):
    for _ in range(len(SAMPLE_QUESTIONS)):
        sess = _session(client)
        q = sess["questions"][sess["current_index"]]
        if all_correct:
            answer = q["correct_answer"]
        else:
            answer = next(o for o in q["options"] if o != q["correct_answer"])
        _answer(client, answer, follow=True)
        client.get("/quiz")
    return client.get("/result")


#FR1 — check that the main pages load and display the right UI elements
class TestUserInterface:
    def test_home_page_renders_html(self, client):
        #Check that the home page loads and returns actual HTML
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"<html" in resp.data or b"<!DOCTYPE" in resp.data

    def test_quiz_page_renders_form(self, client):
        #Check that the quiz page has a form with radio buttons and a submit button
        _login(client)
        _start(client)
        resp = client.get("/quiz")
        assert b"<form" in resp.data
        assert b'type="radio"' in resp.data
        assert b"Submit Answer" in resp.data

    def test_feedback_page_renders_after_answer(self, client):
        #Check that submitting an answer takes you to a feedback page
        _login(client)
        _start(client)
        sess = _session(client)
        resp = _answer(client, sess["questions"][0]["correct_answer"])
        assert resp.status_code == 200
        assert b"feedback" in resp.data.lower() or b"correct" in resp.data.lower()

    def test_results_page_renders(self, client):
        #Check that the results page loads after finishing the quiz
        _login(client)
        _start(client)
        resp = _complete_quiz(client)
        assert resp.status_code == 200
        assert b"Score" in resp.data or b"score" in resp.data


#FR2 — check that questions load from the JSON file, show up on the page, and get randomized
class TestQuestionDisplay:
    def test_questions_loaded_into_session(self, client):
        #Check that starting the quiz loads questions into the session
        _login(client)
        _start(client)
        sess = _session(client)
        assert "questions" in sess
        assert len(sess["questions"]) == len(SAMPLE_QUESTIONS)

    def test_question_text_visible_on_quiz_page(self, client):
        #Check that the current question actually shows up on the quiz page
        _login(client)
        _start(client)
        current_q = _session(client)["questions"][0]
        resp = client.get("/quiz")
        assert current_q["question"].encode() in resp.data

    def test_all_answer_options_visible(self, client):
        #Check that all answer options for the current question are displayed
        _login(client)
        _start(client)
        current_q = _session(client)["questions"][0]
        resp = client.get("/quiz")
        for option in current_q["options"]:
            assert option.encode() in resp.data

    def test_question_order_is_randomized(self, client):
        #Run 12 sessions and check that the question order isnt always the same
        orders = []
        for _ in range(12):
            _login(client, "RandomUser")
            client.get("/start")
            orders.append(tuple(q["question"] for q in _session(client)["questions"]))
        unique_orders = set(orders)
        assert len(unique_orders) > 1, \
            "Question order should vary across sessions (12 runs produced only one order)"

    def test_answer_option_order_is_randomized(self, client):
        #Run 12 sessions and check that the answer options arent always in the same order
        option_orders = []
        for _ in range(12):
            _login(client, "RandomUser")
            client.get("/start")
            first_q = _session(client)["questions"][0]
            option_orders.append(tuple(first_q["options"]))
        assert len(set(option_orders)) > 1, \
            "Answer option order should vary across sessions"


#FR3 — check that submitting answers gives the right feedback and updates the score correctly
class TestAnswerFeedback:
    def test_correct_answer_shows_positive_feedback(self, client):
        #Check that a correct answer shows positive feedback on the page
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        resp = _answer(client, correct)
        assert b"Correct" in resp.data

    def test_incorrect_answer_shows_negative_feedback(self, client):
        #Check that a wrong answer shows negative feedback and reveals the correct answer
        _login(client)
        _start(client)
        q = _session(client)["questions"][0]
        wrong = next(o for o in q["options"] if o != q["correct_answer"])
        resp = _answer(client, wrong)
        assert b"Not quite" in resp.data or b"Incorrect" in resp.data
        assert q["correct_answer"].encode() in resp.data

    def test_explanation_displayed_after_answer(self, client):
        #Check that the explanation shows up after answering a question
        _login(client)
        _start(client)
        q = _session(client)["questions"][0]
        resp = _answer(client, q["correct_answer"])
        assert q["explanation"].encode() in resp.data

    def test_score_increments_for_correct_answer(self, client):
        #Check that the session score goes up by 1 when the user gets a question right
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        _answer(client, correct)
        assert _session(client)["score"] == 1

    def test_score_unchanged_for_wrong_answer(self, client):
        #Check that the score stays the same when the user gets a question wrong
        _login(client)
        _start(client)
        q = _session(client)["questions"][0]
        wrong = next(o for o in q["options"] if o != q["correct_answer"])
        _answer(client, wrong)
        assert _session(client).get("score", 0) == 0


#FR4 — check that questions have the right fields and that scores get saved to the data store
class TestDataManagement:
    def test_each_question_has_required_fields(self, client):
        #Check that every question in the session has all the required fields
        _login(client)
        _start(client)
        for q in _session(client)["questions"]:
            assert "question" in q
            assert "options" in q
            assert "correct_answer" in q
            assert "explanation" in q

    def test_score_saved_after_completing_quiz(self, client):
        #Check that finishing the quiz saves the score to the history store
        _login(client, "Alice")
        _start(client)
        _complete_quiz(client)
        assert "Alice" in _history_store
        assert len(_history_store["Alice"]) == 1

    def test_score_entry_has_score_total_and_date(self, client):
        #Check that each saved score entry has score, total, and date fields
        _login(client, "Alice")
        _start(client)
        _complete_quiz(client)
        entry = _history_store["Alice"][0]
        assert "score" in entry
        assert "total" in entry
        assert "date" in entry

    def test_multiple_game_scores_all_saved(self, client):
        #Check that playing multiple games saves all scores and doesnt overwrite old ones
        _login(client, "Bob")
        for _ in range(2):
            _start(client)
            _complete_quiz(client)
        assert len(_history_store.get("Bob", [])) == 2


#FR5 — check that all the routes are accessible and return the right status codes
class TestBackendRoutes:
    def test_home_route_returns_200(self, client):
        assert client.get("/").status_code == 200

    def test_start_route_redirects_to_quiz(self, client):
        #Check that /start sets up the quiz and redirects to /quiz
        _login(client)
        resp = client.get("/start")
        assert resp.status_code == 302
        assert "quiz" in resp.headers["Location"]

    def test_quiz_get_returns_200(self, client):
        _login(client)
        resp = _start(client)
        assert resp.status_code == 200

    def test_quiz_post_processes_answer(self, client):
        #Check that posting an answer to /quiz returns the feedback page directly as a 200
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        resp = _answer(client, correct, follow=False)
        assert resp.status_code == 200  # renders question_result.html directly

    def test_result_route_returns_200_after_quiz(self, client):
        _login(client)
        _start(client)
        resp = _complete_quiz(client)
        assert resp.status_code == 200

    def test_logout_route_clears_session(self, client):
        #Check that logging out clears the username from the session
        _login(client, "TestUser")
        client.get("/logout")
        assert _session(client).get("username") is None

    def test_quiz_without_session_redirects_home(self, client):
        #Check that going to /quiz with no session redirects back to home
        resp = client.get("/quiz")
        assert resp.status_code == 302
        assert resp.headers["Location"].endswith("/")

    def test_result_without_session_redirects_home(self, client):
        #Check that going to /result with no session redirects back to home
        resp = client.get("/result")
        assert resp.status_code == 302


#FR6 — check that the results page shows the score, time, and answer review correctly
class TestScoreTrackingFeedback:
    def test_final_score_displayed_on_results_page(self, client):
        #Check that the final score shows up as correct/total on the results page
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client, all_correct=True)
        total = len(SAMPLE_QUESTIONS)
        assert f"{total}/{total}".encode() in resp.data

    def test_correct_count_shown_on_results(self, client):
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client, all_correct=True)
        assert b"Correct" in resp.data

    def test_incorrect_count_shown_on_results(self, client):
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client, all_correct=False)
        assert b"Incorrect" in resp.data

    def test_time_taken_shown_on_results(self, client):
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client)
        assert b"Time taken" in resp.data

    def test_answer_review_section_present(self, client):
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client)
        assert b"Answer Review" in resp.data

    def test_explanations_appear_in_review(self, client):
        #Check that each questions explanation shows up in the answer review at the end
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client)
        for q in SAMPLE_QUESTIONS:
            assert q["explanation"].encode() in resp.data


#FR7 — check that the app handles bad input and invalid navigation gracefully
class TestErrorHandling:
    def test_empty_name_shows_error_message(self, client):
        #Check that submitting an empty name shows an error instead of crashing
        resp = client.post("/", data={"name": ""}, follow_redirects=True)
        assert b"Please enter your name" in resp.data

    def test_whitespace_only_name_shows_error(self, client):
        #Check that a name thats just spaces is also rejected
        resp = client.post("/", data={"name": "   "}, follow_redirects=True)
        assert b"Please enter your name" in resp.data

    def test_submitting_without_selecting_answer_shows_error(self, client):
        #Check that submitting the quiz form without picking an answer shows an error
        _login(client)
        _start(client)
        resp = client.post("/quiz", data={"action": "answer"}, follow_redirects=True)
        assert b"Please select an answer" in resp.data

    def test_accessing_result_without_quiz_redirects(self, client):
        #Check that navigating directly to /result without a quiz session doesnt crash
        resp = client.get("/result")
        assert resp.status_code == 302

    def test_accessing_quiz_without_session_redirects(self, client):
        #Check that navigating directly to /quiz without a session doesnt crash
        resp = client.get("/quiz")
        assert resp.status_code == 302


#Individual requirement 1 — check that the app recognizes returning users and shows their score history
class TestPersistentUserIdentification:
    def test_username_saved_in_session_on_first_visit(self, client):
        #Check that entering a name saves it to the session
        _login(client, "Graysen")
        assert _session(client)["username"] == "Graysen"

    def test_returning_user_sees_welcome_back_greeting(self, client):
        #Check that a user already in the session gets a welcome back message
        _login(client, "Graysen")
        resp = client.get("/")
        assert b"Graysen" in resp.data
        assert b"Welcome back" in resp.data or b"Hey, Graysen" in resp.data

    def test_new_user_sees_name_entry_form(self, client):
        #Check that a brand new visitor sees the name form and not the welcome back view
        resp = client.get("/")
        assert b'name="name"' in resp.data

    def test_returning_user_score_history_displayed(self, client):
        #Check that a returning users past scores show up on the home page
        _history_store["Graysen"] = [
            {"score": 8, "total": 10, "date": "2026-01-01 10:00"}
        ]
        _login(client, "Graysen")
        resp = client.get("/")
        assert b"8" in resp.data
        assert b"10" in resp.data

    def test_new_user_sees_no_history_message(self, client):
        #Check that a new user with no history sees a message telling them to play their first round
        _login(client, "BrandNewUser")
        resp = client.get("/")
        assert b"No previous games" in resp.data or b"first round" in resp.data

    def test_score_history_saved_with_correct_values(self, client):
        #Check that the saved score entry has the right score, total, and date after completing a quiz
        _login(client, "Graysen")
        _start(client)
        _complete_quiz(client, all_correct=True)
        assert "Graysen" in _history_store
        entry = _history_store["Graysen"][0]
        assert entry["score"] == len(SAMPLE_QUESTIONS)
        assert entry["total"] == len(SAMPLE_QUESTIONS)
        assert "date" in entry

    def test_session_username_persists_across_multiple_requests(self, client):
        #Check that the username stays in the session across multiple page loads
        _login(client, "Persistent")
        for _ in range(3):
            resp = client.get("/")
            assert b"Persistent" in resp.data

    def test_logout_removes_username_from_session(self, client):
        #Check that logging out removes the username from the session
        _login(client, "Graysen")
        client.get("/logout")
        assert _session(client).get("username") is None

    def test_name_form_shown_again_after_logout(self, client):
        #Check that after logging out the home page shows the name form again
        _login(client, "Graysen")
        resp = client.get("/logout", follow_redirects=True)
        assert b'name="name"' in resp.data


#Individual requirement 8 — check that the progress bar shows up and fills in correctly as the user answers questions
class TestProgressBar:
    def test_progress_bar_element_present_on_quiz_page(self, client):
        #Check that the progress bar HTML elements are on the quiz page
        _login(client)
        _start(client)
        resp = client.get("/quiz")
        assert b"progress-wrap" in resp.data
        assert b"progress-fill" in resp.data

    def test_progress_bar_starts_at_zero_percent(self, client):
        #Check that the progress bar starts at 0% on the first question
        _login(client)
        _start(client)
        resp = client.get("/quiz")
        # quiz.html: width = (index / total * 100)|int = (0/3*100)|int = 0
        assert b"width: 0%" in resp.data

    def test_progress_bar_on_feedback_page_after_first_answer(self, client):
        #Check that the progress bar also shows up on the feedback page after answering
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        resp = _answer(client, correct)
        assert b"progress-fill" in resp.data

    def test_progress_bar_advances_after_answering_first_question(self, client):
        #Check that the progress bar shows ~33% after answering the first of three questions
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        resp = _answer(client, correct)
        # question_result.html: width = (index+1)*100 // total = 1*100//3 = 33
        assert b"width: 33%" in resp.data

    def test_progress_bar_at_second_question(self, client):
        #Check that the quiz page shows 33% when youre on the second question
        _login(client)
        _start(client)
        correct_q1 = _session(client)["questions"][0]["correct_answer"]
        _answer(client, correct_q1)
        resp = client.get("/quiz")
        # quiz.html: width = (1/3*100)|int = 33
        assert b"width: 33%" in resp.data

    def test_progress_bar_at_66_percent_after_second_answer(self, client):
        #Check that the progress bar shows ~66% after answering two of three questions
        _login(client)
        _start(client)
        _answer(client, _session(client)["questions"][0]["correct_answer"])
        client.get("/quiz")
        correct_q2 = _session(client)["questions"][1]["correct_answer"]
        resp = _answer(client, correct_q2)
        # question_result.html: (2)*100//3 = 66
        assert b"width: 66%" in resp.data

    def test_progress_bar_reaches_100_percent_after_last_question(self, client):
        #Check that the progress bar hits 100% after the last question is answered
        _login(client)
        _start(client)
        total = len(SAMPLE_QUESTIONS)
        for i in range(total - 1):
            _answer(client, _session(client)["questions"][i]["correct_answer"])
            client.get("/quiz")
        last_correct = _session(client)["questions"][total - 1]["correct_answer"]
        resp = _answer(client, last_correct)
        # question_result.html: (3)*100//3 = 100
        assert b"width: 100%" in resp.data


#This integration test runs against the real questions.json file to make sure it loads correctly without mocking
class TestJSONFileIntegration:
    @pytest.fixture
    def assignment_dir(self):
        #Change to the Assignment3 directory so the file paths in quiz_webapp resolve correctly
        original = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        yield
        os.chdir(original)

    def test_questions_json_is_valid_and_loadable(self, assignment_dir):
        #Check that questions.json exists, is valid JSON, and every question has all required fields
        from quiz_webapp import load_questions
        questions = load_questions()
        assert isinstance(questions, list)
        assert len(questions) > 0
        for q in questions:
            assert "question" in q, f"Missing 'question' field: {q}"
            assert "options" in q, f"Missing 'options' field: {q}"
            assert "correct_answer" in q, f"Missing 'correct_answer' field: {q}"
            assert "explanation" in q, f"Missing 'explanation' field: {q}"
            assert q["correct_answer"] in q["options"], \
                f"correct_answer '{q['correct_answer']}' not in options {q['options']}"

    def test_score_history_json_loads_gracefully_when_missing(self, assignment_dir, tmp_path):
        #Check that load_score_history returns an empty dict if the file doesnt exist yet
        import quiz_webapp
        import builtins
        original_open = builtins.open

        def raise_not_found(path, *a, **kw):
            if "score_history" in str(path):
                raise FileNotFoundError
            return original_open(path, *a, **kw)

        builtins.open = raise_not_found
        try:
            result = quiz_webapp.load_score_history()
            assert result == {}
        finally:
            builtins.open = original_open


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
