# Automate your channel !
- python 3.10.x (I haven't tested if it works with previous versions)
- All binaries included (ffmpeg, imagemagick, geckodriver)
## setup
- Clone this repo
- ``pip install -r requirements.txt``
- Rename the [.env.sample](.env.sample) file to .env
- Edit your .env file (see [How to create a reddit app](#How-to-create-a-reddit-app-)) :
    - REDDIT_CLIENT_SECRET="YourClientSecret"
    - REDDIT_CLIENT_ID="YourClientId"
    - REDDIT_USER_AGENT="<AppName-AppVersion>"
    - REDDIT_USERNAME="YourRedditUsername"
    - REDDIT_PASSWORD="YourRedditPasswordAccount"

### How to create a reddit app :
- Follow this [tutorial](https://youtu.be/bMT9ZC9sBzI?t=228)

## Usage
run main.py
