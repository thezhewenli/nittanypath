# Phase 2 Progress Review - NittanyPath Project
NittanyPath, a University and Course Manangement System, created using Django

## How to start the system

NittanyPath is created and powered by Django. Make sure you have Python 3 and Django package installed. Then go to the directory at terminal and run `python manage.py runserver`. The web app will start at the default location. You can then access the system using your browser.

## How to populate data

### 1. Data Parser

A data parser is designed and available at `/scripts/data_parse.py`. This program is designed very specifically to parse the three csv files provided by CMPSC 431 teaching team, i.e. the dataset. The program will create several new csv files.

### 2. Data Population Scripts

There are 11 scripts under `/commands` directory, and they will automatically populate the database using data from the pre-parsed csv files.

## How to use the system

Right now, available features are login, logout, view profile, and change password and profile picture. An admin management feature is also available to users with superuser privilege.

By default, NittanyPath will redirect you (anonymous users) to the landing page, showing a picture of the Westgate Building, and prompt user to sign in. Signed-in users will be automatically redirect to the registrar app homepage, showing a picture of the Millennium Science Complex, and a welcome message. The login and logout features are inherited from Django's default functions and views, with some alterations.

After logged in, user can also click to view their University Member Profile, and a form to change their profile picture is also at this page. User can also change their password by clicking on the button. All passwords are hashed (by Django) and stored not in plain text in the database.

## Citations

I learned a lot of basics about Django using an YouTube playlist[^1], created by Corey Schafer. Some of the code snippets are from his GitHub repo and properly cited. The usage of his codes are licensed under MIT License.

I also gained a lot of knowledge through reading Django's official documentation[^2].

## Cited MIT License

MIT License

Copyright (c) [2018] [Corey Schafer]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[^1]: https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
[^2]: https://docs.djangoproject.com/en/3.0/