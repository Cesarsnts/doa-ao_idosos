import flask from flask, render_template

@app.route('/')
def index():
    return render_template(index.html)

