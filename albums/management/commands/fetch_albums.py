import os
import requests
from django.core.management.base import BaseCommand
from albums.models import Genre, Album, Track

API_KEY = os.environ.get("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# Artists organised by genre — Last.fm will return their top albums
ARTISTS_BY_GENRE = {
    "Heavy Metal": [
        "Black Sabbath",
        "Iron Maiden",
        "Judas Priest",
        "Ozzy Osbourne",
        "Dio",
        "Pantera",
        "System of a Down",
        "Rammstein",
        "Ghost",
        "Ozzy Osbourne",
        "Avenged Sevenfold",
        "Volbeat",
        "Black Label Society",
        "Skindred",
    ],
    "Thrash": [
        "Metallica",
        "Megadeth",
        "Slayer",
        "Anthrax",
        "Testament",
        "Exodus",
        "Pantera",
        "Machine Head",
        "Lamb of God",
        "Suicidal Tendencies",
    ],
    "Death Metal": [
        "Death",
        "Cannibal Corpse",
        "Morbid Angel",
        "Obituary",
        "Carcass",
        "Sepultura",
        "Gojira"
    ],
    "Rock": [
        "Led Zeppelin",
        "AC/DC",
        "Queen",
        "Guns N' Roses",
        "Nirvana",
        "Foo Fighters",
        "Red Hot Chili Peppers",
        "Pearl Jam",
        "Radiohead",
        "Paramore",
        "Linkin Park",
        "My Chemical Romance",
        "The Beatles",
        "Maroon 5",
        "Panic! at the Disco",
        "Green Day",
    ],
    "Alternative Rock": [
        "Radiohead",
        "Smashing Pumpkins",
        "Pixies",
        "The Cure",
        "Nine Inch Nails",
        "Placebo",
        "Weezer",
        "Black Stone Cherry",
        "Biffy Clyro",
        "Royal Blood",
    ],
    "Metalcore": [
        "Killswitch Engage",
        "Trivium",
        "Bullet for My Valentine",
        "Parkway Drive",
        "Architects",
        "Bring Me the Horizon",
        "Lamb of God",
        "Architects",
        "Bad Omens",
        "Avenged Sevenfold",
        "Motionless in White",
        "Spiritbox",
        "Parkway Drive",
        "I Prevail",
        "Five Finger Death Punch",
        "Asking Alexandria",
        "Artreyu",
        "In This Moment",
        "While She Sleeps",
        "Of Mice & Men",
        "We Came as Romans",
    ],
}


class Command(BaseCommand):
    help = "Fetch top albums per artist from Last.fm and save to database"

    def handle(self, *args, **kwargs):
        for genre_name, artists in ARTISTS_BY_GENRE.items():
            genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
            self.stdout.write(f"\nFetching albums for genre: {genre_name}")

            for artist_name in artists:
                self.stdout.write(f"  Artist: {artist_name}")

                # Get top albums for this artist
                response = requests.get(BASE_URL, params={
                    "method": "artist.gettopalbums",
                    "artist": artist_name,
                    "api_key": API_KEY,
                    "format": "json",
                    "limit": 5,
                })

                if response.status_code != 200:
                    self.stdout.write(self.style.ERROR(f"    Failed to fetch albums for {artist_name}"))
                    continue

                top_albums = response.json().get("topalbums", {}).get("album", [])

                for album in top_albums:
                    album_title = album.get("name", "")

                    # Skip placeholder entries
                    if not album_title or album_title == "(null)":
                        continue

                    keywords = ['remaster', 'deluxe', 'edition', 'anniversary', 'bonus']
                    if any(kw in album_title.lower() for kw in keywords):
                         self.stdout.write(f"    Skipping remaster: {album_title}")
                         continue

                    # Get full album info including tracks and better artwork
                    info_response = requests.get(BASE_URL, params={
                        "method": "album.getinfo",
                        "artist": artist_name,
                        "album": album_title,
                        "api_key": API_KEY,
                        "format": "json",
                        "limit": 10,
                    })

                    if info_response.status_code != 200:
                        continue

                    data = info_response.json().get("album")
                    if not data:
                        continue

                    # Get cover image
                    images = data.get("image", [])
                    cover_url = next((i["#text"] for i in images if i["size"] == "extralarge"), "")
                    if not cover_url:
                        self.stdout.write(f"    No image, skipping: {album_title}")
                        continue

                    # Save or update album
                    album_obj, created = Album.objects.update_or_create(
                        external_id=data.get("mbid", "") or f"{artist_name}_{album_title}",
                        defaults={
                            "title": data.get("name", album_title),
                            "artist": artist_name,
                            "genre": genre_obj,
                            "cover_image_url": cover_url,
                            "external_url": data.get("url", ""),
                            "description": data.get("wiki", {}).get("summary", ""),
                            "source": "lastfm",
                            "is_imported": True,
                        }
                    )

                    status = "Created" if created else "Updated"
                    self.stdout.write(f"    {status}: {album_title}")

                    # Fetch tracks
                    self.fetch_tracks(album_obj, data)

        self.stdout.write(self.style.SUCCESS("\nDone! All albums and tracks imported."))

    def fetch_tracks(self, album_obj, album_data):
        tracks = album_data.get("tracks", {}).get("track", [])

        # Last.fm returns a dict instead of a list for single track albums
        if isinstance(tracks, dict):
            tracks = [tracks]

        # Clear existing tracks before reimporting
        album_obj.tracks.all().delete()

        for i, track in enumerate(tracks, start=1):
            if not isinstance(track, dict):
                continue
            duration = track.get("duration")
            Track.objects.create(
                album=album_obj,
                external_id=track.get("mbid", ""),
                track_number=i,
                title=track.get("name", ""),
                duration_seconds=int(duration) if duration else None,
            )