import discord
from discord.ext import commands, tasks

import pandas as pd
import json
import requests
import random
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from token_disc import TOKEN

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def getID(course_id, term):
    # The Link we are trying to Scrape.
    link_subject_based = f"https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=A&honors=F&keywords={course_id}&promod=F&searchType=all&term={term}"

    # Setting options to add arguments.
    chrome_options = Options()
    
    # Disabling most chrome options that we dont need to increase speed of the script.
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")

    # Setting the chrome driver to the options we just set.
    driverChrome = webdriver.Chrome(options=chrome_options)

    # Getting the link.
    driverChrome.get(link_subject_based)

    # Waiting 20 seconds so all items load.
    wait = WebDriverWait(driverChrome, 20)

    # We get the text from the xpath where the table is located.
    element = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='class-results']")))
    # Get the text.
    text = element.text

    # Close the web driver.
    driverChrome.close()

    # Return the Text.
    pattern = r'(\d+) of (\d+)'

    # Use regex to find the match in the string
    match = re.search(pattern, text)

    # Check if a match is found
    if match:
        n_avail = int(match.group(1))
        # n_total = int(match.group(2))
        
        # Determine availability based on n_avail
        avail = n_avail > 0
        print(f"Available: {avail}")

        return avail, text
    else:
        print("Pattern not found in the given string.")
        return False, ""

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@tasks.loop(minutes=random.randint(6, 15))
async def check_class_availability(class_num, class_subject, class_term, channel_id):
    headers = {'Authorization': 'Bearer null'}
    response = requests.get("https://eadvs-cscc-catalog-api.apps.asu.edu/catalog-microservices/api/v1/search/classes",
                            headers=headers, params={
                                "refine": "Y",
                                "campusOrOnlineSelection": "A",
                                "catalogNbr": class_num,
                                "honors": "F",
                                "promod": "F",
                                "searchType": "all",
                                "subject": class_subject,
                                "term": class_term
                            })
    data = json.loads(response.text)

    # Extract and format data
    formatted_data = []
    class_name = f"{class_subject} {class_num}"
    for item in data['classes']:
        class_info = item['CLAS']
        row = {
            'Class': class_name,
            'Class Name': class_info.get('TITLE', ''),
            'Class ID': class_info.get('CLASSNBR', ''),
            'Instructor Name': ", ".join(class_info.get('INSTRUCTORSLIST', [])),
            'Location': class_info.get('LOCATION', ''),
            'Occupancy': f"{class_info.get('ENRLTOT', '')} of {class_info.get('ENRLCAP', '')}"
        }
        formatted_data.append(row)

    # Convert to Pandas DataFrame
    df = pd.DataFrame(formatted_data)

    # Add 'Available' column
    df['Available'] = False
    j = -1
    for i in df['Occupancy']:
        j += 1
        numbers = i.split(' of ')
        if len(numbers) == 2 and numbers[0].isdigit() and numbers[1].isdigit():
            if int(numbers[0]) < int(numbers[1]):
                df.at[j, 'Available'] = True

    # Get available classes
    available_classes = df[df['Available']]

    # Notify on Discord if there are available classes
    if not available_classes.empty:
        channel = bot.get_channel(channel_id)
        
        # Print the table of available classes
        table_message = f"```{available_classes.to_string(index=False)}```"
        await channel.send(f"There are available classes:\n{table_message}")


@tasks.loop(minutes=random.randint(6, 15))
async def check_course_availability(course_id, term, channel_id, ctx):
    is_available, text = getID(course_id, term)

    if is_available:
        channel = bot.get_channel(channel_id)
        user = ctx.author
        await channel.send(f"{user.mention}, the course is available! Register now.\n{text}")
        check_course_availability.stop()


@bot.command()
async def checkCourse(ctx, course_id, term):
    channel_id = ctx.channel.id
    print(channel_id)
    check_course_availability.start(course_id, term, channel_id, ctx)
    await ctx.send(f'Course availability checking has started for Course ID: {course_id}, Term: {term}.')


@bot.command()
async def checkClass(ctx, class_num, class_subject, class_term):
    channel_id = ctx.channel.id
    # Call your check_class_availability function for class
    check_class_availability.start(class_num, class_subject, class_term, channel_id)
    await ctx.send(f'Class availability checking has started for Class ID: {class_num}, Term: {class_term}.')


@bot.command()
async def stop_checking(ctx, task_type):
    if task_type.lower() == 'course':
        check_course_availability.stop()
        await ctx.send('Course availability checking has stopped.')
    elif task_type.lower() == 'class':
        check_class_availability.stop()
        await ctx.send('Class availability checking has stopped.')
    else:
        await ctx.send('Invalid task type. Please specify either "course" or "class".')


bot.run(TOKEN)