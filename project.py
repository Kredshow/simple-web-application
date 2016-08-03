from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
app = Flask(__name__)

engine = create_engine("sqlite:///puppyshelter.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/shelters')
@app.route('/shelters/')
def mainMenu():
    shelters = session.query(Shelter).all()
    return render_template('main_menu.html', shelters=shelters)

@app.route('/shelters/new', methods=['GET', 'POST'])
def addShelter():
    if request.method == 'POST':
        if (len(request.form["name"]) > 0):
            newShelter = Shelter(name=request.form["name"], address=request.form["address"],
                                city=request.form["city"], state=request.form["city"],
                                zipCode=request.form["zipCode"], website=request.form["webSite"])
            session.add(newShelter)
            session.commit()
            flash("New shelter added!")
            return redirect(url_for('mainMenu'))
        else:
            flash("The Name field is empty!")
            return redirect(url_for('addShelter'))
    else:
        return render_template('new_shelter.html')

@app.route('/shelters/<int:shelter_id>/edit', methods=['GET', 'POST'])
def editShelter(shelter_id):
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    if request.method == 'POST':
        shelter.name = request.form["name"]
        shelter.address = request.form["address"]
        shelter.city = request.form["city"]
        shelter.state = request.form["state"]
        shelter.zipCode = request.form["zipCode"]
        shelter.website = request.form["webSite"]
        session.add(shelter)
        session.commit()
        flash("Shelter edited!")
        return redirect(url_for('mainMenu'))
    else:
        return render_template('edit_shelter.html', shelter=shelter)

@app.route('/shelters/<int:shelter_id>/delete', methods=['GET', 'POST'])
def deleteShelter(shelter_id):
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    if request.method == 'POST':
        session.delete(shelter)
        session.commit()
        flash("Shelter " + shelter.name + " deleted")
        return redirect(url_for('mainMenu'))
    else:
        return render_template('delete_shelter.html', shelter_name=shelter.name, shelter_id=shelter_id)

@app.route('/shelters/<int:shelter_id>')
def puppyMenu(shelter_id):
    shelter = session.query(Shelter).filter_by(id= shelter_id).one()
    puppies = session.query(Puppy).filter_by(shelter_id= shelter_id)
    return render_template('shelter.html', shelter=shelter, puppies=puppies)

@app.route('/shelters/<int:shelter_id>/add', methods=['GET', 'POST'])
def newPuppy(shelter_id):
    if request.method == 'POST':
        newPuppy = Puppy(name= request.form['name'], gender='Male', shelter_id=shelter_id)
        session.add(newPuppy)
        session.commit()
        flash('New puppy added')
        return redirect(url_for('puppyMenu', shelter_id = shelter_id))
    else:
        return render_template('new_puppy.html', shelter_id=shelter_id)

@app.route('/shelters/<int:shelter_id>/<int:puppy_id>/edit', methods=['GET', 'POST'])
def editPuppy(shelter_id, puppy_id):
    if request.method == 'POST':
        puppy = session.query(Puppy).filter_by(id=puppy_id).one()
        flash(puppy.name + " edited")
        puppy.name = request.form['name']
        session.add(puppy)
        session.commit()
        return redirect(url_for('puppyMenu', shelter_id=shelter_id))
    else:
        return render_template('edit_puppy.html', shelter_id=shelter_id, puppy_id=puppy_id)

@app.route('/shelters/<int:shelter_id>/<int:puppy_id>/delete', methods=['GET', 'POST'])
def deletePuppy(shelter_id, puppy_id):
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    if request.method == 'POST':
        session.delete(puppy)
        session.commit()
        flash(puppy.name + " deleted")
        return redirect(url_for('puppyMenu', shelter_id=shelter_id))
    else:
        return render_template('delete_page.html', puppy_name=puppy.name, shelter_id=shelter_id,
                               puppy_id=puppy_id)

@app.route('/shelters/JSON')
def allSheltersJSON():
    shelters = session.query(Shelter).all()
    return jsonify(Shelters=[shelter.serialize for shelter in shelters])

@app.route('/shelters/<int:shelter_id>/JSON')
def shelterJSON(shelter_id):
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    return jsonify(Shelter=shelter.serialize)

@app.route('/puppies/JSON')
def allPupppiesJSON():
    puppies = session.query(Puppy).all()
    return jsonify(Puppies=[puppy.serialize for puppy in puppies])

@app.route('/puppies/<int:shelter_id>/JSON')
def shelterPuppiesJSON(shelter_id):
    puppies = session.query(Puppy).filter_by(shelter_id=shelter_id).all()
    return jsonify(Puppies=[puppy.serialize for puppy in puppies])

@app.route('/puppy/<int:puppy_id>/JSON')
def puppyJSON(puppy_id):
    puppies = session.query(Puppy).filter_by(id=puppy_id).all()
    return jsonify(Puppy=[puppy.serialize for puppy in puppies])

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host="0.0.0.0", port=5000)