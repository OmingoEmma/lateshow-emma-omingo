import csv
import random
from app import create_app, db
from app.models import Episode, Guest, Appearance

app = create_app()

with app.app_context():
    # Clear existing data
    Appearance.query.delete()
    Guest.query.delete()
    Episode.query.delete()

    with open('seed.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        episode_number = 1

        for row in reader:
            # Create or get Episode
            episode = Episode.query.filter_by(number=episode_number).first()
            if not episode:
                episode = Episode(
                    number=episode_number,
                    date=row['Show']
                )
                db.session.add(episode)

            # Create or get Guest
            guest = Guest.query.filter_by(name=row['Raw_Guest_List']).first()
            if not guest:
                guest = Guest(
                    name=row['Raw_Guest_List'],
                    occupation=row['GoogleKnowlege_Occupation']
                )
                db.session.add(guest)

            db.session.flush()

            # Create Appearance with random rating
            rating = random.randint(1, 5)
            appearance = Appearance(
                rating=rating,
                guest_id=guest.id,
                episode_id=episode.id
            )
            db.session.add(appearance)
            episode_number += 1

        db.session.commit()
        print("Database seeded successfully!")
