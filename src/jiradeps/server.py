from flask import Flask, render_template, request, session, redirect, url_for, flash


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = b'qew3fsafgb43gherbfd'
    app.server = 'https://jira.tngtech.com'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session['username'] = request.form['username']
            session['password'] = request.form['password']
            return redirect(url_for('index'))
        return render_template('login.html', server=app.server)

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        for k in 'username', 'password', 'server':
            session.pop(k, None)
        return redirect(url_for('index'))

    @app.route('/')
    def index():
        if 'username' not in session:
            flash('You need to log in first,  with your Jira server', 'error')
        return render_template('index.html', config=app.config)

    @app.route('/deps/<key>')
    def generate(key: str):
        return f'Key: {key}'

    return app


def main():
    create_app().run(debug=True)


if __name__ == '__main__':
    main()
