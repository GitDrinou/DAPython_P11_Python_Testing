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
        flash("Format d'email invalide. Veuillez réessayer.", 'error')
        return redirect(url_for('index'))

    club = next((club for club in clubs if club['email'] == email), None)

    if not club:
        flash("Aucun club trouvé avec cet email. Veuillez réessayer.", 'error')
        return redirect(url_for('index'))

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    if not competition or not club:
        flash("Le nom du club ou de la compétition est manquant.")
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions)

    found_club = next((c for c in clubs if c['name'] == club), None)
    found_competition = next(
        (c for c in competitions if c['name'] == competition),
        None)

    if not found_club or not found_competition:
        if not found_club:
            flash(f"Le club '{club}' n'a pas été trouvé.", 'error')

        if not found_competition:
            flash(f"La compétition '{competition}' n'a pas été trouvée.",
                  'error')

        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions)

    return render_template(
        'booking.html',
        club=found_club,
        competition=found_competition)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = next(
        (c for c in competitions if c['name'] == request.form['competition']),
        None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    places_required = int(request.form['places'])
    club_points = int(club['points'])
    available_places = int(competition['numberOfPlaces'])

    if not competition or not club:
        flash('Competition or club not found.')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions)

    if (club_points >= places_required and available_places >=
            places_required):
        competition['numberOfPlaces'] = available_places - places_required
        club['points'] = str(int(club['points']) - places_required)
        flash(f"Great-booking complete, with {places_required} places "
              f"booked", 'success')

    if int(competition['numberOfPlaces']) == 0:
        flash("Cette compétition est complète.", 'error')
        return redirect(url_for('index'))

    if places_required > int(competition['numberOfPlaces']):
        flash('Pas assez de places disponibles', 'error')
        return redirect(url_for('index'))

    if places_required > 12:
        flash("Vous ne pouvez pas réserver plus de 12 places par "
              "compétition", 'error')
        return redirect(url_for('index'))

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
