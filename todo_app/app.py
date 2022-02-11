from flask import Flask, render_template, url_for, request, session, redirect
from datetime import datetime
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template("index.html",
                           todos=session.get("todos",[]),
                           added=session.get("added",[]),
                           complete=session.get("complete",[]),
                           removed=session.get("removed",[]))

@app.route('/add', methods=["POST"])
def add():
    if "newTask" in request.form:
        if "todos" in session:
            todos = session["todos"]
            todos.append(request.form["newTask"])
            session["added"] = [request.form["newTask"]]
            session["todos"] = todos
        else:
            session["todos"] = [request.form["newTask"]]
            session["added"] = [request.form["newTask"]]
    return redirect('/')



@app.route('/complete', methods=["POST"])
def complete():
    if "todos" not in session:
        return redirect('/')

    if "complete" not in session:
        session["complete"]=[]
        complete=[]
    else:
        complete=session["complete"]

    delTaskNums = []
    for key in request.form:
       if key.startswith("complete_"):
           taskNumString = key[9:]
           try:
               realTaskNum = int(taskNumString)
               if realTaskNum >= 0:
                   if realTaskNum < len(session["todos"]):
                       delTaskNums.append(realTaskNum)
           except ValueError:
               pass
    delTaskNums.reverse()
    todos = session["todos"]
    removed=[]
    for delTask in delTaskNums:
        removed.append(todos[delTask])
        cell=[todos.pop(delTask)]
        cell.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        complete.insert(0,cell)
    session["complete"]=complete
    session["todos"]=todos
    session["removed"]=removed
    return redirect('/')


@app.route('/clear', methods=["POST"])
def clear():
    session["complete"]=[]
    return redirect('/')
