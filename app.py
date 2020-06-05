import sqlite3,os,json,jsonify
from flask import Flask,request,g,jsonify,render_template,Response
from flask_api import status

app=Flask(__name__)

DATABASE = "homework.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Enable foreign key check
        #db.execute("PRAGMA foreign_keys = ON")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/task/<int:id>",methods=['PUT','DELETE'])
def UDTask(id):
    db = get_db()
    if request.method == 'PUT':
        try:
            vName = request.form.get('name',type=str)
            vStatus =  request.form.get('status',type=int)
            update_sql = "UPDATE task set name = ? ,status = ? WHERE id = ?"
            cursor = db.execute(update_sql,(vName,vStatus,id))
            db.commit()
            data ={}
            if cursor.rowcount > 0 :                
                data = {
                    "id":id,
                    "name":vName,
                    "status":vStatus
                }
            msg = data
        except:
            db.rollback()
            msg = 'U error'
        finally:
            db.close()
            #return render_template('result.html',result=msg),200
            #return msg,status.HTTP_200_OK
            return jsonify(msg),200
            
    elif request.method == 'DELETE':           
        try:
            delete_sql = "DELETE FROM task WHERE id = ?"
            cursor = db.execute(delete_sql,(id,))
            db.commit()
            if cursor.rowcount > 0 :
                msg = 'successfully deleted',200
            else:
                msg = 'no data be delete'
        except:
            db.rollback()
            msg = 'D error'        
        finally:
            db.close()
            return jsonify(msg)  

@app.route("/task",methods=['POST'])
def insTask():
    db = get_db()
    msg = None
    try:
        vId = request.form.get('id', type=int)
        vName = request.form.get('name',type=str)
        #vStatus = 0  db.table column default
        insert_sql = "INSERT INTO task (id,name) VALUES (?,?)"
        db.execute(insert_sql,(vId,vName))
        db.commit()
        cursor = db.execute("SELECT id,name,status FROM task WHERE id = ? ",(vId,))
        #data = [{'id' : row[0], 'name' : row[1], 'status' : row[2],} for row in cursor]
        data = {}
        for row in cursor:
            data = {
                "result":{
                        "id":row[0],
                        "name":row[1],
                        "status":row[2],
                    }                
            }

    except:
        db.rollback()
        msg = 'insert error'
    finally:
        db.close()
        if msg is not None:
            return msg
        else:
            return jsonify(data),201
            #return render_template('result.html',result=msg,status_code=200)

@app.route("/tasks",methods=['GET'])
def getTask():
    db = get_db()
    vId = request.args.get('id') 
    if vId is None :
        query_sql = "SELECT id,name,status FROM task Where id = (SELECT MAX(ID) FROM TASK) "
    else:
        query_sql = "SELECT id,name,status FROM task Where id = ?" 
    
    cursor = db.execute(query_sql,(vId,)) 
    #data = [{'id' : row[0], 'name' : row[1], 'status' : row[2],} for row in cursor]
    data = {}
    for row in cursor:
        data = {
            "result":[
                {
                    "id":row[0],
                    "name":row[1],
                    "status":row[2],
                }
            ]
        }    
    return jsonify(data),201
    #return render_template('result.html',result=data)

    '''  todo study
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    '''            
    '''
    #回傳 json格式     
    #return json.dumps(cur) #Content-Type 不變
    #return json.dumps(cur,mimetype='application/json') #指定Content-Type
    #return jsonify(data)    
    '''
     
if __name__=="__main__":
    app.debug=True #debug mode,auto reload and compile program
    app.run()