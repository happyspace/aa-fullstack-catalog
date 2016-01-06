from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)

    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(menu_items=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'],
                            restaurant_id=restaurant_id,
                            description=request.form.get('description', ""),
                            price=request.form.get('price'))
        session.add(new_item)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    if request.method == 'POST':
        menu_item.name = request.form['name']
        menu_item.price = request.form.get('price', '$0.0')
        menu_item.description = request.form.get('description', '')
        session.commit()
        flash("menu item edited!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, menu_item=menu_item)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurant_menu_item_jason(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    return jsonify({"MenuItem": menu_item.serialize})


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        flash("menu item " + menu_item.name + " deleted!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('deleetemenuitem.html', menu_item=menu_item)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant " + restaurant.name + " deleted!")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('deleterestaurant.html', restaurant=restaurant)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        restaurant = Restaurant(name=request.form['name'])
        session.add(restaurant)
        session.commit()
        flash("new restaurant created!")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        restaurant.name = request.form.get('name', '')
        session.commit()
        flash("Restaurant" + restaurant.name + " edited!")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=restaurant)


@app.route('/restaurants/JSON')
def show_restaurants_json():
    restaurants = session.query(Restaurant)
    return jsonify(restaurant_items=[i.serialize for i in restaurants])


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    # return "Hello World"
    restaurants = session.query(Restaurant)
#    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('restaurant.html', restaurants=restaurants, is_home=True)

if __name__ == '__main__':
    app.secret_key = 'moo moo I am a cow'
    app.debug = True
    app.run(host='0.0.0.0', port=5002)