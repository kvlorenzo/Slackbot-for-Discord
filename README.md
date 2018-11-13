# Slackbot for Discord

Slackbot for Discord is a Discord chatbot that allows users to set reminders and automated messages from the message box. This bot must be 
self-hosted, meaning one user must run the bot in order to use it.

## How to Install

First, download our Github repository by cloning it. To do so in Git, type the following command:

- "git clone https://github.com/kvlorenzo/Slackbot-for-Discord.git"

Next, enter the directory holding the files to the Slackbot project.

From inside the directory, enter the command:

- "python3 setup.py install"

This will help download all the required modules in order for the bot to work.

Finally, to run the bot, type in the following command:

- "python3 slackbot.py"

And congrats! Your bot should be running now. If you have any questions/problems with installation, contact me at kvlorenz@ucsd.edu

## How to Use

Using the bot is very simple. All it takes is typing either "/remind" or "/response" in a text channel. Here's a demo of the response:

![slackbot_response_demo](https://user-images.githubusercontent.com/35363207/48341075-02cb7e80-e621-11e8-82c9-1611535b6add.gif)

As you can see, our bot allows you to set your own automated messages. Whether it's asking a question or just greeting you when you say "Hi," Slackbot will be able to respond to any of your messages immediately.

But the fun doesn't stop there. Users can also set future reminders to send messages at a particular time. Here's a demo of the reminder:

![slackbot_reminder_demo1](https://user-images.githubusercontent.com/35363207/48385411-436bdc00-e6a3-11e8-88b4-a5cc7adb3607.gif)

Pretty cool, huh?

The features also come with their own usage message. To display the message, type "/remind help" or "/response help" and the message will pop up. Here are the usage messages just in case:

![response-help](https://user-images.githubusercontent.com/35363207/48341522-1e835480-e622-11e8-8c55-08caa2e551e9.PNG)
![remind-help](https://user-images.githubusercontent.com/35363207/48341530-22af7200-e622-11e8-95a9-dfe3d1e4cc8a.png)

## Other Notes
Installation and usage of this bot requires Python 3.4 or above. The program also uses an SQLite3 database to manage the messages and reminders across multiple servers. If you see any bugs, report them as issues in this repository or contact me at kvlorenz@ucsd.edu
