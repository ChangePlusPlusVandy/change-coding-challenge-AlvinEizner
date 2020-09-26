import requests
import os
import json
import random
from flask import Flask, redirect, url_for, render_template, request, session, flash, g
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tkinter import *

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_headers(bearer_token):
    headers = {f"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAACGMHwEAAAAASXD3fT1VPGbIXik6onAYMIKnNu8%3Dkev3FnvHMyINZ6Fdzhw8X86XA86c7OTCuefzm3xGmwoacREnp1"}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

kanye, elon, handle1, handle2, wrong = [], [], [], [], []
tick, pick, score, elon_score, kanye_score, num_elon_tweets, num_kanye_tweets, index = 0, 0, 0, 0, 0, 0, 0, 0

def loadTweets():
    bearer_token = auth()
    headers = create_headers(bearer_token)
    kanye_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=kanyewest&count=200'
    elon_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=elonmusk&count=200'
    kanye_tweets = connect_to_endpoint(kanye_url, headers)
    elon_tweets = connect_to_endpoint(elon_url, headers)
    count = 0
    for item in kanye_tweets:
        if item['text'][0] != '@' and 'https' not in item['text'] and item['text'][3] != '@':
            count += 1
            kanye.append(item['text'])
    count = 0
    for item in elon_tweets:
        if item['text'][0] != '@' and 'https' not in item['text'] and item['text'][3] != '@':
            count += 1
            elon.append(item['text'])

loadTweets()

root = Tk()#initializes GUI
root.title('Tweet Guesser')
root.geometry("920x350")#GUI size


testLabel = Label(root, fg="white", bg="#856ff8", font=('Helvetica', 20))#testLabel = GUI text for each tweet
elonButton = Button(root)
kanyeButton = Button(root)
defaultButton = Button(root)

def elonCmd():
    global tick
    global elonButton
    global kanyeButton
    global score
    global elon_score
    global index
    global pick
    if pick == 1:
        score += 1
        elon_score += 1
    else:
        wrong.append(kanye[index])
    elonButton.destroy()
    kanyeButton.destroy()
    tick += 1
    defaultClick()


def kanyeCmd():
    global tick
    global elonButton
    global kanyeButton
    global score
    global kanye_score
    global index
    global pick
    if pick == 2:
        score += 1
        kanye_score += 1
    else:
        wrong.append(elon[index])
    elonButton.destroy()
    kanyeButton.destroy()
    tick += 1
    defaultClick()

againButton = Button(root)

def defaultClick():
    global elonButton#setting global variables so tweets and gui elments can keep being reproduced while gui is running
    global kanyeButton
    global defaultButton
    global testLabel
    global num_elon_tweets
    global num_kanye_tweets
    global wrong
    global tick
    global index
    global pick
    testLabel.destroy()
    defaultButton.destroy()
    if tick < 7:
        pick = random.randint(1,2)
        if pick == 1:
            num_elon_tweets += 1
            index = random.randint(0, len(elon) - 1)
            testLabel = Label(root, text = elon[index], fg="yellow", bg="#856ff8", font=('Helvetica', 15))
            testLabel.pack()
        else:
            num_kanye_tweets += 1
            index = random.randint(0, len(kanye) - 1)
            testLabel = Label(root, text = kanye[index], fg="yellow", bg="#856ff8", font=('Helvetica', 15))
            testLabel.pack()
        elonButton = Button(root, text="Elon", command=elonCmd, highlightbackground='#856ff8')
        elonButton.pack()
        kanyeButton = Button(root, text="Kanye", command=kanyeCmd, highlightbackground='#856ff8')
        kanyeButton.pack()
    else:
        scoreLabel = Label(root, text = f'You got {score}/7 total tweets right!', fg="white", bg="#856ff8", font=('Helvetica', 20))
        scoreLabel.pack()
        elonLabel = Label(root, text = f'You got {elon_score}/{num_elon_tweets} Elon tweets right!', fg="white", bg="#856ff8", font=('Helvetica', 20))
        elonLabel.pack()
        kanyeLabel = Label(root, text =f'You got {kanye_score}/{num_kanye_tweets} Kanye tweets right!', fg="white", bg="#856ff8", font=('Helvetica', 20))
        kanyeLabel.pack()
        if len(wrong) == 0:
            messageLabel = Label(root, text = "Wow! You're great at guessing!", fg="white", bg="#856ff8")
            messageLabel.pack()
        else:
            label1 = Label(root, text = '', fg="black", bg="#856ff8")
            label1.pack()
            messageLabel = Label(root, text = 'You got these tweets wrong:', fg="white", bg="#856ff8", font=('Helvetica', 25))
            messageLabel.pack()
            wrong_labels = []
            for tweet in wrong:
                wrongLabel = Label(root, text = tweet, fg="yellow", bg="#856ff8", font=('Helvetica', 15))
                wrongLabel.pack()
                wrong_labels.append(wrongLabel)
            label2 = Label(root, text = '', fg="black", bg="#856ff8")
            label2.pack()
            tick = 0
            wrong = []
            def playAgain():
                global score
                global elon_score
                global kanye_score
                global num_elon_tweets
                global num_kanye_tweets
                score, elon_score, kanye_score, num_elon_tweets, num_kanye_tweets = 0, 0 ,0, 0 ,0
                scoreLabel.destroy()
                elonLabel.destroy()
                kanyeLabel.destroy()
                messageLabel.destroy()
                label1.destroy()
                label2.destroy()
                for label in wrong_labels:
                    label.destroy()
                againButton.destroy()
                defaultClick()
            againButton = Button(root, text="Play Again", highlightbackground='#856ff8', command=playAgain)
            againButton.pack()

defaultButton = Button(root, text="Start", highlightbackground='#856ff8', command=defaultClick)#make start func that calls click
defaultButton.place(relx=0.5, rely=0.5, anchor=CENTER)

root['background']='#856ff8'#makes background color of app purple
root.mainloop() #keeps gui constantly running until closed


def custom_handles():#function for playing with custom handles
    bearer_token = auth()
    handle1, handle2 = [], []
    headers = create_headers(bearer_token)
    handle1_input = input('Enter a valid twitter handle (Note: case-sensitive): ')
    handle2_input = input('Enter another valid twitter handle: ')
    url1 = f'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={handle1_input}&count=200'
    url2 = f'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={handle2_input}&count=200'
    try:
        tweets1 = connect_to_endpoint(url1, headers)
    except:
        tweets1 = False
        count = 11

    try:
        tweets2 = connect_to_endpoint(url2, headers)
        print("Type '1' as the guess for the first handle, and '2' for the second.")
    except Exception:
        tweets2 = False
        count = 11
    count = 0
    if tweets1:
        for item in tweets1:
            if item['text'][0] != '@' and 'https' not in item['text'] and item['text'][3] != '@':
                count += 1
                handle1.append(item['text'])
    count = 0
    if tweets2:
        for item in tweets2:
            if item['text'][0] != '@' and 'https' not in item['text'] and item['text'][3] != '@':
                count += 1
                handle2.append(item['text'])
    counter, score, handle1_score, handle2_score, num_handle1_tweets, num_handle2_tweets = 0, 0, 0, 0, 0 , 0 
    wrong = []
    while counter < 7:
        pick = random.randint(1,2)
        if pick == 1:
            num_handle1_tweets += 1
            try:
                index = random.randint(0, len(handle1) -1)
            except ValueError:
                print('Error: One the users does not have any unique tweets w/out links or images, or the handle DNE.')
                counter = 11
                break
            except Exception:
                print('Error: Not a valid twitter handle (Remember, this is case-sensitive).')
                counter = 11
                break
            guess = input(handle1[index] + '\n')
            if guess.lower() == "1":
                score += 1
                handle1_score += 1
            else:
                wrong.append(handle1[index])
        else:
            num_handle2_tweets += 1
            try:
                index = random.randint(0, len(handle2) -1)
            except ValueError:
                print('Error: This user does not have any unique tweets w/out links or images, or the handle DNE.')
                counter = 11
                break
            except Exception:
                print('Error: Not a valid twitter handle (Remember, this is case-sensitive).')
                counter = 11
                break
            guess = input(handle2[index] + '\n')
            if guess.lower() == "2":
                score += 1
                handle2_score += 1
            else:
                wrong.append(handle2[index])
        counter += 1
    if counter == 7:
        print(f'You got {score}/7 total tweets right!')
        print(f'You got {handle1_score}/{num_handle1_tweets} @{handle1_input} tweets right!')
        print(f'You got {handle2_score}/{num_handle2_tweets} @{handle2_input} tweets right!')
        if len(wrong) == 0:
            print("Wow! You're great at guessing!")
        else:
            print('You got these tweets wrong:')
            for tweet in wrong:
                print(tweet)

custom_handles()

