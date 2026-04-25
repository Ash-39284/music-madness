# Music Madness



## Table of Contents

1. [UX](#ux)
    - [Project Goals](#project-goals)
    - [User Goals](#user-goals)
    - [User Stories](#user-stories)
    - [Developer Goals](#developer-goals)
    - [Design Choices](#design-choices)
        - [Colour Pallete](#colour-pallete)
        - [Frontend Design (Canva)](#frontend-design-canva)
            - [Home Page](#home-page)
            - [About Page](#about-page)
            - [Genre Page](#genre-page)
            - [Explore Page](#explore-page)
            - [Album Discuss Page](#album-discussion-page)
            - [Login Page](#login-page)
            - [Signup Page](#signup-page)
        - [Wireframes](#wireframes)
            - [Mobile](#mobile)
            - [Tablet](#tablet)
            - [Desktop](#desktop)
        - [ERD](#erd)
2. [Features](#features)
    - [Existing Features](#existing-features)
    - [Features to Implement](#features-to-implement)
3. [Technologies Used](#technologies-used)
4. [Testing](#testing)
    - Code Validation
    - [Bugs Discovered](#bugs-discovered)
    - Manual Testing
    - Automated Testing
5. [Deployment](#deployment)
    - [How To Run The Project Locally](#how-to-run-the-project-locally)
6. [Credits](#credits)
    - [Content](#content)
    - [Code](#code)
    - [Images](#images)
    - [API](#api)
    - [Acknowledgements](#acknowledgements)

## Introduction

**Music Madness** is a community-driven web application where metal fans can explore albums, react to releases, and join discussions around their favourite music.

The platform focuses on conversation over ratings, giving users a space to share opinions, debate iconic records, and discover new music across multiple genres. From classic heavy metal to modern subgenres, Music Madness brings together fans who want more than just a score — they want a voice.

---

# UX


## Project Goals

The goal of **Music Madness** is to build a full-stack web app where users can explore albums, share their opinions, and get involved in discussions around music. The focus is on creating something interactive rather than just a simple rating platform.

The project uses Django and PostgreSQL to handle the backend, with a database designed around albums, genres, users, and interactions. On the frontend, the aim is to bring custom designs to life with a consistent and responsive layout.

Users will be able to create accounts, react to albums, and leave comments, making the experience more personal and community-driven. The project is also structured in a way that makes it easy to expand later on.

---

## User Goals

Users of **Music Madness** should be able to easily discover new albums, revisit favourites, and share their opinions with others who enjoy the same kind of music. The goal is to give people a space where they can do more than just rate an album — they can actually talk about it.

A user should be able to browse albums by genre, view album details, and see how others in the community feel about a release. They should also be able to react to albums and leave comments, making it easy to join ongoing discussions or start their own.

The overall experience should feel simple and intuitive, so users can quickly find what they’re looking for and get involved without any friction.

---

## User Stories

---

## Developer Goals

---

# Design Choices

## Colour Pallete

![Colour Pallette](./static/images/colour-pallette.png)

## Frontend Design (Canva)

### Home Page

![Home Page](./static/images/music-madness-frontend-designs/home-page.png)

### About Page

![About Page](./static/images/music-madness-frontend-designs/about-page.png)

### Genre Page

![Genre Page](./static/images/music-madness-frontend-designs/genre-page.png)

### Explore Page

![Explore Page](./static/images/music-madness-frontend-designs/explore-page.png)

### Album Discussion Page

![Album Discussion Page](./static/images/music-madness-frontend-designs/album-discuss-pge.png)

### Login Page

![Login Page](./static/images/music-madness-frontend-designs/login-page.png)

### Signup Page

![Signup Page](./static/images/music-madness-frontend-designs/signup-page.png)

---

## Wireframes

### Mobile

![Home Page/ Explore page](./static/images/mobile-wireframes/home_mobile_wireframe.svg)

![About Page](./static/images/mobile-wireframes/about_mobile_wireframe.svg)

![Genre Page](./static/images/mobile-wireframes/genre_mobile_wireframe.svg)

![Album Page](./static/images/mobile-wireframes/album_mobile_wireframe.svg)

![Signup Page](./static/images/mobile-wireframes/signup_mobile_wireframe.svg)

![Login Page](./static/images/mobile-wireframes/login_mobile_wireframe.svg)

### Tablet
![Home Page/ Explore page](./static/images/tablet-wireframes/home_tablet_wireframe.svg)

![About Page](./static/images/tablet-wireframes/about_tablet_wireframe.svg)

![Genre Page](./static/images/tablet-wireframes/genre_tablet_wireframe.svg)

![Album Page](./static/images/tablet-wireframes/album_tablet_wireframe.svg)

![Signup Page](./static/images/tablet-wireframes/signup_tablet_wireframe.svg)

![Login Page](./static/images/tablet-wireframes/login_tablet_wireframe.svg)


### Desktop

![Home Page/ Explore page](./static/images/desktop-wireframes/home_desktop_wireframe.svg)

![About Page](./static/images/desktop-wireframes/about_desktop_wireframe.svg)

![Genre Page](./static/images/desktop-wireframes/genre_desktop_wireframe.svg)

![Album Page](./static/images/desktop-wireframes/album_desktop_wireframe.svg)

![Signup Page](./static/images/desktop-wireframes/signup_desktop_wireframe.svg)

![Login Page](./static/images/desktop-wireframes/login_desktop_wireframe.svg)

--- 

## ERD

![ERD Diagram](./static/images/music-madness-erd-diagram.png)

---

# Features

## Existing Features

---

## Features To Implement

---

# Technologies Used

# Testing

## Bugs Discovered

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

## Bug 6 - Most Discussed Section Info Not Displaying

**Description:**
After building the explore page, the "Most Discussed" section only showed the album cover image on the left with no title, stats or "View discussion" button appearing beside it. The right side of the card was completely empty despite the correct HTML being in place.

![Most discussed info bug](./static/images/bug-6-screenshot.png)

**Cause:**
Inspecting the element in Chrome DevTools revealed that the `.most-discussed__info` div was rendering as empty in the DOM. The CSS for `.most-discussed__info` was showing "No matching selector or style" in the Styles panel, meaning the browser was still serving a cached version of `style.css` that did not include the new explore page styles.

**Fix:**
Running `python manage.py collectstatic --clear` forced Django to regenerate the stylesheet. After a hard browser refresh (`Cmd + Shift + R`) the styles loaded correctly and the info content appeared alongside the image.

---






# Deployment

## How To Run The Project Locally

# Credits

## Content

---

## Code

---

## Images

---

## API

---

## Acknowledgements

This project was developed and coded by Ashley Roberts in 2026