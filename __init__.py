#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, GameGenre, Game, Users
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import os


path = os.path.dirname(__file__)
app = Flask(__name__)

CLIENT_ID = json.loads(open(path+'/client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///games.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# For SignIn

@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code, now compatible with Python3

    request.get_data()
    code = request.data.decode('utf-8')

    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets(path + '/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = \
            make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token

    # Submit request, parse response - Python3 compatible

    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += \
        ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash('you are now logged in as %s' % login_session['username'])
    return output


# User Helper Functions

def createUser(login_session):
    newUser = Users(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None


# For SignOut

@app.route('/gdisconnect')
def gdisconnect():

    # Only disconnect a connected user.

    access_token = login_session.get('access_token')
    if access_token is None:
        flash('User not connected!')
        return redirect(url_for('showAllCategories'))
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':

        # Reset the user's sesson.

        username = login_session['username']
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('%s logged out!' % username)
        return redirect(url_for('showAllCategories'))
    else:

        # For whatever reason, the given token was invalid.

        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        flash('Failed to revoke token for given user!')
        return redirect(url_for('showAllCategories'))


# For Reading and listing all Genre and Latest 10 added games(READ)

@app.route('/')
@app.route('/catalog')
def showAllCategories():
    allgenres = session.query(GameGenre).all()
    latestGames = \
        session.query(Game).order_by(desc(Game.time)).limit(10)
    return render_template('allgames.html', allgenres=allgenres,
                           games=latestGames, session=login_session)


# For Reading list of games in specifiv genre(READ)

@app.route('/catalog/<category>/items')
def showItems(category):
    try:
        allgenres = session.query(GameGenre).all()
        categoryGames = \
            session.query(Game).filter_by(genre=category).order_by(Game.name).all()
        return render_template('allgames.html', allgenres=allgenres,
                               games=categoryGames, genre=category)
    except Exception, e:
        flash(e.message)
        return redirect(url_for('showAllCategories'))


# For Reading information about specific game(READ)

@app.route('/catalog/<category>/<int:item>')
def showItemDetails(category, item):
    try:
        game = session.query(Game).filter_by(id=item).one()
        return render_template('item.html', game=game)
    except:
        flash('No Game Found!')
        return redirect(url_for('showAllCategories'))


# For Adding a new Game(CREATE)

@app.route('/catalog/add', methods=['GET', 'POST'])
def addItem():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        if request.method == 'POST':
            try:
                name = request.form['name']
                description = request.form['description']
                if not name:
                    return render_template('additem.html', description=description, gamename=True)
                elif not description:
                    return render_template('additem.html', name=name, gamedescription=True)
                else:
                    game = Game(name=name, description=description, genre=request.form['genre'], user_id=login_session['user_id'])
                    session.add(game)
                    flash('New Game %s Successfully Added' % game.name)
                    session.commit()
                    return redirect(url_for('showAllCategories'))
            except:
                flash('Unable to add Game!')
                return redirect(url_for('showAllCategories'))
        else:
            return render_template('additem.html')


# For Editing existing game(UPDATE)

@app.route('/catalog/<int:item>/edit', methods=['GET', 'POST'])
def editItem(item):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        game = session.query(Game).filter_by(id=item).one()
        if not game.user_id == login_session['user_id']:
            flash('Unauthorized Excess!')
            return redirect(url_for('showAllCategories'))
        else:
            if request.method == 'POST':
                try:
                    name = request.form['name']
                    desc = request.form['description']
                    if not name:
                        return render_template('edititem.html', game=game, gamename=True)
                    elif not desc:
                        return render_template('edititem.html', game=game, gamedescription=True)
                    else:
                        game.name = name
                        game.description = desc
                        game.genre = request.form['genre']
                        session.add(game)
                        session.commit()
                        flash('%s edited Successfully!' % game.name)
                        return redirect(url_for('showAllCategories'))
                except:
                    flash('Unable to update Game Info!')
                    return redirect(url_for('showAllCategories'))
            else:
                return render_template('edititem.html', game=game)


# For Deleting existing game(DELETE)

@app.route('/catalog/<int:item>/delete', methods=['GET', 'POST'])
def deleteItem(item):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        try:
            game = session.query(Game).filter_by(id=item).one()
            name = game.name
            if not game.user_id == login_session['user_id']:
                flash('Unauthorized Excess!')
                return redirect(url_for('showAllCategories'))
            else:
                if request.method == 'POST':
                    session.delete(game)
                    session.commit()
                    flash('%s delete Successfully!' % name)
                    return redirect(url_for('showAllCategories'))
                else:
                    return render_template('deleteitem.html', game=game)
        except:
            flash('Unable to Delete Game!')
            return redirect(url_for('showAllCategories'))


# JSON error response, when  data doesn't exist
# or is not found due to some error

error = {'status': 404, 'error': 'Data not found'}


# Gives back JSON object with all games list

@app.route('/catalog.json')
def allGamesJSOn():
    try:
        games = session.query(Game).all()
        return jsonify(Games=[i.serialize for i in games])
    except:
        return jsonify(error)


# Gives back JSON object with games list for specific genre

@app.route('/catalog/<category>.json')
def categoryGamesJSOn(category):
    try:
        genre = session.query(GameGenre).filter_by(name=category).one()
        if genre:
            games = session.query(Game).filter_by(genre=category).all()
            return jsonify(Games=[i.serialize2 for i in games])
        else:
            return jsonify(error)
    except:
        return jsonify(error)


# To handle random url
# Taken from https://stackoverflow.com/a/14023909/6032818

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('showAllCategories'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
