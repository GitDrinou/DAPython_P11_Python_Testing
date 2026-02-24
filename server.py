import json
import re
from json import JSONDecodeError
from typing import TypedDict
from flask import Flask, render_template, request, redirect, flash, url_for, \
    session
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
        return {"error": "The file clubs.json could not be found."}
    except JSONDecodeError:
        return {"error": "The clubs.json file is not a valid JSON file."}
    except KeyError:
        return {"error": "The clubs.json file does not contain a key "
                         "'clubs'."}


def load_competitions():
    try:
        with open('competitions.json') as comps:
            list_of_competitions = json.load(comps)['competitions']
            return list_of_competitions
    except FileNotFoundError:
        return {"error": "The file competitions.json could not be found."}
    except JSONDecodeError:
        return {"error": "The competitions.json file is not a valid JSON "
                         "file."}
    except KeyError:
        return {"error": "The competitions.json file does not contain a key "
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
        flash("Invalid email format. Please try again.", 'error')
        return redirect(url_for('index'))

    club = next((club for club in clubs if club['email'] == email), None)

    if not club:
        flash("No clubs were found with this email address. Please try "
              "again.", 'error')
        return redirect(url_for('index'))

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    if not competition or not club:
        flash("The name of the club or competition is missing.")
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
            flash(f"The club '{club}' was not found.", 'error')

        if not found_competition:
            flash(f"The competition '{competition}' was not found.",
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

    if not competition or not club:
        flash('Competition or club not found.', 'error')
        return redirect(url_for('index'))

    places_required = int(request.form['places'])
    club_points = int(club['points'])
    available_places = int(competition['numberOfPlaces'])

    if int(competition['numberOfPlaces']) == 0:
        flash("This competition is full.", 'error')
        return redirect(url_for('index'))

    if places_required > available_places:
        flash("Not enough places available", 'error')
        return redirect(url_for('index'))

    if places_required > 12:
        flash("You cannot reserve more than 12 places per competition",
              'error')
        return redirect(url_for('index'))

    if places_required > club_points:
        flash("Not enough points", 'error')
        return redirect(url_for('index'))

    competition['numberOfPlaces'] = available_places - places_required
    club['points'] = str(int(club['points']) - places_required)

    flash(f"Great-booking complete, with {places_required} places "
              f"booked", 'success')

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    session.pop('club', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
