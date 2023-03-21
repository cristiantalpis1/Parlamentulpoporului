import mysql.connector
from argon2 import PasswordHasher
verifi=0 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="legi"
)
# getting the cursor by cursor() method
def introdu(tit,pro,contra,neu):
  mycursor = db.cursor()
  a=''

  if int(contra)<int(pro):
     a='pro'
  elif int(neu)<int(contra):
     a='contra'
  else:
     a='neu'
 

  insertQuery = "INSERT INTO legi (titlu, pro, contra, neu) VALUES ('"+tit+"','"+pro+"','"+contra+"','"+neu+"');"
  
  mycursor.execute(insertQuery)
  
  print("No of Record Inserted :", mycursor.rowcount)
  
  # we can use the id to refer to that row later.
  print("Inserted Id :", mycursor.lastrowid)
  
  # To ensure the Data Insertion, commit database.
  db.commit() 
  
  # close the Connection
 # db.close()

def titluri():
  mycursor = db.cursor()

  mycursor.execute("SELECT titlu FROM legi")

  myresult = mycursor.fetchall()

  return myresult

def select_id():
  mycursor = db.cursor()

  mycursor.execute("SELECT nr FROM legi")

  myresult = mycursor.fetchall()

  return myresult


def inregistrare(user,email,phone,password):
  print("----------------------")
  mycursor = db.cursor()
  print("?????????????????????????????")
  insertQuery = "INSERT INTO inregistrare (username, email, phone, password) VALUES ('"+user+"','"+email+"','"+phone+"','"+password+"');"
  print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
  mycursor.execute(insertQuery)
  print("999999999999999999999")
  print("No of Record Inserted :", mycursor.rowcount)
  
  # we can use the id to refer to that row later.
  print("Inserted Id :", mycursor.lastrowid)
  
  # To ensure the Data Insertion, commit database.
  db.commit()

def username():
  mycursor = db.cursor()

  mycursor.execute("SELECT username FROM inregistrare")

  myresult = mycursor.fetchall()

  return myresult

def verificare(camp,nume):
    mycursor = db.cursor()

    sql = "SELECT * FROM inregistrare WHERE "+camp+"='"+nume+"'"

    mycursor.execute(sql)
    ok=1
    myresult = mycursor.fetchall()
    
    if not(myresult):
      ok=0
    print(ok)
    return ok
def verify_password(self, password):
     hasher = PasswordHasher()
     try:
         hasher.verify(self, password)
         return True
     except Exception:
         return False

def verificare_pass(password,email):
    mycursor = db.cursor()

    sql = "SELECT password FROM inregistrare WHERE email ='"+email+"';"

    mycursor.execute(sql)

    myresult = mycursor.fetchall()
    ph = PasswordHasher()
    a=verify_password(myresult[0][0],password)
    return a
  
def inregistrare_changes_db(camp, value, email):
    mycursor = db.cursor()

    sql = "UPDATE inregistrare SET "+camp+" = '"+value+"' WHERE email = '"+email+"'"

    mycursor.execute(sql)

    db.commit()

def postare_db(titlu, descriere, username, data):
  mycursor = db.cursor()

  insertQuery = "INSERT INTO legipropuse (titlu, descriere, username, data) VALUES ('"+titlu+"','"+descriere+"','"+username+"', '"+data+"');"
  
  mycursor.execute(insertQuery)
  
  print("No of Record Inserted :", mycursor.rowcount)
  
  # we can use the id to refer to that row later.
  print("Inserted Id :", mycursor.lastrowid)
  
  # To ensure the Data Insertion, commit database.
  db.commit()

def get_id_lege(id):
  mycursor = db.cursor()
  sql = "SELECT * FROM legipropuse WHERE nr ='"+id+"'"
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  titlu = myresult[0][1]
  descriere = myresult[0][2]
  username = myresult[0][3]
  data = myresult[0][4]
  insertQuery = "INSERT INTO legipr_admise (titlu, descriere, username, data) VALUES ('"+titlu+"','"+descriere+"','"+username+"', '"+data+"');"
  mycursor.execute(insertQuery)
  
  print("No of Record Inserted :", mycursor.rowcount)
  
  # we can use the id to refer to that row later.
  print("Inserted Id :", mycursor.lastrowid)
  
  # To ensure the Data Insertion, commit database.
  db.commit()

def get_legi(camp):
  mycursor = db.cursor()

  mycursor.execute("SELECT "+camp+" FROM legipr_admise")

  myresult = mycursor.fetchall()

  return myresult

def get_data_by_id(camp, id):

  mycursor = db.cursor()

  mycursor.execute("SELECT * FROM "+camp+" WHERE nr ='"+id+"'")

  myresult = mycursor.fetchall()

  return myresult

def cautar(caut):
  mycursor = db.cursor()

  mycursor.execute("SELECT titlu FROM legi WHERE titlu LIKE '%"+caut+"%'")

  myresult = mycursor.fetchall()

  return myresult

def inreg_data(camp1, camp2, nume):
    mycursor = db.cursor()
    sql = "SELECT "+camp1+" FROM inregistrare WHERE "+camp2+" = '"+nume+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()[0]
    try:
      return myresult
    except:
      print("An exception occurred")

def verificare_legi(nume):
    mycursor = db.cursor()

    sql = "SELECT * FROM legi WHERE titlu='"+nume+"'"

    mycursor.execute(sql)
    ok=1
    myresult = mycursor.fetchall()
    
    if not(myresult):
      ok=0
    print(ok)
    return ok

def select(id):
  mycursor = db.cursor()

  sql = "SELECT pro_popor,contra_popor,neu_popor FROM legi WHERE nr ="+id+""


  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult

def set_vot(nr,id,camp):
  
  mycursor = db.cursor()
  nr=str(nr)
  camp=str(camp)
  id=str(id)
  sql = "UPDATE legi SET "+camp+" = "+nr+" WHERE nr = "+id+""

  mycursor.execute(sql)

  db.commit()

def vot_db(id_user,id_legi,vot):
  mycursor = db.cursor()
  id_legi=str(id_legi)
  id_user=str(id_user)
  insertQuery = "INSERT INTO vot(id_user,id_lege,vot) VALUES ("+id_user+","+id_legi+",'"+vot+"');"
  
  mycursor.execute(insertQuery)

  db.commit()

def validvot(id):
  mycursor = db.cursor()
  id=str(id)
  sql = "SELECT id_lege FROM vot WHERE id_user ="+id+""


  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult

def set_vot_popor(max_vot,id):
  
  mycursor = db.cursor()

  id=str(id)
  sql = "UPDATE legi SET max_popor= '"+max_vot+"' WHERE nr = "+id+""

  mycursor.execute(sql)

  db.commit()

def get_id_by_title(camp, title):

  mycursor = db.cursor()

  mycursor.execute("SELECT nr FROM "+camp+" WHERE titlu ='"+title+"'")

  myresult = mycursor.fetchall()

  return myresult

def vot_select(id_user,id):
    mycursor = db.cursor()

    mycursor.execute("SELECT id FROM vot WHERE vot ='"+id+"' and id_user='"+id_user+"'")

    myresult = mycursor.fetchall()

    return myresult

def id_user(username):
    mycursor = db.cursor()

    mycursor.execute("SELECT id FROM inregistrare WHERE username ='"+username+"'")

    myresult = mycursor.fetchall()

    return myresult 

def vot_statistic(tabel,camp,data,nume):
    mycursor = db.cursor()

    mycursor.execute("SELECT "+nume+" FROM "+tabel+" WHERE "+camp+" ='"+data+"'")

    myresult = mycursor.fetchall()

    return myresult

   

