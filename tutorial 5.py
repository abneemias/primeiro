from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
import easygui
from pythonosc.udp_client import SimpleUDPClient
import time

ip = "192.168.1.111"
port = 8089

client = SimpleUDPClient(ip, port)  # Create client

def certa():
    client.send_message("/1/push1", 1.0)
    time.sleep(0.5)
    client.send_message("/1/push1", 0.0)
    redefinir()
    pass


def errada():
    client.send_message("/1/push2", 1.0)
    time.sleep(0.5)
    client.send_message("/1/push2", 0.0)
    redefinir()
    pass


def amarelo():
    client.send_message("/1/push3", 1.0)
    time.sleep(0.5)
    client.send_message("/1/push3", 0.0)
    pass

def azul():
    client.send_message("/1/push4", 1.0)
    time.sleep(0.5)
    client.send_message("/1/push4", 0.0)
    pass
    
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
    if(nome=="amarelo"):
        amarelo()
    else:
        if(nome=="azul"):
            azul()
        else:
            easygui.msgbox(""+nome+"!", title="O PRIMEIRO")
            redefinir()
    
    pass
    
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
        return render_template('user.html')
    else:
        return redirect(url_for("login"))
        
@app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == 'POST':
        if request.form['submit_button'] == 'CERTA':
            certa()
            return render_template("admin.html")
        elif request.form['submit_button'] == 'ERRADA':
            errada()
            return render_template("admin.html")
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template("admin.html") 
        
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
   