# Music Madness



## Table of Contents

1. UX
    - Project Goals
    - User Goals
    - User Stories
    - Developer Goals
    - Design Choices
2. Features
    - Existing Features
    - Features to Implement
3. Technologies Used
4. Testing
    - Code Validation
    - Bugs Discovered
    - Manual Testing
    - Automated Testing
5. Deployment
    - How To Run The Project Locally
6. Credits
    - Content
    - Code
    - Images
    - API
    - Acknowledgements

## Introduction

This Project is developed for 

## Design Choices

### Colour Pallete

![Colour Pallette](./static/images/colour-pallette.png)

# Bugs Discovered

This section documents bugs encountered during the development of Music Madness, including screenshots, descriptions, and how each was resolved.

---

## Bug 1 — Duplicate and Remastered Albums Appearing on Homepage

**Description:**
When album data was first imported from the Last.fm API using the fetch_albums management command, the homepage "Inside the Pit" section displayed duplicate entries and remastered versions of albums alongside the originals. All three cards showed Black Sabbath albums, including "Paranoid (2009 Remastered Version)" as a separate entry. Additionally, two album cards (Metallica and Ozzy Osbourne) had broken images as Last.fm returned no cover art for those entries.

![Duplicate Albums bug](./static/images/bug-1-screenshot.png)

**Cause**
The `fetch_albums` command used `artist.gettopalbums` from Last.fm which returned remastered and deluxe editions as separate albums. The homepage view was also using `Album.objects.all()[:3]` which simply returned the first three database entries rather than a varied selection.

**Fix:**
- Added a keyword filter to the fetch command to skip remastered/deluxe editions:
```python
keywords = ['remaster', 'deluxe', 'edition', 'anniversary', 'bonus']
if any(kw in album_title.lower() for kw in keywords):
    continue
```
- Added a `featured` boolean field to the `Album` model, allowing specific albums to be manually selected in the Django admin panel
- Updated the homepage view to filter by `featured=True`

---

## Bug 2 - About Page CSS Is Not Displaying

**Description:**
After building the about page, the CSS styles were not being applied. The page rendered as plain unstyled text — no dark blue hero card, no bordered content cards, and no styled "How it works" section.

![About page unstyled](./static/images/bug-2-screenshot.png)

**Cause**
The browser was serving a cached version of `style.css` that did not include the newly added about page styles.

**Fix**
Running `python manage.py collectstatic` forced Django to serve the latest version of the stylesheet. A hard browser refresh (`Cmd + Shift + R`) cleared the cached version and the styles applied correctly.

---

## Bug 3 - Genre Page Returning 404

**Description:**
Navigating to `/genres/heavy-metal/` returned a 404 Page Not Found error. Django listed only three URL patterns (`admin/`, `home`, `about/`) and could not match the genre URL.

![Genre 404 bug](./static/images/bug-3-screenshot.png)

**Cause**
The `urls.py` file had not been updated to include the `genre_detail` URL pattern. The genre detail view and its URL route had been written but not yet added to `urlpatterns`.

**Fix:**
Added the genre detail URL pattern to `music_madness/urls.py`:
```python
path('genres/<slug:slug>/', genre_detail_view, name='genre_detail'),
```
And imported the view:
```python
from albums.views import home_view, about_view, genre_detail_view
```
 
---

## Bug 4 - Genre Page Hero Section CSS Not Applying

**Description:**
After implementing the genre detail page, the hero section appeared as plain unstyled text on a white background. The dark blue rounded card styling defined by `.genre-hero` in `style.css` was not being applied despite the class being present in the HTML. Inspecting the element in Chrome DevTools confirmed "No matching selector or style" for `.genre-hero`.

![Genre hero unstyled bug](./static/images/bug-4-screenshot.png)

**Cause**
The browser was loading a cached version of `style.css` that predated the genre styles being added.

**Fixed**
Running the following command forced Django to regenerate and serve the updated stylesheet:
```bash
python manage.py collectstatic --clear
```
 
---

## Bug 5 — Database Migration Failure When Adding Slug Field to Genre
 
**Description:**
Running `python manage.py migrate` after adding a `slug` field to the `Genre` model failed with a `UniqueViolation` error. The migration attempted to create a unique index on the slug column but all existing genres had empty slug values, causing a duplicate key violation.
 
**Cause:**
The migration tried to add the `slug` field with `unique=True` in a single step. Since existing genre records all had empty slugs, PostgreSQL could not create a unique index on a column full of identical empty strings.
 
**Fix:**
The migration file `0005_genre_slug.py` was rewritten as a three-step operation:
1. Add the slug column without the unique constraint
2. Run a data migration (`RunPython`) to populate slugs for all existing genres using `slugify(genre.name)`
3. Alter the field to add the unique constraint
```python
operations = [
    migrations.AddField(
        model_name='genre',
        name='slug',
        field=models.SlugField(blank=True, default='', unique=False),
    ),
    migrations.RunPython(populate_slugs),
    migrations.AlterField(
        model_name='genre',
        name='slug',
        field=models.SlugField(blank=True, unique=True),
    ),
]
```
 
---

