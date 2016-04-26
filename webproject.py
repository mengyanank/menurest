import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/')
def restaurantList():
    cur_restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html',restaurants=cur_restaurants)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/')
def showMenuItem(restaurant_id,menu_id):
    Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return render_template('MenuItem.html',Item=Item)

 # Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)
    #return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',  methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method== 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',Item=deleteItem)
    #return "page to delete a menu item. Task 3 complete!"

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuItemJSON(restaurant_id,menu_id):
    Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=Item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
