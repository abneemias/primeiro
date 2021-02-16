from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
import easygui


app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

primeiro = False
quem = "nenhum"

def definir(nome):
    global quem
    quem=nome
    global primeiro
    primeiro = True
    easygui.msgbox(""+nome+"!", title="O PRIMEIRO")
    redefinir()
    
def redefinir():
    global primeiro
    primeiro = False

@app.route("/")
def home():
	return render_template("index.html")    

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        if(user==""):
            return render_template("login.html")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            if(not primeiro):
                definir(user)
                print(quem)
        return render_template('user.html')
    else:
        return redirect(url_for("login"))

@app.route("/output")
def saida():
        return "neemias"

@app.route("/reset")
def reset():
    redefinir()
    return "oi"

@app.route("/logout")
def logout():
	session.pop("user", None)
	return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
   