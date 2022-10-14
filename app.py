from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.get('/')
def get_landing_page():
    """Serves the home page for our survey"""

    title = survey.title
    instructions = survey.instructions

    return render_template(
        'survey_start.html',
        title=title,
        instructions=instructions
    )


@app.post('/begin')
def handle_start_btn():
    """Handles survey start button"""
    print("----------- start button ----------")

    session["responses"] = []
    session["active_question_idx"] = 0

    print("session responses is", session["responses"])

    return redirect("/question/0")


@app.post('/response/')
def handle_survey_continuation():
    """Handles next question continuation"""

    q_idx = session["active_question_idx"]
    q_idx += 1
    session["active_question_idx"] = q_idx

    response = request.form.get("response")

    responses_list = session["responses"]
    responses_list.append(response)
    session["responses"] = responses_list

    print("session responses is", session["responses"])

    return redirect(f'/question/{q_idx}')


@app.get('/question/<int:q_idx_url>')
def load_questions_page(q_idx_url):
    """Loads questions from survey instances to serve to user"""

    q_idx = session["active_question_idx"]

    if q_idx_url != q_idx:
        print("------you got here!------")
        flash(f"Hey! Don't try and visit a different question!")
        redirect(f'/question/{q_idx}')

    # for completion page
    if q_idx >= len(survey.questions):
        qa_tuples = [
            (question.question, response)
            for ques_idx, question in enumerate(survey.questions)
            for resp_idx, response in enumerate(session["responses"])
            if ques_idx == resp_idx
        ]
        return render_template('/completion.html', qa_tuples=qa_tuples)

    # for active question
    else:
        question = survey.questions[q_idx]
        choices = question.choices
        return render_template(
            'question.html',
            question=question,
            choices=choices,
            q_idx=q_idx
        )
