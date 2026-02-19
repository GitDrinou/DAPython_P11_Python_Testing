import json
import re
from json import JSONDecodeError
from typing import TypedDict

from flask import Flask, render_template, request, redirect, flash, url_for

from constants import EMAIL_REGEX


class Club(TypedDict):
    name: str
    email: str
    points: str


def load_clubs():
    try:
        with open('clubs.json') as c:
            list_of_clubs: list[Club] = json.load(c)['clubs']
            return list_of_clubs
    except FileNotFoundError:
        return {"error": "Le fichier clubs.json est introuvable."}
    except JSONDecodeError:
        return {"error": "Le fichier clubs.json n'est pas un JSON valide."}
    except KeyError:
        return {"error": "Le fichier clubs.json ne contient pas de clé "
                         "'clubs'."}


def load_competitions():
    try:
        with open('competitions.json') as comps:
            list_of_competitions = json.load(comps)['competitions']
            return list_of_competitions
    except FileNotFoundError:
        return {"error": "Le fichier competitions.json est introuvable."}
    except JSONDecodeError:
        return {"error": "Le fichier competitions.json n'est pas un JSON "
                         "valide."}
    except KeyError:
        return {"error": "Le fichier competitions.json ne contient pas de clé "
                         "'competitions'."}


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    email = request.form.get('email')

    if not re.match(EMAIL_REGEX, email):
        return render_template(
            'index.html',
            error="Cet email ne correspond pas au format attendu"
        )

    club = next((club for club in clubs if club['email'] == email), None)

    if not club:
        return render_template('index.html', error="Cet email est inconnu")

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions
    )


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form[
        'competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition[
                                            'numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club,
                           competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
