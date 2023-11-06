from flask import render_template

from src.repositories.UserRepository import UserRepository


class AppController:
    def index(self):
        users = UserRepository().get_all_users()
        users = []

        return render_template("index.html", users=users)
