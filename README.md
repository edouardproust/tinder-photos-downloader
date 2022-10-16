# Tinder Photos Downloader

**TPD helps you to download your photos from you Tinder profile. Add user ID to you account in your Tinder profile, then enter it in TPD and download your photos. 100% free, no email required.**

**Technologies:** Python, Flask, scrapping (BeatifuSoup4 + Selenium), Bootstrap, Javascript, HTML, CSS

![Screenshot](screenshot.png)

## Development

1. Clone repository 
```bash
clone <repo> .
````

2. Update `config.py` file with your informations

3. Reload app:
```bash
kill-port <port> && pipenv shell
pipenv install
gunicorn app:app
```