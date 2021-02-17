from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
import easygui
from pythonosc.udp_client import SimpleUDPClient
import time

import tkinter

class MessageBox(object):

    def __init__(self, msg, b1, b2, frame, t, entry):

        root = self.root = tkinter.Tk()
        root.title('Message')
        self.msg = str(msg)
        # ctrl+c to copy self.msg
        root.bind('<Control-c>', func=self.to_clip)
        # remove the outer frame if frame=False
        if not frame: root.overrideredirect(True)
        # default values for the buttons to return
        self.b1_return = True
        self.b2_return = False
        # if b1 or b2 is a tuple unpack into the button text & return value
        if isinstance(b1, tuple): b1, self.b1_return = b1
        if isinstance(b2, tuple): b2, self.b2_return = b2
        # main frame
        frm_1 = tkinter.Frame(root)
        frm_1.pack(ipadx=2, ipady=2)
        # the message
        message = tkinter.Label(frm_1, text=self.msg,font=("Verdana", 150))
        

        message.pack(padx=8, pady=8)
        # if entry=True create and set focus
        if entry:
            self.entry = tkinter.Entry(frm_1)
            self.entry.pack()
            self.entry.focus_set()
        # button frame
        frm_2 = tkinter.Frame(frm_1)
        frm_2.pack(padx=4, pady=4)
        # buttons
        btn_1 = tkinter.Button(frm_2, width=8, text=b1)
        btn_1['command'] = self.b1_action
        btn_1.pack(side='left')
        if not entry: btn_1.focus_set()
        btn_2 = tkinter.Button(frm_2, width=8, text=b2)
        btn_2['command'] = self.b2_action
        btn_2.pack(side='left')
        # the enter button will trigger the focused button's action
        btn_1.bind('<KeyPress-Return>', func=self.b1_action)
        btn_2.bind('<KeyPress-Return>', func=self.b2_action)
        # roughly center the box on screen
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        root.update_idletasks()
        xp = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        yp = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        geom = (root.winfo_width(), root.winfo_height(), xp, yp)
        root.geometry('{0}x{1}+{2}+{3}'.format(*geom))
        # call self.close_mod when the close button is pressed
        root.protocol("WM_DELETE_WINDOW", self.close_mod)
        # a trick to activate the window (on windows 7)
        root.deiconify()
        
        root.attributes('-topmost', True)
        root.focus_force()
        
        # if t is specified: call time_out after t seconds
        if t: root.after(int(t*1000), func=self.time_out)

    def b1_action(self, event=None):
        try: x = self.entry.get()
        except AttributeError:
            self.returning = self.b1_return
            self.root.quit()
        else:
            if x:
                self.returning = x
                self.root.quit()

    def b2_action(self, event=None):
        self.returning = self.b2_return
        self.root.quit()

    # remove this function and the call to protocol
    # then the close button will act normally
    def close_mod(self):
        pass

    def time_out(self):
        try: x = self.entry.get()
        except AttributeError: self.returning = None
        else: self.returning = x
        finally: self.root.quit()

    def to_clip(self, event=None):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.msg)
        
def mbox(msg, b1='OK', b2='Cancel', frame=True, t=False, entry=False):
    """Create an instance of MessageBox, and get data back from the user.
    msg = string to be displayed
    b1 = text for left button, or a tuple (<text for button>, <to return on press>)
    b2 = text for right button, or a tuple (<text for button>, <to return on press>)
    frame = include a standard outerframe: True or False
    t = time in seconds (int or float) until the msgbox automatically closes
    entry = include an entry widget that will have its contents returned: True or False
    """
    msgbox = MessageBox(msg, b1, b2, frame, t, entry)
    msgbox.root.mainloop()
    # the function pauses here until the mainloop is quit
    msgbox.root.destroy()
    return msgbox.returning



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
            mbox(nome)
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
   