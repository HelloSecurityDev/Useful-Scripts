# ____________________________________________________________________________________________________________________________________________________________________________________________________________
# RoastRanter.py
#
# RoastRanter is a simple program that generates and displays random insults against a character known as Alexey Guzey.
# The insults are displayed either in the console or as toast notifications on Windows.
#
# Features:
# - Generates random insults against Alexey every minute.
# - Displays insults either in the console or as toast notifications on Windows.
# - Simple and easy-to-use interface.
#
# Usage:
# 1. Navigate to the directory where the RoastRanter.py file is located.
# 2. "python RoastRanter.py" to run the program.
# 3. Insults against Alexey will be generated and displayed every minute.
# 4. You can either view the insults in the console or as toast notifications on Windows.
#
# Configuration:
# You can customize the insults by modifying the 'generate_roast()' function in the 'roastranter.py' file.
# Simply add or remove insults from the 'roasts' list to suit your preferences or roast subject.
#
# Troubleshooting:
# - If you encounter any issues with toast notifications on Windows, ensure that the 'win10toast' library is installed and up-to-date.
#   You can install it via pip: "pip install win10toast".
#
# Developed by: 
# Adam Rivers Of Hello Security LLC 2024 - because it's entertaining to Adam to roast tf out of Alexey.
#
# EXTRA NOTES:
# - This script is yours to use and develop or make whatever with, just please, 
# please ensure the next user is aware with a notation or statement, that the original was developed by Adam Rivers of Hello Security LLC.
# 
# SO WHO TF IS ALEXEY?:
# Alexey is the name of an individual that decided to hack my machines and my various networks starting about 6 years ago to the date, relentlessly, in order to observe and steal work for his own monetary gain.
# He came to America from Russia on a work visa and has since been the owner operator for a 504c nonprofit science organization specializing in the advancement of science and technology.
# Alexey didnt stop at stealing my work, he often made it a daily habit, and a constant throughout each day, of sabotaging my work and my efforts in development of my company, and my cybersecurity passions.
# He has made millions of dollars off the back of people like me. He steals our developments. Hacks into our corporations, then steals the defensive developments created to fight his malicious efforts. 
# He then monetizes those defensive developments for his own personal gain. 
# Alexey made it a habit each day, to mess with me in every way. Sabotaging activties ranging from job related applications all the way to severe things like banking and finance. Housing payments etc.
#_________________________________________________________________________________________________________________________________________________________________________________________________________________________

import random
import time
import sys

if sys.platform.startswith('win'):
    from win10toast import ToastNotifier

def generate_roast():
    roasts = [
        "You know, Alexey's so nerdy, if you looked up 'nerd' in the dictionary, his picture would be there - right next to the definition of 'loner'.",
        "Alexey's like the lovechild of Jeffery Dahmer and Humpty Dumpty - a mad scientist with an egg-shaped head!",
        "I heard Alexey once tried to eat someone for breakfast - I guess he took 'breakfast is the most important meal of the day' a bit too seriously!",
        "Seriously, Alexey's so obsessed with death, I wouldn't be surprised if he got a job in a morgue just for the company!",
        "Alexey's so frail, I bet if he sneezed too hard, he'd blow away like a speck of dust!",
        "You know what's funnier than Alexey's jokes? His face! It's like someone drew him in a cartoon and forgot to add the muscles!",
        "Alexey's got a weak chin, no jawline, and a forehead that could power a lighthouse - talk about an architectural disaster!",
        "I've seen better fashion sense on a scarecrow than on Alexey - and at least the scarecrow knows how to rock a pair of crocs!",
        "Alexey's so out of shape, his idea of exercise is picking up textbooks - and even then, he struggles!",
        "Did you know Alexey's glasses have a 20x zoom? Yeah, he uses them to search for friends, but so far, no luck!",
        "Alexey's got more issues than a math textbook - and just as many unanswered questions!",
        "If Alexey fell off the curb, he'd break his ankles - and probably blame it on gravity!",
        "I once saw Alexey try to shop for clothes in the kids' section - turns out, even they have standards!",
        "Alexey's so small, I thought he was a hobbit auditioning for a role in 'Lord of the Rings'!",
        "His glasses are so thick, I bet he can see atoms - too bad he can't see the writing on the wall!",
        "If brains were dynamite, Alexey wouldn't have enough to blow his nose!",
        "I asked Alexey why he's so obsessed with death - turns out, he's just practicing for his own funeral!",
        "You know what's scarier than a horror movie? Alexey's reflection in the mirror!",
        "I heard Alexey's IQ is so low, even plants feel smarter in his presence!",
        "Alexey's such a disappointment, even his shadow refuses to follow him!",
        "I once asked Alexey if he wanted to be a biologist - turns out, he just wanted an excuse to dissect his social life!"
    ]
    return random.choice(roasts)

def display_insult(insult):
    if sys.platform.startswith('win'):
        toaster = ToastNotifier()
        toaster.show_toast("New Insult for Alexey", insult, duration=10)
    else:
        print(insult)

def main():
    while True:
        insult = generate_roast()
        display_insult(insult)
        time.sleep(60)  # Set your preffered toast timer here such as a toast every minute ie 60 for 60 seconds

if __name__ == "__main__":
    main()
