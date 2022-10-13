from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

answers = []


@app.get('/')
def get_landing_page():
    """Serves the home page for our survey"""

    title = survey.title
    instructions = survey.instructions

    return render_template('survey_start.html',
        title = title,
        instructions = instructions
    )

@app.post('/begin')
def handle_start_btn():
    """Handles survey start button"""

    return redirect("/question/0")

@app.post('/answer/<int:q_idx>')
def handle_survey_continuation(q_idx):
    """Handles next question continuation"""
    answer = request.form.get("answer")

    answers.append(answer)

    # how_many_answers = len(answers)

    q_idx += 1

    if(q_idx < len(survey.questions)):
        return redirect(f'/question/{q_idx}')
    else:
        return redirect('/completion.html')

@app.get('/question/<int:q_idx>')
def load_questions_page(q_idx):
    """Loads questions from survey instances to serve to user"""

    question = survey.questions[q_idx]
    choices = question.choices


    return render_template('question.html',
        question = question,
        choices = choices,
        q_idx = q_idx
    )
