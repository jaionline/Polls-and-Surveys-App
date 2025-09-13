from flask import Flask, render_template_string, request, redirect, url_for
import uuid

app = Flask(__name__)

polls = {}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Polls and Surveys App</title>
</head>
<body>
    <h1>Polls & Surveys</h1>
    <form method="post" action="/create">
        <input name="question" placeholder="Enter your poll question" required>
        <br>
        <input name="option1" placeholder="Option 1" required>
        <input name="option2" placeholder="Option 2" required>
        <input name="option3" placeholder="Option 3">
        <input name="option4" placeholder="Option 4">
        <br>
        <button type="submit">Create Poll</button>
    </form>
    <h2>All Polls</h2>
    <ul>
    {% for pid, poll in polls.items() %}
        <li>
            <a href="{{ url_for('vote', poll_id=pid) }}">{{ poll['question'] }}</a>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

VOTE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ poll['question'] }}</title>
</head>
<body>
    <h1>{{ poll['question'] }}</h1>
    <form method="post">
    {% for idx, opt in enumerate(poll['options']) %}
        {% if opt %}
            <input type="radio" name="vote" value="{{ idx }}" required> {{ opt }}<br>
        {% endif %}
    {% endfor %}
        <button type="submit">Vote</button>
    </form>
    <h2>Results</h2>
    <ul>
    {% for idx, opt in enumerate(poll['options']) %}
        {% if opt %}
            <li>{{ opt }}: {{ poll['votes'][idx] }} votes</li>
        {% endif %}
    {% endfor %}
    </ul>
    <a href="{{ url_for('index') }}">Back to polls</a>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML, polls=polls)

@app.route("/create", methods=["POST"])
def create():
    poll_id = uuid.uuid4().hex
    question = request.form["question"]
    options = [
        request.form["option1"],
        request.form["option2"],
        request.form.get("option3"),
        request.form.get("option4")
    ]
    votes = [0, 0, 0, 0]
    polls[poll_id] = {"question": question, "options": options, "votes": votes}
    return redirect(url_for('vote', poll_id=poll_id))

@app.route("/vote/<poll_id>", methods=["GET", "POST"])
def vote(poll_id):
    poll = polls.get(poll_id)
    if not poll:
        return "Poll not found", 404
    if request.method == "POST":
        idx = int(request.form["vote"])
        poll["votes"][idx] += 1
    return render_template_string(VOTE, poll=poll)

if __name__ == "__main__":
    app.run(debug=True)