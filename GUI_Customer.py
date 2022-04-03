import sys,time,datetime
import pymysql
import mysql.connector
#import base64
import random,urllib.request 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import *
from Custom_Widgets import *
from style import *


USERNAME=''
PASSWORD=''
data=()
krathsh=['','','','','',]

#ΣΥΝΔΕΣΗ ΧΡΗΣΤΗ
class Login_Form(QWidget):

    trigger=pyqtSignal()

    def __init__(self,parent=None):
        super(Login_Form,self).__init__(parent)
 
        layout= QVBoxLayout()
        self.lbl = QLabel('<h2 style="text-align:center;font-size:50px" > LOGIN </h2>',self)
        layout.addWidget(self.lbl)
        
        #Εισαγωγή πεδίων username και password
        self.username = QLineEdit(self)
        self.username.setPlaceholderText('Username')
        self.username.setAlignment(Qt.AlignCenter)
        self.username.setStyleSheet("font-size:18px;margin-bottom:20px;margin-left:150px;margin-right:150px")
        self.username.setText('mariapapa')
        
        layout.addWidget(self.username)
        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setAlignment(Qt.AlignCenter)
        self.username.textChanged.connect(lambda : self.username.setText(self.username.text()))
        self.password.setStyleSheet("font-size:18px;margin-bottom:20px;margin-left:150px;margin-right:150px")
        self.password.textChanged.connect(lambda : self.password.setText(self.password.text()))
        layout.addWidget(self.password)
        
        self.password.setText('maria123')

        self.login = QPushButton('Login',self)
        self.login.setStyleSheet("background : green; font-size:18px; margin-bottom:20px;margin-left:150px;margin-right:150px")
        layout.addWidget(self.login)
        
        #Πεδίο ανάκτησης λογαριασμού
        self.forgot_passw = QPushButton('Forgot Password?',self)
        self.forgot_passw.setStyleSheet("color:black;background :orange; font-size:18px; margin-bottom:20px;margin-left:150px;margin-right:150px")
        layout.addWidget(self.forgot_passw)

        self.donthaveaccount=QLabel("<h3 style='text-align:center'> Don't have an account? </h3>",self)
        layout.addWidget(self.donthaveaccount)

        #Πεδίο εγγραφής καινούριου χρήστη
        self.reg = QPushButton('Create an account',self)
        self.reg.setStyleSheet("background : blue; font-size:18px; margin-bottom:20px;margin-left:150px;margin-right:150px")
        layout.addWidget(self.reg)
        self.Exit = QPushButton('Έξοδος',self)
        self.Exit.setStyleSheet("margin-bottom:20px; font-size:16px; margin-left:150px;margin-right:150px")

        layout.addWidget(self.Exit)
        self.Exit.clicked.connect(self.Exit_Application)
        #self.setFixedSize(600,600)
        self.setLayout(layout)
        
    #Έξοδος εφαρμογής
    def Exit_Application(self):
        sys.exit(self)

    #Έλεγχος του κωδικού πρόσβασης για τη σύνδεση του χρήστη
    def Check_Password(self):
        msg=QMessageBox()
        username=self.username.text()
        password=self.password.text()
        if username=='' and password=='':
            msg.setText('Παρακαλώ εισάγετε τα στοιχεία σας')
            msg.exec_()
            self.login.clicked.connect(self.Check_Password)
            
        elif username!='' and password=='':
            msg.setText('Παρακαλώ εισάγετε κωδικό πρόσβασης.')
            msg.exec_()

        elif username=='' and password!='':
            msg.setText('Παρακαλώ εισάγετε όνομα χρήστη')
            msg.exec_()

        else:
            sql='SELECT username,password FROM EGGEGRAMMENOS'
            c.execute(sql)
            rows=c.fetchall()
            username_flag=0
            password_flag=0
            Account=0
            
            for i in rows:
                if str(username)==i[0] and password==str(i[1]):
                    username_flag=1
                    password_flag=1
                    Account=1
                    break
                elif str(username)==str(i[0]) and str(password)!=str(i[1]):
                    username_flag=1
                    password_flag=0
                    Account=0
                    break
                elif str(username)!=str(i[0]) and str(password)==str(i[1]):
                    username_flag=0
                    password_flag=1
                    Account=0
                    break
                elif str(username)!=str(i[0]) and str(password)!=str(i[1]):
                    username_flag=0
                    password_flag=0
                    Account=0
                    
            if username_flag==1 and password_flag==1 and Account==1:
                msg.setText('Καλώς ήλθατε '+str(username))
                msg.exec_()
                global USERNAME,PASSWORD,data
                USERNAME=str(username)
                PASSWORD=str(password)
                c.execute("SELECT * FROM EGGEGRAMMENOS WHERE username=%s and password=%s" % ("'"+username+"'","'"+password+"'"))
                user=c.fetchall()
                c.execute("SELECT TK,poli,odos,arithmos FROM DIEUTHINSH WHERE username=%s" % ("'"+username+"'"))
                dieuth=c.fetchall()[0]
                
                data=list(user[0])
                data.append(dieuth)
                self.lbl.setText('<h3 style="text-align:center">LOGGED IN AS</h3> '+str(username))                
                self.trigger.emit()

            elif username_flag==1 and password_flag==0 and Account==0:
                msg.setText('Λάθος Κωδικός')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
            elif username_flag==0 and password_flag==1 and Account==0:
                msg.setText('Λάθος όνομα χρήστη.')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
            elif username_flag==0 and password_flag==0 and Account==0:
                msg.setText("Δεν υπάρχει τέτοιος λογαριασμός.")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                
#ΑΝΑΚΤΗΣΗ ΛΟΓΑΡΙΑΣΜΟΥ
class Anakthsh_Account(QDialog):
    def __init__(self,parent=None):
        super(Anakthsh_Account,self).__init__(parent)

        layout=QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        #Φόρμα εισαγωγής προσωπικών στοιχείων για την αναζήτηση του λογαριασμού με τα στοιχεία αυτά
        form1=QFormLayout()
        form1.addRow(QLabel('<p style="margin:10px;font-size:20px;text-align:center">Δώστε μας μερικά από τα στοιχεία σας</p>'))
        self.fname_lbl=QLabel('Όνομα')
        self.fname_lbl.setStyleSheet('margin:10px;font-size:17px;')
        self.fname=QLineEdit(self)
        self.fname.setStyleSheet('margin:10px;font-size:17px;')
        form1.addRow(self.fname_lbl,self.fname)
        self.lname_lbl=QLabel('Επώνυμο')
        self.lname_lbl.setStyleSheet('margin:10px;font-size:17px;')
        self.lname=QLineEdit(self)
        self.lname.setStyleSheet('margin:10px;font-size:17px;')
        form1.addRow(self.lname_lbl,self.lname)
        self.adt_lbl=QLabel('Αριθμός Δελτίου Ταυτότητας')
        self.adt_lbl.setStyleSheet('margin:10px;font-size:17px;')
        self.adt=QLineEdit(self)
        self.adt.setStyleSheet('margin:10px;font-size:17px;')
        form1.addRow(self.adt_lbl,self.adt)
        self.ar_dipl_lbl=QLabel('Αριθμός Διπλώματος')
        self.ar_dipl_lbl.setStyleSheet('margin:10px;font-size:17px;')
        self.ar_dipl=QLineEdit(self)
        self.ar_dipl.setStyleSheet('margin:10px;font-size:17px;')
        form1.addRow(self.ar_dipl_lbl,self.ar_dipl)
        self.email_lbl=QLabel('Email')
        self.email_lbl.setStyleSheet('margin:10px;font-size:17px;')
        self.email=QLineEdit(self)
        self.email.setStyleSheet('margin:10px;font-size:17px;')
        form1.addRow(self.email_lbl,self.email)
        
        layout.addLayout(form1)

        #Στοιχεία επικοινωνίας της Εταιρείας
        self.lbl=QLabel('<p style="text-align:center;font-size:17px;"> Eπικοινωνήστε με την Εταιρεία μας.</p>')
        layout.addWidget(self.lbl)
        form=QFormLayout()
        self.lbl1=QLabel('Τηλέφωνο: ')
        self.lbl1.setStyleSheet('margin:5px;font-size:15px;')
        self.thl=QLabel('2204-600111')
        self.thl.setStyleSheet('margin:5px;font-size:15px;')
        self.lbl2=QLabel('Email: ')
        self.lbl2.setStyleSheet('margin:5px;font-size:15px;')
        self.mail=QLabel('EtairiaRendCars@gmail.com')
        self.mail.setStyleSheet('margin:5px;font-size:15px;')
        self.lbl3=QLabel('Fax: ')
        self.lbl3.setStyleSheet('margin:5px;font-size:15px;')
        self.fax=QLabel('+49-631-237-262')
        self.fax.setStyleSheet('margin:5px;font-size:15px;')
        form.addRow(self.lbl1,self.thl)
        form.addRow(self.lbl2,self.mail)
        form.addRow(self.lbl3,self.fax)
        
        layout.addLayout(form)

        self.ok=QPushButton('OK')
        self.ok.setStyleSheet('margin-bottom:10px;font-size:17px;background:green')
        layout.addWidget(self.ok)

        self.setLayout(layout)
        self.show()

    #Αναζήτηση λογαριασμού στην βάση δεδομένων που έχει τα εισαχθέντα στοιχεία της φόρμας.
    def Check_Data(self):
        msg=QMessageBox()
        fname=self.fname.text()
        lname=self.lname.text()
        adt=self.adt.text()
        ar_dipl=self.ar_dipl.text()
        email=self.email.text()
        c.execute('SELECT username,password FROM EGGEGRAMMENOS WHERE firstname=%s AND lastname=%s AND adt=%s AND ar_diplomatos=%s AND email=%s'%("'"+fname+"'","'"+lname+"'","'"+adt+"'","'"+ar_dipl+"'","'"+email+"'") )
        data=c.fetchall()
        
        #Μύνημα ενημέρωσης για το αν βρέθηκε ή όχι ο λογαριασμός.
        if data==[]:
            msg.setIcon(QMessageBox.Critical)
            msg.setText('<p style="font-size:17px;">Δεν βρήκαμε λογαριασμό με τα στοιχεία αυτά.</p>')
            msg.exec_()
        else:
            msg.setText('<p style="font-size:17px;">Τα στοιχεία λογαριασμού σας είναι: <br> username:'+str(data[0][0])+'<br>password: '+str(data[0][1])+ '</p>' )
            msg.exec_()

#ΕΓΓΡΑΦΗ ΚΑΙΝΟΥΡΙΟΥ ΧΡΗΣΤΗ
class Registration_Window(QWidget):

    finished=pyqtSignal()

    def __init__(self,parent=None):
        super(Registration_Window,self).__init__(parent)

        #Φόρμα Εγγραφής καινούριου χρήστη με στοιχεία: username,password, όνομα, επώνυμο
        # αριθμός δελτίου ταυτότητας,αριθμός διπλώματος, τηλέφωνο, email, και διεύθυνση.
        form=QFormLayout()
        self.lbl = QLabel('<p style="font-size:25px;text-align:center" > Εισάγετε τα στοιχεία σας </p>',self)
        form.addRow(self.lbl)
        self.Fname = QLineEdit(self)
        self.Fname.setStyleSheet('font-size:18px;margin-left:100px;margin-right:100px;')
        self.Fname.textChanged.connect(lambda : self.Fname.setText(self.Fname.text()))
        form.addRow(QLabel('<p style="font-size:20px;"> Όνομα: </p>'),self.Fname)
        self.Lname = QLineEdit(self)
        self.Lname.setStyleSheet('font-size:18px;margin-left:100px;margin-right:100px;')
        self.Lname.textChanged.connect(lambda : self.Lname.setText(self.Lname.text()))
        form.addRow(QLabel('<p style="font-size:20px;">Επώνυμο:</p>'),self.Lname)
        self.Username=QLineEdit(self)
        self.Username.setStyleSheet('font-size:18px;margin-left:100px;margin-right:100px;')
        self.Username.textChanged.connect(lambda : self.Username.setText(self.Username.text()))
        form.addRow(QLabel('<p style="font-size:20px;">Username:</p>'),self.Username)
        self.Password=QLineEdit(self)
        self.Password.setStyleSheet('font-size:18px;margin-left:100px;margin-right:100px;')
        self.Password.textChanged.connect(lambda : self.Password.setText(self.Password.text()))
        form.addRow(QLabel('<p style="font-size:20px;">Password:</p>'),self.Password)
        self.adt = QLineEdit(self)
        self.adt.setStyleSheet('font-size:18px;margin-left:100px;margin-right:100px;')
        self.adt.textChanged.connect(lambda : self.adt.setText(self.adt.text()))
        form.addRow(QLabel('<p style="font-size:20px;">Αριθμός Δελτίου Ταυτότητας:</p>'),self.adt)
        self.ar_diplomatos = QLineEdit(self)
        self.ar_diplomatos.setStyleSheet('font-size:18px;margin-left:100px;margin-right:100px;')
        self.ar_diplomatos.textChanged.connect(lambda : self.ar_diplomatos.setText(self.ar_diplomatos.text()))
        form.addRow(QLabel('<p style="font-size:20px;">Αριθμός Διπλώματος:</p>'),self.ar_diplomatos)
        self.Phone = QLineEdit(self)
        self.Phone.setStyleSheet('font-size:18px;margin-left:100px;margin-right:100px;')
        self.Phone.textChanged.connect(lambda : self.Phone.setText(self.Phone.text()))
        form.addRow(QLabel('<p style="font-size:20px;">Τηλέφωνο:</p>'),self.Phone)
        self.Email = QLineEdit(self)
        self.Email.setStyleSheet('font-size:18px;margin-left:100px;margin-right:100px;')
        self.Email.textChanged.connect(lambda : self.Email.setText(self.Email.text()))
        form.addRow(QLabel('<p style="font-size:20px;">Email:</p>'),self.Email)
        form.addRow(QLabel('<p style="font-size:22px;text-align:center">Διεύθυνση</p>'))
        self.TK_label=QLabel('<p style="font-size:20px;">TK:</p>')
        self.TK = QLineEdit(self)
        self.TK.setStyleSheet('font-size:18px;margin-left:0px;margin-right:100px;text-align:center;')
        self.TK.textChanged.connect(lambda : self.TK.setText(self.TK.text()))
        form.addRow(self.TK_label,self.TK)
        self.poli_label=QLabel('<p style="font-size:20px;">Πόλη:</p>')
        self.poli= QLineEdit(self)
        self.poli.setStyleSheet('font-size:18px;margin-left:0px;margin-right:100px;text-align:center;')
        self.poli.textChanged.connect(lambda : self.poli.setText(self.poli.text()))
        form.addRow(self.poli_label,self.poli)
        self.odos_label=QLabel('<p style="font-size:20px;">Οδός:</p>')
        self.odos = QLineEdit(self)
        self.odos.setStyleSheet('font-size:18px;margin-left:0px;margin-right:100px;text-align:center;')
        self.odos.textChanged.connect(lambda : self.odos.setText(self.odos.text()))
        form.addRow(self.odos_label,self.odos)
        self.arithm_label=QLabel('<p style="font-size:20px;">Αριθμός:</p>')
        self.arithm = QLineEdit(self)
        self.arithm.setStyleSheet('font-size:18px;margin-left:0px;margin-right:100px;margin-bottom:30px;text-align:center;')
        self.arithm.textChanged.connect(lambda : self.arithm.setText(self.arithm.text()))
        form.addRow(self.arithm_label,self.arithm)

        groupbox=QGroupBox()
        groupbox.setLayout(form)
        scroll=QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        #scroll.setFixedHeight(800)
        scroll.setFixedWidth(900)
        
        layout=QVBoxLayout()
        layout.addWidget(scroll) 
        self.registr = QPushButton('Εγγραφή',self)
        self.registr.setStyleSheet('font-size:18px;margin-top:30px;margin-left:200px;margin-right:200px;background-color:orange;color:black;')

        #Ακύρωση εγγραφής
        self.go_back = QPushButton('Ακύρωση',self)
        self.go_back.setStyleSheet('font-size:18px;text-align:center;margin-top:10px;margin-left:200px;margin-right:200px;')
        layout.addWidget(self.registr)
        layout.addWidget(self.go_back)
        self.setStyleSheet('margin:10px;font-size: 20 px')
        #self.setFixedSize(800,800)
        self.setLayout(layout)
        
#ΕΛΕΓΧΟΣ ΣΤΟΙΧΕΙΩΝ ΚΑΙΝΟΥΡΙΟΥ ΧΡΗΣΤΗ ΚΑΙ ΕΙΣΑΓΩΓΗ ΑΥΤΩΝ ΣΤΗ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ
    def Check_Reg_Data(self):
        msg=QMessageBox()
        username=self.Username.text()      
        password=self.Password.text()
        firstname=self.Fname.text()
        lastname=self.Lname.text()
        adt=self.adt.text()
        ar_diplomatos=self.ar_diplomatos.text()
        thl=self.Phone.text()
        email=self.Email.text()
        dieuthinsi=[self.TK.text(),self.poli.text(),self.odos.text(),self.arithm.text()]
        
        global data
        data=(username,password,firstname,lastname,adt,ar_diplomatos,thl,email,dieuthinsi)
        
        blank=0
        for i in data:
            if i=='':
                blank=1
                break    
        if blank==1:
            msg.setText('Please enter all your data.')
            msg.exec_()
        else:
            sql='SELECT * FROM EGGEGRAMMENOS'
            c.execute(sql)
            user=c.fetchall() 
            
            flag_adt=0            
            flag_ar_dipl=0
            used=0
            #Έλεγχος για τα γνωρίσματα username,ΑΔΤ και αριθμού διπλώματος αν χρησιμοποιούται, καθώς είναι μοναδικά.
            for i in user:
                if username==i[0]:
                    used=1
                    break
                else:
                    if adt==i[4]:
                        flag_adt=1
                    if ar_diplomatos==i[5]:
                        flag_ar_dipl=1

            if used==1 :
                msg.setText('Αυτό το username χρησιμοποιείται.')
                msg.exec_()
            else:
                if flag_adt==1:
                    msg.setText('Αυτό το ΑΔΤ χρησιμοποιείται')
                    msg.exec_()
                else:
                    if flag_ar_dipl==1:
                        msg.setText('Αυτός ο Αριθμός Διπλώματος χρησιμοποιείται')
                        msg.exec_()
                    else:
                        #Εισαγωγή των στοιχείων στη βάση.
                        try:
                            sql="INSERT INTO EGGEGRAMMENOS(username,password,firstname,lastname,adt,ar_diplomatos,thl,email) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)" % ("'"+username+"'","'"+password+"'","'"+firstname+"'","'"+lastname+"'","'"+adt+"'","'"+ar_diplomatos+"'","'"+thl+"'","'"+email+"'")
                            c.execute(sql)
                            sql='INSERT INTO DIEUTHINSH(username,TK,poli,odos,arithmos) VALUES(%s,%s,%s,%s,%s)'%("'"+username+"'","'"+dieuthinsi[0]+"'","'"+dieuthinsi[1]+"'","'"+dieuthinsi[2]+"'","'"+dieuthinsi[3]+"'")
                            c.execute(sql)
                            msg.setText('Εγγραφήκατε!\n Πηγαίνετε πίσω και συνδεθείτε στον λογαριασμό σας.')
                            msg.exec_()
                            self.finished.emit()
                        except:
                            msg=QMessageBox()
                            msg.setText('Εισάγετε σωστά τα στοιχεία σας.')
                            msg.exec_()
                
#Παράθυρο Ειδοποίησης της ολοκληρωμένη εγγραφής.
class Registered_Window(QWidget):
    def __init__(self,parent=None):
        super(Registered_Window,self).__init__(parent)

        layout=QVBoxLayout()

        self.lbl1_welcome = QLabel('<h1 style="text-align:center">Ευχαριστούμε για την εγγραφή! </h1>',self)
        layout.addWidget(self.lbl1_welcome)
        self.lbl2_welcome = QLabel('<p style="text-align:center;font-size:20px;">Θα επικοινωνήσουμε σύντομα μαζί σας για επιβεβαίωση. </p>',self)
        layout.addWidget(self.lbl2_welcome)

        #Κουμπί επαναφοράς στην αρχική σελίδα για σύνδεση του καινούριου χρήστη.
        self.go_log = QPushButton('Login',self)
        self.go_log.setStyleSheet("font-size:20px;margin-left:200px;margin-right:200px;margin-bottom:200px;background : green") 
        layout.addWidget(self.go_log)

        self.setStyleSheet('font-size: 30 px')
        #self.setFixedSize(600,600)
        self.setLayout(layout)

#Κεντρική σελίδα της εφαρμογής μετά τη σύνδεση χρήστη.
class Main_Customer_Window(QWidget):
    def __init__(self,parent=None):
        super(Main_Customer_Window,self).__init__(parent)

        layout= QGridLayout()

        self.lbl_welcome = QLabel('<h1 style="text-align:center"> Καλώς ήλθατε<br>στην εφαρμογή</h1>',self)

        ##Κουμπί για αποσύνδεση χρήστη.
        self.logout=QPushButton('Logout',self)
        self.logout.setStyleSheet('font-size:16px;margin-bottom:100px;margin-top:10px;height:20px;width:30%')

        #Κουμπί για Ρυθμίσεις του προφίλ του χρήστη.
        self.Profile_Settings=QPushButton('Ρυθμίσεις Προφίλ',self)
        self.Profile_Settings.setStyleSheet('font-size:16px;margin-bottom:100px;margin-top:10px;height:20px;width:30%')

        #Κουμπί για επίβλεψη των κρατήσεων του χρήστη.
        self.Krathseis = QPushButton('Κρατήσεις',self)
        self.Krathseis.setStyleSheet('font-size:16px;margin-bottom:150px;')

        #Κουμπί για καινούρια κράτηση.
        self.New_krathsh=QPushButton('Καινούρια κράτηση',self)
        self.New_krathsh.setStyleSheet('font-size:16px;margin-bottom:150px;')

        layout.addWidget(self.lbl_welcome,0,1)
        layout.addWidget(self.Profile_Settings,1,0)
        layout.addWidget(self.logout,1,2)
        layout.addWidget(self.Krathseis,2,1)
        layout.addWidget(self.New_krathsh,3,1)

        #self.setFixedSize(600,600)
        self.setLayout(layout) 
       
#ΡΥΘΜΙΣΕΙΣ ΠΡΟΦΙΛ
class Profile_Settings(QWidget):
    def __init__(self,parent=None):
        super(Profile_Settings,self).__init__(parent)

        #Πεδία των στοιχείων του λογαριασμού και κουμπιά με δυνατότητα αλλαγής των στοιχείων αυτών.
        layout=QGridLayout()

        self.mainlabel=QLabel('<p style="font-size:22px;text-align:center;margin-top:10px;">Ρυθμίσεις Προφίλ </p>',self)
        layout.addWidget(self.mainlabel,0,0)
        self.lbl_username=QLabel('<p style="font-size:17px;margin-right:50px;">Username</p>',self)
        layout.addWidget(self.lbl_username,1,0)
        self.username=QLineEdit(self)
        self.username.setReadOnly(True)
        self.username.setPlaceholderText(data[0])
        self.username.setStyleSheet('font-size:17px;color:white;margin-right:50px;')
        layout.addWidget(self.username,2,0)
        self.lbl_firstname=QLabel('<p style="font-size:17px;">Όνομα</p>',self)
        layout.addWidget(self.lbl_firstname,3,0)
        self.fname=QLineEdit(self)
        self.fname.setReadOnly(True)
        self.fname.setPlaceholderText(data[2])
        self.fname.setStyleSheet('font-size:17px;color:white;margin-right:50px;')
        layout.addWidget(self.fname,4,0)
        self.btn_fname=QPushButton('Αλλαγή Ονόματος',self)
        self.btn_fname.setStyleSheet('font-size:17px;margin-left:50px;margin-right:50px;')
        layout.addWidget(self.btn_fname,4,1)
        self.lbl_lastname=QLabel('<p style="font-size:17px;">Επώνυμο</p>',self)
        layout.addWidget(self.lbl_lastname,5,0)
        self.lname=QLineEdit(self)
        self.lname.setReadOnly(True)
        self.lname.setPlaceholderText(data[3])
        self.lname.setStyleSheet('font-size:17px;color:white;margin-right:50px;')
        layout.addWidget(self.lname,6,0)
        self.btn_lname=QPushButton('Αλλαγή Επωνύμου',self)
        self.btn_lname.setStyleSheet('font-size:17px;margin-left:50px;margin-right:50px;')
        layout.addWidget(self.btn_lname,6,1)
        self.lbl_password=QLabel('<p style="font-size:17px;">Κωδικός</p>',self)
        layout.addWidget(self.lbl_password,7,0)
        self.password=QLineEdit(self)
        self.password.setReadOnly(True)
        self.password.setPlaceholderText(data[1])
        self.password.setStyleSheet('font-size:17px;color:white;margin-right:50px;')
        layout.addWidget(self.password,8,0)
        self.btn_passw=QPushButton('Αλλαγή Κωδικού',self)
        self.btn_passw.setStyleSheet('font-size:17px;margin-left:50px;margin-right:50px;')
        layout.addWidget(self.btn_passw,8,1)
        self.lbl_adt=QLabel('<p style="font-size:17px;">Αριθμός Δελτίου Ταυτότητας</p>',self)
        layout.addWidget(self.lbl_adt,9,0)
        self.adt=QLineEdit(self)
        self.adt.setReadOnly(True)
        self.adt.setPlaceholderText(data[4])
        self.adt.setStyleSheet('font-size:17px;color:white;margin-right:50px;')
        layout.addWidget(self.adt,10,0)
        self.btn_adt=QPushButton('Αλλαγή ΑΔΤ',self)
        self.btn_adt.setStyleSheet('font-size:17px;margin-left:50px;margin-right:50px;')
        layout.addWidget(self.btn_adt,10,1)
        self.lbl_ar_diplomatos=QLabel('<p style="font-size:17px;">Αριθμός Διπλώματος</p>',self)
        layout.addWidget(self.lbl_ar_diplomatos,11,0)
        self.ar_diplomatos=QLineEdit(self)
        self.ar_diplomatos.setReadOnly(True)
        self.ar_diplomatos.setPlaceholderText(data[5])
        self.ar_diplomatos.setStyleSheet('font-size:17px;color:white;margin-right:50px;')
        layout.addWidget(self.ar_diplomatos,12,0)
        self.btn_ar_diplomatos=QPushButton('Αλλαγή Αριθμού Διπλώματος',self)
        self.btn_ar_diplomatos.setStyleSheet('font-size:15px;margin-left:50px;margin-right:50px;')
        layout.addWidget(self.btn_ar_diplomatos,12,1)
        self.lbl_phone=QLabel('<p style="font-size:17px;">Τηλέφωνο</p>',self)
        layout.addWidget(self.lbl_phone,13,0)
        self.phone=QLineEdit(self)
        self.phone.setReadOnly(True)
        self.phone.setPlaceholderText(data[6])
        self.phone.setStyleSheet('font-size:15px;color:white;margin-right:50px;')
        layout.addWidget(self.phone,14,0)
        self.btn_phone=QPushButton('Αλλαγή Τηλεφώνου',self)
        self.btn_phone.setStyleSheet('font-size:17px;margin-left:50px;margin-right:50px;')
        layout.addWidget(self.btn_phone,14,1)
        self.lbl_email=QLabel('<p style="font-size:17px;">Email</p>',self)
        layout.addWidget(self.lbl_email,15,0)
        self.email=QLineEdit(self)
        self.email.setReadOnly(True)
        self.email.setPlaceholderText(data[7])
        self.email.setStyleSheet('font-size:17px;color:white;margin-bottom:20px;margin-right:50px;')
        layout.addWidget(self.email,16,0)
        self.btn_email=QPushButton('Αλλαγή Email',self)
        self.btn_email.setStyleSheet('font-size:15px;margin-bottom:20px;margin-left:50px;margin-right:50px;')
        layout.addWidget(self.btn_email,16,1)
        self.lbl_dieuth=QLabel('<p style="font-size:17px;">Διεύθυνση</p>',self)
        layout.addWidget(self.lbl_dieuth,17,0)
        self.dieuth=QLineEdit(self)
        self.dieuth.setReadOnly(True)
        self.dieuth.setPlaceholderText(str(data[8][1])+' '+str(data[8][2])+' '+str(data[8][3])+' '+str(data[8][0]))
        self.dieuth.setStyleSheet('font-size:17px;color:white;margin-bottom:20px;margin-right:50px;')
        layout.addWidget(self.dieuth,18,0)
        self.btn_dieuth=QPushButton('Αλλαγή Διεύθυνσης',self)
        self.btn_dieuth.setStyleSheet('font-size:15px;margin-bottom:20px;margin-left:50px;margin-right:50px;')
        layout.addWidget(self.btn_dieuth,18,1)
        
        #Επιστροφή στο κεντρικό Παράθυρο
        self.go_back=QPushButton('Πίσω',self)
        self.go_back.setStyleSheet('font-size:16px;margin-top:10px;margin-left:70px;margin-right:70px;')
        layout.addWidget(self.go_back,0,1)
               
        self.setStyleSheet('font-size: 30 px')
        layout.setRowMinimumHeight(5,100)
        #self.setFixedSize(500,500)
        self.setLayout(layout)

#Αλλαγή Ονόματος χρήστη
class Change_Fname_Window(QDialog):
    def __init__(self,parent=None):
        super(Change_Fname_Window,self).__init__(parent)
        
        layout=QGridLayout()
        layout.setRowMinimumHeight(3,55)
        self.setWindowTitle('Αλλαγή Ονόματος')
        self.mainlabel=QLabel('<h4> Αλλαγή Ονόματος </h4>')
        layout.addWidget(self.mainlabel,0,0)
        
        #Πεδίο παλιού ονόματος χρήστη
        self.lbl_old=QLabel('<p style="font-size:16px;">Παλιό Όνομα</p>')
        layout.addWidget(self.lbl_old,1,0)
        self.old_fname=QLineEdit(self)
        self.old_fname.setReadOnly(True)
        self.old_fname.setStyleSheet("font-size:16px;")
        self.old_fname.setText(data[2])
        layout.addWidget(self.old_fname,2,0)
        
        #Πεδίο εισαγωγής καινούριου ονόματος χρήστη
        self.lbl_new=QLabel('<p style="font-size:16px;">Kαινούριο Όνομα</p>')
        layout.addWidget(self.lbl_new,3,0)
        self.new_fname=QLineEdit(self)
        self.new_fname.setStyleSheet("font-size:16px;")
        layout.addWidget(self.new_fname,4,0)
        self.new_fname.textChanged.connect(lambda : self.new_fname.setText(self.new_fname.text()))
        
        #Πεδίο εισαγωγής κωδικού
        self.lbl_pass=QLabel('<p style="font-size:16px;">Password',self)
        layout.addWidget(self.lbl_pass,5,0)
        self.password=QLineEdit(self)
        self.password.setStyleSheet("font-size:16px;")
        layout.addWidget(self.password,6,0)
        self.password.textChanged.connect(lambda : self.password.setText(self.password.text()))
        self.Done=QPushButton('Τέλος',self)
        self.Done.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Done,7,0)

        #Ακύρωση της διαδικασίας αλλαγής στοιχείων χρήστη.
        self.Cancel=QPushButton('Ακύρωση',self)
        self.Cancel.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Cancel,8,0)

        #Με την επιλογή του κουμπιού "Τέλος" καλείται η συνάρτηση Αναβάθμισης των δεδομένων της βάσης με τα καινούρια εισαχθέντα στοιχεία χρήστη.
        self.Done.clicked.connect(self.Changed)

        self.setLayout(layout)
        self.setFixedSize(400,400)
        self.show()
    
    #Αναβάθμιση της βάσης δεδομένων με τα καινούρια εισαχθέντα στοιχεία χρήστη. 
    def Changed(self):
        try:
            msg=QMessageBox()
            new_fname=self.new_fname.text()
            #Έλεγχος κωδικού πρόσβασης.
            if self.password.text()==PASSWORD:
                msg.setText('Το όνομα σας άλλαξε.')
                msg.exec_()
                sql="UPDATE EGGEGRAMMENOS SET firstname =%s WHERE username=%s and password=%s" %("'"+new_fname+"'","'"+USERNAME+"'","'"+PASSWORD+"'")
                c.execute(sql)
                global data
                data=(data[0],data[1],new_fname,data[3],data[4],data[5],data[6],data[7],data[8])
                self.close()
            else:
                msg.setText('Λανθασμένος κωδικός.')
                msg.exec_()
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()
            
#Αλλαγή Επωνύμου χρήστη
class Change_Lname_Window(QDialog):
    def __init__(self,parent=None):
        super(Change_Lname_Window,self).__init__(parent)
        
        layout=QGridLayout()
        layout.setRowMinimumHeight(3,55)
        self.setWindowTitle('Αλλαγή Επωνύμου')
        self.mainlabel=QLabel('<h4> Αλλαγή Επωνύμου </h4>')
        layout.addWidget(self.mainlabel,0,0)

        #Πεδίο παλιού επωνύμου χρήστη
        self.lbl_old=QLabel('<p style="font-size:16px;">Παλιό Επώνυμο</p>')
        layout.addWidget(self.lbl_old,1,0)
        self.old_lname=QLineEdit(self)
        self.old_lname.setReadOnly(True)
        self.old_lname.setStyleSheet("font-size:16px;")
        self.old_lname.setText(data[3])
        layout.addWidget(self.old_lname,2,0)

        #Πεδίο εισαγωγής καινούριου επωνύμου χρήστη
        self.lbl_new=QLabel('<p style="font-size:16px;">Καινούριο Επώνυμο</p>')
        layout.addWidget(self.lbl_new,3,0)
        self.new_lname=QLineEdit(self)
        self.new_lname.setStyleSheet("font-size:16px;")
        layout.addWidget(self.new_lname,4,0)
        self.new_lname.textChanged.connect(lambda : self.new_lname.setText(self.new_lname.text()))
        self.lbl_pass=QLabel('Password',self)
        layout.addWidget(self.lbl_pass,5,0)

        #Πεδίο εισαγωγής κωδικού
        self.password=QLineEdit(self)
        self.password.setStyleSheet("font-size:16px;")
        layout.addWidget(self.password,6,0)
        self.password.textChanged.connect(lambda : self.password.setText(self.password.text()))
        self.Done=QPushButton('Τέλος',self)
        self.Done.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Done,7,0)

        #Ακύρωση της διαδικασίας αλλαγής στοιχείων χρήστη.
        self.Cancel=QPushButton('Ακύρωση',self)
        self.Cancel.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Cancel,8,0)
        
        #Με την επιλογή του κουμπιού "Τέλος" καλείται η συνάρτηση Αναβάθμισης των δεδομένων της βάσης με τα καινούρια εισαχθέντα στοιχεία χρήστη.
        self.Done.clicked.connect(self.Changed)

        self.setLayout(layout)
        self.setStyleSheet('font-size: 30 px')
        self.setFixedSize(400,400)
        self.show()
   
    #Αναβάθμιση της βάσης δεδομένων με τα καινούρια εισαχθέντα στοιχεία χρήστη.  
    def Changed(self):
        try:
            msg=QMessageBox()
            new_lname=self.new_lname.text()
            #Έλεγχος κωδικού πρόσβασης.
            if self.password.text()==PASSWORD:
                msg.setText('Το επώνυμό σας άλλαξε.')
                msg.exec_()
                sql="UPDATE EGGEGRAMMENOS SET lastname =%s WHERE username=%s and password=%s" %("'"+new_lname+"'","'"+USERNAME+"'","'"+PASSWORD+"'")
                c.execute(sql)
                global data
                data=(data[0],data[1],data[2],new_lname,data[4],data[5],data[6],data[7],data[8])
                self.close()
            else:
                msg.setText('Λανθασμένος κωδικός.')
                msg.exec_()
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()

#Αλλαγή Κωδικού πρόσβασης χρήστη
class Change_Password_Window(QDialog):
    def __init__(self,parent=None):
        super(Change_Password_Window,self).__init__(parent)
        
        layout=QGridLayout()
        layout.setRowMinimumHeight(3,55)
        self.setWindowTitle('Αλλαγή Password')
        self.mainlabel=QLabel('<h4> Αλλαγή Password </h4>')
        layout.addWidget(self.mainlabel,0,0)
        
        #Πεδίο παλιού κωδικού χρήστη
        self.lbl_old=QLabel('<p style="font-size:16px;">Παλιός κωδικός</p>')
        layout.addWidget(self.lbl_old,1,0)
        self.old_pass=QLineEdit(self)
        self.old_pass.setReadOnly(True)
        self.old_pass.setStyleSheet("font-size:16px;")
        self.old_pass.setText(PASSWORD)
        layout.addWidget(self.old_pass,2,0)

        #Πεδίο εισαγωγής καινούριου κωδικού χρήστη
        self.lbl_new=QLabel('<p style="font-size:16px;">Καινούριος κωδικός</p>')
        layout.addWidget(self.lbl_new,3,0)
        self.new_pass=QLineEdit(self)
        self.new_pass.setStyleSheet("font-size:16px;")
        layout.addWidget(self.new_pass,4,0)
        self.new_pass.textChanged.connect(lambda : self.new_pass.setText(self.new_pass.text()))

        #Πεδίο εισαγωγής τρέχοντος κωδικού
        self.lbl_pass=QLabel('Password',self)
        layout.addWidget(self.lbl_pass,5,0)
        self.password=QLineEdit(self)
        self.password.setStyleSheet("font-size:16px;")
        layout.addWidget(self.password,6,0)
        self.password.textChanged.connect(lambda : self.password.setText(self.password.text()))
        self.Done=QPushButton('Τέλος',self)
        self.Done.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Done,7,0)

        #Ακύρωση της διαδικασίας αλλαγής στοιχείων χρήστη.
        self.Cancel=QPushButton('Ακύρωση',self)
        self.Cancel.setStyleSheet("font-size:15px;")
        layout.addWidget(self.Cancel,8,0)

        #Με την επιλογή του κουμπιού "Τέλος" καλείται η συνάρτηση Αναβάθμισης των δεδομένων της βάσης με τα καινούρια εισαχθέντα στοιχεία χρήστη.
        self.Done.clicked.connect(self.Changed)
        
        self.setLayout(layout)
        self.setStyleSheet('font-size: 30 px')
        self.setFixedSize(400,400)
        self.show()
    
    #Αναβάθμιση της βάσης δεδομένων με τα καινούρια εισαχθέντα στοιχεία χρήστη.      
    def Changed(self):
        try:
            msg=QMessageBox()
            new_password=self.new_pass.text()
            #Έλεγχος κωδικού πρόσβασης.
            if self.password.text()==PASSWORD:
                msg.setText('Ο κωδικός σας άλλαξε.')
                msg.exec_()
                sql="UPDATE EGGEGRAMMENOS SET password =%s WHERE username=%s and password=%s" %("'"+new_password+"'","'"+USERNAME+"'","'"+PASSWORD+"'")
                c.execute(sql)
                global data
                self.password.setText(data[2])
                data=(data[0],new_password,data[2],data[3],data[4],data[5],data[6],data[7],data[8])            
                self.close()
            else:
                msg.setText('Λανθασμένος κωδικός.')
                msg.exec_()
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()

#Αλλαγή ΑΔΤ χρήστη
class Change_adt_Window(QDialog):
    def __init__(self,parent=None):
        super(Change_adt_Window,self).__init__(parent)
        
        layout=QGridLayout()
        layout.setRowMinimumHeight(3,55)
        self.setWindowTitle('Αλλαγή Αριθμού Δελτίου Ταυτότητας')
        self.mainlabel=QLabel('<h4> Αλλαγή Αριθμού Δελτίου Ταυτότητας </h4>')
        layout.addWidget(self.mainlabel,0,0)

        #Πεδίο παλιού ΑΔΤ χρήστη
        self.lbl_old=QLabel('<p style="font-size:16px;">Παλιό ΑΔΤ</p>')
        layout.addWidget(self.lbl_old,1,0)
        self.old_adt=QLineEdit(self)
        self.old_adt.setReadOnly(True)
        self.old_fname.setReadOnly(True)
        self.old_adt.setStyleSheet("font-size:16px;")
        self.old_adt.setText(data[4])
        layout.addWidget(self.old_adt,2,0)

        #Πεδίο καινούριου ΑΔΤ χρήστη
        self.lbl_new=QLabel('<p style="font-size:16px;">Καινούριο ΑΔΤ</p>')
        layout.addWidget(self.lbl_new,3,0)
        self.new_adt=QLineEdit(self)
        self.new_adt.setStyleSheet("font-size:16px;")
        layout.addWidget(self.new_adt,4,0)
        self.new_adt.textChanged.connect(lambda : self.new_adt.setText(self.new_adt.text()))

        #Πεδίο εισαγωγής κωδικού
        self.lbl_pass=QLabel('Password',self)
        layout.addWidget(self.lbl_pass,5,0)
        self.password=QLineEdit(self)
        self.password.setStyleSheet("font-size:16px;")
        layout.addWidget(self.password,6,0)
        self.password.textChanged.connect(lambda : self.password.setText(self.password.text()))
        self.Done=QPushButton('Τέλος',self)
        self.Done.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Done,7,0)

        #Ακύρωση της διαδικασίας αλλαγής στοιχείων χρήστη.
        self.Cancel=QPushButton('Ακύρωση',self)
        self.Cancel.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Cancel,8,0)

        #Με την επιλογή του κουμπιού "Τέλος" καλείται η συνάρτηση Αναβάθμισης των δεδομένων της βάσης με τα καινούρια εισαχθέντα στοιχεία χρήστη.
        self.Done.clicked.connect(self.Changed)

        self.setLayout(layout)
        self.setStyleSheet('font-size: 30 px')
        self.setFixedSize(400,400)
        self.show()

    #Αναβάθμιση της βάσης δεδομένων με τα καινούρια εισαχθέντα στοιχεία χρήστη.  
    def Changed(self):
        try:
            msg=QMessageBox()
            new_adt=self.new_adt.text()
            #Έλεγχος κωδικού πρόσβασης.
            if self.password.text()==PASSWORD:
                msg.setText('Το ADT σας άλλαξε.')
                msg.exec_()
                sql="UPDATE EGGEGRAMMENOS SET adt =%s WHERE username=%s and password=%s" %("'"+new_adt+"'","'"+USERNAME+"'","'"+PASSWORD+"'")
                c.execute(sql)
                global data
                data=(data[0],data[1],data[2],data[3],new_adt,data[5],data[6],data[7],data[8])            
                self.close()
            else:
                msg.setText('Λανθασμένος κωδικός.')
                msg.exec_()
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()

#Αλλαγή Αριθμού Διπλώματος χρήστη
class Change_ar_diplomatos_Window(QDialog):
    def __init__(self,parent=None):
        super(Change_ar_diplomatos_Window,self).__init__(parent)
        
        layout=QGridLayout()
        layout.setRowMinimumHeight(3,55)
        self.setWindowTitle('Αλλαγή Αριθμού Διπλώματος')
        self.mainlabel=QLabel('<h4> Αλλαγή Αριθμού Διπλώματος </h4>')
        layout.addWidget(self.mainlabel,0,0)
        layout.addWidget(self.lbl_old,1,0)
        
        #Πεδίο παλιού Αριθμού Διπλώματος χρήστη
        self.old_ar_dipl=QLineEdit(self)
        self.old_ar_dipl.setReadOnly(True)
        self.old_ar_dipl.setStyleSheet("font-size:16px;")
        self.old_ar_dipl.setText(data[5])
        layout.addWidget(self.old_ar_dipl,2,0)
        self.lbl_new=QLabel('<p style="font-size:16px;">Καινούριος Αριθμός Διπλώματος</p>')
        layout.addWidget(self.lbl_new,3,0)

        #Πεδίο καινούριου Αριθμού Διπλώματος χρήστη
        self.new_ar_dipl=QLineEdit(self)
        self.new_ar_dipl.setStyleSheet("font-size:16px;")
        layout.addWidget(self.new_ar_dipl,4,0)
        self.new_ar_dipl.textChanged.connect(lambda : self.new_ar_dipl.setText(self.new_ar_dipl.text()))
        self.lbl_pass=QLabel('<p style="font-size:16px;">Password</p>',self)
        layout.addWidget(self.lbl_pass,5,0)

        #Πεδίο κωδικού χρήστη
        self.password=QLineEdit(self)
        self.password.setStyleSheet("font-size:16px;")
        layout.addWidget(self.password,6,0)
        self.password.textChanged.connect(lambda : self.password.setText(self.password.text()))
        self.Done=QPushButton('Τέλος',self)
        self.Done.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Done,7,0)

        #Ακύρωση της διαδικασίας αλλαγής στοιχείων χρήστη.
        self.Cancel=QPushButton('Ακύρωση',self)
        self.Cancel.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Cancel,8,0)

        #Με την επιλογή του κουμπιού "Τέλος" καλείται η συνάρτηση Αναβάθμισης των δεδομένων της βάσης με τα καινούρια εισαχθέντα στοιχεία χρήστη.
        self.Done.clicked.connect(self.Changed)

        self.setLayout(layout)
        self.setStyleSheet('font-size: 30 px')
        self.setFixedSize(400,400)
        self.show()

    #Αναβάθμιση της βάσης δεδομένων με τα καινούρια εισαχθέντα στοιχεία χρήστη.  
    def Changed(self):
        try:
            msg=QMessageBox()
            new_ar_dipl=self.new_ar_dipl.text()
            #Έλεγχος κωδικού πρόσβασης.
            if self.password.text()==PASSWORD:
                msg.setText('Ο αριθμός διπλώματος σας άλλαξε.')
                msg.exec_()
                sql="UPDATE EGGEGRAMMENOS SET ar_diplomatos =%s WHERE username=%s and password=%s" %("'"+new_ar_dipl+"'","'"+USERNAME+"'","'"+PASSWORD+"'")
                c.execute(sql)
                global data
                data=(data[0],data[1],data[2],data[3],data[4],new_ar_dipl,data[6],data[7],data[8])            
                self.close()
            else:
                msg.setText('Λανθασμένος κωδικός.')
                msg.exec_()
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()

#Αλλαγή Τηλεφώνου χρήστη
class Change_Phone_Window(QDialog):
    def __init__(self,parent=None):
        super(Change_Phone_Window,self).__init__(parent)

        layout=QGridLayout()
        layout.setRowMinimumHeight(3,55)
        self.setWindowTitle('Αλλαγή Τηλεφώνου')
        self.mainlabel=QLabel('<h4> Αλλαγή Τηλεφώνου </h4>')
        layout.addWidget(self.mainlabel,0,0)

        #Πεδίο παλιού τηλεφώνου χρήστη
        self.lbl_old=QLabel('<p style="font-size:16px;">Παλιό τηλέφωνο</p>')
        layout.addWidget(self.lbl_old,1,0)
        self.old_phone=QLineEdit(self)
        self.old_phone.setReadOnly(True)
        self.old_phone.setStyleSheet("font-size:16px;")
        self.old_phone.setText(data[6])
        layout.addWidget(self.old_phone,2,0)

        #Πεδίο καινούριου τηλεφώνου χρήστη
        self.lbl_new=QLabel('<p style="font-size:16px;">Καινούριο τηλέφωνο</p>')
        layout.addWidget(self.lbl_new,3,0)
        self.new_phone=QLineEdit(self)
        self.new_phone.setStyleSheet("font-size:16px;")
        layout.addWidget(self.new_phone,4,0)
        self.new_phone.textChanged.connect(lambda : self.new_phone.setText(self.new_phone.text()))
        
        #Regular Expression για το τηλέφωνο. 
        #Επιτρέπεται να ξεκινάει μόνο από 69 και να ακολουθούν 8 ακόμη αριθμοί.
        reg_ex=QRegExp( r'^(69(\d{8})(?:\s|$))')
        input_validator = QtGui.QRegExpValidator(reg_ex, self.new_phone)
        self.new_phone.setValidator(input_validator)

        #Εισαγωγή κωδικού χρήστη
        self.lbl_pass=QLabel('Password',self)
        layout.addWidget(self.lbl_pass,5,0)
        self.password=QLineEdit(self)
        self.password.setStyleSheet("font-size:15px;")
        layout.addWidget(self.password,6,0)
        self.password.textChanged.connect(lambda : self.password.setText(self.password.text()))
        self.Done=QPushButton('Τέλος',self)
        self.Done.setStyleSheet("font-size:15px;")
        layout.addWidget(self.Done,7,0)

        #Ακύρωση της διαδικασίας αλλαγής στοιχείων χρήστη.
        self.Cancel=QPushButton('Ακύρωση',self)
        self.Cancel.setStyleSheet("font-size:15px;")
        layout.addWidget(self.Cancel,8,0)
    
        #Με την επιλογή του κουμπιού "Τέλος" καλείται η συνάρτηση Αναβάθμισης των δεδομένων της βάσης με τα καινούρια εισαχθέντα στοιχεία χρήστη.
        self.Done.clicked.connect(self.Changed)

        self.setLayout(layout)
        self.setStyleSheet('font-size: 30 px')
        self.setFixedSize(400,400)
        self.show()
    
    #Αναβάθμιση της βάσης δεδομένων με τα καινούρια εισαχθέντα στοιχεία χρήστη.  
    def Changed(self):
        try:
            msg=QMessageBox()
            new_phone=self.new_phone.text()
            #Έλεγχος κωδικού πρόσβασης.
            if self.password.text()==PASSWORD:
                msg.setText('Το τηλέφωνό σας άλλαξε.')
                msg.exec_()
                sql="UPDATE EGGEGRAMMENOS SET thl =%s WHERE username=%s and password=%s" %("'"+new_phone+"'","'"+USERNAME+"'","'"+PASSWORD+"'")
                c.execute(sql)
                global data
                data=(data[0],data[1],data[2],data[3],data[4],data[5],new_phone,data[7],data[8])            
                
                self.close()
            else:
                msg.setText('Λανθασμένος κωδικός.')
                msg.exec_()
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()

#Αλλαγή Email χρήστη  
class Change_Email_Window(QDialog):
    def __init__(self,parent=None):
        super(Change_Email_Window,self).__init__(parent)
        
        layout=QGridLayout()
        layout.setRowMinimumHeight(3,55)
        self.setWindowTitle('Αλλαγή Email')
        self.mainlabel=QLabel('<h4> Αλλαγή Email </h4>')
        layout.addWidget(self.mainlabel,0,0)

        #Πεδίο εισαγωγής παλιού email χρήστη
        self.lbl_old=QLabel('<p style="font-size:16px;">Παλιό Email</p>')
        layout.addWidget(self.lbl_old,1,0)
        self.old_email=QLineEdit(self)
        self.old_email.setReadOnly(True)
        self.old_email.setStyleSheet("font-size:16px;")
        self.old_email.setText(data[7])
        layout.addWidget(self.old_email,2,0)

        #Πεδίο εισαγωγής καινούριου email χρήστη
        self.lbl_new=QLabel('<p style="font-size:16px;">Καινούριο Email</p>')
        layout.addWidget(self.lbl_new,3,0)
        self.new_email=QLineEdit(self)
        self.new_email.setStyleSheet("font-size:16px;")
        layout.addWidget(self.new_email,4,0)
        
        self.new_email.textChanged.connect(lambda : self.new_email.setText(self.new_email.text()))
       
        #Regular Expression για το email χρήστη.
        #Επιτρέπονται οποιαδήποτε αλφαριθμητικά οποιουδήποτε μήκους που να ακολουθούνται από τον χαρακτήρα '@' και να ακολουθεί αλφαριθμητικό.
        reg_ex=QRegExp(r'\S+@\S+')
        input_validator = QtGui.QRegExpValidator(reg_ex, self.new_email)
        self.new_email.setValidator(input_validator)

        #Εισαγωγή κωδικού χρήστη
        self.lbl_pass=QLabel('Password',self)
        layout.addWidget(self.lbl_pass,5,0)
        self.password=QLineEdit(self)
        layout.addWidget(self.password,6,0)
        self.password.textChanged.connect(lambda : self.password.setText(self.password.text()))

        self.Done=QPushButton('Τέλος',self)
        self.Done.setStyleSheet("font-size:15px;")
        layout.addWidget(self.Done,7,0)

        #Ακύρωση της διαδικασίας αλλαγής στοιχείων χρήστη.
        self.Cancel=QPushButton('Ακύρωση',self)
        self.Cancel.setStyleSheet("font-size:15px;")
        layout.addWidget(self.Cancel,8,0)
    
        #Με την επιλογή του κουμπιού "Τέλος" καλείται η συνάρτηση Αναβάθμισης των δεδομένων της βάσης με τα καινούρια εισαχθέντα στοιχεία χρήστη.
        self.Done.clicked.connect(self.Changed)

        self.setLayout(layout)
        self.setStyleSheet('font-size: 30 px')
        self.setFixedSize(400,400)
        self.show()
    
    #Αναβάθμιση της βάσης δεδομένων με τα καινούρια εισαχθέντα στοιχεία χρήστη.  
    def Changed(self):
        try:
            msg=QMessageBox()
            new_email=self.new_email.text()
            #Έλεγχος κωδικού πρόσβασης.
            if self.password.text()==PASSWORD:
                msg.setText('Το email σας άλλαξε.')
                msg.exec_()
                sql="UPDATE EGGEGRAMMENOS SET email =%s WHERE username=%s and password=%s" %("'"+new_email+"'","'"+USERNAME+"'","'"+PASSWORD+"'")
                c.execute(sql)
                global data
                data=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],new_email,data[8])            
                self.close()
            else:
                msg.setText('Λανθασμένος κωδικός.')
                msg.exec_()
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()

#Αλλαγή Διεύθυνσης χρήστη
class Change_Dieuthinsh_Window(QDialog):
    def __init__(self,parent=None):
        super(Change_Dieuthinsh_Window,self).__init__(parent)
        
        layout=QGridLayout()
        layout.setRowMinimumHeight(3,55)
        self.setWindowTitle('Αλλαγή Διεύθυνσης')
        self.mainlabel=QLabel('<h4> Αλλαγή Διεύθυνσης </h4>')
        layout.addWidget(self.mainlabel,0,0)
        self.lbl_poli=QLabel('<p style="font-size:16px;">Πόλη</p>')
        layout.addWidget(self.lbl_poli,1,0)

        #Πεδίο εισαγωγής παλιάς πόλης χρήστη
        self.poli=QLineEdit(self)
        self.poli.setReadOnly(True)
        self.poli.setStyleSheet("font-size:16px;")
        self.poli.setText(data[8][1])
        layout.addWidget(self.poli,2,0)
        self.poli.textChanged.connect(lambda : self.poli.setText(self.poli.text()))
        self.lbl_odos=QLabel('<p style="font-size:16px;">Οδός</p>')
        layout.addWidget(self.lbl_odos,3,0)

        #Πεδίο εισαγωγής παλιάς οδού χρήστη
        self.odos=QLineEdit(self)
        self.odos.setStyleSheet("font-size:16px;")
        self.odos.setText(str(data[8][2]))
        layout.addWidget(self.odos,4,0)
        self.odos.textChanged.connect(lambda : self.odos.setText(self.odos.text()))
        self.lbl_ar=QLabel('<p style="font-size:16px;">Αριθμός</p>')
        layout.addWidget(self.lbl_ar,5,0)

        #Πεδίο εισαγωγής παλιού αριθμού διεύθυνσης χρήστη
        self.ar=QLineEdit(self)
        self.ar.setStyleSheet("font-size:16px;")
        self.ar.setText(str(data[8][3]))
        layout.addWidget(self.ar,6,0)
        self.ar.textChanged.connect(lambda : self.ar.setText(self.ar.text()))
        self.lbl_TK=QLabel('<p style="font-size:16px;">TK</p>')
        layout.addWidget(self.lbl_TK,7,0)

        #Πεδίο εισαγωγής παλιού ΤΚ πόλης χρήστη
        self.TK=QLineEdit(self)
        self.TK.setStyleSheet("font-size:16px;")
        self.TK.setText(data[8][0])
        layout.addWidget(self.TK,8,0)
        self.TK.textChanged.connect(lambda : self.TK.setText(self.TK.text()))
        
        #Πεδίο εισαγωγής κωδικού χρήστη
        self.lbl_pass=QLabel('Password',self)
        layout.addWidget(self.lbl_pass,9,0)
        self.password=QLineEdit(self)
        self.password.setStyleSheet("font-size:16px;")
        layout.addWidget(self.password,10,0)
        self.password.textChanged.connect(lambda : self.password.setText(self.password.text()))
        self.Done=QPushButton('Τέλος',self)
        self.Done.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Done,11,0)

        #Ακύρωση της διαδικασίας αλλαγής στοιχείων χρήστη.
        self.Cancel=QPushButton('Ακύρωση',self)
        self.Cancel.setStyleSheet("font-size:16px;")
        layout.addWidget(self.Cancel,12,0)

        #Με την επιλογή του κουμπιού "Τέλος" καλείται η συνάρτηση Αναβάθμισης των δεδομένων της βάσης με τα καινούρια εισαχθέντα στοιχεία χρήστη.
        self.Done.clicked.connect(self.Changed)

        self.setLayout(layout)
        self.setFixedSize(400,400)
        self.show()
    
    #Αναβάθμιση της βάσης δεδομένων με τα καινούρια εισαχθέντα στοιχεία χρήστη.  
    def Changed(self):
        try:
            msg=QMessageBox()
            TK=self.TK.text()
            poli=self.poli.text()
            odos=self.odos.text()
            arithmos=self.ar.text()
            #Έλεγχος κωδικού πρόσβασης
            if self.password.text()==PASSWORD:
                if arithmos.isdigit():
                    msg.setText('Η διέυθυνσή σας άλλαξε.')
                    msg.exec_()
                    sql="UPDATE DIEUTHINSH SET TK=%s, poli=%s, odos=%s,arithmos=%s WHERE username=%s" %("'"+TK+"'","'"+poli+"'","'"+odos+"'","'"+arithmos+"'","'"+USERNAME+"'")
                    c.execute(sql)
                    global data
                    data=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],[TK,poli,odos,arithmos])
                    self.close()
                else:
                    msg.setText('Δώστε αριθμό διεύθυνσης.')
                    msg.exec_()
            else:
                msg.setText('Λανθασμένος κωδικός.')
                msg.exec_()
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()

#ΚΑΙΝΟΥΡΙΑ ΚΡΑΤΗΣΗ      
class New_Krathsh_Window(QWidget):   

    ok=pyqtSignal()

    def __init__(self,parent=None):
        super(New_Krathsh_Window,self).__init__(parent)

        v=QVBoxLayout()
        self.main_lbl=QLabel('<h2 style="text-align:center;font-size:30px;"> Καινούρια Κράτηση </h2>',self)
        v.addWidget(self.main_lbl)

        self.lbl1=QLabel('<p style="text-align:center;font-size:20px"> Εισάγετε κοντινή περιοχή παραλαβής αυτοκινήτου</p>')
        v.addWidget(self.lbl1)
        self.topothesia=QComboBox(self)

        self.lbl2=QLabel('<p style="text-align:center;font-size:20px"> Εισάγετε κοντινή περιοχή επιστροφής αυτοκινήτου</p>')
        self.topothesia_ep = QComboBox(self)
      
        #Αναζήτηση περιοχών Σταθμών.
        c.execute('SELECT perioxh FROM STATHMOS')
        rows=c.fetchall()
        for i in rows:
            self.topothesia.addItems([str(i[0])])
            self.topothesia_ep.addItems([str(i[0])])
        
        #Εμφάνιση αποτελεσμάτων αναζήτησης: περιοχές Σταθμών.
        #Δυνατότητα επιλογής τοποθεσίας παραλαβής και επιστροφής οχήματος βάσει των αποτελεσμάτων αναζήτησης.
        index = self.topothesia.findText(krathsh[0], QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.topothesia.setCurrentIndex(index)

        self.topothesia.setStyleSheet("text-align:center;margin-left:150px;margin-right:150px;font-size:16px;")
        self.topothesia_ep.setStyleSheet("text-align:center;margin-left:150px;margin-right:150px;font-size:16px;")
        v.addWidget(self.topothesia)
        v.addWidget(self.lbl2)
        v.addWidget(self.topothesia_ep)

        h=QHBoxLayout()
        vbox1=QVBoxLayout()
        vbox2=QVBoxLayout()

        #Πεδία εισαγωγής ημερομηνιών παραλαβής και επιστροφής οχήματος
        self.lbldate1=QLabel('Ημερομηνία Παραλαβής',self)
        self.lbldate1.setStyleSheet("font-size:16px;text-align:center")
        self.im_paralavhs=QtWidgets.QDateEdit(calendarPopup=True)
        self.im_paralavhs.setDateTime(QtCore.QDateTime.currentDateTime())
        self.im_paralavhs.setStyleSheet("font-size:16px;")
        self.im_paralavhs.setFixedSize(200,35)
        vbox1.addWidget(self.lbldate1)
        vbox1.addWidget(self.im_paralavhs)
        self.lbldate2=QLabel('Ημερομηνία Επιστροφής',self)
        self.lbldate2.setStyleSheet("font-size:16px;text-align:center")
        vbox2.addWidget(self.lbldate2)
        
        self.im_epistrofhs=QtWidgets.QDateEdit(calendarPopup=True)
        self.im_epistrofhs.setDateTime(QtCore.QDateTime.currentDateTime())
        self.im_epistrofhs.setStyleSheet("font-size:16px;")
        self.im_epistrofhs.setFixedSize(200,35)
        vbox2.addWidget(self.im_epistrofhs)
        
        h.addLayout(vbox1)
        h.addLayout(vbox2)
        v.addLayout(h)

        #Μετάβαση στην επιλογή Κλάσης Οχήματος.
        self.next=QPushButton('Επόμενο',self)
        self.next.setStyleSheet(" margin-top:40px;margin-left:120px;margin-right:120px;margin-bottom:10px;font-size:15px;text-align:center")
        v.addWidget(self.next)
        self.go_back=QPushButton('Ακύρωση',self)
        self.go_back.setStyleSheet(" margin-left:120px;margin-right:120px;margin-bottom:10px;font-size:15px;text-align:center")
        v.addWidget(self.go_back)
        self.setLayout(v)
        #self.setFixedSize(500,500)
        self.setStyleSheet('font-size: 30 px')
        self.show()

    #Έλεγχος ημερομηνιών παραλαβής και επιστροφής οχήματος.
    def Check_Dates(self):
        msg=QMessageBox()
        date1=self.im_paralavhs.text()
        date2=self.im_epistrofhs.text()
        date11=date1[0:len(date1)-4]+date1[len(date1)-2:len(date1)]
        date22=date2[0:len(date2)-4]+date2[len(date2)-2:len(date2)]
        self.d1=datetime.datetime.strptime(date11,"%m/%d/%y")
        self.d2=datetime.datetime.strptime(date22,"%m/%d/%y")
        krathsh[1]=self.d1
        krathsh[2]=self.d2
        today = time.strftime("%m/%d/%y")
        today1=datetime.datetime.strptime(today,"%m/%d/%y")
        #Έλεγχος για το αν η σημερινή ημερομηνία είναι μεγαλύτερη της ημερομηνίας παραλαβής και αν η ημερομηνία παραλαβής είναι μικρότερη της ημερομηνίας επιστροφής.
        if today1>self.d1 or self.d1>self.d2:
            msg.setText('Εισάγετε έγκυρες ημερομηνίες')
            msg.exec_()
        else:
            self.Check_Diathesimes_Klaseis() 


    #ΑΝΑΖΗΤΗΣΗ ΔΙΑΘΕΣΙΜΩΝ ΚΛΑΣΕΩΝ ΟΧΗΜΑΤΩΝ
    def Check_Diathesimes_Klaseis(self):
        topothesia=self.topothesia.currentText()
        d1=str(self.d1)
        d2=str(self.d2)

        #Αναζήτηση αριθμού κατειλημμένων οχημάτων κατηγοριοποιημένα βάσει της κλάσης οχήματος για τη χρονική περίοδο: ημερομηνία παραλαβής-ημερομηνία επιτροφής.
        c.execute("SELECT KLASH_OXHMATOS.typos_oxhmatos,COUNT(*) FROM KRATHSH,AFORA,KLASH_OXHMATOS WHERE KRATHSH.topothesia=%s AND ((KRATHSH.im_paralavhs<=%s AND KRATHSH.im_epistrofhs>=%s) OR (KRATHSH.im_paralavhs>=%s AND KRATHSH.im_epistrofhs<=%s )OR (KRATHSH.im_paralavhs<=%s AND KRATHSH.im_epistrofhs>=%s))AND KRATHSH.ar_krathshs=AFORA.ar_krathshs AND AFORA.typos_oxhmatos=KLASH_OXHMATOS.typos_oxhmatos GROUP BY KLASH_OXHMATOS.typos_oxhmatos"%("'"+topothesia+"'","'"+d1+"'","'"+d2+"'","'"+d1+"'","'"+d2+"'","'"+d2+"'","'"+d2+"'"))
        self.rended_cars=c.fetchall()
        #Αναζήτηση όλων των οχημάτων της βάσης δεδομένων κατηγοριοποιημένα βάσει της κλάσης οχήματος .
        sql ="""SELECT KLASH_OXHMATOS.typos_oxhmatos,COUNT(*) FROM OXHMA,KLASH_OXHMATOS,STATHMOS,DIATITHETAI 
        WHERE STATHMOS.perioxh='%s' AND STATHMOS.kod_stathmou=DIATITHETAI.kod_stathmou AND DIATITHETAI.ar_pinakidas=OXHMA.ar_pinakidas 
        AND OXHMA.typos_oxhmatos=KLASH_OXHMATOS.typos_oxhmatos GROUP BY KLASH_OXHMATOS.typos_oxhmatos""" % (topothesia)
        c.execute(sql)
        self.all_cars_in_klash=c.fetchall()
        
        #Δημιουργία λίστας διαθέσιμων κλάσεων οχημάτων
        self.diathesimes_klaseis=list()
        for i in range(0, len(self.rended_cars)):
            for j in range(0, len(self.all_cars_in_klash)):
                #Έλεγχος σε κάθε κλάση των κατειλλημένων οχημάτων για το αν ο αριθμός τους είναι μικρότερος από τον συνολικό αριθμό αυτών.
                #Αν ναι: εισάγουμε στις διαθέσιμες κλάσεις την συγκεκριμένη κλάση οχήματος.
                if self.rended_cars[i][0]==self.all_cars_in_klash[j][0] and self.rended_cars[i][1]<self.all_cars_in_klash[j][1]:
                    self.diathesimes_klaseis.append(str(self.rended_cars[i][0]))
        
        #Εισαγωγή στη λίστα των διαθέσιμων κλάσεων όλες τις κλάσεις που δεν είναι κατειλημμένες.
        for i in range(len(self.rended_cars),len(self.all_cars_in_klash)):
            for j in range(0,len(self.all_cars_in_klash)):
                if self.all_cars_in_klash[j][0] not in self.diathesimes_klaseis and self.all_cars_in_klash[j] not in self.rended_cars:
                    self.diathesimes_klaseis.append(self.all_cars_in_klash[j][0])
        
        #Έλεγχος για το αν όλες οι κλάσεις οχημάτων είναι κατειλημμένες και ακύρωση της δυνατότητας επιλογής κλάσης οχήματος και κατά συνέπεια της κράτησης.
        if self.diathesimes_klaseis==[]:
            msg=QMessageBox()
            msg.setText('Δεν υπάρχουν διαθέσιμες κλάσεις για αυτή τη χρονική περίοδο.')
            msg.exec_()
        else:
            self.ok.emit()

    #Δεδομένα ημερομηνιών και τοποθεσίας που θα χρησιμοποιηθούν στο τελικό στάδιο της πληρωμής και της εισαγωγής των δεδομένων κράτησης στη βάση.
    def final_selection(self):
        self.place = str(self.topothesia.currentText())
        self.end_place = str(self.topothesia_ep.currentText())
        self.start_date = self.im_paralavhs.date().toPyDate()
        self.end_date = self.im_epistrofhs.date().toPyDate()
        
#Επιλογή κλάσης οχήματος
class Select_Klash(QWidget):

    trigger=pyqtSignal()

    def __init__(self,parent=None):
        super(Select_Klash,self).__init__(parent)
   
        self.vlayout1=QVBoxLayout()
      
        self.lbl1=QLabel('<p style="text-align:center;margin-bottom:20px;font-size:30px;"> Επιλέξτε Kλάση Oχήματος </p>',self)
        self.vlayout1.addWidget(self.lbl1)
        self.lbl2=QLabel('',self)
        self.vlayout1.addWidget(self.lbl2)
        self.hlayout2=QHBoxLayout()
        
        #Πεδία εισαγωγής λίστας διαθέσιμων κλάσεων και φωτογραφίας οχήματος που ανήκει σε αυτήν.
        self.klash=QListWidget(self)

        self.hlayout2.addWidget(self.klash)       
       
        self.photo = QLabel(self)
        self.photo.setFixedSize(50,50)
        self.hlayout2.addWidget(self.photo)
        self.vlayout1.addLayout(self.hlayout2)

        self.lbl3=QLabel('',self)
        self.vlayout1.addWidget(self.lbl3)
        self.lbl4=QLabel('',self)
        self.vlayout1.addWidget(self.lbl4)
        self.lbl5=QLabel('',self)
        self.vlayout1.addWidget(self.lbl5)
        self.lbl6=QLabel('',self)
        self.vlayout1.addWidget(self.lbl6)
        self.lbl7=QLabel('',self)
        self.vlayout1.addWidget(self.lbl7)
##        self.lbl8=QLabel('',self)
##        self.vlayout1.addWidget(self.lbl8)
##        self.lbl9=QLabel('',self)
##        self.vlayout1.addWidget(self.lbl9)
##        self.lbl10=QLabel('',self)
##        self.vlayout1.ad
        
        self.next=QPushButton('Επόμενο',self)
        self.next.setStyleSheet(" font-size:15px;text-align:center")

        #Πίσω στην επιλογή ημερομηνιών και τοποθεσίας κράτησης.
        self.vlayout1.addWidget(self.next)
        self.go_back=QPushButton('Πίσω',self)
        self.go_back.setStyleSheet("font-size:15px;text-align:center")
        self.vlayout1.addWidget(self.go_back)

        #Ακύρωση κράτησης.
        self.cancel=QPushButton('Ακύρωση',self)
        self.cancel.setStyleSheet("margin-left:150px;margin-right:150px;margin-bottom:10px;font-size:15px;text-align:center")
        self.vlayout1.addWidget(self.cancel)
        
        self.setLayout(self.vlayout1)
        #self.setFixedSize(700,900)
        self.setGeometry(400,0,800,800)
        self.setStyleSheet('text-align:center;font-size: 30 px')
        self.show()

    #Προβολή της λίστας των διαθέσιμων κλάσεων οχημάτων.
    def Show_Diathesimes_Klaseis(self,data,diathesimes_klaseis):
        self.diathesimes_klaseis=diathesimes_klaseis
        d1=str(data[1]).split(' ')[0]
        d2=str(data[2]).split(' ')[0]
        self.lbl2.setText('<p style="text-align:center; font-size:21px;"> Διαθεσιμότητα κοντά στην '+str(data[0])+'</p><br><p style="text-align:center; font-size:20px;">Για τις Ημερομηνίες '+str(d1)+' και '+str(d2)+'</p>')
        for i in diathesimes_klaseis:
            self.klash.addItems([str(i)])

        self.klash.clicked.connect(self.Select_Klash_photo)
        self.klash.setFixedSize(self.klash.sizeHintForColumn(0) + 15 * self.klash.frameWidth(), self.klash.sizeHintForRow(0) * self.klash.count() + 7.5 * self.klash.frameWidth())        
        
    #Προβολή της φωτογραφίας οχήματος που ανήκει σε αυτήν την κλάση με url λίνκ.
    def Select_Klash_photo(self):
        c.execute("SELECT KLASH_OXHMATOS.typos_oxhmatos,photo FROM OXHMA,KLASH_OXHMATOS WHERE OXHMA.typos_oxhmatos=KLASH_OXHMATOS.typos_oxhmatos GROUP BY KLASH_OXHMATOS.typos_oxhmatos")
        self.photos=c.fetchall()
        for item in self.klash.selectedItems():
            for i in self.diathesimes_klaseis:
                if item.text()==i:
                    data=i
                    break
            url=''
            for j in self.photos:
                print(j,data)
                if j[0]==data:
                    url=j[1]
                    break
            print(url)
            image = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            pixmap_resized = pixmap.scaled(400,400, QtCore.Qt.KeepAspectRatio)
            self.photo.setPixmap(pixmap_resized) 
            self.photo.setFixedSize(400,400)

            #Προβολή στοιχείων περιγραφής κλάσης οχήματος.
            c.execute('SELECT KLASH_OXHMATOS.typos_oxhmatos,timh,ar_thesewn FROM KLASH_OXHMATOS,OXHMA WHERE KLASH_OXHMATOS.typos_oxhmatos=%s AND OXHMA.typos_oxhmatos=KLASH_OXHMATOS.typos_oxhmatos'%("'"+str(i)+"'"))
            rows=c.fetchall()
            self.lbl4.setText('<h3 style="font-size:20px; text-align:center"> Περιγραφή Κλάσης Οχήματος </h3>')
            self.lbl5.setText('<p style="font-size:17px; text-align:center">Τύπος Οχήματος: '+str(rows[0][0])+'</p>')
            self.lbl6.setText('<p style="font-size:17px; text-align:center">Τιμή: '+str(rows[0][1])+'</p>')
            self.lbl7.setText('<p style="font-size:17px; text-align:center">Αριθμός θέσεων: '+str(rows[0][2])+'</p>')
            
        global krathsh
        krathsh[3]=item.text()
    
    #Δεδομένα κλάσης οχήματος που θα χρησιμοποιηθούν στο τελικό στάδιο της πληρωμής και της εισαγωγής των δεδομένων κράτησης στη βάση.
    def final_selection(self):
        self.car_class='None'
        msg=QMessageBox()
        for item in self.klash.selectedItems():
            self.car_class = item.text()
            sql = "SELECT typos_oxhmatos,timh FROM KLASH_OXHMATOS WHERE typos_oxhmatos='%s'" % (self.car_class)
            c.execute(sql)
            rows = c.fetchall()
            self.kod_klashs = rows[0][0]
            self.cost = rows[0][1]

        if self.car_class=='None':
            msg.setText('Επιλέξτε Κλάση Οχήματος')
            msg.exec_()
        else:
            self.trigger.emit()
    
#Επιλογή Υπηρεσιών κράτησης
class Select_Yphresies(QWidget):   
    def __init__(self,parent=None):
        super(Select_Yphresies,self).__init__(parent)

        self.services=[]

        layout=QVBoxLayout()
        self.lbl1=QLabel("<h1 style='text-align:center'> Επιλέξτε Υπηρεσίες </h1>",self)
        self.lbl1.setStyleSheet('margin:20px;margin-bottom:50px;')
        layout.addWidget(self.lbl1)

        #Λίστα με τις υπηρεσίες που προσφέρει η εταιρεία. 
        self.packets = QComboBox(self)
        self.packets.setStyleSheet('font-size:16px;margin-bottom:100px')
        
        #Πεδία εισαγωγής περιγραφής της κάθε Υπηρεσίας.
        self.lbl_title = QLabel('<p style="font-size:20px; text-align:center"> Τίτλος </p>',self)
        self.lbl_desc = QLabel('<p style="font-size:20px; text-align:center"> Περιγραφή </p>',self)
        self.lbl_price = QLabel('<p style="font-size:20px; text-align:center"> Κόστος </p>',self)
        self.lbl_title_text = QLabel('',self)
        self.lbl_title_text.setStyleSheet('text-align:center;')
        self.lbl_desc_text = QLabel('',self)
        self.lbl_desc_text.setStyleSheet('text-align:center;')
        self.lbl_price_text = QLabel('')
        self.lbl_price_text.setStyleSheet('text-align:center;')

        vert_1 = QVBoxLayout()
        vert_1.addWidget(self.lbl_title)
        vert_1.addWidget(self.lbl_title_text)
        vert_1.addWidget(self.lbl_desc)
        vert_1.addWidget(self.lbl_desc_text)
        vert_1.addWidget(self.lbl_price)
        vert_1.addWidget(self.lbl_price_text)
        hor_1 = QVBoxLayout()
        hor_1.addWidget(self.packets)
        hor_1.addLayout(vert_1)
        layout.addLayout(hor_1)
        layout.addStretch(1)

        #Απαραίτητη επιλογή "Προσθήκη στο καλάθι" για την επιλογή μίας ή και περισσότερων υπηρεσιών.
        self.cart = QPushButton('Προσθήκη στο καλάθι',self)
        self.cart.setStyleSheet('margin-top:40px;margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:16px;color:black;background-color:yellow')
        layout.addWidget(self.cart)
        
        #Μετάβαση σε επιλογή Πακέτου Κάλυψης.
        self.next=QPushButton('Επόμενο',self)
        self.next.setStyleSheet("margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:15px;text-align:center")
        layout.addWidget(self.next)

        #Πίσω σε επιλογή διαθέσιμης κλάσης οχήματος
        self.go_back=QPushButton('Πίσω',self)
        self.go_back.setStyleSheet("margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:15px;text-align:center")
        layout.addWidget(self.go_back)

        #Ακύρωση κράτησης
        self.cancel=QPushButton('Ακύρωση',self)
        self.cancel.setStyleSheet("margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:15px;text-align:center")
        layout.addWidget(self.cancel)
        
        #Αναζήτηση των υπηρεσιών στη βάση και εισαγωγή τους στη λίστα.
        c.execute("SELECT titlos FROM YPHRESIES")
        db_data = c.fetchall()
        for i in db_data:
            self.packets.addItem(str(i[0]))
        
        self.set_labels()

        self.packets.currentTextChanged.connect(lambda : self.set_labels())
        self.setLayout(layout)
        # self.setFixedSize(1300,900)
        self.setStyleSheet('text-align:center;font-size: 30 px')
        #vlayout1.setContentsMargins(-1,0,-1,-1)
        self.show()

    #Για κάθε επιλεγμένη Υπηρεσία προβάλλεται η κάθε της περιγραφή.Ο χρήστης πρέπει οπωσδήποτε να επιλέξει μια Υπηρεσία.
    def set_labels(self):
        title = str(self.packets.currentText())

        sql = "SELECT perigrafh,kostos FROM YPHRESIES WHERE titlos=%s" % ("'"+title+"'")
        c.execute(sql)
        try:
            db_data = c.fetchall()[0]
            
            self.lbl_title_text.setText('<p style="font-size:17px; text-align:center">'+str(title)+'</p>')
            self.lbl_desc_text.setText('<p style="font-size:17px; text-align:center">'+str(db_data[0])+'</p>')
            self.lbl_price_text.setText('<p style="font-size:17px; text-align:center">'+str(db_data[1])+'</p>')
        except:
            self.lbl_title_text.setText('')
            self.lbl_desc_text.setText('')
            self.lbl_price_text.setText('')

    #Έλεγχος για τις διαθέσιμες υπηρεσίες, αν τις έχει επιλέξει όλες ή όχι ο χρήστης.
    def selection(self):
        msg=QMessageBox()
        title = self.packets.currentText()
        if title=='':
            msg.setText('Έχετε επιλέξει όλες τις υπηρεσίες')
            msg.exec_()
        else:
            sql = "SELECT kostos FROM YPHRESIES WHERE titlos='%s'" % (title)
            c.execute(sql)
            data = c.fetchall()
            kod_yphresias = title
            cost = data[0][0]
            self.services.append([title,cost])
            index = self.packets.findText(title)
            self.packets.removeItem(index)

#Επιλογή Πακέτου Κάλυψης.
class Select_Paketa(QWidget):
    def __init__(self,parent=None):
        super(Select_Paketa,self).__init__(parent)

        
        layout=QVBoxLayout()
        self.lbl1=QLabel('<h1 style="font-size:20px; text-align:center"> Επιλέξτε Πακέτα Κάλυψης </h1>',self)
        self.lbl1.setStyleSheet('margin:20px;margin-bottom:50px;')
        layout.addWidget(self.lbl1)

        #Λίστα Πακέτων Κάλυψης.
        self.packets = QComboBox(self) 
        self.packets.setStyleSheet('font-size:16px;margin-bottom:100px')        
        layout.addWidget(self.packets)

        #Προβολή στοιχείων περιγραφής για κάθε Πακέτο Κάλυψης.
        self.lbl_title = QLabel('<p style="font-size:20px; text-align:center"> Τίτλος </p>',self)
        self.lbl_desc = QLabel('<p style="font-size:20px; text-align:center"> Περιγραφή </p>',self)
        self.lbl_price = QLabel('<p style="font-size:20px; text-align:center"> Κόστος </p>',self)
        self.lbl_title_text = QLabel('',self)
        self.lbl_title_text.setStyleSheet('text-align:center;')
        self.lbl_desc_text = QLabel('',self)
        self.lbl_desc_text.setStyleSheet('text-align:center;')
        self.lbl_price_text = QLabel('')
        self.lbl_price_text.setStyleSheet('text-align:center;')

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_title_text)
        layout.addWidget(self.lbl_desc)
        layout.addWidget(self.lbl_desc_text)
        layout.addWidget(self.lbl_price)
        layout.addWidget(self.lbl_price_text)
        
        layout.addStretch(1)

        #Μετάβαση στην Πληρωμή.
        self.next=QPushButton('Επόμενο',self)
        self.next.setStyleSheet("margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:15px;text-align:center")
        layout.addWidget(self.next)

        #Πίσω στην πιλογή Υπηρεσιών
        self.go_back=QPushButton('Πίσω',self)
        self.go_back.setStyleSheet("margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:15px;text-align:center")
        layout.addWidget(self.go_back)

        #Ακύρωση κράτησης.
        self.cancel=QPushButton('Ακύρωση',self)
        self.cancel.setStyleSheet("margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:15px;text-align:center")
        layout.addWidget(self.cancel)

        c.execute("SELECT titlos FROM PAKETO_KALYPSHS")
        db_data = c.fetchall()
        
        #Εισαγωγή όλων των πακέτων κάλυψης από τη βάση δεδομένων στη λίστα.
        for i in db_data:
            self.packets.addItem(str(i[0]))
        self.packets.addItem("Κανένα επιλεγμένο")
    
        self.set_labels()
        self.packets.currentTextChanged.connect(lambda : self.set_labels())

        self.setLayout(layout)
        # self.setFixedSize(1300,900)
        self.setStyleSheet('text-align:center;font-size:30 px')
        self.show()

    #Προβολή των στοιχείων περιγραφής για κάθε επιλεγμένο Πακέτο Κάλυψης.Ο χρήστης μπορεί να μην επιλέξει κανένα πακέτο κάλυψης.
    def set_labels(self):
        title = str(self.packets.currentText())
        if title=="Κανένα επιλεγμένο":
            self.lbl_title_text.setText('')
            self.lbl_desc_text.setText('')
            self.lbl_price_text.setText('')
            return 0
        sql = "SELECT perigrafh,kostos FROM PAKETO_KALYPSHS WHERE titlos=%s" % ("'"+title+"'")
        c.execute(sql)
        db_data = c.fetchall()[0]
        self.lbl_title_text.setText('<p style="font-size:17px; text-align:center">'+str(title)+'</p>')
        self.lbl_desc_text.setText('<p style="font-size:17px; text-align:center">'+str(db_data[0])+'</p>')
        self.lbl_price_text.setText('<p style="font-size:17px; text-align:center">'+str(db_data[1])+'</p>')

    #Δεδομένα πακέτου κάλυψης που θα χρησιμοποιηθούν στο τελικό στάδιο της πληρωμής και της εισαγωγής των δεδομένων κράτησης στη βάση.
    def final_selection(self):
        try:
            self.title = str(self.packets.currentText())
            sql = "SELECT kostos FROM PAKETO_KALYPSHS WHERE titlos='%s'" % (self.title)
            c.execute(sql)
            data =c.fetchall()
            self.cost = data[0][0]
        except:
            self.title = 'Δεν επιλέξατε πακέτο κάλυψης'
            self.cost=0

#Πληρωμή
class Payment(QWidget):

    Done=pyqtSignal()
    trigger = pyqtSignal()
    def __init__(self,parent=None):
        super(Payment,self).__init__(parent)
        self.ver=None
        self.percent=0
        
        h_layout=QHBoxLayout()
        v_layout=QVBoxLayout()

        #Πεδία προβολής όλων των στοιχείων της κράτησης.
        self.lbl1=QLabel('<h1> Επισκόπηση </h1>',self)
        h_layout.addWidget(self.lbl1)
        self.lbl_place_title = QLabel('<p style="font-size:20px"> Τοποθεσία Ενοικίασης </p>',self)
        self.lbl_place = QLabel('place test',self)
        v_layout.addWidget(self.lbl_place_title)
        v_layout.addWidget(self.lbl_place)
        self.lbl_start_date_title = QLabel('<p style="font-size:20px"> Ημερομηνία Παραλαβής </p>',self)
        self.lbl_start_date = QLabel('start date test',self)
        v_layout.addWidget(self.lbl_start_date_title)
        v_layout.addWidget(self.lbl_start_date)
        self.lbl_end_date_title = QLabel('<p style="font-size:20px"> Ημερομηνία Επιστροφής </p>',self)
        self.lbl_end_date = QLabel('end date test',self)
        v_layout.addWidget(self.lbl_end_date_title)
        v_layout.addWidget(self.lbl_end_date)
        self.lbl_car_class_title = QLabel('<p style="font-size:20px"> Κλάση Οχήματος </p>',self)
        self.lbl_car_class = QLabel('class test',self)
        v_layout.addWidget(self.lbl_car_class_title)
        v_layout.addWidget(self.lbl_car_class)
        self.service_title = QLabel('<p style="font-size:20px"> Υπηρεσίες </p>',self)
        self.service = QLabel('service test',self)
        v_layout.addWidget(self.service_title)
        v_layout.addWidget(self.service)
        self.package_title = QLabel('<p style="font-size:20px"> Πακέτο Κάλυψης </p>',self)
        self.package = QLabel('package test',self)
        v_layout.addWidget(self.package_title)
        v_layout.addWidget(self.package)
        self.cost_title = QLabel('<p style="font-size:20px"> Τελική Τιμή </p>',self)
        self.cost = QLabel('cost test',self)
        v_layout.addWidget(self.cost_title)
        v_layout.addWidget(self.cost)
        h_layout.addLayout(v_layout)

        #Επιλογή Τρόπου Πληρωμής: 1)Μετρητά 2) Τιμολόγιο 3)Κάρτα
        self.payment_0 = QRadioButton(self)
        self.payment_0.setText('Μετρητά')
        self.payment_0.setStyleSheet('margin-top:20px; font-size:16px;')
        self.payment_1 = QRadioButton(self)
        self.payment_1.setText('Τιμολόγιο')
        self.payment_1.setStyleSheet('margin-top:20px; font-size:16px;')
        self.payment_2 = QRadioButton(self)
        self.payment_2.setStyleSheet('margin-top:20px; font-size:16px;')
        self.payment_2.setText('Κάρτα')

        fin_layout = QVBoxLayout()
        fin_layout.addLayout(h_layout)
        fin_layout.addStretch(1)

        #Δυνατότητα εισαγωγής κουπονιού έκπτωσης για έκπτωση στην τελική τιμή.
        self.dicount_lbl = QLabel('Εισάγετε τον αριθμό κουπονιού για να κερδίσετε έκπτωση!',self)
        self.dicount_lbl.setStyleSheet('font-size:16px;')
        
        #Έλεγχος εγκυρότητας κουπονιού έκπτωσης.
        self.check_discount = QPushButton('Έλεγχος κουπονιού',self)
        self.check_discount.setStyleSheet('margin-left:20px;margin-right:20px;font-size:16px;')
        self.discount = QLineEdit(self)
        self.discount.setStyleSheet('margin-left:100px;margin-right:100px;margin-bottom:30px;font-size:16px;')
        disc_v = QVBoxLayout()
        disc_h = QHBoxLayout()

        disc_h.addWidget(self.dicount_lbl)
        disc_h.addWidget(self.check_discount)
        disc_v.addLayout(disc_h)
        disc_v.addWidget(self.discount)

        fin_layout.addLayout(disc_v)

        ph_layout = QHBoxLayout()
        pv_layout = QVBoxLayout()

        self.cv_layout = QVBoxLayout()

        pv_layout.addWidget(self.payment_2)
        pv_layout.addWidget(self.payment_1)
        pv_layout.addWidget(self.payment_0)

        #By default είναι επιλεγμένος ο τρόπος πληρωμμής με κάρτα.
        self.payment_2.setChecked(True)

        #Πεδία εισαγωγής στοιχείων κάρτας. Εμφανίζονται μόνο όταν είναι επιλεγμένος ο τρόπος πληρωμής: Κάρτα.
        self.card_no = QLineEdit('Αριθμός Κάρτας',self)
        self.user = QLineEdit('Όνομα Κατόχου',self)
        self.date = QLineEdit('Ημερομηνία Λήξης (ΜΜ/ΕΕ)',self)

        self.cv_layout.addWidget(self.card_no)
        self.cv_layout.addWidget(self.user)
        self.cv_layout.addWidget(self.date)
    
        self.payment_0.toggled.connect(lambda: self.SetChecked0)
        self.payment_0.toggled.connect(self.clear)
        self.payment_1.toggled.connect(self.SetChecked1)
        self.payment_1.toggled.connect(self.clear)
        self.payment_2.toggled.connect(self.card_data)

        ph_layout.addLayout(pv_layout)
        ph_layout.addStretch(1)
        ph_layout.addLayout(self.cv_layout)
        ph_layout.addStretch(1)

        fin_layout.addLayout(ph_layout)
        fin_layout.addStretch(1)

        #Μετάβαση στην ολοκλήρωση της κράτησης
        self.next=QPushButton('Ολοκλήρωση Κράτησης',self)
        self.next.setStyleSheet("margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:15px;text-align:center")

        #Πίσω στην επιλογή Πακέτου Κάλυψης.
        fin_layout.addWidget(self.next)
        self.go_back=QPushButton('Πίσω',self)
        self.go_back.setStyleSheet("margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:15px;text-align:center")
        fin_layout.addWidget(self.go_back)

        #Ακύρωση Κράτησης
        self.cancel=QPushButton('Ακύρωση',self)
        self.cancel.setStyleSheet("margin-left:200px;margin-right:200px;margin-bottom:10px;font-size:15px;text-align:center")
        fin_layout.addWidget(self.cancel)

        self.setLayout(fin_layout)
        # self.setFixedSize(500,500)
        self.setStyleSheet('text-align:center;font-size: 30 px')
        self.show()

    def SetChecked0(self):
        self.payment_0.setChecked(True)
    def SetChecked1(self):
        self.payment_1.setChecked(True)

    #Εμφάνιση των πεδίων εισαγωγής στοιχείων κάρτας όταν είναι επιλεγμένος ο τροόπος πληρωμής: Κάρτα.
    def card_data(self):
        self.card_no = QLineEdit('Αριθμός Κάρτας',self)
        self.user = QLineEdit('Όνομα Κατόχου',self)
        self.date = QLineEdit('Ημερομηνία Λήξης (ΜΜ/ΕΕ)',self)

        self.cv_layout.addWidget(self.card_no)
        self.cv_layout.addWidget(self.user)
        self.cv_layout.addWidget(self.date)

    #Επικύρωση έκπτωσης 
    def verify_discount(self):
        self.code = self.discount.text()
        
        sql = "SELECT 1 FROM EKPTWSH WHERE kod_ekptwshs='%s'" % self.code
        c.execute(sql)
        self.ver = c.fetchone()
        if self.ver==None:
            self.discount.setStyleSheet("background: red;")
            self.percent=0
        else:
            self.discount.setStyleSheet("background: green;")

            sql = "SELECT pososto FROM EKPTWSH WHERE kod_ekptwshs='%s'" % self.code
            c.execute(sql)
            self.percent = c.fetchone()[0]/100

    #Εξαφάνιση πεδίων εισαγωγής στοιχείων κάρτας όταν δεν είναι επιλεγμένος ο τρόπος πληρωμής : Κάρτα.
    def clear(self):
        for i in reversed(range(self.cv_layout.count())): 
            layoutItem = self.cv_layout.itemAt(i)
            if layoutItem.widget() is not None:
                widgetToRemove = layoutItem.widget()
                widgetToRemove.hide()
                
    #Προβολή όλων των στοιχείων κράτησης στα αντίστοιχα πεδία βάσει των δεδομένων που ανακτήθηκαν από τις επιμέρους επιλογές σε κάθε στάδιο της κράτησης.
    def fill_data(self,data_tuple):
        self.data_tuple=data_tuple
        self.lbl_place.setText('<p style="font-size:17px">'+data_tuple[0]+' </p>')
        self.lbl_start_date.setText('<p style="font-size:17px">'+str(data_tuple[1])+' </p>')
        self.lbl_end_date.setText('<p style="font-size:17px">'+str(data_tuple[2])+' </p>')
        self.lbl_car_class.setText('<p style="font-size:17px">'+data_tuple[3]+' </p>')
        self.package.setText('<p style="font-size:17px">'+data_tuple[4]+' </p>')
        string=''
        
        if data_tuple[5]==[]:
            self.service.setText('<p style="font-size:17px"> Δεν επιλέξατε υπηρεσίες </p>')
        else:
            for i in data_tuple[5]:
                string = string+i[0]+'/'
                
            string = string[:-1]
            self.service.setText('<p style="font-size:17px">'+string+' </p>')
        self.cost.setText('<p style="font-size:17px">'+str(data_tuple[6]*(1-self.percent))+' </p>')

    #Έλεγχος εγκυρότητας των στοιχείων κάρτας.
    def check_card_info(self):
        if self.payment_2.isChecked() and (len(self.card_no.text())!=16 or self.user.text()=='' or self.user.text()=='Όνομα Κατόχου' or len(self.date.text())!=4):
            
            self.error_box = QMessageBox(self)
            self.error_box.setText('Παρακαλώ εισάγετε τα στοιχεία της κάρτας σας')
            self.error_box.exec_()
        else:
            self.trigger.emit()

    #Εισαγωγή όλων των δεδομένων της κράτησης στη βάση δεδομένων.
    def insert_reservation(self,data_tuple):
        reservation_info = (data_tuple[1],data_tuple[2],data_tuple[0],data_tuple[7])
        try:
            sql = "INSERT INTO KRATHSH(im_paralavhs,im_epistrofhs,topothesia,topothesia_ep) VALUES('%s','%s','%s','%s')" % reservation_info
            c.execute(sql)

            sql ="SELECT LAST_INSERT_ID()"
            c.execute(sql)
            key = c.fetchone()[0]
            sql = "INSERT INTO PRAGMATOPOIEI(username,ar_krathshs,im_krathshs) VALUES('%s','%s',SYSDATE())" % (USERNAME,key)
            c.execute(sql)
            
            for i in data_tuple[5]:
                sql = "INSERT INTO EPILEGEI(ar_krathshs,titlos_yphresias) VALUES('%s','%s')" % (key,i[0])
                c.execute(sql)
            
            sql = "INSERT INTO KALYPTETAI(titlos_paketou,ar_krathshs) VALUES('%s','%s')" % (data_tuple[4],key)
            c.execute(sql)

            if self.ver!=None:
                sql = "INSERT INTO PERIEXEI(ar_krathshs,kod_ekptwshs) VALUES('%s','%s')" % (key,self.code)
                c.execute(sql)
                data_tuple[6]=data_tuple[6]*(1-self.percent)

            if self.payment_0.isChecked()==True:
                sql = "INSERT INTO PLHRWMH(poso,tropos) VALUES('%s',0)" % data_tuple[6]
                c.execute(sql)
                sql = "SELECT LAST_INSERT_ID()"
                c.execute(sql)
                payment_key = c.fetchone()[0]

            elif self.payment_1.isChecked()==True:
                sql = "INSERT INTO PLHRWMH(poso,tropos) VALUES('%s',1)" % data_tuple[6]
                c.execute(sql)
                sql = "SELECT LAST_INSERT_ID()"
                c.execute(sql)
                payment_key = c.fetchone()[0]
            
            elif self.payment_2.isChecked()==True:
                sql = "INSERT INTO PLHRWMH(poso,tropos) VALUES('%s',2)" % data_tuple[6]
                c.execute(sql)
                sql = "SELECT LAST_INSERT_ID()"
                c.execute(sql)
                payment_key = c.fetchone()[0]
                sql = "INSERT INTO STOIXEIA_KARTAS(kod_plhr,ar_kartas,on_katoxou,im_lhkshs) VALUES('%s','%s','%s','%s')" % (payment_key,self.card_no.text(),self.user.text(),self.date.text())
                c.execute(sql)

            sql = "INSERT INTO PLHRWNEI(username,kod_plhr) VALUES('%s','%s')" % (USERNAME,payment_key)
            c.execute(sql)

            sql = "INSERT INTO EKSOFLEITAI(ar_krathshs,kod_plhr) VALUES('%s','%s')" % (key,payment_key)
            c.execute(sql)

            c.execute("SELECT OXHMA.ar_pinakidas FROM OXHMA WHERE OXHMA.typos_oxhmatos=%s"%("'"+self.data_tuple[3]+"'"))
            all_pinakides=c.fetchall()
            
            d1=data_tuple[8]
            d2=data_tuple[9]
            c.execute('SELECT OXHMA.ar_pinakidas FROM KRATHSH,AFORA,KLASH_OXHMATOS,AFORA_SYGKEKRIMENA,OXHMA WHERE KRATHSH.topothesia=%s AND ((KRATHSH.im_paralavhs<=%s AND KRATHSH.im_epistrofhs>=%s) OR (KRATHSH.im_paralavhs>=%s AND KRATHSH.im_epistrofhs<=%s )OR (KRATHSH.im_paralavhs<=%s AND KRATHSH.im_epistrofhs>=%s)) AND KRATHSH.ar_krathshs=AFORA.ar_krathshs AND AFORA.typos_oxhmatos=%s AND KRATHSH.ar_krathshs=AFORA_SYGKEKRIMENA.ar_krathshs AND AFORA_SYGKEKRIMENA.ar_pinakidas=OXHMA.ar_pinakidas GROUP BY OXHMA.ar_pinakidas'%("'"+str(data_tuple[2])+"'","'"+str(d1)+"'","'"+str(d2)+"'","'"+str(d1)+"'","'"+str(d2)+"'","'"+str(d2)+"'","'"+str(d2)+"'","'"+data_tuple[3]+"'"))
            self.rended_pinakides=c.fetchall()

            for i in range(0, len(self.rended_pinakides)):
                all_pinakides.remove(self.rended_pinakides[i])

            pinakida=str(random.choice(all_pinakides)[0])
            
            
            sql="INSERT INTO AFORA_SYGKEKRIMENA(ar_krathshs,ar_pinakidas, im_pragm_paralavhs,im_pragm_epistrofhs) VALUES('%s','%s',NULL,NULL)" %(key,pinakida) 
            c.execute(sql)
            sql="INSERT INTO AFORA(ar_krathshs,typos_oxhmatos) VALUES('%s','%s')" %(key,self.data_tuple[3]) 
            c.execute(sql)
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()

#ΕΠΙΒΛΕΨΗ ΚΡΑΤΗΣΕΩΝ
class Krathseis_Window(QWidget):   
    def __init__(self,parent=None):
        super(Krathseis_Window,self).__init__(parent)
        
        layout=QVBoxLayout()
        self.lbl=QLabel('<p style="text-align:center;font-size:30px;margin-top:150px;margin-bottom:50px;"> Αρχείο κρατήσεων </p>',self)
        layout.addWidget(self.lbl)
         
        global USERNAME
        #Αναζήτηση στη βάση δεδομένων όλων των οχημάτων που αφορούν κρατήσεις του συγκεκριμένου χρήστη. 
        sql='SELECT im_krathshs,im_paralavhs,im_epistrofhs,topothesia,modelo,KLASH_OXHMATOS.typos_oxhmatos, timh, xroma,ar_thesewn,kubismos,eid_kafsimou,photo,KRATHSH.ar_krathshs FROM PRAGMATOPOIEI,KRATHSH,AFORA,KLASH_OXHMATOS,AFORA_SYGKEKRIMENA,OXHMA WHERE PRAGMATOPOIEI.username=%s AND KRATHSH.ar_krathshs=PRAGMATOPOIEI.ar_krathshs AND AFORA.ar_krathshs=KRATHSH.ar_krathshs AND KLASH_OXHMATOS.typos_oxhmatos=AFORA.typos_oxhmatos AND AFORA_SYGKEKRIMENA.ar_krathshs=KRATHSH.ar_krathshs AND OXHMA.ar_pinakidas=AFORA_SYGKEKRIMENA.ar_pinakidas' % ("'"+USERNAME+"'")
        c.execute(sql)
        self.cars=c.fetchall()

        #Αναζήτηση στη βάση δεδομένων όλων των Πακετων Κάλυψης που αφορούν κρατήσεις του συγκεκριμένου χρήστη.
        sql='SELECT KRATHSH.ar_krathshs,titlos,perigrafh,kostos FROM PRAGMATOPOIEI,KRATHSH,KALYPTETAI, PAKETO_KALYPSHS WHERE PRAGMATOPOIEI.username=%s AND KRATHSH.ar_krathshs=PRAGMATOPOIEI.ar_krathshs AND KALYPTETAI.ar_krathshs=KRATHSH.ar_krathshs AND PAKETO_KALYPSHS.titlos=KALYPTETAI.titlos_paketou' % ("'"+USERNAME+"'")
        c.execute(sql)
        self.paketa=c.fetchall()

        #Αναζήτηση στη βάση δεδομένων όλων των Υπηρεσιών που αφορούν κρατήσεις του συγκεκριμένου χρήστη.
        sql='SELECT KRATHSH.ar_krathshs,titlos,perigrafh,kostos FROM PRAGMATOPOIEI,KRATHSH,EPILEGEI, YPHRESIES WHERE PRAGMATOPOIEI.username=%s AND KRATHSH.ar_krathshs=PRAGMATOPOIEI.ar_krathshs AND EPILEGEI.ar_krathshs=KRATHSH.ar_krathshs AND YPHRESIES.titlos=EPILEGEI.titlos_yphresias' % ("'"+USERNAME+"'")
        c.execute(sql)
        self.yphresies=c.fetchall()

        #Αναζήτηση στη βάση δεδομένων όλων των πληρωμών που αφορούν κρατήσεις του συγκεκριμένου χρήστη.
        sql='SELECT KRATHSH.ar_krathshs,PLHRWMH.tropos,poso FROM KRATHSH,EKSOFLEITAI,PLHRWMH,EGGEGRAMMENOS,PLHRWNEI WHERE EGGEGRAMMENOS.username=%s AND PLHRWNEI.username=EGGEGRAMMENOS.username AND EKSOFLEITAI.ar_krathshs=KRATHSH.ar_krathshs AND EKSOFLEITAI.kod_plhr=PLHRWMH.kod_plhr' % ("'"+str(USERNAME)+"'")
        c.execute(sql)
        self.pay=c.fetchall()
        
        self.l=QVBoxLayout()

        #Δημιουργία πίνακα για την εισαγωγή της κάθε μίας κράτησης με κελιά κάποια στοιχεία αυτής.
        self.table=QTableWidget(self)
        self.table.setGeometry(0,0,0,0)

        #Έλεγχος για το αν ο χρήστης έχει πραγματοποιήσει κρατήσεις μέχρι τώρα.
        if self.cars==[]:
            self.labl=QLabel('<p style="text-align:center;font-size:24px;"> Δεν έχετε κάνει ακόμη καμία κράτηση.</p>',self)
            layout.addWidget(self.labl)
        else:
            
            self.table.setColumnCount(6)
            self.table.setRowCount(len(self.cars))
            self.table.setHorizontalHeaderLabels(["Ημερομηνία Κράτησης","Ημερομηνία Παραλαβής","Ημερομηνία επιστροφής","Τοποθεσία","Μοντέλο","Σύνολο"])
            self.table.horizontalHeader()
            self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.table.setSelectionBehavior(QTableWidget.SelectRows)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.table.setSelectionMode(QAbstractItemView.SingleSelection)
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

            #Εισαγωγή στον πίνακα την κάθε κράτηση και των μερικών στοιχείων αυτής.
            self.kostos_aytokinhtoy=list()
            kostos_yphresiwn=list()
            self.synoliko_kostos=0
            for i in range(0,len(self.cars)):
                for k in range (0,len(self.pay)):
                    if str(self.pay[k][0])==str(self.cars[i][12]):
                        pay=self.pay[k]
                for j in range(0,5):
                    self.table.setItem(i,j,QTableWidgetItem(str(self.cars[i][j])))
                self.table.setItem(i,5,QTableWidgetItem(str(pay[2])))

            self.table.setFixedHeight(400)
            self.l.addWidget(self.table)
    	    
        layout.addLayout(self.l)

        #Πίσω στο Κεντρικό Παράθυρο της εφαρμογής μετά τη σύνδεση του χρήστη.
        self.go_back=QPushButton('Πίσω',self)
        self.go_back.setStyleSheet('margin-left:200px;margin-right:200px;font-size:17px')
        layout.addWidget(self.go_back)
        self.setLayout(layout)    
        self.setStyleSheet('font-size: 30 px')
        #self.setFixedSize(500,500)
        self.setGeometry(400,200,600,600)
        self.show()

#Λεπτομέρειες Κράτησης
class Leptomereies_Krathshs(QDialog):
    
    deleted=pyqtSignal()

    def __init__(self,parent=None):
        super(Leptomereies_Krathshs,self).__init__(parent)

        vlayout1=QVBoxLayout()
        groupbox=QGroupBox()
        self.lbl=QLabel('<h1 style="text-align:center">Λεπτομέρειες Κράτησης</h1><br>')
        vlayout1.addWidget(self.lbl)

        hlayout1=QHBoxLayout()
        self.photo=QLabel(self)

        #Πεδία προβολής όλων των στοιχείων της επιλεχθείσας κράτησης 
        layout1=QFormLayout()
        self.lbl1=QLabel('')
        self.lbl1.setStyleSheet('font-size:16px;')
        self.lbl2=QLabel('')
        self.lbl2.setStyleSheet('font-size:16px;')
        self.lbl3=QLabel('')
        self.lbl3.setStyleSheet('font-size:16px;')
        self.lbl4=QLabel('')
        self.lbl4.setStyleSheet('font-size:16px;')
        self.lbl5=QLabel('')
        self.lbl5.setStyleSheet('font-size:16px;')
        self.lbl6=QLabel('')
        self.lbl6.setStyleSheet('font-size:16px;')
        self.lbl7=QLabel('')
        self.lbl7.setStyleSheet('font-size:16px;')
        self.lbl8=QLabel('')
        self.lbl8.setStyleSheet('font-size:16px;')
        self.lbl9=QLabel('')
        self.lbl9.setStyleSheet('font-size:16px;')
        self.lbl10=QLabel('')
        self.lbl10.setStyleSheet('font-size:16px;')
        layout1.addRow(QLabel('<h3 style="font-size:20px;">Όχημα </h3>'))
        layout1.addRow(QLabel('<p style="font-size:16px;">Ημερομηνία Κράτησης: </p>'),self.lbl1)
        layout1.addRow(QLabel('<p style="font-size:16px;">Ημερομηνία Παραλαβής: </p>'),self.lbl2)
        layout1.addRow(QLabel('<p style="font-size:16px;">Ημερομηνία Επιστροφής: </p>'),self.lbl3)
        layout1.addRow(QLabel('<p style="font-size:16px;">Τοποθεσία: </p>'),self.lbl4)
        layout1.addRow(QLabel('<p style="font-size:16px;">Μοντέλο :</p>'),self.lbl5)
        layout1.addRow(QLabel('<p style="font-size:16px;">Χρώμα: </p>'),self.lbl6)
        layout1.addRow(QLabel('<p style="font-size:16px;">Αριθμός θέσεων: </p>'),self.lbl7)
        layout1.addRow(QLabel('<p style="font-size:16px;">Κυβισμός: </p>'),self.lbl8)
        layout1.addRow(QLabel('<p style="font-size:16px;">Είδος Καυσίμου: </p>'),self.lbl9)
        layout1.addRow(QLabel('<p style="font-size:16px;">Τιμή: </p>'),self.lbl10)
        layout1.addRow(QLabel('------------------------------------------------------------------------'))

        hlayout1.addLayout(layout1)
        hlayout1.addWidget(self.photo)
        vlayout1.addLayout(hlayout1)

        hlayout2=QHBoxLayout()
        vlayout2=QVBoxLayout()

        self.layout2=QFormLayout()
        self.layout2.addRow(QLabel('<h3 style="font-size:20px;">Υπηρεσίες</h3>'))

        self.layout3=QFormLayout()
        self.layout3.addRow(QLabel('<h3 style="margin-bottom:20px;font-size:20px;">Πακέτα Κάλυψης</h3>'))       

        vlayout2.addLayout(self.layout2)
        vlayout2.addLayout(self.layout3)
        hlayout2.addLayout(vlayout2)

        vlayout3=QVBoxLayout()
        self.layout4=QFormLayout()
        self.layout4.addRow(QLabel('<h3 style="font-size:20px;">Αναλυτικό Κόστος</h3>'))
        
        self.layout5=QFormLayout()
        lbl_plhr=QLabel('<h3>Πληρωμή</h3>')
        lbl_plhr.setStyleSheet('margin-top:20px;')
        self.layout5.addRow(lbl_plhr)
        self.tropos_plhrwmhs=QLabel('')
        self.tropos_plhrwmhs.setStyleSheet('font-size:16px;')
        lbl_tropos=QLabel('<p style="margin-top:20px;font-size:16px;">Τρόπος πληρωμής:</p>')
        self.layout5.addRow(lbl_tropos,self.tropos_plhrwmhs)

        vlayout3.addLayout(self.layout4)
        vlayout3.addLayout(self.layout5)
        hlayout2.addLayout(vlayout3)
        vlayout1.addLayout(hlayout2)

        self.ok=QPushButton('OK',self)
        self.ok.setStyleSheet('color:black;font-size:15px;')

        groupbox.setLayout(vlayout1)
        scroll=QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        #scroll.setFixedHeight(800)
        # scroll.setFixedWidth(900)
        
        self.layout=QVBoxLayout()
        self.layout.addWidget(scroll) 
        self.layout.addWidget(self.ok)

        self.setLayout(self.layout)
        self.setGeometry(400,200,800,600)
        self.show()

    #Εισαγωγή όλων των στοιχείων κράτησης στα αντίστοιχα πεδία προβολής.
    def fill_data(self,cars,paketa,yphresies,pay,real_dates):
        self.cars=cars
        self.paketa=paketa
        self.yphresies=yphresies
        self.pay=pay
        d0=cars[0].strftime("%Y/%m/%d")
        d1=cars[1].strftime("%Y/%m/%d")
        d2=cars[2].strftime("%Y/%m/%d")
        self.lbl1.setText(str(d0))
        self.lbl2.setText(str(d1))
        self.lbl3.setText(str(d2))
        self.lbl4.setText(str(cars[3]))
        self.lbl5.setText( str(cars[4]))
        self.lbl6.setText(str(cars[7]))
        self.lbl7.setText(str(cars[8]))
        self.lbl8.setText(str(cars[9]))
        self.lbl9.setText(str(cars[10]))
        
        #Προβολή φωτογραφίας οχήματος
        url=cars[11]
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        pixmap_resized = pixmap.scaled(400,400, QtCore.Qt.KeepAspectRatio)
        self.photo.setPixmap(pixmap_resized) 
        self.photo.setFixedSize(400,400)

        #Προβολή λεπτομερειών επιλεχθέντων Υπηρεσιών
        kostos_yphresiwn=0
        if yphresies==[]:
            self.layout2.addRow(QLabel('<p style="font-size:16px;">Δεν έχετε επιλέξει υπηρεσίες</p>'))
        else:
            for i in range(0,len(yphresies)):
                self.lbl11=QLabel(str(yphresies[i][1]))
                self.lbl11.setStyleSheet('font-size:16px;')
                self.lbl12=QLabel(str(yphresies[i][2]))
                self.lbl12.setStyleSheet('font-size:16px;')
                self.lbl13=QLabel(str(yphresies[i][3]))
                self.lbl13.setStyleSheet('font-size:16px;')
                self.layout2.addRow(QLabel('<p style="font-size:16px;">Τίτλος: </p>'),self.lbl11)
                self.layout2.addRow(QLabel('<p style="font-size:16px;">Περιγραφή: </p>'),self.lbl12)
                self.layout2.addRow(QLabel('<p style="font-size:16px;">Κόστος: </p>'),self.lbl13)
                self.layout2.addRow(QLabel('--------------------------------------------------------------------------'))
                kostos_yphresiwn=kostos_yphresiwn+int(yphresies[i][3])
        
        #Προβολή λεπτομερειών Πακέτου Κάλυψης.
        kostos_paketoy=0
        if paketa==[]:
            self.layout3.addRow(QLabel('<p style="font-size:16px;">Δεν έχετε επιλέξει Πακέτα Κάλυψης</p>'))
        else:
            self.lbl14=QLabel(str(paketa[1]))
            self.lbl14.setStyleSheet('font-size:16px;')
            self.lbl15=QLabel(str(paketa[2]))
            self.lbl15.setStyleSheet('font-size:16px;')
            self.lbl16=QLabel(str(paketa[3]))
            self.lbl16.setStyleSheet('font-size:16px;')
            self.layout3.addRow(QLabel('<p style="font-size:16px;">Τίτλος: </p>'),self.lbl14)
            self.layout3.addRow(QLabel('<p style="font-size:16px;">Περιγραφή: </p>'),self.lbl15)
            self.layout3.addRow(QLabel('<p style="font-size:16px;">Κόστος: </p>'),self.lbl16)
            #self.layout3.addRow(QLabel('--------------------------------------------------------------------------'))
            kostos_paketoy=paketa[3]

        d1=datetime.datetime.strptime(str(cars[1]),"%Y-%m-%d %H:%M:%S")
        d2=datetime.datetime.strptime(str(cars[2]),"%Y-%m-%d %H:%M:%S")
        if d1==d2:
            delta=1
        else:
            delta=int((d2-d1).days)
        
        #Αναλυτικός υπολογισμός κόστους οχήματος κάνοντας μόνο χρήση τα δεδομένα της βάσης.
        
        k=int(pay[2])-int(kostos_yphresiwn)-int(kostos_paketoy)
        kostos_aytokinhtoy= round(k/delta )
        self.lbl_kostos_aytokinhtoy=QLabel(str(k))
        self.lbl_kostos_aytokinhtoy.setStyleSheet('font-size:16px;')
        self.kostos_yphresiwn=QLabel(str(kostos_yphresiwn))
        self.kostos_yphresiwn.setStyleSheet('font-size:16px;')
        self.kostos_paketoy=QLabel(str(kostos_paketoy))
        self.kostos_paketoy.setStyleSheet('font-size:16px;')
        self.sum_kostos=QLabel(str(pay[2]))
        self.lbl10.setText(str(cars[6]))
        self.sum_kostos.setStyleSheet('font-size:16px;')
        self.layout4.addRow(QLabel('<p style="font-size:16px;">Κόστος αυτοκινήτου για το επιλεγμένο χρονικό διάστημα: </p>'),self.lbl_kostos_aytokinhtoy) 
        self.layout4.addRow(QLabel('<p style="font-size:16px;">Κόστος υπηρεσιών: </p>'),self.kostos_yphresiwn) 
        self.layout4.addRow(QLabel('<p style="font-size:16px;">Κόστος πακέτου κάλυψης: </p>'),self.kostos_paketoy) 
        self.layout4.addRow(QLabel('<p style="font-size:16px;">Συνολικό Ποσό: </p>'),self.sum_kostos) 
        self.layout4.addRow(QLabel('-------------------------------------------------------------------------------------------------'))

        #Προβολή λεπτομερειών του επιλεχθέντος τρόπου πληρωμής.
        if str(pay[1])=='2':
            c.execute('SELECT ar_kartas,on_katoxou,im_lhkshs FROM EKSOFLEITAI,PLHRWMH,STOIXEIA_KARTAS WHERE EKSOFLEITAI.ar_krathshs=%s AND EKSOFLEITAI.kod_plhr=PLHRWMH.kod_plhr AND PLHRWMH.kod_plhr=STOIXEIA_KARTAS.kod_plhr'%("'"+str(cars[12])+"'"))
            stoixeia_kartas=c.fetchall()
            self.tropos_plhrwmhs.setText('Kάρτα')
            self.ar_kartas=QLabel(str(stoixeia_kartas[0][0]))
            self.ar_kartas.setStyleSheet('font-size:16px;')
            self.on_katoxou=QLabel(str(stoixeia_kartas[0][1]))
            self.on_katoxou.setStyleSheet('font-size:16px;')
            self.im_lhkshs=QLabel(str(stoixeia_kartas[0][2]))
            self.im_lhkshs.setStyleSheet('font-size:16px;')
            self.lbl_karta=QLabel('<h3 style="margin-top:20px;font-size:20px;">Στοιχεία Κάρτας:</h3>')
            self.lbl_karta.setStyleSheet('margin-top:20px;')
            self.layout5.addRow(self.lbl_karta)
            self.layout5.addRow(QLabel('<p style="font-size:16px;">Αριθμός Κάρτας:</p>'),self.ar_kartas)
            self.layout5.addRow(QLabel('<p style="font-size:16px;">Όνομα Κατόχου:</p>'),self.on_katoxou)
            self.layout5.addRow(QLabel('<p style="font-size:16px;">Ημερομηνία Λήξης:</p>'),self.im_lhkshs)
        elif str(pay[1])=='1':
            self.tropos_plhrwmhs.setText('Tιμολόγιο')
        elif str(pay[1])=='0':
            self.tropos_plhrwmhs.setText('Mετρητά')
        
        #Έλεγχος διαφοράς ημερομηνιών για δυνατότητα ακύρωσης της κράτησης.
        now=datetime.datetime.today()
        today = datetime.datetime.strptime(str(now),"%Y-%m-%d %H:%M:%S.%f")
        
        diafora_hmerwn=d1.date()-today.date()

        
        #Αν η ημερομηνία παραλαβής απέχει 2 μέρες ή και λιγότερο από τη σημερινή, αποκλείεται η δυνατότητα χρήστη για ακύρωση της κράτησης.
        if real_dates[2]==None and int(diafora_hmerwn.days)>=2 :
            self.cancel_reservation=QPushButton('Ακύρωση Κράτησης')
            self.cancel_reservation.setStyleSheet('color:black;background:red;font-size:15px;')
            self.layout.addWidget(self.cancel_reservation)
            self.cancel_reservation.clicked.connect(self.epivevaiwsh_akyrwshs)

    #Μήνυμα για επιβεβαίωση της ακύρωσης της κράτησης
    def epivevaiwsh_akyrwshs(self):
        msg = QMessageBox()
        msg.setText('Είστε σίγουρος ότι θέλετε να ακυρώσετε την κράτηση;')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        r=msg.exec_()
        if r==QMessageBox.Yes:
            self.Akyrwsh_Krathshs()
            self.close()
    
    #Ακύρωση της Κράτησης 
    def Akyrwsh_Krathshs(self):
        try:
            msg=QMessageBox()
            #Διαγραφή των πινάκων που αφορούν την κράτηση από τη βάση δεδομένων: KRATHSH,PLHRWMH 
            c.execute('DELETE FROM KRATHSH WHERE KRATHSH.ar_krathshs=%s '%("'"+str(self.cars[12])+"'"))
            c.execute('DELETE FROM PLHRWMH WHERE PLHRWMH.kod_plhr=%s'%("'"+str(self.pay[0])+"'"))
            msg.setText("Η κράτηση που αφορούσε τις ημερομηνίες: "+str(self.cars[1])+' και '+str(self.cars[2])+' ακυρώθηκε.')
            #Εκπέμπεται το σήμα που ειδοποιεί για τη διαγραφή μιας κράτησης.
            self.deleted.emit()
        except:
            msg=QMessageBox()
            msg.setText('Προέκυψε σφάλμα')
            msg.exec_()


#Συναρτήσεις που επιτρέπουν την επικοινωνία των διαφόρων κλάσεων και συνεπώς τη μεταβίβαση δεδομένων 
class Main_Window(QMainWindow):
    
    #Αρχικοποιήση της εφαρμογής με πρώτο παράθυρο την Φόρμα Σύνδεσης Χρήστη
    def __init__(self,parent=None):
        super(Main_Window,self).__init__(parent)

        self.setGeometry(600,100,600,600)
        self.setWindowTitle('Application')
        self.start_Login_Form()
        
    #Συνάρτηση σύνδεσης χρήστη
    def start_Login_Form(self):
        self.con = Login_Form(self)
        self.setCentralWidget(self.con)
        self.username=self.con.username.text()
        self.password=self.con.password.text()
        #Με την επιλογή του κουμπιού "Login" της φόρμας σύνδεσης, καλείται η συνάρτηση του ελέγχου λογαριασμού.
        self.con.login.clicked.connect(self.con.Check_Password)
        #Με την ενεργοποίηση του σήματος "trigger", δηλαδή όταν έχει γίνει επιτυχώς ο έλεγχος και έχει εξακριβωθεί η ύπαρξη του λογαριασμού,
        #καλείται το Κεντρικό Παράθυρο της εφαρμογής μετά τη σύνδεση του χρήστη
        self.con.trigger.connect(self.start_Main_Customer_Window)
        #Με την επιλογή του κουμπιού "create Account" της φόρμας σύνδεσης, καλείται η συνάρτηση της δημιουργίας καινούριου λογαριασμού.
        self.con.reg.clicked.connect(self.start_Registration_Window)
        #Με την επιλογή του κουμπιού "Forgot Password?" της φόρμας σύνδεσης, καλείται η Συνάρτηση της Ανάκτησης λογαριασμού.
        self.con.forgot_passw.clicked.connect(self.start_Anakthsh_Account)
        self.show()
       
    #Συνάρτηση Ανάκτησης λογαριασμού
    def start_Anakthsh_Account(self):
        self.anakthsh=Anakthsh_Account(self)
        #Με την επιλογή του κουμπιού "Οk" της φόρμας ανάκτησης λογαριασμού, καλείται η συνάρτηση ελέγχου των δοθέντων στοιχείων.
        self.anakthsh.ok.clicked.connect(self.anakthsh.Check_Data)
        self.show()

    #Συνάρτηση Εγγραφής καινούριου χρήστη
    def start_Registration_Window(self):
        self.reg = Registration_Window(self)    
        self.setCentralWidget(self.reg)
        #Με την επιλογή του κουμπιού "Πίσω" της φόρμας εγγραφής χρήστη, καλείται η Συνάρτηση σύνδεσης χρήστη.
        self.reg.go_back.clicked.connect(self.start_Login_Form)
        #Με την επιλογή του κουμπιού "Εγγραφή" της φόρμας εγγραφής χρήστη, καλείται η συνάρτηση ελέγχου δοθέντων δεδομένων.
        self.reg.registr.clicked.connect(self.reg.Check_Reg_Data)
        #Με την ενεργοποίηση του σήματος "finished", όταν δηλαδή έχει τελείωσει επιτυχώς ο έλεγχος της εγκυρότητας των δοθέντων δεδομένων,
        # κλαείται η συνάρτηση Ολοκλήρωση Εγγραφής.
        self.reg.finished.connect(self.finished_Registration) 
        self.show()  
        
    #Ολοκλήρωση Εγγραφής
    def finished_Registration(self):
        self.finished=Registered_Window(self)
        self.setCentralWidget(self.finished)
        #Με την επιλογή του κουμπιού "Login" του παραθύρου Ολοκλήρωσης Εγγραφής, καλείται η Συνάρτηση σύνδεσης χρήστη.
        self.finished.go_log.clicked.connect(self.start_Login_Form)
        self.show()

    #Κεντρικό Παράθυρο 
    def start_Main_Customer_Window(self):
        self.Main_CW = Main_Customer_Window(self)
        self.setCentralWidget(self.Main_CW)
        #Με την επιλογή του κουμπιού "Ρυθμίσεις Προφίλ" του Κεντρικού Παραθύρου, καλείται η Συνάρτηση Ρυθμίσεων Προφίλ.
        self.Main_CW.Profile_Settings.clicked.connect(self.start_Profile_Settings)
        #Με την επιλογή του κουμπιού "Κρατήσεις" του Κεντρικού Παραθύρου, καλείται η Συνάρτηση Επίβλεψης Κρατήσεων.
        self.Main_CW.Krathseis.clicked.connect(self.start_Krathseis_Window)
        #Με την επιλογή του κουμπιού "Καινούρια Κράτηση" του Κεντρικού Παραθύρου, καλείται η Συνάρτηση Καινούριας Κράτησης.
        self.Main_CW.New_krathsh.clicked.connect(self.start_New_krathsh_Window)
        #Με την επιλογή του κουμπιού "Κρατήσεις" του Κεντρικού Παραθύρου, καλείται η Συνάρτηση Αποσύνδεσης.
        self.Main_CW.logout.clicked.connect(self.start_Login_Form)
        self.show()      
    
    #Συνάρτηση Ρυθμίσεων Προφίλ
    def start_Profile_Settings(self):
        self.Prof=Profile_Settings(self)
        self.setCentralWidget(self.Prof)
        #Με την επιλογή του κουμπιού "Αλλαγή Ονόματος" της φόρμας Ρυθμίσεων Προφίλ, καλείται η Συνάρτηση Αλλαγής Ονόματος.
        self.Prof.btn_fname.clicked.connect(self.Change_Fname)
        #Με την επιλογή του κουμπιού "Αλλαγή Επωνύμου" της φόρμας Ρυθμίσεων Προφίλ, καλείται η Συνάρτηση Αλλαγής Επωνύμου
        self.Prof.btn_lname.clicked.connect(self.Change_Lname)
        #Με την επιλογή του κουμπιού "Αλλαγή Κωδικού" της φόρμας Ρυθμίσεων Προφίλ, καλείται η Συνάρτηση Αλλαγής Κωδικού
        self.Prof.btn_passw.clicked.connect(self.Change_Password)
        #Με την επιλογή του κουμπιού "Αλλαγή ΑΔΤ" της φόρμας Ρυθμίσεων Προφίλ, καλείται η Συνάρτηση Αλλαγής ΑΔΤ
        self.Prof.btn_adt.clicked.connect(self.Change_adt)
        #Με την επιλογή του κουμπιού "Αλλαγή Αριθμού Διπλώματος" της φόρμας Ρυθμίσεων Προφίλ, καλείται η Συνάρτηση Αλλαγής Αριθμού Διπλώματος
        self.Prof.btn_ar_diplomatos.clicked.connect(self.Change_ar_diplomatos)
        #Με την επιλογή του κουμπιού "Αλλαγή Τηλεφώνου" της φόρμας Ρυθμίσεων Προφίλ, καλείται η Συνάρτηση Αλλαγής Τηλεφώνου
        self.Prof.btn_phone.clicked.connect(self.Change_Phone)
        #Με την επιλογή του κουμπιού "Αλλαγή Email" της φόρμας Ρυθμίσεων Προφίλ, καλείται η Συνάρτηση Αλλαγής Email
        self.Prof.btn_email.clicked.connect(self.Change_Email)
        #Με την επιλογή του κουμπιού "Αλλαγή Διεύθυνσης" της φόρμας Ρυθμίσεων Προφίλ, καλείται η Συνάρτηση Αλλαγής Ονόματος
        self.Prof.btn_dieuth.clicked.connect(self.Change_Dieuth)
        #Με την επιλογή του κουμπιού "Πίσω" της φόρμας Ρυθμίσεων Προφίλ, καλείται το Κεντρικό Πράθυρο
        self.Prof.go_back.clicked.connect(self.start_Main_Customer_Window)
        self.show()

    #Συνάρτηση Αλλαγής Ονόματος
    def Change_Fname(self):
        self.Change=Change_Fname_Window(self)
        #Με την επιλογή του κουμπιού "Τέλος" της φόρμας Αλλαγής Ονόματος, καλείται η Συνάρτηση Ρυθμίσεων Προφίλ.
        self.Change.Done.clicked.connect(self.start_Profile_Settings)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Αλλαγής Ονόματος κλείνει το παράθυρο της φόρμας.
        self.Change.Cancel.clicked.connect(self.Change.close)
        self.show() 

    #Συνάρτηση Αλλαγής Επωνύμου
    def Change_Lname(self):
        self.Change=Change_Lname_Window(self)
        #Με την επιλογή του κουμπιού "Τέλος" της φόρμας Αλλαγής Ονόματος, καλείται η Συνάρτηση Ρυθμίσεων Προφίλ.
        self.Change.Done.clicked.connect(self.start_Profile_Settings)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Αλλαγής Ονόματος κλείνει το παράθυρο της φόρμας.
        self.Change.Cancel.clicked.connect(self.Change.close)
        self.show() 

    #Συνάρτηση Αλλαγής Κωδικού 
    def Change_Password(self):
        self.Change=Change_Password_Window(self)
        #Με την επιλογή του κουμπιού "Τέλος" της φόρμας Αλλαγής Ονόματος, καλείται η Συνάρτηση Ρυθμίσεων Προφίλ.
        self.Change.Done.clicked.connect(self.start_Profile_Settings)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Αλλαγής Ονόματος κλείνει το παράθυρο της φόρμας.  
        self.Change.Cancel.clicked.connect(self.Change.close)
        self.show() 

    #Συνάρτηση Αλλαγής ΑΔΤ
    def Change_adt(self):
        self.Change=Change_adt_Window(self)
        #Με την επιλογή του κουμπιού "Τέλος" της φόρμας Αλλαγής Ονόματος, καλείται η Συνάρτηση Ρυθμίσεων Προφίλ.
        self.Change.Done.clicked.connect(self.start_Profile_Settings)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Αλλαγής Ονόματος κλείνει το παράθυρο της φόρμας.
        self.Change.Cancel.clicked.connect(self.Change.close)
        self.show() 

    #Συνάρτηση Αλλαγής Αριθμού Διπλώματος
    def Change_ar_diplomatos(self):
        self.Change=Change_ar_diplomatos_Window(self)
        #Με την επιλογή του κουμπιού "Τέλος" της φόρμας Αλλαγής Ονόματος, καλείται η Συνάρτηση Ρυθμίσεων Προφίλ.
        self.Change.Done.clicked.connect(self.start_Profile_Settings)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Αλλαγής Ονόματος κλείνει το παράθυρο της φόρμας.
        self.Change.Cancel.clicked.connect(self.Change.close)
        self.show() 

    #Συνάρτηση Αλλαγής Τηλεφώνου
    def Change_Phone(self):
        self.Change=Change_Phone_Window(self)
        #Με την επιλογή του κουμπιού "Τέλος" της φόρμας Αλλαγής Ονόματος, καλείται η Συνάρτηση Ρυθμίσεων Προφίλ.
        self.Change.Done.clicked.connect(self.start_Profile_Settings)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Αλλαγής Ονόματος κλείνει το παράθυρο της φόρμας.
        self.Change.Cancel.clicked.connect(self.Change.close)
        self.show() 

    #Συνάρτηση Αλλαγής Email
    def Change_Email(self):
        self.Change=Change_Email_Window(self)
        #Με την επιλογή του κουμπιού "Τέλος" της φόρμας Αλλαγής Ονόματος, καλείται η Συνάρτηση Ρυθμίσεων Προφίλ.
        self.Change.Done.clicked.connect(self.start_Profile_Settings)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Αλλαγής Ονόματος κλείνει το παράθυρο της φόρμας.
        self.Change.Cancel.clicked.connect(self.Change.close)
        self.show() 
    
    #Συνάρτηση Αλλαγής Διεύθυνσης
    def Change_Dieuth(self):
        self.Change=Change_Dieuthinsh_Window(self)
        #Με την επιλογή του κουμπιού "Τέλος" της φόρμας Αλλαγής Ονόματος, καλείται η Συνάρτηση Ρυθμίσεων Προφίλ.
        self.Change.Done.clicked.connect(self.start_Profile_Settings)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Αλλαγής Ονόματος κλείνει το παράθυρο της φόρμας.
        self.Change.Cancel.clicked.connect(self.Change.close)
        self.show() 

    #Συνάρτηση Καινούριας Κράτησης
    def start_New_krathsh_Window(self):
        self.new_krathsh=New_Krathsh_Window(self)
        self.setCentralWidget(self.new_krathsh)
        #Με την επιλογή του κουμπιού "Επόμενο" της φόρμας Καινούριας Κράτησης, καλείται η Συνάρτηση Ελέγχου Ημερομηνιών.
        self.new_krathsh.next.clicked.connect(self.new_krathsh.Check_Dates)
        #Με την ενεργοποίηση του σήματος "ok", δηλαδή της επιτυχούς ολοκλήρωσης του ελέγχου ημερομηνιών και διαθεσιμότητας κλάσεων,
        #καλείται η Συνάρτηση Επιλογής Κλάσης Οχήματος, και της τελικής επιλογής.
        self.new_krathsh.ok.connect(self.start_Select_Klash_Oxhmatos)
        self.new_krathsh.ok.connect(self.new_krathsh.final_selection)
        #Με την επιλογή του κουμπιού "Πίσω" της φόρμας Καινούριας Κράτησης, καλείται το Κεντρικό Παράθυρο.
        self.new_krathsh.go_back.clicked.connect(self.start_Main_Customer_Window)
        self.show()

    #Συνάρτηση Επιλογής Κλάσης Οχήματος
    def start_Select_Klash_Oxhmatos(self):

        self.select_k=Select_Klash(self)
        self.data=[krathsh[0],krathsh[1],krathsh[2]]
        self.setCentralWidget(self.select_k)
        #Καλείται η συνάρτηση Προβολής των Διαθέσιμων ΚΛάσεων Οχημάτων για τις συγκεκριμένες ημερομηνίες
        self.select_k.Show_Diathesimes_Klaseis(self.data,self.new_krathsh.diathesimes_klaseis)
        #Με την ενεργοποίηση του σήματος "ok", δηλαδή της επιτυχούς ολοκλήρωσης του ελέγχου διαθέσιμων Υπηρεσιών,
        #καλείται η Συνάρτηση Επιλογής Κλάσης Οχήματος, και της τελικής επιλογής.
        self.select_k.trigger.connect(self.start_Select_Yphresies)
        #Με την επιλογή του κουμπιού "Επόμενο" της φόρμας Επιλογής Κλάσης Οχήματος, καλείται η Συνάρτηση Επιλογής Υπηρεσιών.
        self.select_k.next.clicked.connect(self.select_k.final_selection)
        #Με την επιλογή του κουμπιού "Πίσω" της φόρμας Επιλογής Κλάσης Οχήματος, καλείται η Συνάρτηση Καινούριας Κράτησης.
        self.select_k.go_back.clicked.connect(self.start_New_krathsh_Window)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Επιλογής Κλάσης Οχήματος, καλείται το Κεντρικό Παράθυρο.
        self.select_k.cancel.clicked.connect(self.start_Main_Customer_Window)
        self.show()
    
    #Συνάρτηση Επιλογής Υπηρεσιών
    def start_Select_Yphresies(self):
        self.select_Y=Select_Yphresies(self)
        self.setCentralWidget(self.select_Y)
        #Με την επιλογή του κουμπιού "Προσθήκη στο Καλάθι" της φόρμας Επιλογής Υπηρεσιών, καλείται η Συνάρτηση Επιλογής.
        self.select_Y.cart.clicked.connect(self.select_Y.selection)
        #Με την επιλογή του κουμπιού "Επόμενο" της φόρμας Επιλογής Υπηρεσιών, καλείται η Συνάρτηση Επιλογής Πακέτου κάλυψης.
        self.select_Y.next.clicked.connect(self.start_Select_Paketa)
        #Με την επιλογή του κουμπιού "Πίσω" της φόρμας Επιλογής Υπηρεσιών, καλείται η Συνάρτηση Επιλογής Κλάσης Οχήματος.
        self.select_Y.go_back.clicked.connect(self.start_Select_Klash_Oxhmatos)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Επιλογής Υπηρεσιών, καλείται η Συνάρτηση Επιλογής Κλάσης Οχήματος.
        self.select_Y.cancel.clicked.connect(self.start_Main_Customer_Window)
        self.show()

    #Συνάρτηση Επιλογής Πακέτου Κάλυψης
    def start_Select_Paketa(self):
        self.select_P=Select_Paketa(self)
        self.setCentralWidget(self.select_P)

        #Με την επιλογή του κουμπιού "Επόμενο" της φόρμας Επιλογής Πακέτου Κάλυψης, καλείται η Συνάρτηση Πληρωμής και τελικής Επιλογής δεδομένων.
        self.select_P.next.clicked.connect(self.select_P.final_selection)
        self.select_P.next.clicked.connect(self.start_Payment)
        #Με την επιλογή του κουμπιού "Πίσω" της φόρμας Επιλογής Πακέτου Κάλυψης, καλείται η Συνάρτηση Επιλογής Υπηρεσιών.
        self.select_P.go_back.clicked.connect(self.start_Select_Yphresies)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Επιλογής Πακέτου Κάλυψης, καλείται η Συνάρτηση Επιλογής Υπηρεσιών.
        self.select_P.cancel.clicked.connect(self.start_Main_Customer_Window)
        self.show()

    #Συνάρτηση Πληρωμής
    def start_Payment(self):
        self.delta = self.new_krathsh.end_date-self.new_krathsh.start_date
        self.cost = self.select_k.cost*(self.delta.days+1)+self.select_P.cost
        data_tuple=[self.new_krathsh.place,self.new_krathsh.start_date,self.new_krathsh.end_date,self.select_k.car_class,self.select_P.title,self.select_Y.services,self.cost,self.new_krathsh.end_place]
        for i in data_tuple[5]:
            data_tuple[6]+=i[1]
        
        self.pay=Payment(self)
        self.setCentralWidget(self.pay)
        #Καλείται η συνάρτηση προβολής όλων των στοιχείων της καινούριας κράτησης
        self.pay.fill_data(data_tuple)
        #Με την επιλογή του κουμπιού "Έλεγχος κουπονιού " της φόρμας Πληρωμής, καλείται η συνάρτηση επικύρωση έκπτωσης και προβολής αυτής.
        self.pay.check_discount.clicked.connect(self.pay.verify_discount)
        self.pay.check_discount.clicked.connect(lambda : self.pay.fill_data(data_tuple))
        #Με την επιλογή του κουμπιού "Επόμενο" της φόρμας Πληρωμής, καλείται η συνάρτηση ελέγχου των στοιχείων της κάρτας.
        self.pay.next.clicked.connect(self.pay.check_card_info)
        #Με την επιλογή του κουμπιού "Πίσω" της φόρμας Πληρωμής, καλείται η Συνάρτηση Επιλογής Πακέτου Κάλυψης.
        self.pay.go_back.clicked.connect(self.start_Select_Paketa)
        data_tuple.append(self.new_krathsh.d1)
        data_tuple.append(self.new_krathsh.d2)
        #Με την ενεργοποίηση του σήματος "trigger",δηλαδή του ελέγχου της εφκυρότητας των δεδομένων της κάρτας,
        #καλείται η συνάρτηση της εισαγωγής στη βάση δεδομένων όλων των στοιχείων της κράτησης και ύστερα καλειται το Κεντρικό Παράθυρο.
        self.pay.trigger.connect(lambda : self.pay.insert_reservation(data_tuple))
        self.pay.trigger.connect(self.start_Main_Customer_Window)
        #Με την επιλογή του κουμπιού "Ακύρωση" της φόρμας Πληρωμής, καλείται το Κεντρικό Παράθυρο.
        self.pay.cancel.clicked.connect(self.start_Main_Customer_Window)
        
        self.show()

    #Συνάρτηση Επίβλεψης Κρατήσεων
    def start_Krathseis_Window(self):
        self.Krathseis=Krathseis_Window(self)
        self.setCentralWidget(self.Krathseis)
        #Με την ειλογή μίας κράτησης από τον πίνακα των κρατήσεων του χρήστη, καλέιται η Συνάρτηση Προβολής των Λεπτομερειών της Κράτησης
        self.Krathseis.table.clicked.connect(self.show_details)
        #Με την επιλογή του κουμπιού "Πίσω" του παραθύρου Επίβλεψης, καλείται το Κνετρικό Παράθυρο.
        self.Krathseis.go_back.clicked.connect(self.start_Main_Customer_Window)
        self.show()
    
    #Συνάρτηση Προβολής Λεπτομερειών Κράτησης
    def show_details(self):
        self.det=Leptomereies_Krathshs(self)
        data=list()
        for i in self.Krathseis.table.selectedItems():
            data.append(i.text())
        #Αναζήτηση στη βάση για τα στοιχεία της κράτησης που έχουν τα συγκεκριμένα επιλεχθέντα στοιχεία Κράτησης του συγκεκριμένου χρήστη, που την καθιστούν μοναδική.
        sql='SELECT KRATHSH.ar_krathshs,AFORA_SYGKEKRIMENA.im_pragm_epistrofhs,AFORA_SYGKEKRIMENA.im_pragm_epistrofhs FROM PRAGMATOPOIEI,KRATHSH,AFORA_SYGKEKRIMENA,OXHMA WHERE PRAGMATOPOIEI.username=%s AND im_krathshs=%s AND im_paralavhs=%s AND im_epistrofhs=%s AND topothesia=%s AND modelo=%s AND PRAGMATOPOIEI.ar_krathshs=KRATHSH.ar_krathshs AND KRATHSH.ar_krathshs=AFORA_SYGKEKRIMENA.ar_krathshs AND AFORA_SYGKEKRIMENA.ar_pinakidas=OXHMA.ar_pinakidas'%("'"+USERNAME+"'","'"+str(data[0])+"'","'"+str(data[1])+"'","'"+str(data[2])+"'","'"+str(data[3])+"'","'"+str(data[4])+"'")
        c.execute(sql)
        real_dates=c.fetchone()
        print(real_dates)
        id=real_dates[0]
        yphresies=list()
        cars=list()
        paketa=list()
        pay=list()
        #Επιλογή των στοιχείων του Οχήματος της συγκεκριμένης κράτησης.
        for i in range (0,len(self.Krathseis.cars)):
            if str(self.Krathseis.cars[i][12])==str(id):
                cars=self.Krathseis.cars[i]
                break
        #Επιλογή των στοιχείων των Υπηρεσιών της συγκεκριμένης κράτησης.
        for i in range(0,len(self.Krathseis.yphresies)):
            if str(self.Krathseis.yphresies[i][0])==str(id):
                yphresies.append(self.Krathseis.yphresies[i])
        #Επιλογή των στοιχείων του Πακέτου Κάλυψης της συγκεκριμένης κράτησης.
        for i in range (0,len(self.Krathseis.paketa)):
            if str(self.Krathseis.paketa[i][0])==str(id):
                paketa=self.Krathseis.paketa[i]
                break
        #Επιλογή των στοιχείων Πληρωμής της συγκεκριμένης κράτησης.
        for i in range (0,len(self.Krathseis.pay)):
            if str(self.Krathseis.pay[i][0])==str(id):
                pay=self.Krathseis.pay[i]

        #Καλείται η συνάρτηση προβολής όλων των στοιχείων της συγκεκριμένης κράτησης, έχοντας ως δεδομένα τα παραπάνω επιλεχθέντα στοιχεία.
        self.det.fill_data(cars,paketa,yphresies,pay,real_dates)
        #Με την ενεργοποίηση του σήματος "deleted", κλείνει το παράθυρο των Λεπτομερειών Κράτησης και διαγράφεται από τον πίνακα η συγκεκριμένη κράτηση.
        self.det.deleted.connect(self.start_Krathseis_Window)
        #Με την ενεργοποίηση του σήματος "ok", κλείνει το παράθυρο των Λεπτομερειών Κράτησης και επιστρέφει ο χρήστης στο παράθυρο Επίβλεψης των Κρατήσεων.
        self.det.ok.clicked.connect(self.det.close)
        self.show()

#ΣΥΝΔΕΣΗ ΣΤΗ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ 
#στον συγκεκριμένο host
def connect_to_database():
    global conn
    global c
    conn = mysql.connector.connect(
    host = '150.140.186.221',
    user = 'db20_up1063425',
    password = 'up1063425',
    database = 'project_db20_up1063425',
    autocommit = True
    ) 

    c= conn.cursor()
    
#Συνάρτηση main
def main():
    #Σύνδεση στη βάση δεδομένων
    connect_to_database()
    #Ορισμός της εφαρμογής
    app = QApplication(sys.argv)
    #Καθορισμός του style της εφαρμογής
    app.setStyleSheet(stylesheet)
    #Αρχικοποίηση και έναρξη της εφαρμογής 
    main_window = Main_Window()
    sys.exit(app.exec_())

#Ο κώδικας που τρέχει πρώτος και καλεί μόνο τη συνάρτηση main
if __name__=='__main__':
    main()
