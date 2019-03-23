from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, g,  make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items, User
from functools import wraps
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import requests, random, string, httplib2, json

app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/bookcatalog')
def homePage():
    """Show the main page of the app displaying the categories with the 6 latest added items"""
    categories = session.query(Categories).all()
    items = session.query(Items).order_by(
        Items.id.desc()).limit(6)
    if 'username' not in login_session:  # make sure user has logined
        return render_template('public.html', categories=categories,
                               items=items)
    else:  # if user logined, able to access create a new item
        return render_template('logged.html', categories=categories,
                               items=items)


@app.route('/bookcatalog/<int:categories_id>')
def showCategories(categories_id):
    """Show items inside the specified category"""
    allcategories = session.query(Categories).all()
    categories = session.query(Categories).filter_by(id=categories_id).one()
    items = session.query(Items).filter_by(category_id=categories.id)
    return render_template('category.html', categories=categories, items=items,
                           allcategories=allcategories)


@app.route('/bookcatalog/<int:categories_id>/<int:items_id>')
def showItem(categories_id, items_id):
    """Show details of a specified item.

    Args:
        categories_id (int): The id of the category to which the item
            belongs.
        items_id (int): The id of the item.
    """

    categories = session.query(Categories).filter_by(id=categories_id).one()
    items = session.query(Items).filter_by(id=items_id).one()
    if 'username' not in login_session or \
            items.user_id != login_session['user_id']:
        # make sure user logined and user is the creator
        return render_template('publicitem.html', categories=categories,
                               items=items)
    else:  # if user is the creator, able to access update and delete the item
        return render_template('item.html', categories=categories, items=items)


@app.route('/login')
def showLogin():
    """Show the login page to the user."""
    # Create a state token to prevent request forgery.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Handle Google sign in."""
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
            connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; height: 200px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions:

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    """Revoke a current user's token and reset their login session."""
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # If the given token was invalid notice the user.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response




# Login Required function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You must be logged in to access there.")
            return redirect('/login')
    return decorated_function


@app.route('/bookcatalog/new', methods=['GET', 'POST'])
@login_required
def newItem():
    """Allow users to create a new item."""
    if request.method == 'POST':  # get data from the form
        newItem = Items(name=request.form['name'],
                               description=request.form['description'],
                               category_id=request.form['category_id'],
                               author=request.form['author'],
                               user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("New book item created!")
        return redirect(url_for('homePage'))
    else:
        return render_template('newitem.html')


@app.route('/bookcatalog/<int:categories_id>/<int:items_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editItem(categories_id, items_id):
    """Allow users to edit their own items"""
    editedItem = session.query(Items).filter_by(id=items_id).one()
    # make sure user is the creator
    if editedItem.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not allowed"\
         "to edit this item as you're not the owner of it.');"\
         "window.location = '/';}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if not request.form['name']:
            editedItem.name = editedItem.name
        else:
            editedItem.name = request.form['name']

        if not request.form['author']:
            editedItem.author = editedItem.author
        else:
            editedItem.author = request.form['author']

        # if description is empty it will return unchange
        if not request.form['description']:
            editedItem.description = editedItem.description
        else:
            editedItem.description = request.form['description']

        # if category is empty it will return unchange
        if not request.form['category_id']:
            editedItem.category_id = editedItem.category_id
        else:
            editedItem.category_id = request.form['category_id']

        session.add(editedItem)
        session.commit()
        flash("Item edited successfully!")
        return redirect(url_for('showItem', categories_id=request.form['category_id'],
                                items_id=items_id))
    else:
        return render_template('edititem.html', categories_id=categories_id,
                               items_id=items_id, item=editedItem)


@app.route('/bookcatalog/<int:categories_id>/<int:items_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteItem(categories_id, items_id):
    """Allow users to delete their own items"""
    itemToDelete = session.query(Items).filter_by(id=items_id).one()
    # make sure user is the creator
    if itemToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not allowed "\
         "to delete this item as you're not the owner of it."\
         " .');window.location = '/';}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item deleted successfully!")
        return redirect(url_for('showCategories', categories_id=categories_id))
    else:
        return render_template('deleteitem.html', categories_id=categories_id,
                               items_id=items_id, item=itemToDelete)


@app.route('/logout')
def logout():
    """Log out and clear the login session"""
    if 'username' in login_session:
        gdisconnect()
        login_session.clear()
        flash("You have been logged out.")
        return redirect(url_for('homePage'))
    else:
        flash("You were not logged in.")
        return redirect(url_for('homePage'))


# JSON Endpoints:

@app.route('/bookcatalog/JSON')
def catalogJSON():
    categorieslist = session.query(Categories).all()
    return jsonify(CategoriesList=[r.serialize for r in categorieslist])

@app.route('/bookcatalog/<int:categories_id>/JSON')
def categoryJSON(categories_id):
    categories = session.query(Categories).filter_by(id=categories_id).one()
    items = session.query(Items).filter_by(categories_id=categories.id)
    return jsonify(CategoryItem=[i.serialize for i in items])

@app.route('/bookcatalog/<int:categories_id>/<int:items_id>/JSON')
def itemJSON(categories_id, items_id):
    categories = session.query(Categories).filter_by(id=categories_id).one()
    items = session.query(Items).filter_by(id=items_id).one()
    return jsonify(ItemDetails=[items.serialize])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)

