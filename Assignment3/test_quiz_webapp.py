# test_quiz_webapp.py
# Assignment 3 - Quiz Web Application Test Suite
# Covers all 7 main functional requirements (FR1-FR7)
# and individual requirements 1 (Persistent User ID) and 8 (Progress Bar).
#
# Run from the Assignment3 directory:
#   cd Assignment3
#   pytest test_quiz_webapp.py -v

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quiz_webapp import app

# ---------------------------------------------------------------------------
# Shared test data
# ---------------------------------------------------------------------------

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

# In-memory score history shared across a test's client fixture and test body.
_history_store: dict = {}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def reset_history():
    """Clear the in-memory score history before (and after) every test."""
    _history_store.clear()
    yield
    _history_store.clear()


@pytest.fixture
def client(monkeypatch):
    """Flask test client with file I/O fully mocked."""
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


def _update_history(h: dict):
    """Helper used by the save mock to update the shared store in-place."""
    _history_store.clear()
    _history_store.update(h)


# ---------------------------------------------------------------------------
# Request helpers
# ---------------------------------------------------------------------------

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


def _complete_quiz(client, all_correct=True):
    """Answer every question in the current quiz session and fetch the results page."""
    for _ in range(len(SAMPLE_QUESTIONS)):
        sess = _session(client)
        q = sess["questions"][sess["current_index"]]
        if all_correct:
            answer = q["correct_answer"]
        else:
            answer = next(o for o in q["options"] if o != q["correct_answer"])
        _answer(client, answer, follow=True)
        client.get("/quiz")  # advance to next question (redirects to /result on last)
    return client.get("/result")


# ===========================================================================
# FR1 — User Interface Requirements
# ===========================================================================

class TestUserInterface:
    def test_home_page_renders_html(self, client):
        """FR1: Home page returns HTML with expected structural elements."""
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"<html" in resp.data or b"<!DOCTYPE" in resp.data

    def test_quiz_page_renders_form(self, client):
        """FR1: Quiz page contains a form for selecting and submitting an answer."""
        _login(client)
        _start(client)
        resp = client.get("/quiz")
        assert b"<form" in resp.data
        assert b'type="radio"' in resp.data
        assert b"Submit Answer" in resp.data

    def test_feedback_page_renders_after_answer(self, client):
        """FR1: Dedicated feedback page is shown immediately after each answer."""
        _login(client)
        _start(client)
        sess = _session(client)
        resp = _answer(client, sess["questions"][0]["correct_answer"])
        assert resp.status_code == 200
        assert b"feedback" in resp.data.lower() or b"correct" in resp.data.lower()

    def test_results_page_renders(self, client):
        """FR1: Results page renders after completing the quiz."""
        _login(client)
        _start(client)
        resp = _complete_quiz(client)
        assert resp.status_code == 200
        assert b"Score" in resp.data or b"score" in resp.data


# ===========================================================================
# FR2 — Question Display Requirements
# ===========================================================================

class TestQuestionDisplay:
    def test_questions_loaded_into_session(self, client):
        """FR2: Questions are loaded dynamically (not hardcoded) into the session."""
        _login(client)
        _start(client)
        sess = _session(client)
        assert "questions" in sess
        assert len(sess["questions"]) == len(SAMPLE_QUESTIONS)

    def test_question_text_visible_on_quiz_page(self, client):
        """FR2: The current question's text appears on the quiz page."""
        _login(client)
        _start(client)
        current_q = _session(client)["questions"][0]
        resp = client.get("/quiz")
        assert current_q["question"].encode() in resp.data

    def test_all_answer_options_visible(self, client):
        """FR2: All answer options for the current question are displayed."""
        _login(client)
        _start(client)
        current_q = _session(client)["questions"][0]
        resp = client.get("/quiz")
        for option in current_q["options"]:
            assert option.encode() in resp.data

    def test_question_order_is_randomized(self, client):
        """FR2: Question order is shuffled differently across multiple sessions."""
        orders = []
        for _ in range(12):
            _login(client, "RandomUser")
            client.get("/start")
            orders.append(tuple(q["question"] for q in _session(client)["questions"]))
        unique_orders = set(orders)
        assert len(unique_orders) > 1, \
            "Question order should vary across sessions (12 runs produced only one order)"

    def test_answer_option_order_is_randomized(self, client):
        """FR2: Answer option order is shuffled for each session."""
        option_orders = []
        for _ in range(12):
            _login(client, "RandomUser")
            client.get("/start")
            first_q = _session(client)["questions"][0]
            option_orders.append(tuple(first_q["options"]))
        assert len(set(option_orders)) > 1, \
            "Answer option order should vary across sessions"


# ===========================================================================
# FR3 — Answer Submission and Feedback
# ===========================================================================

class TestAnswerFeedback:
    def test_correct_answer_shows_positive_feedback(self, client):
        """FR3: Correct answer submission results in positive on-screen feedback."""
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        resp = _answer(client, correct)
        assert b"Correct" in resp.data

    def test_incorrect_answer_shows_negative_feedback(self, client):
        """FR3: Wrong answer shows negative feedback and reveals the correct answer."""
        _login(client)
        _start(client)
        q = _session(client)["questions"][0]
        wrong = next(o for o in q["options"] if o != q["correct_answer"])
        resp = _answer(client, wrong)
        assert b"Not quite" in resp.data or b"Incorrect" in resp.data
        assert q["correct_answer"].encode() in resp.data

    def test_explanation_displayed_after_answer(self, client):
        """FR3: An explanation for the correct answer appears after each submission."""
        _login(client)
        _start(client)
        q = _session(client)["questions"][0]
        resp = _answer(client, q["correct_answer"])
        assert q["explanation"].encode() in resp.data

    def test_score_increments_for_correct_answer(self, client):
        """FR3: Session score increases by 1 when a correct answer is submitted."""
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        _answer(client, correct)
        assert _session(client)["score"] == 1

    def test_score_unchanged_for_wrong_answer(self, client):
        """FR3: Session score does not increase for a wrong answer."""
        _login(client)
        _start(client)
        q = _session(client)["questions"][0]
        wrong = next(o for o in q["options"] if o != q["correct_answer"])
        _answer(client, wrong)
        assert _session(client).get("score", 0) == 0


# ===========================================================================
# FR4 — Data Management Requirements
# ===========================================================================

class TestDataManagement:
    def test_each_question_has_required_fields(self, client):
        """FR4: Every question loaded from JSON has question, options, correct_answer, and explanation."""
        _login(client)
        _start(client)
        for q in _session(client)["questions"]:
            assert "question" in q
            assert "options" in q
            assert "correct_answer" in q
            assert "explanation" in q

    def test_score_saved_after_completing_quiz(self, client):
        """FR4: Completing the quiz persists the user's score to the data store."""
        _login(client, "Alice")
        _start(client)
        _complete_quiz(client)
        assert "Alice" in _history_store
        assert len(_history_store["Alice"]) == 1

    def test_score_entry_has_score_total_and_date(self, client):
        """FR4: Each saved score entry contains score, total, and date fields."""
        _login(client, "Alice")
        _start(client)
        _complete_quiz(client)
        entry = _history_store["Alice"][0]
        assert "score" in entry
        assert "total" in entry
        assert "date" in entry

    def test_multiple_game_scores_all_saved(self, client):
        """FR4: Playing multiple games accumulates all scores in the data store."""
        _login(client, "Bob")
        for _ in range(2):
            _start(client)
            _complete_quiz(client)
        assert len(_history_store.get("Bob", [])) == 2


# ===========================================================================
# FR5 — Backend / Route Requirements
# ===========================================================================

class TestBackendRoutes:
    def test_home_route_returns_200(self, client):
        """FR5: GET / is accessible and returns 200."""
        assert client.get("/").status_code == 200

    def test_start_route_redirects_to_quiz(self, client):
        """FR5: GET /start initialises the quiz and redirects to /quiz."""
        _login(client)
        resp = client.get("/start")
        assert resp.status_code == 302
        assert "quiz" in resp.headers["Location"]

    def test_quiz_get_returns_200(self, client):
        """FR5: GET /quiz returns the question page."""
        _login(client)
        resp = _start(client)
        assert resp.status_code == 200

    def test_quiz_post_processes_answer(self, client):
        """FR5: POST /quiz with a valid answer returns feedback (200)."""
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        resp = _answer(client, correct, follow=False)
        assert resp.status_code == 200  # renders question_result.html directly

    def test_result_route_returns_200_after_quiz(self, client):
        """FR5: GET /result returns 200 after the quiz is finished."""
        _login(client)
        _start(client)
        resp = _complete_quiz(client)
        assert resp.status_code == 200

    def test_logout_route_clears_session(self, client):
        """FR5: GET /logout clears the session and redirects to home."""
        _login(client, "TestUser")
        client.get("/logout")
        assert _session(client).get("username") is None

    def test_quiz_without_session_redirects_home(self, client):
        """FR5: GET /quiz with no active session redirects to home."""
        resp = client.get("/quiz")
        assert resp.status_code == 302
        assert resp.headers["Location"].endswith("/")

    def test_result_without_session_redirects_home(self, client):
        """FR5: GET /result with no active session redirects to home."""
        resp = client.get("/result")
        assert resp.status_code == 302


# ===========================================================================
# FR6 — Score Tracking and Feedback
# ===========================================================================

class TestScoreTrackingFeedback:
    def test_final_score_displayed_on_results_page(self, client):
        """FR6: Results page shows the final score as correct/total."""
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client, all_correct=True)
        total = len(SAMPLE_QUESTIONS)
        assert f"{total}/{total}".encode() in resp.data

    def test_correct_count_shown_on_results(self, client):
        """FR6: Results page shows how many answers were correct."""
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client, all_correct=True)
        assert b"Correct" in resp.data

    def test_incorrect_count_shown_on_results(self, client):
        """FR6: Results page shows how many answers were incorrect."""
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client, all_correct=False)
        assert b"Incorrect" in resp.data

    def test_time_taken_shown_on_results(self, client):
        """FR6: Results page includes the time taken to complete the quiz."""
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client)
        assert b"Time taken" in resp.data

    def test_answer_review_section_present(self, client):
        """FR6: Results page includes an answer review section with explanations."""
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client)
        assert b"Answer Review" in resp.data

    def test_explanations_appear_in_review(self, client):
        """FR6: Each question's explanation appears in the answer review."""
        _login(client, "Scorer")
        _start(client)
        resp = _complete_quiz(client)
        for q in SAMPLE_QUESTIONS:
            assert q["explanation"].encode() in resp.data


# ===========================================================================
# FR7 — Error Handling and Validation
# ===========================================================================

class TestErrorHandling:
    def test_empty_name_shows_error_message(self, client):
        """FR7: Submitting an empty name field shows a user-friendly error."""
        resp = client.post("/", data={"name": ""}, follow_redirects=True)
        assert b"Please enter your name" in resp.data

    def test_whitespace_only_name_shows_error(self, client):
        """FR7: A name consisting only of whitespace is rejected with an error."""
        resp = client.post("/", data={"name": "   "}, follow_redirects=True)
        assert b"Please enter your name" in resp.data

    def test_submitting_without_selecting_answer_shows_error(self, client):
        """FR7: Submitting the quiz form with no answer selected shows an error."""
        _login(client)
        _start(client)
        resp = client.post("/quiz", data={"action": "answer"}, follow_redirects=True)
        assert b"Please select an answer" in resp.data

    def test_accessing_result_without_quiz_redirects(self, client):
        """FR7: Navigating directly to /result without a quiz session redirects safely."""
        resp = client.get("/result")
        assert resp.status_code == 302

    def test_accessing_quiz_without_session_redirects(self, client):
        """FR7: Navigating directly to /quiz without a session redirects safely."""
        resp = client.get("/quiz")
        assert resp.status_code == 302


# ===========================================================================
# Individual Requirement 1 — Persistent User Identification and History
# ===========================================================================

class TestPersistentUserIdentification:
    def test_username_saved_in_session_on_first_visit(self, client):
        """IR1: Username is stored in the session after the name form is submitted."""
        _login(client, "Graysen")
        assert _session(client)["username"] == "Graysen"

    def test_returning_user_sees_welcome_back_greeting(self, client):
        """IR1: A user whose name is already in the session sees a welcome-back message."""
        _login(client, "Graysen")
        resp = client.get("/")
        assert b"Graysen" in resp.data
        assert b"Welcome back" in resp.data or b"Hey, Graysen" in resp.data

    def test_new_user_sees_name_entry_form(self, client):
        """IR1: A visitor with no session sees the name entry form, not the welcome back view."""
        resp = client.get("/")
        assert b'name="name"' in resp.data

    def test_returning_user_score_history_displayed(self, client):
        """IR1: Past quiz scores are shown to a returning user on the home page."""
        _history_store["Graysen"] = [
            {"score": 8, "total": 10, "date": "2026-01-01 10:00"}
        ]
        _login(client, "Graysen")
        resp = client.get("/")
        assert b"8" in resp.data
        assert b"10" in resp.data

    def test_new_user_sees_no_history_message(self, client):
        """IR1: A new user with no previous scores sees an appropriate placeholder message."""
        _login(client, "BrandNewUser")
        resp = client.get("/")
        assert b"No previous games" in resp.data or b"first round" in resp.data

    def test_score_history_saved_with_correct_values(self, client):
        """IR1: Completed quiz score is saved with the right score, total, and date."""
        _login(client, "Graysen")
        _start(client)
        _complete_quiz(client, all_correct=True)
        assert "Graysen" in _history_store
        entry = _history_store["Graysen"][0]
        assert entry["score"] == len(SAMPLE_QUESTIONS)
        assert entry["total"] == len(SAMPLE_QUESTIONS)
        assert "date" in entry

    def test_session_username_persists_across_multiple_requests(self, client):
        """IR1: The username stays in the session across several page requests."""
        _login(client, "Persistent")
        for _ in range(3):
            resp = client.get("/")
            assert b"Persistent" in resp.data

    def test_logout_removes_username_from_session(self, client):
        """IR1: Clicking logout clears the username from the session."""
        _login(client, "Graysen")
        client.get("/logout")
        assert _session(client).get("username") is None

    def test_name_form_shown_again_after_logout(self, client):
        """IR1: After logout, the home page shows the name entry form again."""
        _login(client, "Graysen")
        resp = client.get("/logout", follow_redirects=True)
        assert b'name="name"' in resp.data


# ===========================================================================
# Individual Requirement 8 — Progress Bar
# ===========================================================================

class TestProgressBar:
    def test_progress_bar_element_present_on_quiz_page(self, client):
        """IR8: The quiz page includes progress bar HTML elements."""
        _login(client)
        _start(client)
        resp = client.get("/quiz")
        assert b"progress-wrap" in resp.data
        assert b"progress-fill" in resp.data

    def test_progress_bar_starts_at_zero_percent(self, client):
        """IR8: Progress bar shows 0% on the first question (index 0 of 3)."""
        _login(client)
        _start(client)
        resp = client.get("/quiz")
        # quiz.html: width = (index / total * 100)|int = (0/3*100)|int = 0
        assert b"width: 0%" in resp.data

    def test_progress_bar_on_feedback_page_after_first_answer(self, client):
        """IR8: Progress bar appears on the question feedback page."""
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        resp = _answer(client, correct)
        assert b"progress-fill" in resp.data

    def test_progress_bar_advances_after_answering_first_question(self, client):
        """IR8: After answering Q1, the feedback page shows ~33% progress (1 of 3 done)."""
        _login(client)
        _start(client)
        correct = _session(client)["questions"][0]["correct_answer"]
        resp = _answer(client, correct)
        # question_result.html: width = (index+1)*100 // total = 1*100//3 = 33
        assert b"width: 33%" in resp.data

    def test_progress_bar_at_second_question(self, client):
        """IR8: Quiz page shows 33% at question 2 (index 1 of 3)."""
        _login(client)
        _start(client)
        correct_q1 = _session(client)["questions"][0]["correct_answer"]
        _answer(client, correct_q1)
        resp = client.get("/quiz")
        # quiz.html: width = (1/3*100)|int = 33
        assert b"width: 33%" in resp.data

    def test_progress_bar_at_66_percent_after_second_answer(self, client):
        """IR8: After answering Q2, the feedback page shows ~66% progress (2 of 3 done)."""
        _login(client)
        _start(client)
        # Answer Q1
        _answer(client, _session(client)["questions"][0]["correct_answer"])
        client.get("/quiz")
        # Answer Q2
        correct_q2 = _session(client)["questions"][1]["correct_answer"]
        resp = _answer(client, correct_q2)
        # question_result.html: (2)*100//3 = 66
        assert b"width: 66%" in resp.data

    def test_progress_bar_reaches_100_percent_after_last_question(self, client):
        """IR8: After answering the last question, the progress bar shows 100%."""
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


# ---------------------------------------------------------------------------
# Integration test — verify questions.json is valid (no mocking)
# ---------------------------------------------------------------------------

class TestJSONFileIntegration:
    @pytest.fixture
    def assignment_dir(self):
        """Change working directory to Assignment3 so file paths resolve correctly."""
        original = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        yield
        os.chdir(original)

    def test_questions_json_is_valid_and_loadable(self, assignment_dir):
        """FR2/FR4: questions.json exists, is valid JSON, and each entry has required fields."""
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
        """FR4: load_score_history() returns empty dict if the file does not exist."""
        import quiz_webapp
        # Temporarily point to a nonexistent file by patching open
        original_load = quiz_webapp.load_score_history

        # Direct unit test of the function's except branch
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
