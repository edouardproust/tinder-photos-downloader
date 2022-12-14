# Tinder Photos Downloader

**TPD helps you to download your photos from you Tinder profile. Add user ID to you account in your Tinder profile, then enter it in TPD and download your photos. 100% free, no email required.**

👉 [**Video demo**](https://edouardproust.dev/portfolio/tinder-photos-downloader_58)

**Technologies:** Python, Flask, scrapping (BeatifuSoup4 + Selenium), Bootstrap, Javascript, HTML, CSS

![Screenshot](screenshot.jpg)

## Upcoming updates

- Increase speed ofthe app (optimise scrapping process and use Threads) in order to reduce Timeout exception and improve UX.

## Development

1. Clone repository 
```bash
clone <repo> .
````

2. Update `config.py` file with your informations

3. Install dependencies app:
```bash
pipenv shell && pipenv install
```

4. Launch server using gunicorn 
```bash
gunicorn app:app
```

## Deployment

1. Create a repository on Heroku
```bash
heroku create <app_name>
```

2. Add a Buildpack for Heroku (replace `<app_name>` by your app name)
```bash
heroku buildpacks:set heroku/python -a <app_name>
heroku buildpacks:add https://github.com/pyronlaboratory/heroku-integrated-firefox-geckodriver 
``` 

3. To use the second buildpack (geckodriver) you'll need to downgrade to `heroku-20` stack
```bash
heroku stack:set heroku-20 -a <app name>
```

3. Add the need varibles to the PATH in Heroku
```bash
heroku config:set FIREFOX_BIN=/app/vendor/firefox/firefox GECKODRIVER_PATH=/app/vendor/geckodriver/geckodriver LD_LIBRARY_PATH=/usr/local/lib:/usr/lib:/lib:/app/vendor PATH=/usr/local/bin:/usr/bin:/bin:/app/vendor/
```

3. Push code to heroku using git
```bash
git init
heroku git:remote -a <app_name>
git add .
git commit -m "First commit"
git push -u heroku master # or if you are working on another branch: `git push heroku <branch_name>:master`
```

4. Launch flask web app (dyno) on Heroku
```bash
heroku ps:scale web=1 # This will launch the "web" line script of the `Procfile` file
```

5. Visit the app:
```bash
heroku info -s | grep web_url | cut -d= -f2 
# And click the link ;)
```

If the app is not working properly after you followd the previous steps: 
- Check logs: `heroku logs --tail`
- Run Heroku CLI (to list files etc.): `heroku run bash` (close it with `exit`)

## Tips

- Redeploy Heroku app without code changes: 
```bash
git commit --allow-empty -m "Redeploy app on heroku"
git push heroku master
```