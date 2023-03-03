from collections import UserList
from logging import RootLogger
import pygame, sys
import tkinter as tk
import subprocess
import random
import socket
import threading
import sqlite3
from settings import *
from level import Level
from overworld import Overworld
from gameinterface import userInterface

class Game:
    def __init__(self):
        #attributes of the game
        self.max_level = 2

        #attributes of the player
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        #creating an instance of the user interface
        self.gameinterface = userInterface(screen)
         
        #creating the overworld
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.update_coins, self.update_current_health)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.current_health = 100
        self.coins = 0

    def update_coins(self, amount):
        self.coins += amount

    def update_current_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.gameinterface.player_coins(self.coins)
            self.gameinterface.player_health(self.current_health, self.max_health)
            self.check_game_over()
     
#setting up screen
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
game = Game()

#creating the database to store user login details
conn = sqlite3.connect('user_db.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')

c.execute("INSERT INTO users VALUES ('user1', 'password1')")
c.execute("INSERT INTO users VALUES ('user2', 'password2')")
c.execute("INSERT INTO users VALUES ('user3', 'password3')")
c.execute("INSERT INTO users VALUES ('user4', 'password4')")
c.execute("INSERT INTO users VALUES ('user5', 'password5')")

conn.commit()

window = tk.Tk()
window.title('Platformer Game')

def single_player():
    #check if login details are correct
    username = username_entry.get()
    password = password_entry.get()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()

    if result:
        #displaying the single player game screen
        while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                screen.fill('grey')
                text = font.render("Single player Game", True, (0, 0, 0))
                screen.blit(text, (10, 10))
                game.run()

                pygame.display.update()
                clock.tick(60)
    else:
        #displays error message for wrong login details
        error_label.config(text = 'Invalid username or password')

def multiplayer():
    print('Connecting to game server... ')

    #displaying the multi player game screen
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill('grey')
            text = font.render("Multi player Game", True, (0, 0, 0))
            screen.blit(text, (10, 10))
            game.run()

            pygame.display.update()
            clock.tick(60)

single_player_button = tk.Button(window, text = 'Single Player', command = single_player)
single_player_button.pack()

multiplayer_button = tk.Button(window, text = 'Multiplayer', command = multiplayer)
multiplayer_button.pack()

#displaying username box to enter username
username_label = tk.Label(window, text = "Username: ")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

#displaying password box to enter password
password_label = tk.Label(window, text = "Password: ")
password_label.pack()
password_entry = tk.Entry(window, show = "*")
password_entry.pack()

error_label = tk.Label(window, fg = 'red')
error_label.pack()

window.mainloop()
conn.close()