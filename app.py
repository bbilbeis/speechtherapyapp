from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

# ── Your full exercise catalog, now with images ──
all_exercises = [
    {'id':'ex1','name':'Repeat "pa-ta-ka"','image_url':'https://via.placeholder.com/100?text=Pa-ta-ka'},
    {'id':'ex2','name':'Tongue Twister','image_url':'https://via.placeholder.com/100?text=Twister'},
    {'id':'ex3','name':'Sustain "ah"','image_url':'https://via.placeholder.com/100?text="ah"'},
    {'id':'ex4','name':'Lip Trills','image_url':'https://via.placeholder.com/100?text=Lip+Trills'},
    {'id':'ex5','name':'Vowel Stretch','image_url':'https://via.placeholder.com/100?text=Vowel'}
]

# ── Speech-metric sections for the dashboard ──
metrics = [
    'Pitch (F0)',
    'Jitter/Shimmer',
    'Loudness',
    'Speaking Rate / Pauses'
]

@app.route('/')
def onboarding():
    return render_template('index.html')

# ── Main exercise flow ──
@app.route('/session')
def session_flow():
    # if user has chosen a custom set, use that; otherwise default to first 3
    chosen = session.get('selected')
    if chosen:
        exercises = [ex for ex in all_exercises if ex['id'] in chosen]
    else:
        exercises = all_exercises[:3]

    # reset or initialize performance placeholders
    session['performance'] = [0] * len(exercises)
    return render_template('session.html', exercises=exercises)

# ── Initial signup flow ──
@app.route('/choose', methods=['GET','POST'])
def choose_exercises():
    if request.method=='POST':
        session['selected'] = request.form.getlist('exercises')
        return redirect(url_for('schedule'))
    return render_template('choose_exercises.html', exercises=all_exercises)

# ── Modify existing selection ──
@app.route('/modify', methods=['GET','POST'])
def modify_exercises():
    if request.method=='POST':
        session['selected'] = request.form.getlist('exercises')
        return redirect(url_for('home'))
    return render_template(
        'modify_exercises.html',
        exercises=all_exercises,
        selected=session.get('selected', [])
    )

# ── Schedule picker ──
@app.route('/schedule', methods=['GET','POST'])
def schedule():
    times = ['Morning','Afternoon','Evening','Flexible']
    if request.method=='POST':
        session['schedule'] = request.form.get('time')
        return redirect(url_for('home'))
    return render_template('schedule.html', times=times)

# ── Dashboard ──
@app.route('/home')
def home():
    # map selected IDs → names
    selected_ids   = session.get('selected', [])
    selected_names = [ex['name'] for ex in all_exercises if ex['id'] in selected_ids]

    # overall performance (placeholder)
    overall = session.get('performance', [])

    # prepare per-metric histories (simple placeholders)
    sessions_list = ['Session 1','Session 2','Session 3']
    sections = []
    for metric in metrics:
        # simple ramp example
        history = [20, 50, 80]  
        sections.append({'section': metric, 'labels': sessions_list, 'data': history})

    # leaderboard example
    leaderboard = {
        'You': overall[-1] if overall else 0,
        'Average User': 75,
        'Top Performer': 98
    }

    return render_template(
      'home.html',
      labels=[f"#{i+1}" for i in range(len(overall))],
      data=overall,
      sections=sections,
      leaderboard=leaderboard,
      selected=selected_names,
      schedule=session.get('schedule','Not set')
    )

if __name__=='__main__':
    app.run(debug=True)
