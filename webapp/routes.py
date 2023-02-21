from flask import render_template, url_for, redirect, request, session
from webapp.form import  verify_register_form, autentificarea ,reset_pass, send_otp, send_otp_phone, register_user, verify_changes, password_hash
from webapp import app
from webapp.database import vot_statistic ,id_user, vot_select ,titluri,select,set_vot,vot_db,validvot,set_vot_popor, get_data_by_id, cautar,introdu,verificare_legi, select_id, get_id_by_title, verificare, inregistrare_changes_db, inreg_data
from datetime import datetime
from flask_session import Session
import pandas as pd
import time


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
global poc
poc=1
##session['ver']
def global_variables():
    global da
    session['ver']='1'
    
    if session.get('username')!=None:
        global username
        global email
        username = session.get('username')
        email = session.get('email')


@app.route("/")
@app.route("/acasa")
@app.route("/acasa/")
@app.route("/acasa/<id>")
def acasa(id=None):
    global_variables()
    titles=titluri()
    if id == None:
        global da
        titles=titluri()
        ids = select_id()
        da=len(titles)//10
        global poc
        
        if session['ver']=='1' and da>poc:
            poc+=1
            print("eu")
            session['ver']=None
        if poc*10+len(titles)%10==len(titles):
            session['ver']='2'
        c=poc
        return render_template("index.html", len = len(titles),titles=titles, ids=ids,b=c)
    else:
        session['id']=id
        content = get_data_by_id("legi", id)
        print(content)
        titlu = content[0][1]
        if content[0][2] != None and content[0][2] != "nan":
            pro = content[0][2]
        else:
            pro = 0

        if content[0][3] != None and content[0][3] != "nan":
            contra= content[0][3]
        else:
            contra = 0
        
        if content[0][4] != None and content[0][4] != "nan":
            neu = content[0][4]
        else:
            neu = 0
        
        if content[0][5] != None and content[0][5] != "nan":
            pro_pop = content[0][5]
        else:
            pro_pop = 0

        if content[0][6] != None and content[0][6] != "nan":
            con_pop = content[0][6]
        else:
            con_pop = 0
        
        if content[0][7] != None and content[0][7] != "nan":
            neu_pop = content[0][7]
        else:
            neu_pop = 0

        ok = None

        if session.get("username"):
            id_user=inreg_data("id","username",session['username'])
            legi_votate_ids=validvot(id_user)
            ok=True
            id=str(session['id'])
            for id_lege in legi_votate_ids:
                id_lege = id_lege[0]
                id_lege = str(id_lege)
                if id==id_lege:
                    ok=False
            print(ok)
        
        return render_template("layout_lege.html", titlu=titlu, pro=pro, contra=contra, neu=neu, pro_pop=pro_pop, con_pop=con_pop, neu_pop=neu_pop, ok=ok)


@app.route("/inregistrare", methods=['GET', 'POST'])
def inregistrare():
    global_variables()
    if session.get("username")  == None:
        error=""
        taken_username = False
        taken_email = False
        taken_phone = False
        if request.method == "POST":
            global username
            username = request.form.get("user")
            global email
            email = request.form.get("email") 
            phone = request.form.get("phone")
            password = request.form.get("password") 
            pass_conf= request.form.get("pass_conf")
            global passwordh
            global phone_nr
            error, taken_username, taken_email, taken_phone, passwordh, phone_nr=verify_register_form(username,email,phone,password,pass_conf)
            print(phone_nr)
            if error!="Inregistrare completa": 
                print(error)
            else:
                return redirect(url_for('email_verification', exceptie = ''))    
    else:
        return redirect(url_for("acasa"))

    return render_template("register.html" ,error=error, taken_username=taken_username, taken_email=taken_email, taken_phone=taken_phone)

@app.route("/autentificare", methods=['GET', 'POST'])
def autentificare():
    global_variables()
    if session.get("username") == None:
        eror=""
        if request.method == "POST":
            global username
            global email
            user = request.form.get("user")  
            if user == "Admin" or user == 'parlamentulpoporului@gmail.com' and password=="parlamentulpoporului":
                session['username']="Admin"
                return redirect(url_for("admin"))
            else:
                if '@' in user:
                    email = user
                    username = inreg_data("username",'email', email)
                else:
                    username = user
                    email = inreg_data("email",'username', username)
                password = request.form.get("password") 
                eror=""
                eror = autentificarea(email, username,password)
                if eror=="" :
                    if user=="Admin" or user == 'parlamentulpoporului@gmail.com' and password=="parlamentulpoporului":
                        return redirect(url_for("admin"))
                    else :
                        session["username"] = username
                        session["email"] = email
                    return redirect(url_for("acasa",user=username))
    else:
        return redirect(url_for("acasa"))

    return render_template("login.html",e=eror)


@app.route("/account",methods=['GET', 'POST'])
def account():
    global_variables()
    if session.get('username'):
        error_em = None
        error_us = None
        global email
        global username
        if request.method == "POST":
            username_form = request.form.get('user')
            email_form = request.form.get('email')
            gl_username, gl_email, error_us, error_em = verify_changes(username, username_form, email, email_form)
            email = gl_email
            username = gl_username
        id=id_user(session['username'])
        aux=vot_select(str(id[0][0]),"pro")
        a=len(aux)
        aux=vot_select(str(id[0][0]),"contra")
        b=len(aux)
        aux=vot_select(str(id[0][0]),"neu")
        c=len(aux)
        max1=0
        max_eu=''
        if a>b:
            max1=a
            max_eu="pro"
        else: 
            max1=b
            max_eu="contra"
        if max1<c :
            max1=c
            max_eu="neutru"

        aux=vot_statistic("legi","max_parlament","pro","nr")
        pro_par=len(aux)
        aux=vot_statistic("legi","max_parlament","contra","nr")
        cont_par=len(aux)
        aux=vot_statistic("legi","max_parlament","neu","nr")
        neu_par=len(aux)
        aux=vot_statistic("vot","vot","pro","id")
        pro_pop=len(aux)
        aux=vot_statistic("vot","vot","contra","id")
        cont_pop=len(aux)
        aux=vot_statistic("vot","vot","neutru","id")
        neu_pop=len(aux)
        stat_par=0
        if pro_par+cont_par+neu_par!=0:
            if max_eu=="pro":
                stat_par=int((pro_par/(pro_par+cont_par+neu_par))*100)
                stat_pop=int((pro_pop/(pro_pop+cont_pop+neu_pop))*100)
            elif max_eu=="contra":
                stat_par=int((cont_par/(pro_par+cont_par+neu_par))*100)
                stat_pop=int((cont_pop/(pro_pop+cont_pop+neu_pop))*100)
            elif max_eu=="neutru":
                stat_par=int((neu_par/(pro_par+cont_par+neu_par))*100)
                stat_pop=int((neu_pop/(pro_pop+cont_pop+neu_pop))*100)
    

        return render_template("account.html", email = email, error_em = error_em, error_us = error_us,a=a,b=b,c=c,tot=a+b+c,stat_par=stat_par,stat_pop=stat_pop)
    else:
        return redirect(url_for('autentificare'))

@app.route("/reset-password",methods=['GET', 'POST'])
@app.route("/reset-password/",methods=['GET', 'POST'])
@app.route("/reset-password/<exceptie>",methods=['GET', 'POST'])
def reseteaza_parola(exceptie = None):
    global_variables()
    if session["username"] != None or exceptie != None:
        global email
        e=""
        if exceptie:
            if request.method == 'POST':
                password_new =request.form.get("new_pass")
                password_conf=request.form.get("conf_pass")
                if password_new == password_conf:
                    pas=password_hash(password_new)
                    inregistrare_changes_db('password',pas,email)
                    return redirect(url_for('autentificare'))
                else:
                    e = 'Parolele nu coincid'
        else:
            if request.method == "POST":
                password = request.form.get("password")
                password_new =request.form.get("new_pass")
                password_conf=request.form.get("conf_pass") 
                e=reset_pass(password, password_new, password_conf, email)  
                if e=="":
                    return redirect(url_for("acasa"))
        return render_template("reseteazaparola.html",e=e, exceptie=exceptie)
    else:
        return redirect(url_for('acasa'))

# @app.route("/legi-propuse")
# @app.route("/legi-propuse/")
# @app.route("/legi-propuse/<titlu>")
# def legi_propuse(titlu=None):
#     if titlu == None:
#         titlu = get_legi("titlu")
#         descriere = get_legi("descriere")
#         username = get_legi("username")
#         data = get_legi("data")
#         nr = len(titlu)
#         return render_template("legi_propuse.html", title = "Legi Propuse", titlu=titlu, descriere=descriere, username=username, data=data, nr=nr)
#     else:
#         content = get_data_by_title("legipr_admise", titlu)
#         titlu = content[0][1]
#         descriere = content[0][2]
#         username = content[0][3]
#         data = content[0][4]
#         if content[0][5] != None:
#             pro = content[0][5]
#         else:
#             pro = 0

#         if content[0][6] != None:
#             contra = content[0][6]
#         else:
#             contra = 0
        
#         if content[0][7] != None:
#             neutru = content[0][7]
#         else:
#             neutru = 0
#         return render_template("layout_lege_propusa.html", title = "Legi Propuse", titlu=titlu, descriere=descriere, username=username, data=data, pro=pro, contra=contra, neutru=neutru)

# @app.route("/legi-recente")
# @app.route("/legi-recente/")
# @app.route("/legi-recente/<titlu>")
# def legi_recente(titlu=None):
#     if titlu == None:
#         titles=titluri()
#         return render_template("legi_recente.html", title = "Legi Recente", len=len(titles), titles=titles)
#     else:
#         content = get_data_by_title("legi", titlu)
#         titlu = content[0][1]
#         if content[0][2] != None:
#             pro_lect1 = content[0][2]
#         else:
#             pro_lect1 = 0

#         if content[0][3] != None:
#             con_lect1 = content[0][3]
#         else:
#             con_lect1 = 0
        
#         if content[0][4] != None:
#             neu_lect1 = content[0][4]
#         else:
#             neu_lect1 = 0
        
#         if content[0][5] != None:
#             pro_lect2 = content[0][5]
#         else:
#             pro_lect2 = 0

#         if content[0][6] != None:
#             con_lect2 = content[0][6]
#         else:
#             con_lect2 = 0
        
#         if content[0][7] != None:
#             neu_lect2 = content[0][7]
#         else:
#             neu_lect2 = 0
#         return render_template("layout_lege_recenta.html", titlu=titlu, pro_lect1=pro_lect1, con_lect1=con_lect1, neu_lect1=neu_lect1, pro_lect2=pro_lect2, con_lect2=con_lect2, neu_lect2=neu_lect2)


# @app.route("/propune-legi", methods=['GET', 'POST'])
# def propune_legi():
#     if session["username"] != None:
#         if request.method == "POST":

#             titlu = request.form.get("titlu")
#             descriere = request.form.get("descriere")
#             username = session["username"]
#             now = datetime.now()
#             data = now.strftime('%d-%m-%Y')
#             postare_db(titlu, descriere, username, data)
#             if True:
#                 return redirect(url_for("acasa"))
#         return render_template("propune_legi.html", title = "Propune o lege")
#     else:
#         if session["username"] == None:
#             flash('Trebuie sa va autentificati pentru a accesa Propune Legi!', 'danger')
#             return redirect(url_for('autentificare'))
#         else:
#             flash('Trebuie sa va verificati email-ul pentru a accesa Propune Legi!', 'danger')
#             return redirect(url_for('legi_propuse'))

@app.route("/logout")
def logout():
    global_variables()
    global username
    username = None
    global email
    email = None
    global phone_nr
    phone_nr = None
    session["email"]=None
    session["username"]=None
    return redirect(url_for("acasa"))

@app.route("/cautare", methods = ['POST'])
def cautare():
    
    if request.method == "POST":
        caut = request.form.get("caut")
        a=cautar(caut)
    ids = []
    for i in a:
        id = get_id_by_title("legi", i[0])
        id = id[0]
        ids.append(id)
    eror=""
    n=len(a)
    if n==0:
        eror="Ne pare rau nu sa gasit nicio lege"
    return render_template("index.html", title = "Cautare",titles=a,len=len(a), eror=eror, ids=ids)

@app.route("/verificare-email" , methods=["GET","POST"])
@app.route("/verificare-email/" , methods=["GET","POST"])
@app.route("/verificare-email/<exceptie>" , methods=["GET","POST"])
def email_verification(exceptie = None):
    global_variables()
    if session.get('username') and exceptie == None:
        return redirect(url_for("acasa"))
    else:
        global email
        msg = send_otp(email)
        if request.method == "POST":
            otp = request.form.get("otp")
            print(msg, " ", otp)
            if otp == msg:
                if exceptie == "forgot-password":
                    return redirect(url_for('reseteaza_parola', exceptie = "forgot-password"))
                else:
                    return redirect(url_for("sms"))
            else:
                print("Otp invalid")

    return render_template('email_verification.html', email=email, msg=msg)

@app.route("/admin" , methods=["GET","POST"])
def admin():
    if request.method == "POST":
        a=request.form.get("file1")
        print(a)
        data = pd.read_excel(a)
        print(data)
        tit=data['Denumire'].tolist()
        pro1=data['Lectura 1'].tolist()
        cont1=data['Unnamed: 2'].tolist()
        neu1=data['Unnamed: 3'].tolist()
        pro2=data['Lectura 2'].tolist()
        cont2=data['Unnamed: 5'].tolist()
        neu2=data['Unnamed: 6'].tolist()
        pro3=data['Lectura 3'].tolist()
        cont3=data['Unnamed: 8'].tolist()
        neu3=data['Unnamed: 9'].tolist()
        len1=len(tit)
        for i in range(1, len(tit) ):
            b=verificare_legi(tit[i])
            pro_s=0
            cont_s=0
            neu_s=0
            if b==0:
                if not pd.isna(pro1[i]):
                    pro_s+=int(pro1[i])
                if not pd.isna(pro2[i]):
                    pro_s+=int(pro2[i])
                if not pd.isna(pro3[i]):
                    pro_s+=int(pro3[i])
                if not pd.isna(cont1[i]):
                    cont_s=int(cont1[i])
                if not pd.isna(cont2[i]):
                    cont_s+=int(cont2[i])
                if not pd.isna(cont3[i]):
                    cont_s+=int(cont3[i])
                if not pd.isna(neu1[i]):
                    neu_s=int(neu1[i])
                if not pd.isna(neu2[i]):
                    neu_s+=int(neu2[i])
                if not pd.isna(neu3[i]) :
                    neu_s+=int(neu3[i])
                introdu(str(tit[i]),str(pro_s),str(cont_s),str(neu_s))
            print(b)
    return render_template("admin.html")

@app.route("/acasa/pro" , methods=["GET","POST"])
def pro():
    print('provot')
    a=select(session['id'])
    if a[0][0] != None:
        b=a[0][0]
    else:
        b = 0
    if a[0][1] != None:
        c=a[0][1]
    else:
        c = 0
    if a[0][2] != None:
        d=a[0][2]
    else:
        d = 0
    b=b+1
    max=0
    vot_max=''
    if b>max:
        max=b
        vot_max='pro'
    if c>max:
        max=c
        vot_max='contra'
    if d>max :
        max=d
        vot_max='neutru'
    set_vot_popor(vot_max,session['id'])
    set_vot(b,session['id'],"pro_popor")
    a=inreg_data("id",'username',session['username'])
    print(a)
    vot_db(a,session['id'],"pro")
    print(session['id'])
    return redirect(url_for('acasa',id=session['id']))

@app.route("/acasa/contra" , methods=["GET","POST"])
def contra():
    print('provot')
    a=select(session['id'])
    if a[0][0] != None:
        b=a[0][0]
    else:
        b = 0
    if a[0][1] != None:
        c=a[0][1]
    else:
        c = 0
    if a[0][2] != None:
        d=a[0][2]
    else:
        d = 0
    c=c+1
    max=0
    vot_max=''
    if b>max:
        max=b
        vot_max='pro'
    if c>max:
        max=c
        vot_max='contra'
    if d>max :
        max=d
        vot_max='neutru'
    set_vot_popor(vot_max,session['id'])
    set_vot(c,session['id'],"contra_popor")
    a=inreg_data("id",'username',session['username'])
    print(a)
    vot_db(a,session['id'],"contra")
    print(session['id'])
    return redirect(url_for('acasa',id=session['id']))

@app.route("/acasa/neutru" , methods=["GET","POST"])
def neutru():
    print('provot')
    a=select(session['id'])
    if a[0][0] != None:
        b=a[0][0]
    else:
        b = 0
    if a[0][1] != None:
        c=a[0][1]
    else:
        c = 0
    if a[0][2] != None:
        d=a[0][2]
    else:
        d = 0
    d=d+1
    print("???????????????????")
    print(b)
    print("????????????????????????????")
    max=0
    vot_max=''
    if b>max:
        max=b
        vot_max='pro'
    if c>max:
        max=c
        vot_max='contra'
    if d>max :
        max=d
        vot_max='neutru'
    set_vot_popor(vot_max,session['id'])
    set_vot(d,session['id'],"neu_popor")
    a=inreg_data("id",'username',session['username'])
    print(a)
    vot_db(a,session['id'],"neutru")
    print(session['id'])
    return redirect(url_for('acasa',id=session['id']))

# @app.route("/update_account",methods=['GET', 'POST'])
# def update_account():
#     if session["username"] != None:
#         e=""
#         if request.method == "POST":
#             password = request.form.get("password")
#             password_new =request.form.get("new_pass")
#             password_conf=request.form.get("conf_pass") 
#             global email
#             e=reset_pass(password, password_new, password_conf, email)  
#             if e=="":
#                 return redirect(url_for("acasa"))
#         return render_template("reseteazaparola.html",e=e)
#     else:
#         return redirect(url_for('acasa'))

@app.route("/verificare-telefon" , methods=["GET","POST"])
def sms():
    global_variables()
    if session.get('username'):
        return redirect(url_for("acasa"))
    else:
        global phone_nr
        msg = send_otp_phone(phone_nr)
        if request.method == "POST":
            otp = request.form.get("otp")
            print(msg, " ", otp)
            if otp == msg:
                register_user(username, email, phone_nr, passwordh)
                session["email"]=email
                session["username"]=username
                print(session['username'])
                print(session['email'])
                return redirect(url_for("acasa"))
            else:
                print("Otp invalid")
    return render_template("phone_verification.html",phone=phone_nr)

@app.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    exceptie = "forgot-password"
    var = None
    error = None
    global email
    if request.method == 'POST':
        email = request.form.get('email')
        var = verificare('email', email)
    if var:
        return redirect(url_for('email_verification', exceptie = exceptie))
    else:
        error = "Email inexistent"
    return render_template('forgot_password.html')

    
