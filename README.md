# ASU Class Availability Discord Bot

## About
This Discord bot allows users to check the availability of ASU courses and classes. It scrapes data from the ASU Class Search website and queries the ASU class catalog API to provide real-time information about course and class availability. It will notify you as soon as the class is open.

## Setup
1. Install the required Python packages:

    ```bash
    pip install discord.py pandas selenium
    ```

2. Make sure you have the Chrome browser installed, as the script uses Selenium for web scraping. Download the ChromeDriver executable from [ChromeDriver](https://sites.google.com/chromium.org/driver/) and ensure it's in your system PATH.

3. Obtain a Discord bot token and save it in a file named `token_disc.py`:

    ```python
    TOKEN = 'token here'
    ```

4. Update the bot command prefix and other configurations in the script if needed:

    ```python
    bot = commands.Bot(command_prefix='!', intents=intents)
    ```

5. Run the script:

    ```bash
    python your_script_name.py
    ```

## Bot Commands

- `!helpBot`: Display a list of available bot commands.
- `!checkCourse [courseID] [term]`: Check the availability of a single course. Example: `!checkCourse 12345 2241`.
- `!checkClass [ClassNum] [ClassSubject] [Term]`: Check the availability of a list of classes. Example: `!checkClass 205 CSE 2241`.
- `!stopChecking [course/class]`: Stop checking availability for courses or classes. Example: `!stopChecking course`.

## Background Tasks

- `check_class_availability`: Periodically checks the availability of classes based on the ASU class catalog API.
- `check_course_availability`: Periodically checks the availability of a specific course based on web scraping.