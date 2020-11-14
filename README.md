# TU-telegram-bot
Telegram bot that automatically send messages to the group from a product link.

## Installation

### Creating a bot
You must create a Telegram bot and then grant it administrator permissions for the group you want it to send messages to.

If you don't know how to create a bot [click here](https://www.sohamkamani.com/blog/2016/09/21/making-a-telegram-bot/#:~:text=Go%20to%20the%20telegram%20app%20on%20your%20phone%20and%E2%80%A6&text=Click%20on%20or%20type%20%2Fnewbot,to%20be%20a%20unique%20name.).

Once you have created it, remember to grant it administrator permissions in the group.

### Installing Python
This bot is fully developed in Python 3.8. That's why you should install Python (>= 3.8) **in your server**.

If you don't know how to do it, visit [this link](https://realpython.com/installing-python/).

You must also install pip to be able to download the necessary libraries later.

Everything is specified in the link above but here is a brief summary of what you should do if your server is, for example, Ubuntu.
```shell script
$ sudo apt-get update
$ sudo apt-get install python3.8 python3-pip
```

### Creating a virtual enviroment (optional but recommended)
In the next step we will see how to download the libraries needed to run our bot.

It is highly recommended to create a virtual environment that allows us to isolate these libraries from the rest of the libraries installed in our server, since there are probably other services that share them but require different versions.

Everything is perfectly explained in [this link](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/). However, we will briefly recapitulate again assuming an Ubuntu server.
```shell script
# installing virtualenv
$ pip intall virtualenv

# before create the virtualenv, we have to go to the directory where our code is
$ cd path/to/repo/folder/TU-telegram-bot

# creating virtualenv
$ virtualenv telegram-venv

# activating the enviroment created
$ source telegram-venv/bin/activate
```

If we have done everything correctly, our terminal will look like this:
```shell script
(telegram-venv) $
```

### Installing dependencies
With the virtual environment activated (if we have chosen this option) we must execute the following command to install all the necessary dependencies.
```shell script
(telegram-venv) $ pip install -r requirements.txt
```

It goes without saying that for our bot to work, it must have an Internet connection.

### Deactivating the virtual enviroment (only if we have created it)
Once all the previous steps have been successfully completed, all that remains is to deactivate the virtual environment.

To do so, execute the following command:
```shell script
(telegram-venv) $ deactivate
```

Our terminal should once again look like:
```shell script
$
```

### Running the bot
The only thing left to do would be to run our bot.

To do so, just execute the following command in the TU-telegram-bot folder:
```shell script
telegram-venv/bin/python -m telegram-bot
```

Our bot will be running and waiting for our messages

## How to use our bot

### Setting application.conf
You have a file called application-template.conf

Copy it into a new one called application.conf with your configuration.

Each parameter is explained in the file itself

### Sending a link
The bot will recognize any link that starts with _*https://www.tu.com/products/...*_

Simply send a text message with the link and the bot will do the rest.

## Use and collaborate
Feel free to use this code.

If you want to collaborate, you can open a pull request.

