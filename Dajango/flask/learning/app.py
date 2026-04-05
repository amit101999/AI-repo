from flask import Flask , request , redirect , url_for,session,Response,render_template

app = Flask(__name__)
app.secret_key = "my_scret_key"  #



# @app.route("/" ,methods = ["POST" , "GET"])
# def login():
#     if request.method == "POST":
#         username = request.form.get("name")
#         password = request.form.get("password")
#         if username == "admin" and password == "123":
#             session["user"] = username 
#             # store the username in the session
#             return redirect(url_for("Welcome"))
#         else:
#             return  Response("Invalid credentials" , mimetype="text/plain")
#     return '''
#             <form method="post">
#             <input type="text" name="name" placeholder="Username">
#             <input type="password" name="password" placeholder="Password">
#             <button type="submit">Login</button>
#             </form>
#             '''

# @app.route("/welcome")
# def Welcome():
#     if "user" in session:
#         return f'''
#             Welcome {session['user']}!
#             <a href="{url_for('logout')}">Logout</a>
#                 '''
#     return redirect(url_for("login"))


# @app.route("/logout")
# def logout():
#     session.pop("user" , None)
#     return redirect(url_for("login"))


@app.route("/")
def login():
    return render_template("login.html")

@app.route("/submit" , methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "123":
        return render_template("welcome.html" , username=username)
    else:
        return "Invalid credentials" 
    