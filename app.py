import requests

from flask import Flask, session, url_for, render_template, request, redirect

app = Flask(__name__)

app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'secret-key'
app.config['CLIENT_ID'] = ''					# insert you GitHub OAuth app's client ID
app.config['CLIENT_SECRET'] = ''				# insert you GitHub OAuth app's client secret


@app.route('/')
def index():
    if not 'access_token' in session:
        return render_template('index.html', client_id=app.config['CLIENT_ID'])
    url = 'https://api.github.com/user?access_token={}'
    response = requests.get(url.format(session['access_token']))
    response_json = response.json()
    login = response_json['login']
    return render_template('index.html', username=login)


@app.route('/callback')
def callback():
    if 'code' in request.args:
        url = 'https://github.com/login/oauth/access_token'
        payload = {
            'client_id': app.config['CLIENT_ID'],
            'client_secret': app.config['CLIENT_SECRET'],
            'code': request.args['code'],
        }
        headers = {'Accept': 'application/json'}
        response = requests.post(url, params=payload, headers=headers)
        response_json = response.json()
        if 'access_token' in response_json:
            session['access_token'] = response_json['access_token']
        return redirect(url_for('index'))
    return 'Something is wrong with getting GitHub auth data', 404


@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)