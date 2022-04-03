import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import Qt 
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QDate
import PyQt5.QtGui
from style import *
import mysql.connector
import pymysql
import time
from datetime import date


#Αυτή η εφαρμογή αφορά την εταιρεία ενοικίασης οχημάτων και προορίζεται
#να την χειριστεί κάποιος υπάλληλος της εταιρείας. Ο υπάλληλος θα
#έχει τη δυνατότητα να εισάγει, ενημερώσει,διαγράψει όλα τα βασικά
#assets της εταιρείας. Παράλληλα μπορεί να δει τα ήδη υπάρχοντα assets
#να λάβει στοιχεία πληρωμών ανάλογα με το χρονικό διάστημα που επιθυμεί
#και να επεξεργαστεί τις κρατήσεις
#Ο σχολιασμός που θα ακολουθήσει δεν θα είναι υπεραναλυτικός.
#Τα σημεία του κώδικα που αφορούν τη μορφοποίηση του γραφικού περιβάλλοντος
#παραλέιπονται από τον σχολιασμό καθώς δεν είναι το κύριο ζητούμενο της
#εφαρμογής μας. Σημεία τα οποία θεωρούμε αξιόλογα έχουν αναλυθεί και στην
#αναφορά.






#Κλάση δημιουργίας του γραφικού περιβάλλοντος του κεντρικού παραθύρου της
#εφαρμογής. Από εδώ ο χρήτης μπορεί να επιλέξει ποια κίνηση θέλει να κάνει
#σύμφωνα με όσα περιγράψαμε παραπάνω
class Main_Window_UI(QWidget):
####################Μορφοποίηση##############################   
    def __init__(self,parent=None):
        super(Main_Window_UI,self).__init__(parent)
        self.lbl_welcome = QLabel('<h1 style="font-size:20px; text-align:center"> Καλώς Ορίσατε στην Εφαρμογή </h1>',self)
        self.lbl_welcome.adjustSize()
        self.car_button = QPushButton('Ενημέρωση Οχημάτων',self)
        self.type_button = QPushButton('Εισαγωγή Τύπου Οχήματος',self)
        self.service_button = QPushButton('Επεξεργασία Υπηρεσιών',self)
        self.package_button = QPushButton('Εισαγωγή Πακέτου Κάλυψης',self)
        self.discount_button = QPushButton('Εισάγωγή Έκπτωσης',self)
        self.reserve_button = QPushButton('Επεξεργασία Κρατήσεων',self)
        self.payment_button = QPushButton('Επεξεργασία Πληρωμών',self)
        self.exit_button = QPushButton('Έξοδος',self)

        self.grid = QGridLayout(self)
        self.grid.setSpacing(10)
        self.grid.addWidget(self.car_button,0,0)
        self.grid.addWidget(self.type_button,0,1)
        self.grid.addWidget(self.service_button,1,0)
        self.grid.addWidget(self.package_button,1,1)
        self.grid.addWidget(self.discount_button,2,0)
        self.grid.addWidget(self.reserve_button,2,1)
        self.grid.addWidget(self.payment_button,3,0)
        self.grid.addWidget(self.exit_button,3,1)
        


        v_layout = QVBoxLayout()
        v_layout.addWidget(self.lbl_welcome)
        v_layout.addLayout(self.grid)
        

        self.setLayout(v_layout)
############################################################

#Κλάση που προσδιορίζει τις ιδιότητες του παραθύρου ενημέρωσης οχημάτων
#Σε αυτό το παράθυρο ο χρήστης βλέπει τα οχήματα της εταιρείας σε έναν πίνακα
#ταξινομημένα κατα αριθμό πινακίδας ώστε να είναι ευκολότερη η αναζήτησή τους.
#Χρησιμοποιώντας τα 3 κουμπιά που ορίζονται στη διεπαφή μπορει να 
#εισάγει ένα νέο όχημα,να διαγράψει ένα ή περισσότερα οχήματα που έχει επιλέξει
#στον πίνακα και να ενημερώσει ένα όχημα που επέλεξε από τον πίνακα

class Car_Update_Window(QWidget):
####################Μορφοποίηση############################## 
    def __init__(self,parent=None):
        super(Car_Update_Window,self).__init__(parent)
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.fetch_data()
        self.table.setGeometry(125,0,250,250)
        self.table.setHorizontalHeaderLabels(['Αρ Πινακίδας','Κλάση','Μοντέλο'])
        self.table.resizeColumnsToContents()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.go_for = QPushButton('Ολοκλήρωση',self)
        self.delete = QPushButton('Διαγραφή',self)
        self.update = QPushButton('Ενημέρωση',self)
        self.insert = QPushButton('Εισαγωγή',self)



        
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.delete)
        h_layout.addWidget(self.update)
        h_layout.addWidget(self.insert)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.go_for)
        
        v_layout.setAlignment(Qt.AlignBottom)
        self.setLayout(v_layout)
############################################################

#Αυτή είναι μια συνάρτηση που εμφανίζεται συχνά και χρησιμοποιειται ώστε να
#πάρουμε όλα τα δεδομένα ενός συγκεκριμένου οχήματος και να τα εισάγουμε στην
#φόρμα ενημέρωσης ώστε ο χρήστης να μην χρειάζεται να τα γράψει όλα εάν θέλει να κάνει
#μια μικρή αλλαγή στα δεδομένα. Όμοιες συναρτήσεις θα παραπέπονται εδώ.
    def fetch_old(self):
        sql = "SELECT ar_pinakidas,typos_oxhmatos,modelo,xroma,kubismos,eid_kafsimou FROM OXHMA WHERE ar_pinakidas='%s'" % (self.cont_list[0])
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()

        self.update_data_tuple = curs.fetchall()

#Αυτή η συνάρτηση φέρνει όλα τα στιγμιότυπα από τη βάση δεδομένων και τα εισάγει στον πίνακα
#Επίσης χρησιμοποιείται συχνά και οι επόμενες όμοιες συναρτήσεις θα παραπέμπονται εδώ
    def fetch_data(self):
        sql = 'SELECT ar_pinakidas,typos_oxhmatos,modelo FROM OXHMA ORDER BY ar_pinakidas'
        curs.execute(sql)
        data = curs.fetchall()
        self.table.setRowCount(len(data))
        for num,i in enumerate(data):
            self.table.setItem(num,0,QTableWidgetItem(i[0]))
            self.table.setItem(num,1,QTableWidgetItem(i[1]))
            self.table.setItem(num,2,QTableWidgetItem(i[2]))

#Συνάρτηση που επιτρέπει την επιλογή στοιχειων από τον πίνακα
#Επίσης χρησιμοποιείται συχνά και οι επόμενες όμοιες συναρτήσεις θα παραπέμπονται εδώ        
    def get_table_keys(self):
        selected = self.table.selectionModel().selectedRows()
        self.cont_list=[]
        for i in selected:
           self.cont_list.append(self.table.item(i.row(),0).text())
        print(self.cont_list)


#Συνάρτηση εισαγωγής στη βάση δεδομένων. Εφόσον το έχει επιλέξει ο χρήστης εισάγουμε στη βάση
#ένα νέο στιγμιότυπο του οχήματος. Η μεταβλητή data_tuple περιέχει όλα τα γνωρίσματα του οχήματος
#ενώ η μεταβλητή depot_text περιέχει το όνομα του σταθμού στον οποίο ανήκει το όχημα.
#Επειδή έχουμε την συσχέτιση Διατίθεται, πρέπει πέρα από τα δεδομένα του οχήματος να εισάγουμε
#σε αυτό τον πίνακα και τα δεδομένα που αφορούν το από ποιον σταθμό διατίθεται το όχημα
    def insert_to_db(self,data_tuple,depot_text):
        try:
            sql = 'INSERT INTO OXHMA(ar_pinakidas,typos_oxhmatos,modelo,xroma,kubismos,eid_kafsimou) VALUES(%s,%s,%s,%s,%s,%s)' % data_tuple
            curs.execute(sql)
            sql = "SELECT kod_stathmou FROM STATHMOS WHERE perioxh=%s" % ("'"+depot_text+"'")
            curs.execute(sql)
            code = curs.fetchone()
            sql = "INSERT INTO DIATITHETAI(kod_stathmou,ar_pinakidas) VALUES(%s,%s)" % (code[0],data_tuple[0])
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()

#Συνάρτηση η οποία διαγράφει στιγμιότυπα του πίνακα όχημα ανάλογα με το τι έχει επιλέξει
#ο χρήστης από τον πίνακα. Καλείται η συνάρτηση get_table_keys και δημιουργειται η λίστα
#cont_list η οποία περιέχει τους αριθμούς πινακίδας των οχημάτων προς διαγραφή
    def delete_entry(self):
        self.get_table_keys()
        if len(self.cont_list)==1:
            sql = "DELETE FROM OXHMA WHERE ar_pinakidas = %s" % "'"+str(self.cont_list[0])+"'"
        else:
            sql = "DELETE FROM OXHMA WHERE ar_pinakidas IN %s" % str(tuple(self.cont_list))
        try:    
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()    
        self.fetch_data()   

#Συνάρτηση ενημέρωσης ενός στιγμιοτύπου. Στο plate_cond περιέχεται ο αριθμός πινακίδας
#του οχήματος του οποίου τα στοιχεία ενημερώνουμε. Στο data_tuple τα στοιχεια που θα ενημερωθούν και
#στο depot_text το όνομα του σταθμού
    def update_entry(self,plate_cond,data_tuple,depot_text):
        data_tuple = list(data_tuple)
        data_tuple.append("'"+plate_cond+"'")
        data_tuple = tuple(data_tuple)
        sql = 'UPDATE OXHMA SET ar_pinakidas=%s,typos_oxhmatos=%s,modelo=%s,xroma=%s,kubismos=%s,eid_kafsimou=%s WHERE ar_pinakidas=%s' % data_tuple
        curs.execute(sql)
        sql = "SELECT kod_stathmou FROM STATHMOS WHERE perioxh=%s" % ("'"+depot_text+"'")
        curs.execute(sql)
        code = curs.fetchone()
        sql = "UPDATE DIATITHETAI SET kod_sthathmou=%s WHERE ar_pinakidas=%s" % (code,data_tuple[0])


#Αυτή η κλάση καθορίζει τις ιδιότητες του παραθύρου ενημέρωσης των στοιχείων κλάσης οχήματος.
#Σε αυτό το παράθυρο ο χρήστης μπορεί να δει τις κλάσεις που προσφέρει η εταιρεία και να
#εκτελέσει εντολές CRUD πάνω σε αυτές
class Car_Type_Update_Window(QWidget):
####################Μορφοποίηση##############################     
    def __init__(self,parent=None):
        super(Car_Type_Update_Window,self).__init__(parent)
        self.table = QTableWidget(self)
        self.table.setColumnCount(1)
        self.fetch_data()
        self.table.setGeometry(125,0,250,250)
        self.table.setHorizontalHeaderLabels(['Όνομα Κλάσης'])
        self.table.resizeColumnsToContents()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        
        self.go_for = QPushButton('Ολοκλήρωση',self)
        self.delete = QPushButton('Διαγραφή',self)
        self.update = QPushButton('Ενημέρωση',self)
        self.insert = QPushButton('Εισαγωγή',self)



        
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.delete)
        h_layout.addWidget(self.update)
        h_layout.addWidget(self.insert)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.go_for)
        
        v_layout.setAlignment(Qt.AlignBottom)
        self.setLayout(v_layout)
############################################################

#Βλέπε κλάση ενημέρωσης οχήματος      
    def fetch_old(self):
        sql = "SELECT typos_oxhmatos,timh,ar_thesewn,photo FROM KLASH_OXHMATOS WHERE typos_oxhmatos='%s'" % (self.cont_list[0])
        curs.execute(sql)
        self.update_data_tuple = curs.fetchall()
        
#Συνάρτηση εισαγωγής μιας νέας κλάσης οχήματος στη βάση δεδομένων
#Η μεταβλητή car_type περιγράφει το όνομα της κλάσης, η cost το κόστος της, η seats τον αριθμό θέσεων
#και η photo περιέχει το λινκ για τη φωτογραφία
    def insert_to_db(self,car_type,cost,seats,photo):
        sql = "INSERT INTO KLASH_OXHMATOS(typos_oxhmatos,timh,ar_thesewn,photo) VALUES(%s,%s,%s,%s)" % ("'"+car_type+"'",cost,"'"+seats+"'","'"+photo+"'")
        try:
            curs.execute(sql)
        except:
            pass
        
#Βλέπε κλάση ενημέρωσης οχήματος   
    def fetch_data(self):
        sql = 'SELECT typos_oxhmatos FROM KLASH_OXHMATOS'
        curs.execute(sql)
        data = curs.fetchall()
        self.table.setRowCount(len(data))
        for num,i in enumerate(data):
            self.table.setItem(num,0,QTableWidgetItem(i[0]))
            
#Βλέπε κλάση ενημέρωσης οχήματος       
    def get_table_keys(self):
        selected = self.table.selectedItems()
        self.cont_list=[]
        for i in selected:   
            self.cont_list.append(i.text())
        
        
        
#Συνάρτηση διαγραφής μιας ή περισσότερων κλάσεων οχήματος        
    def delete_entry(self):
        self.get_table_keys()
        
        if len(self.cont_list)==1:
            sql = "DELETE FROM KLASH_OXHMATOS WHERE typos_oxhmatos = %s" % "'"+str(self.cont_list[0])+"'"
        else:
            sql = "DELETE FROM KLASH_OXHMATOS WHERE typos_oxhmatos IN %s" % str(tuple(self.cont_list))
        try:
            curs.execute(sql)
        except:
            pass
        self.fetch_data()

#Συνάρτηση ενημέρωσης ενός στιγμιοτύπου οχήματος
#Οι μεταβλητές car_type,cost,seats,photo ορίζονται όπως και στην insert
#Ενώ η code_cond φέρει το όνομα της κλάσης την οποία ενημερώνουμε
    def update_entry(self,code_cond,car_type,cost,seats,photo):
        sql = "UPDATE KLASH_OXHMATOS SET typos_oxhmatos=%s,timh=%s,ar_thesewn=%s,photo=%s WHERE typos_oxhmatos=%s" % ("'"+car_type+"'","'"+cost+"'","'"+seats+"'","'"+photo+"'","'"+code_cond+"'")
        try:
            curs.execute(sql)
        except:
            pass    


#Αρχικοοποιεί το παράθυρο ενημέρωησης των υπηρεσιών. Σε αυτό το παράθυρο ο χρήστης μπορεί να δει
#τα ονόματα των υπηρεσιών και να επιλέξει να κάνει εντολές CRUD
class Service_Update_Window(QWidget):
####################Μορφοποίηση##############################     
    def __init__(self,parent=None):
        super(Service_Update_Window,self).__init__(parent)
        
        self.error_box = QMessageBox(self)


        self.table = QTableWidget(self)
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(['Τίτλος'])
        self.table.setGeometry(125,0,250,250)
        self.fetch_data()
        self.table.resizeColumnsToContents()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        
        self.go_for = QPushButton('Ολοκλήρωση',self)
        self.delete = QPushButton('Διαγραφή',self)
        self.update = QPushButton('Ενημέρωση',self)
        self.insert = QPushButton('Εισαγωγή',self)



        
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.delete)
        h_layout.addWidget(self.update)
        h_layout.addWidget(self.insert)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.go_for)
        
        v_layout.setAlignment(Qt.AlignBottom)
        self.setLayout(v_layout)
############################################################

#Βλέπε κλάση οχήματος        
    def fetch_old(self):

        sql = "SELECT titlos,perigrafh,kostos FROM YPHRESIES WHERE titlos='%s'" % (self.cont_list[0])
        curs.execute(sql)
        self.update_data_tuple = curs.fetchall()
        
    

#Βλέπε κλάση οχήματος
    def fetch_data(self):
        sql = "SELECT titlos FROM YPHRESIES"
        curs.execute(sql)
        titles = curs.fetchall()
        self.table.setRowCount(len(titles))
        for num,i in enumerate(titles):
            self.table.setItem(num,0,QTableWidgetItem(i[0]))
    
#Βλέπε κλάση οχήματος
    def get_table_keys(self):
        selected = self.table.selectedItems()
        self.cont_list=[]
        for i in selected:
            self.cont_list.append(i.text())

#Διαγράφει ένα ή περισσότερα στιγμιότυπα του πίνακα Υπηρεσίες ανάλογα με το τι έχει επιλέξει
#ο χρήστης στον πίνακα του παραθύρου
    def delete_entry(self):
        self.get_table_keys()
        if len(self.cont_list)==1:
            
            sql = "DELETE FROM YPHRESIES WHERE titlos = %s" % "'"+str(self.cont_list[0])+"'"
            
        else:
            
            sql = "DELETE FROM YPHRESIES WHERE titlos IN %s" % str(tuple(self.cont_list))
        
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()

        self.fetch_data()

#Εισάγει νέο στιγμιότυπο στο πίνακα Υπηρεσίες
#Όπου title ο τίτλος της υπηρεσίας, text η περιγραφή της και cost το κόστος της
    def insert_to_db(self,title,text,cost):
        try:
            sql = "INSERT INTO YPHRESIES(titlos,perigrafh,kostos) VALUES(%s,%s,%s)" % ("'"+title+"'","'"+text+"'","'"+cost+"'")
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()

#Ενημερώνει ένα στιγμιότυπο του πίνακα Υπηρεσίες.
#Όπου title,text,cost ισχύουν όσα είπαμε στην insert και title_cond
#περιέχει το τίτλο της υπηρεσίας προς ενημέρωση
    def update_entry(self,title_cond,title,text,cost):
        try:
            sql = "UPDATE YPHRESIES SET titlos=%s,perigrafh=%s,kostos=%s WHERE titlos=%s" % ("'"+title+"'","'"+text+"'","'"+str(float(cost))+"'","'"+title_cond+"'")
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()


#Όμοια με την κλάση υπηρεσιών, αρχικοποιεί το παράθυρο ενημέρωσης πακέτων κάλυψης
#και δίνει τη δυνατότητα στον χρήστη να εκτελέσει εντολές CRUD
class Package_Update_Window(QWidget):
####################Μορφοποίηση############################## 
    def __init__(self,parent=None):
        super(Package_Update_Window,self).__init__(parent)
        
        self.error_box = QMessageBox(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(['Τίτλος'])
        self.table.setGeometry(125,0,250,250)
        self.fetch_data()
        self.table.resizeColumnsToContents()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        
        self.go_for = QPushButton('Ολοκλήρωση',self)
        self.delete = QPushButton('Διαγραφή',self)
        self.update = QPushButton('Ενημέρωση',self)
        self.insert = QPushButton('Εισαγωγή',self)

    
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.delete)
        h_layout.addWidget(self.update)
        h_layout.addWidget(self.insert)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.go_for)
        
        v_layout.setAlignment(Qt.AlignBottom)
        self.setLayout(v_layout)
############################################################

#Βλέπε κλάση οχήματος
    def fetch_old(self):
        sql = "SELECT titlos,perigrafh,kostos FROM PAKETO_KALYPSHS WHERE titlos ='%s'" % (self.cont_list[0])
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()


        self.update_data_tuple = curs.fetchall()

#Βλέπε κλασή οχήματος
    def fetch_data(self):
        sql = "SELECT titlos FROM PAKETO_KALYPSHS"
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()
            
        titles = curs.fetchall()
        self.table.setRowCount(len(titles))
        for num,i in enumerate(titles):
            self.table.setItem(num,0,QTableWidgetItem(i[0]))
    
#Βλέπε κλάση οχήματος
    def get_table_keys(self):
        selected = self.table.selectedItems()
        self.cont_list=[]
        for i in selected:
            self.cont_list.append(i.text())

#Διαγράφει ένα ή περισσότερα στιγμιότυπα του πίνακα Πακέτο_Κάλυψης ανάλογα με το τι έχει επιλέξει
#ο χρήστης στον πίνακα του παραθύρου
    def delete_entry(self):
        self.get_table_keys()
        if len(self.cont_list)==1:
            sql = "DELETE FROM PAKETO_KALYPSHS WHERE titlos = %s" % "'"+str(self.cont_list[0])+"'"
        else:
            sql = "DELETE FROM PAKETO_KALYPSHS WHERE titlos IN %s" % str(tuple(self.cont_list))
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()
        self.fetch_data()

#Εισάγει νέο στιγμιότυπο στο πίνακα Πακέτο_Κάλυψης
#Όπου title ο τίτλος του πακέτου, text η περιγραφή του και cost το κόστος του
    def insert_to_db(self,title,text,cost):
        sql = "INSERT INTO PAKETO_KALYPSHS(titlos,perigrafh,kostos) VALUES(%s,%s,%s)" % ("'"+title+"'","'"+text+"'","'"+cost+"'")
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()

#Ενημερώνει ένα στιγμιότυπο του πίνακα Πακέτο_Κάλυψης.
#Όπου title,text,cost ισχύουν όσα είπαμε στην insert και title_cond
#περιέχει το τίτλο του πακέτου προς ενημέρωση
    def update_entry(self,title_cond,title,text,cost):
        sql = "UPDATE PAKETO_KALYPSHS SET titlos=%s,perigrafh=%s,kostos=%s WHERE titlos=%s" % ("'"+title+"'","'"+text+"'","'"+str(float(cost))+"'","'"+title_cond+"'")
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()



#Αρχικοποιεί το παράθυρο ενημέρωσης των εκπτώσεων. Παρουσιάζονται οι κωδικοί των εκπτώσεων
#με το ποσοστό που τους αντιστοιχεί
class Discount_Update_Window(QWidget):
####################Μορφοποίηση############################## 
    def __init__(self,parent=None):
        super(Discount_Update_Window,self).__init__(parent)

        self.error_box = QMessageBox(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.fetch_data()
        self.table.setGeometry(125,0,250,250)
        self.table.setHorizontalHeaderLabels(['Κωδικός Έκπτωσης','Ποσοστό'])
        self.table.resizeColumnsToContents()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.go_for = QPushButton('Ολοκλήρωση',self)
        self.delete = QPushButton('Διαγραφή',self)
        self.update = QPushButton('Ενημέρωση',self)
        self.insert = QPushButton('Εισαγωγή',self)



        
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.delete)
        h_layout.addWidget(self.update)
        h_layout.addWidget(self.insert)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.go_for)
        
        v_layout.setAlignment(Qt.AlignBottom)
        self.setLayout(v_layout)
############################################################

#Βλέπε κλάση ενημέρωσης όχημα
    def get_table_keys(self):
        selected = self.table.selectionModel().selectedRows()
        self.cont_list=[]
        for i in selected:
            self.cont_list.append(self.table.item(i.row(),0).text())

#Βλέπε κλάση ενημέρωσης όχημα
    def fetch_old(self):
        sql = "SELECT kod_ekptwshs,pososto FROM EKPTWSH WHERE kod_ekptwshs='%s'" % (self.cont_list[0]) 
        curs.execute(sql)
        self.update_data_tuple = curs.fetchall()

#Βλέπε κλάση ενημέρωσης όχημα
    def fetch_data(self):
        sql = "SELECT * FROM EKPTWSH"
        curs.execute(sql)
        data = curs.fetchall()
        self.table.setRowCount(len(data))
        for num,i in enumerate(data):
            self.table.setItem(num,0,QTableWidgetItem(str(i[0])))
            self.table.setItem(num,1,QTableWidgetItem(str(i[1])))


    
        
#Διαγράφει μια ή περισσότερες εκπτώσεις ανάλογα με το τι έχει επιλέξει ο
#χρήστης στον πίνακα
    def delete_entry(self):
        self.get_table_keys()
        print('GOT HERE')
        print(self.cont_list)
        if len(self.cont_list)==1:
            sql = "DELETE FROM EKPTWSH WHERE kod_ekptwshs = %s" % "'"+str(self.cont_list[0])+"'"
        else:
            sql = "DELETE FROM EKPTWSH WHERE kod_ekptwshs IN %s" % str(tuple(self.cont_list))
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()

        self.fetch_data()

#Ενημερώνει μια ήδη υπάρχουσα έκπτωση. code_cond ο κωδικός έκπτωσης προς ενημέρωση
#code ο νέος κωδικός έκπτωσης και percent το ποσοστό
    def update_entry(self,code_cond,code,percent):
        sql = "UPDATE EKPTWSH SET kod_ekptwshs=%s,pososto=%s WHERE kod_ekptwshs=%s" % ("'"+code+"'","'"+str(percent)+"'","'"+code_cond+"'")
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()


#Κλάση που αρχικοποιεί το παράθυρο που εμφανίζει στο χρήστη τις κρατήσεις της εταιρείας
#Αρχικά, σε έναν πίνακα φαίνονται όλες οι κρατήσεις που έχουν πραγματοποιηθεί. Με τρια κουμπία
#που υπάρχουν στο παράθυρο, ο χρήστης μπορει να επιλέξει να δει τις τρέχουσες κρατήσεις (αυτές
#που ο πελάτης δεν έχει επιστρέψει το όχημα), τις ολοκληρωμένες (αυτές που ο πελάτης έχει επιστρέψει
#το όχημα) και τις καθυστερημένες (αυτές που ο πελάτης είτε έχει επιστρέψει το όχημα με καθυστέρηση
#είτε δεν το έχει επιστρέψει ενώ θα έπρεπε).Κάνοντας διπλό κλικ σε μια κράτηση ο χρήστης μπορεί να δει
#λεπτομέρειες της
class Reservation_Info(QWidget):
####################Μορφοποίηση############################## 
    trigger = pyqtSignal()

    def __init__(self,parent=None):
        super(Reservation_Info,self).__init__(parent)

        
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Κράτηση','Αριθμός Πινακίδας','Όνομα','Επώνυμο','Ημερομηνία Παραλαβής','Ημερομηνία Επιστροφής'])
        self.table.setGeometry(100,0,300,300)
    
        self.table.resizeColumnsToContents()
   
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        self.go_for = QPushButton('Ολοκλήρωση',self)
        self.due = QPushButton('Καθυστερημένες',self)
        self.completed = QPushButton('Ολοκληρωμένες',self)
        self.current = QPushButton('Τρέχουσες',self)


        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.due)
        h_layout.addWidget(self.completed)
        h_layout.addWidget(self.current)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.go_for)
        
        v_layout.setAlignment(Qt.AlignBottom)
        self.setLayout(v_layout)

        self.table.doubleClicked.connect(self.get_table_keys)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.fetch_all()
############################################################

#Βλέπε κλάση ενημέρωσης οχημάτων
    def get_table_keys(self):
        self.selected = self.table.selectedItems()[0].text()
        self.trigger.emit()

#Βλέπε κλάση ενημέρωσης οχημάτων
    def fetch_all(self):
        sql = """SELECT KRATHSH.ar_krathshs,AFORA_SYGKEKRIMENA.ar_pinakidas,EGGEGRAMMENOS.firstname,EGGEGRAMMENOS.lastname , 
        KRATHSH.im_paralavhs, KRATHSH.im_epistrofhs FROM KRATHSH,PRAGMATOPOIEI,AFORA_SYGKEKRIMENA,EGGEGRAMMENOS 
        WHERE EGGEGRAMMENOS.username = PRAGMATOPOIEI.username AND KRATHSH.ar_krathshs=PRAGMATOPOIEI.ar_krathshs 
        AND KRATHSH.ar_krathshs=AFORA_SYGKEKRIMENA.ar_krathshs ORDER BY AFORA_SYGKEKRIMENA.ar_pinakidas"""
        curs.execute(sql)
        keys = curs.fetchall()
        self.table.setRowCount(len(keys))
        for num,i in enumerate(keys):
            self.table.setItem(num,0,QTableWidgetItem(str(i[0])))
            self.table.setItem(num,1,QTableWidgetItem(str(i[1])))
            self.table.setItem(num,2,QTableWidgetItem(str(i[2])))
            self.table.setItem(num,3,QTableWidgetItem(str(i[3])))
            self.table.setItem(num,4,QTableWidgetItem(str(i[4])))
            self.table.setItem(num,5,QTableWidgetItem(str(i[5])))


#Φέρνει από τη βάση δεδομένων όλες τις τρέχουσες κρατήσεις και τις εισάγει στον πίνακα
    def fetch_current(self):
        sql = """SELECT KRATHSH.ar_krathshs,AFORA_SYGKEKRIMENA.ar_pinakidas,EGGEGRAMMENOS.firstname,EGGEGRAMMENOS.lastname , 
        KRATHSH.im_paralavhs, KRATHSH.im_epistrofhs FROM KRATHSH,PRAGMATOPOIEI,AFORA_SYGKEKRIMENA,EGGEGRAMMENOS 
        WHERE EGGEGRAMMENOS.username = PRAGMATOPOIEI.username AND KRATHSH.ar_krathshs=PRAGMATOPOIEI.ar_krathshs 
        AND KRATHSH.ar_krathshs=AFORA_SYGKEKRIMENA.ar_krathshs AND im_pragm_epistrofhs IS NULL"""
        curs.execute(sql)
        keys = curs.fetchall()
        self.table.setRowCount(len(keys))
        for num,i in enumerate(keys):
            self.table.setItem(num,0,QTableWidgetItem(str(i[0])))
            self.table.setItem(num,1,QTableWidgetItem(str(i[1])))
            self.table.setItem(num,2,QTableWidgetItem(str(i[2])))
            self.table.setItem(num,3,QTableWidgetItem(str(i[3])))
            self.table.setItem(num,4,QTableWidgetItem(str(i[4])))
            self.table.setItem(num,5,QTableWidgetItem(str(i[5])))
         
#Φέρνει από τη βάση δεδομένων όλες τις ολοκληρωμένες κρατήσεις και τις εισάγει στον πίνακα
    def fetch_completed(self):
        
        sql = """SELECT KRATHSH.ar_krathshs,AFORA_SYGKEKRIMENA.ar_pinakidas,EGGEGRAMMENOS.firstname,EGGEGRAMMENOS.lastname ,
        KRATHSH.im_paralavhs, KRATHSH.im_epistrofhs FROM KRATHSH,PRAGMATOPOIEI,AFORA_SYGKEKRIMENA,EGGEGRAMMENOS 
        WHERE EGGEGRAMMENOS.username = PRAGMATOPOIEI.username AND KRATHSH.ar_krathshs=PRAGMATOPOIEI.ar_krathshs AND 
        KRATHSH.ar_krathshs=AFORA_SYGKEKRIMENA.ar_krathshs AND im_pragm_epistrofhs<SYSDATE()"""
        curs.execute(sql)
        keys=curs.fetchall()
        self.table.setRowCount(len(keys))
        for num,i in enumerate(keys):
            self.table.setItem(num,0,QTableWidgetItem(str(i[0])))
            self.table.setItem(num,1,QTableWidgetItem(str(i[1])))
            self.table.setItem(num,2,QTableWidgetItem(str(i[2])))
            self.table.setItem(num,3,QTableWidgetItem(str(i[3])))
            self.table.setItem(num,4,QTableWidgetItem(str(i[4])))
            self.table.setItem(num,5,QTableWidgetItem(str(i[5])))
         

#Φέρνει από τη βάση δεδομένων όλες τις καθυστερημένες κρατήσεις και τις εισάγει στον πίνακα
    def fetch_due(self):
        sql = """SELECT KRATHSH.ar_krathshs,AFORA_SYGKEKRIMENA.ar_pinakidas,EGGEGRAMMENOS.firstname,EGGEGRAMMENOS.lastname ,
        KRATHSH.im_paralavhs, KRATHSH.im_epistrofhs FROM KRATHSH,AFORA_SYGKEKRIMENA,PRAGMATOPOIEI,EGGEGRAMMENOS
        WHERE EGGEGRAMMENOS.username = PRAGMATOPOIEI.username AND KRATHSH.ar_krathshs=PRAGMATOPOIEI.ar_krathshs AND 
        KRATHSH.ar_krathshs=AFORA_SYGKEKRIMENA.ar_krathshs AND (KRATHSH.im_epistrofhs<AFORA_SYGKEKRIMENA.im_pragm_epistrofhs OR 
        (KRATHSH.im_epistrofhs<SYSDATE() AND AFORA_SYGKEKRIMENA.im_pragm_epistrofhs IS NULL))"""
        curs.execute(sql)
        keys=curs.fetchall()
        self.table.setRowCount(len(keys))
        for num,i in enumerate(keys):
            self.table.setItem(num,0,QTableWidgetItem(str(i[0])))
            self.table.setItem(num,1,QTableWidgetItem(str(i[1])))
            self.table.setItem(num,2,QTableWidgetItem(str(i[2])))
            self.table.setItem(num,3,QTableWidgetItem(str(i[3])))
            self.table.setItem(num,4,QTableWidgetItem(str(i[4])))
            self.table.setItem(num,5,QTableWidgetItem(str(i[5])))
         

#Κλάση που αρχικοποιεί το παράθυρο πληροφοριών μιας κράτησης. Ο χρήστης μπορεί να δει περισσότερες πληροφορίες
#για τον χρήστη ή για το συγκεκριμένο όχημα ενω του δίνεται η δυνατότητα να επιβεβαιώσει τις ημερομηνίες πραγματικής
#παραλαβής και επιστροφής του οχήματος από τον πελάτη
class Reservation_Info_Plus(QWidget):
####################Μορφοποίηση############################## 
    tooktrigger = pyqtSignal()
    returnedtrigger = pyqtSignal()

    def __init__(self,parent=None):
        super(Reservation_Info_Plus,self).__init__(parent)
        self.key=1
        self.error_box = QMessageBox(self)

        self.go_for = QPushButton('Ολοκλήρωση',self)
        self.took = QPushButton('Παρέλαβε το όχημα',self)
        self.returned = QPushButton('Επέστρεψε το όχημα',self)
        self.person = QPushButton('Πληροφορίες Πελάτη',self)
        self.car = QPushButton('Πληροφορίες Οχήματος',self)

        self.name_lbl = QLabel(self)
        self.start_lbl = QLabel(self)
        self.end_lbl = QLabel(self)
        self.plate_lbl = QLabel(self)
        self.due_lbl = QLabel(self)


        hbox = QHBoxLayout()
        hbox.addWidget(self.took)
        hbox.addWidget(self.returned)

        hbox_up = QHBoxLayout()
        hbox_up.addWidget(self.person)
        hbox_up.addWidget(self.car)

        vbox_w = QVBoxLayout()
        vbox_w.addWidget(self.name_lbl)
        vbox_w.addWidget(self.start_lbl)
        vbox_w.addWidget(self.end_lbl)
        vbox_w.addWidget(self.plate_lbl)
        vbox_w.addWidget(self.due_lbl)
        
        

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_up)
        vbox.addLayout(vbox_w)
        vbox.addLayout(hbox)
        vbox.addWidget(self.go_for)

        self.setLayout(vbox)


        self.took.clicked.connect(lambda : self.date_dialog('took'))
        self.tooktrigger.connect(self.took_date)

        self.returned.clicked.connect(lambda : self.date_dialog('returned'))
        self.returnedtrigger.connect(self.returned_date)
############################################################

#Σε περίπτωση που ο χρήστης θελήσει να επιβεβαιώσει την ημερομηνία πραγματικής παραλαβής και επιστροφής
#δημιουργείται ένα dialog το οποίο του δίνει τη δυνατότητα να εισάγει μια ημερομηνία
    def date_dialog(self,mode):
        self.popup = Date_Window(self)
        self.popup.setGeometry(0,0,100,100)
        self.popup.show()


        self.popup.save.clicked.connect(self.popup.save_date)
        if mode=='took':
            self.popup.trigger.connect(self.get_date_took)
        else:
            self.popup.trigger.connect(self.get_date_returned)

#Χρησιμοποιείται για την προηγούμενη διαδικασία, αποθηκευει τοπικά την ημερομηνία
#που έβαλε ο χρήστης και τρέχει την συνάρτηση που την εισάγει σαν ημερομηνία επιστροφής
    def get_date_returned(self):
        self.date = self.popup.date_value
        self.popup.accept()
        self.returnedtrigger.emit()
#Όμοια με την από πάνω συνάρτηση με τη διαφορά ότι εισάγει την ημερομηνία ως ημερομηνία παραλαβής
    def get_date_took(self):
        self.date = self.popup.date_value
        self.popup.accept()
        self.tooktrigger.emit()

#Κάνει ενημέρωση στη βάση της ημερομηνίας πραγματικής παραλαβής
    def took_date(self):
        sql = "UPDATE AFORA_SYGKEKRIMENA SET im_pragm_paralavhs='%s' WHERE ar_krathshs='%s'" % (self.date,self.key)
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε σφάλμα')
            self.error_box.exec_()
            return 0
        self.fetch_data(self.key)


#Κάνει ενημέρωση στη βάση της ημερομηνίας πραγματικής επιστροφής
    def returned_date(self):
        
        try:
            sql = "UPDATE AFORA_SYGKEKRIMENA SET im_pragm_epistrofhs='%s' WHERE ar_krathshs='%s'" % (self.date,self.key)
            curs.execute(sql)
            sql = "SELECT kod_stathmou FROM STATHMOS WHERE perioxh='%s'" % self.returned_place
            curs.execute(sql)
            station = curs.fetchone()[0]
            sql = "UPDATE DIATITHETAI SET kod_stathmou='%s' WHERE ar_pinakidas='%s'" %(station,self.plate)
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε σφάλμα')
            self.error_box.exec_()
            return 0        
        self.fetch_data(self.key)


#Φέρνει τα δεδομένα της κράτησης που φαινονται στο παράθυρο και ορισμένα κλειδιά πινάκων για διευκόλυνση
#σε επόεμενες συναρτήσεις
    def fetch_data(self,key):
        sql = """SELECT EGGEGRAMMENOS.firstname,EGGEGRAMMENOS.lastname,KRATHSH.topothesia_ep ,KRATHSH.topothesia,AFORA_SYGKEKRIMENA.ar_pinakidas,
                    KRATHSH.im_epistrofhs,AFORA_SYGKEKRIMENA.im_pragm_epistrofhs,AFORA_SYGKEKRIMENA.im_pragm_paralavhs,EGGEGRAMMENOS.username
                    
                    FROM KRATHSH,PRAGMATOPOIEI,EGGEGRAMMENOS,AFORA_SYGKEKRIMENA WHERE EGGEGRAMMENOS.username = PRAGMATOPOIEI.username AND 
                    KRATHSH.ar_krathshs=PRAGMATOPOIEI.ar_krathshs AND KRATHSH.ar_krathshs=AFORA_SYGKEKRIMENA.ar_krathshs AND KRATHSH.ar_krathshs='%s'""" % key
        curs.execute(sql)
        data = curs.fetchall()[0]
        name_str = '<p style="font-size:17px; text-align:center"> Ονοματεπώνυμο\n %s </p>' % (data[0]+' '+data[1])
        self.name_lbl.setText(name_str)
        start = '<p style="font-size:17px; text-align:center"> Τοποθεσία Παραλαβής\n %s </p>' % data[2]
        self.start_lbl.setText(start)
        end = '<p style="font-size:17px; text-align:center"> Τοποθεσία Επιστροφής\n %s </p>' % data[3]
        self.end_lbl.setText(end)
        plate_str = '<p style="font-size:17px; text-align:center"> Αριθμός Πινακίδας\n %s </p>' % data[4]
        self.plate_lbl.setText(plate_str)
        if data[6]==None:
            due = (data[5].date()-date.today()).days
        else:
            due = (data[5].date()-data[6].date()).days

        if due>0:
            due = 0
        due=-due    
        due_str = '<p style="font-size:17px; text-align:center"> Ημέρες καθυστέρησης\n %s </p>' % due
        self.due_lbl.setText(due_str)
        self.plate = data[4]
        self.returned_place = data[3]
        self.key = key
        self.username = data[8]
        self.firstname = data[0]
        self.lastname = data[1]

        if data[6]!=None: 
            text = 'Επέστρεψε το όχημα στις:%s' % data[6].date()
            self.returned.setText(text)
        
        if data[7]!=None:
            text = 'Παρέλαβε το όχημα στις:%s' % data[7].date()
            self.took.setText(text)
        

#Αρχικοποιεί το παράθυρο που δείχνει τις λεπτομέρεις ενός οχήματος που έχει κρατηθει από κάποιον πελάτη        
class Car_Info(QWidget):
####################Μορφοποίηση############################## 
    def __init__(self,plate,parent=None):
        super(Car_Info,self).__init__(parent)
        self.plate = plate
        

        self.go_for = QPushButton('Επιστροφή',self)
        self.plate_lbl = QLabel(self)
        self.type_lbl = QLabel(self)
        self.model_lbl = QLabel(self)
        self.color_lbl = QLabel(self)
        self.vol_lbl = QLabel(self)
        self.fuel_lbl = QLabel(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.plate_lbl)
        vbox.addWidget(self.type_lbl)
        vbox.addWidget(self.model_lbl)
        vbox.addWidget(self.color_lbl)
        vbox.addWidget(self.vol_lbl)
        vbox.addWidget(self.fuel_lbl)
        vbox.addWidget(self.go_for)
        self.setLayout(vbox)

        self.fetch_data()
############################################################

#Φέρνει τα απαραίτητα δεδομένα        
    def fetch_data(self):
        sql = "SELECT typos_oxhmatos,modelo,xroma,kubismos,eid_kafsimou FROM OXHMA WHERE ar_pinakidas='%s'" % self.plate
        curs.execute(sql)
        data = curs.fetchall()[0]


        plate ='<p style="font-size:17px; text-align:center"> Αριθμός πινακίδας %s </p>' % (self.plate)
        self.plate_lbl.setText(plate)
        type_of =  '<p style="font-size:17px; text-align:center"> Κλάση Οχήματος %s </p>' % data[0]
        self.type_lbl.setText(type_of)
        model =  '<p style="font-size:17px; text-align:center"> Μοντέλο %s </p>' % data[1] 
        self.model_lbl.setText(model)
        col = '<p style="font-size:17px; text-align:center"> Χρώμα %s </p>' % data[2]
        self.color_lbl.setText(col)
        vol =  '<p style="font-size:17px; text-align:center"> Κυβισμός %s </p>' % data[3]
        self.vol_lbl.setText(vol)
        fuel =  '<p style="font-size:17px; text-align:center"> Είδος Καυσίμου %s </p>' % data[4]
        self.fuel_lbl.setText(fuel)


#Αρχικοποιει το παράθυρο που παρουσιάζονται τα δεδομένα του πελάτη που έκανε την κράτηση
class Person_Info(QWidget):
####################Μορφοποίηση############################## 
    def __init__(self,username,firstname,lastname,parent=None):
        super(Person_Info,self).__init__(parent)
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

        self.go_for = QPushButton('Επιστροφή',self)
        self.name_lbl = QLabel(self)
        self.phone_lbl = QLabel(self)
        self.email_lbl = QLabel(self)
        self.adt_lbl = QLabel(self)
        self.license_lbl = QLabel(self)
        self.home_lbl = QLabel(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.name_lbl)
        vbox.addWidget(self.phone_lbl)
        vbox.addWidget(self.email_lbl)
        vbox.addWidget(self.adt_lbl)
        vbox.addWidget(self.license_lbl)
        vbox.addWidget(self.home_lbl)
        vbox.addWidget(self.go_for)
        self.setLayout(vbox)

        self.fetch_data()
############################################################   

#Φέρνει τα δεδομένα του πελάτη
    def fetch_data(self):
        sql = "SELECT adt,ar_diplomatos,thl,email FROM EGGEGRAMMENOS WHERE username='%s'" % self.username
        curs.execute(sql)
        data1 = curs.fetchall()[0]
        print(data1)
        sql = "SELECT TK,poli,odos,arithmos FROM DIEUTHINSH WHERE username='%s'" % self.username
        curs.execute(sql)
        data2 = curs.fetchall()[0]
        print(data2)

        name ='<p style="font-size:17px; text-align:center"> Ονοματεπώνυμο %s </p>' % (self.firstname + ' ' + self.lastname)
        self.name_lbl.setText(name)
        adt =  '<p style="font-size:17px; text-align:center"> ΑΔΤ %s </p>' % data1[0]
        self.adt_lbl.setText(adt)
        lic =  '<p style="font-size:17px; text-align:center"> Αριθμός Διπλώματος %s </p>' % data1[1] 
        self.license_lbl.setText(lic)
        phone = '<p style="font-size:17px; text-align:center"> Τηλέφωνο %s </p>' % data1[2]
        self.phone_lbl.setText(phone)
        email =  '<p style="font-size:17px; text-align:center"> Ονοματεπώνυμο\n %s </p>' % data1[3]
        self.email_lbl.setText(email)
        home =  '<p style="font-size:17px; text-align:center"> Διέυθυνση %s </p>' % (data2[1]+' '+data2[2]+' '+str(data2[3])+' '+data2[0])
        self.home_lbl.setText(home)




#Το dialog που χρησιμοποίησε η κλάση reservation_info_plus    
class Date_Window(QDialog):
####################Μορφοποίηση############################## 
    trigger = pyqtSignal()

    def __init__(self,parent=None):
        super(Date_Window,self).__init__(parent)
        self.date = QDateEdit(self)
        self.date.setDate(QDate(date.today()))

        self.save = QPushButton('Αποθήκευση',self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.date)
        vbox.addWidget(self.save)

        self.setLayout(vbox)
############################################################

#Αποθηκεύει την ημερομηνία που έβαλε ο χρήστης        
    def save_date(self):
        self.date_value = self.date.date().toPyDate()
        self.trigger.emit()



#Αρχικοποιεί το παράθυρο επεξεργασίας πληρωμών. Σε αυτό το παράθυρο ο χρήστης επιλέγει ένα χρονικό διάστημα
#και μπορει να υπολογίσει το πλήθος των κρατήσεων, τις συνολικές εισπράξεις και το μέσο κόστος ανά ενοικίαση
class Payment_Window(QWidget):
####################Μορφοποίηση############################## 
    trigger = pyqtSignal()

    def __init__(self,parent=None):
        super(Payment_Window,self).__init__(parent)

        self.error_box = QMessageBox(self)

        self.pay_lbl = QLabel('<h1> Επιλέξτε το χρονικό διάστημα που επιθυμείτε </h1>' ,self)
        self.pay_lbl.setAlignment(Qt.AlignCenter)
        self.fro = QLabel('Από',self)
        self.to = QLabel('Μέχρι',self)

        self.go_for = QPushButton('Ολοκλήρωση',self)

        self.calc_choice = QComboBox(self)
        self.calc_choice.addItem('Πλήθος Κρατήσεων')
        self.calc_choice.addItem('Συνολικό Κέρδος Κρατήσεων')
        self.calc_choice.addItem('Μέση Κοστολόγιση Κράτησης')
        self.calc = QPushButton('Υπολογισμός',self)

        self.fro_date = QDateEdit(self)
        self.fro_date.setDate(QDate(date.today()))
        self.to_date = QDateEdit(self)
        self.to_date.setDate(QDate(date.today()))

        self.res = QLabel('<p style="text-align:center;font-size:35px">  </p>',self)
        

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.fro_date)
        hbox1.addWidget(self.to_date)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.fro)
        hbox2.addWidget(self.to)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.calc)
        hbox3.addWidget(self.calc_choice)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.pay_lbl)
        
        vbox3.addLayout(hbox2)
        vbox3.addLayout(hbox1)
        vbox3.addWidget(self.res)
        
        vbox3.addLayout(hbox3)
        
        vbox3.addWidget(self.go_for)

        self.setLayout(vbox3)
############################################################

#Υπολογίζει το πλήθος ή το άθροισμα ή τη μέση τιμή των κρατήσεων για το χρονικό διάστημα που εισάγαμε        
    def calculate(self):
        self.fro_date_val = self.fro_date.date().toPyDate()
        self.to_date_val = self.to_date.date().toPyDate()
        
        if self.to_date_val<self.fro_date_val:
            self.error_box.setText('Σφάλμα στις ημερομηνίες')
            self.error_box.exec_()
            return 0

        if self.calc_choice.currentText()=='Πλήθος Κρατήσεων':
            agg = 'COUNT'
        elif self.calc_choice.currentText()=='Συνολικό Κέρδος Κρατήσεων':
            agg = 'SUM'
        elif self.calc_choice.currentText()=='Μέση Κοστολόγιση Κράτησης':
            agg = 'AVG'

        print()
        sql = """SELECT %s(PLHRWMH.poso) FROM PLHRWMH,EKSOFLEITAI,KRATHSH WHERE PLHRWMH.kod_plhr=EKSOFLEITAI.kod_plhr
        AND EKSOFLEITAI.ar_krathshs=KRATHSH.ar_krathshs AND 
        KRATHSH.im_paralavhs>='%s' AND KRATHSH.im_paralavhs<='%s' """ %(agg,self.fro_date_val,self.to_date_val)
        curs.execute(sql)
        summ = curs.fetchone()
        if summ[0]!=None:
            self.res.setText('<p style="text-align:center;font-size:35px">'+str(summ[0])+'</p>')
        else:
            self.res.setText('<p style="text-align:center;font-size:35px"> 0 </p>')


#Αρχικοποιεί τη φόρμα εισαγωγής των στοιχειων Πακέτου Κάλυψης και Υπηρεσιών.
#Επειδή οι δύο έννοιες έχουν τα ίδια γνωρίσματα, χρησιμοποιείται μια φόρμα και για τις δύο
class Package_Service_Form_Window(QWidget):
####################Μορφοποίηση############################## 
    trigger = pyqtSignal()
    def __init__(self,parent=None):
        super(Package_Service_Form_Window,self).__init__(parent)
        self.title_lbl = QLabel('Εισάγετε τον τίτλο της υπηρεσίας/πακέτου',self)
        self.cost_lbl = QLabel('Εισάγετε το κόστος της υπηρεσίας/πακέτου')
        self.text_lbl = QLabel('Εισάγετε την περιγραφή της υπηρεσίας/πακέτου')
    
        self.error_box = QMessageBox(self)

        self.title = QLineEdit(self)
        self.text = QTextEdit(self)
        self.cost = QLineEdit(self)


        self.save = QPushButton('Αποθήκευση',self)
        self.go_for = QPushButton('Ολοκλήρωση',self)

        self.vbox = QVBoxLayout(self)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.title_lbl)
        self.vbox.addWidget(self.title)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.cost_lbl)
        self.vbox.addWidget(self.cost)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.text_lbl)
        self.vbox.addWidget(self.text)
        self.vbox.addStretch(3)
        self.vbox.addWidget(self.save)
        self.vbox.addWidget(self.go_for)
        

        self.hbox = QHBoxLayout(self)
        self.hbox.addLayout(self.vbox)
        
        self.setLayout(self.hbox)
############################################################
        
#Αποθηκέυει όσα έχει γράψει ο χρήστης στη φόρμα. Επόμενες εκδοχές αυτής της συνάρτησης παραπέμπονται εδώ
#Σημειώνουμε πως εδώ γίνεται και το exception handling με βάση τους περιορισμούς δεδομένων που έχουμε
#ορίσει στη βάση
    def save_texts(self,mode='insert'):
        self.title_text = self.title.text()
        self.cost_value = self.cost.text()
        self.text_contents = self.text.toPlainText()

        

       
        if self.title_text=='' or self.cost_value=='' or self.text_contents=='':
            self.error_box.setText('Υπάρχουν κενά πεδία')
            self.error_box.exec_()
            return 0 


        if len(self.title_text)>50:
            
            self.error_box.setText('Ο τίτλος που επιλέξατε ξεπερνάει το όριο των 50 χαρακτήρων')
            self.error_box.exec_()
            self.title.setStyleSheet("QLineEdit{background: red;}")
            return 0

        elif len(self.text_contents)>300:
            self.error_box.setText('Η περιγαφή που επιλέξατε ξεπερνάει το όριο των 300 χαρακτήρων')
            self.error_box.exec_()
            self.text.setStyleSheet("QTextEdit{background: red;}")
            return 0

        try:
            float(self.cost_value)
        except:
            self.error_box.setText('Το πεδίο κόστος πρέπει να είναι αριθμός')
            self.error_box.exec_()
            self.cost.setStyleSheet("QLineEdit{background: red;}")
            return 0
        
        if mode=='insert':
            sql = "SELECT 1 FROM YPHRESIES WHERE titlos='%s'" % self.title_text
            curs.execute(sql)
            check_services = curs.fetchall()

            sql = "SELECT 1 FROM PAKETO_KALYPSHS WHERE titlos='%s'" % self.title_text
            curs.execute(sql)
            check_packets = curs.fetchall()
            if check_packets!=[] or check_services!=[]:
                self.error_box.setText('Προσοχή! Μπορεί ο τίτλος που δώσατε να ανήκει σε άλλο πακέτο')
                self.error_box.exec_()

        if mode=='insert':
            self.error_box.setText('Επιτυχής εισαγωγή')
        else:
            self.error_box.setText('Επιτυχής ενημέρωση')
        self.error_box.exec_()
        self.cost.setStyleSheet("QLineEdit{background: white;}")
        self.text.setStyleSheet("QTextEdit{background: white;}")
        self.title.setStyleSheet("QLineEdit{background: white;}")
        self.trigger.emit()


#Σε περίπτωση που μπήκαμε σε αυτό το παράθυρο για ενημέρωση στοιχείων, γεμίζουμε τη φόρμα με τα προηγούμενα
#στοιχεια ώστε ο χρήστης να μην χρειαστεί να τα ξαναγραψει όλα. Επόμενες εκδοχές αυτής της συνάρτησης παραπέμπονται
#εδώ
    def fill_lines(self,data_tuple):
        data_tuple=data_tuple[0]
        self.title.setText(data_tuple[0])
        self.cost.setText(str(data_tuple[2]))
        self.text.setText(data_tuple[1])


#Κλάση που αρχικοποιεί το παράθυρο της φόρμας κλάσης οχήματος       
class Car_Type_Form_Window(QWidget):
####################Μορφοποίηση############################## 
    trigger = pyqtSignal()

    def __init__(self,parent=None):
        super(Car_Type_Form_Window,self).__init__(parent)
        self.error_box = QMessageBox(self)


        self.type_desc_lbl = QLabel('Εισάγετε την ονομασία της κλάσης',self)
        self.cost_lbl = QLabel('Εισάγετε το κόστος ενοικίασης του οχήματος ανά ημέρα',self)
        self.pass_seats_lbl = QLabel('Εισάγετε τον αριθμό θέσεων του οχήματος',self)
        self.photo_lbl = QLabel('Επιλέξτε μια φωτογραφία για τον τύπο οχήματος (link)',self)


        self.type_desc = QLineEdit(self)
        self.cost = QLineEdit(self)
        self.pass_seats = QLineEdit(self)
        self.photo = QLineEdit(self)
        
        self.save = QPushButton('Αποθήκευση',self)
        self.go_for = QPushButton('Ολοκλήρωση',self)

        self.vbox = QVBoxLayout(self)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.type_desc_lbl)
        self.vbox.addWidget(self.type_desc)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.cost_lbl)
        self.vbox.addWidget(self.cost)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.pass_seats_lbl)
        self.vbox.addWidget(self.pass_seats)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.photo_lbl)
        self.vbox.addWidget(self.photo)
        self.vbox.addStretch(3)
        self.vbox.addWidget(self.save)
        self.vbox.addWidget(self.go_for)
        

        self.hbox = QHBoxLayout(self)
        self.hbox.addLayout(self.vbox)
        
        self.setLayout(self.hbox)

   
############################################################

#Βλέπε φόρμα πακέτων-υπηρεσιών        
    def save_texts(self,mode='insert'):
        self.type_desc_text = self.type_desc.text()
        self.cost_value = self.cost.text()
        self.pass_seats_text = self.pass_seats.text()
        self.photo_text = self.photo.text()

        

        if mode =='insert':
            sql = "SELECT 1 FROM KLASH_OXHMATOS WHERE typos_oxhmatos='%s'" % self.type_desc_text
            curs.execute(sql)
            check_type_desc = curs.fetchall()
            if check_type_desc!=[]:
                self.error_box.setText('Ο τύπος οχήματος που επιλέξατε υπάρχει ήδη')
                self.error_box.exec_()
                self.type_desc.setStyleSheet("QLineEdit{background: red;}")
                return 0

        elif self.type_desc_text=='' or self.cost_value=='' or self.pass_seats_text=='' or self.photo_text=='':
            self.error_box.setText('Υπάρχουν κενά πεδία')
            self.error_box.exec_()
            return 0
        
        elif len(self.photo_text)>255:
            self.error_box.setText('Το link που επιλέξατε ξεπερνάει τους 255 χαρακτήρες')
            self.error_box.exec()
            self.photo.setStyleSheet("QLineEdit{background: red;}")
            return 0
        
        
        try:
            float(self.cost_value) 
        except:
            self.error_box.setText('Το πεδίο κόστος πρέπει να είναι αριθμός')
            self.error_box.exec_()
            self.cost.setStyleSheet("QLineEdit{background: red;}")
            return 0 
        
        try:
            int(self.pass_seats_text)
        except:
            self.error_box.setText('Το πεδίο αριθμός θέσεων πρέπει να είναι ακέραιος αριθμός')
            self.error_box.exec_()
            self.pass_seats.setStyleSheet("QLineEdit{background: red;}")
            return 0 
        
        if mode=='insert':
            self.error_box.setText('Επιτυχής εισαγωγή')
        else:
            self.error_box.setText('Επιτυχής ενημέρωση')
        self.error_box.exec_()
        self.pass_seats.setStyleSheet("QLineEdit{background: white;}")
        self.cost.setStyleSheet("QLineEdit{background: white;}")
        self.photo.setStyleSheet("QLineEdit{background: white;}")
        self.type_desc.setStyleSheet("QLineEdit{background: white;}")
        self.trigger.emit()

#Βλέπε φόρμα πακέτων-υπηρεσιών
    def fill_lines(self,data_tuple):
        data_tuple=data_tuple[0]
        self.type_desc.setText(data_tuple[0])
        self.cost.setText(str(data_tuple[1]))
        self.pass_seats.setText(str(data_tuple[2]))
        self.photo.setText(str(data_tuple[3]))
        

#Κλάση που αρχικοποιεί το παράθυρο της φόρμας στοιχειων οχήματος
class Car_Form_Window(QWidget):
####################Μορφοποίηση############################## 
    trigger = pyqtSignal()

    def __init__(self,parent=None):
        super(Car_Form_Window,self).__init__(parent)

        self.error_box=QMessageBox(self)

        self.class_lbl = QLabel('Επιλέξτε τον τύπο του οχήματος',self)
        self.fuel_lbl =QLabel('Επιλέξτε είδος καυσίμου',self)
        self.plate_lbl = QLabel('Εισάγετε τον αριθμό πινακίδας του οχήματος')
        self.model_lbl = QLabel('Εισάγετε το μοντέλο του οχήματος')
        self.color_lbl = QLabel('Εισάγετε το χρώμα του οχήματος')
        self.vol_lbl = QLabel('Εισάγετε τον κυβισμό του οχήματος')
        self.depot_lbl = QLabel('Επιλέξτε τον σταθμό που διαθέτει το όχημα')

        self.fuel_box = QComboBox(self)
        self.fuel_box.addItem('Ντίζελ')
        self.fuel_box.addItem('Βενζίνη')
        self.fuel_box.addItem('APV εκτός EV')
        self.fuel_box.addItem('ECV')
        self.fuel_box.addItem('HEV')
        self.fuel_box.addItem('BEV')
        self.fuel_box.addItem('PHEV')


        self.class_box = QComboBox(self)
        self.fill_box()

        self.depot_box = QComboBox(self)
        self.fill_depot_box()

        self.plate = QLineEdit(self)
        self.model = QLineEdit(self)
        self.color = QLineEdit(self)
        self.vol = QLineEdit(self)

        self.plus = QPushButton('+',self)
        self.go_for =QPushButton('Ολοκλήρωση',self)
        self.save = QPushButton('Αποθήκευση',self)


        self.grid = QGridLayout(self)

        self.class_box_comp = QVBoxLayout(self)
        self.class_box_comp.addWidget(self.class_lbl)
        self.class_box_comp.addWidget(self.class_box)
        self.grid.addLayout(self.class_box_comp,0,0)

        self.fuel_box_comp = QVBoxLayout(self)
        self.fuel_box_comp.addWidget(self.fuel_lbl)
        self.fuel_box_comp.addWidget(self.fuel_box)
        self.grid.addLayout(self.fuel_box_comp,0,1)

        self.plate_comp = QVBoxLayout(self)
        self.plate_comp.addWidget(self.plate_lbl)
        self.plate_comp.addWidget(self.plate)
        self.grid.addLayout(self.plate_comp,0,2)

        self.model_comp = QVBoxLayout(self)
        self.model_comp.addWidget(self.model_lbl)
        self.model_comp.addWidget(self.model)
        self.grid.addLayout(self.model_comp,1,0)

        self.color_comp = QVBoxLayout(self)
        self.color_comp.addWidget(self.color_lbl)
        self.color_comp.addWidget(self.color)
        self.grid.addLayout(self.color_comp,1,1)

        self.vol_comp = QVBoxLayout(self)
        self.vol_comp.addWidget(self.vol_lbl)
        self.vol_comp.addWidget(self.vol)
        self.grid.addLayout(self.vol_comp,1,2)

        self.depot_comp = QVBoxLayout(self)
        self.depot_comp.addWidget(self.depot_lbl)
        self.depot_comp.addWidget(self.depot_box)
        self.depot_hcomp = QHBoxLayout(self)
        self.depot_hcomp.addLayout(self.depot_comp)
        self.depot_hcomp.addWidget(self.plus)
        self.grid.addLayout(self.depot_hcomp,2,1)

        self.grid.addWidget(self.go_for,3,0)
        self.grid.addWidget(self.save,3,2)

        self.setLayout(self.grid)

############################################################

#Γεμίζει το combobox που περιέχει τους διαθέσιμους σταθμους με βάση τα περιεχόμενα του πίνακα Σταθμος
    def fill_depot_box(self):
        sql = "SELECT perioxh FROM STATHMOS"
        curs.execute(sql)
        depots = curs.fetchall()
        for i in depots:
            self.depot_box.addItem(str(i[0]))

#Γεμίζει το combobox που περιέχει τις διαθέσιμες κλάσεις οχημάτων από τη βάση δεδομένων
    def fill_box(self):
        sql = "SELECT typos_oxhmatos FROM KLASH_OXHMATOS"
        curs.execute(sql)
        classes = curs.fetchall()
        for i in classes:
            self.class_box.addItem(str(i[0]))

#Όμοια με την save_texts βλέπε φόρμα πακέτων-υπηρεσιών
    def save_vals(self,mode='insert'):
        plate_text = self.plate.text()
        model_text = self.model.text()
        color_text = self.color.text()
        vol_text = self.vol.text()
        fuel_text = self.fuel_box.currentText()
        class_text = self.class_box.currentText()
        self.depot_text =self.depot_box.currentText()
        self.data_tuple = ("'"+plate_text+"'","'"+class_text+"'","'"+model_text+"'",
            "'"+color_text+"'","'"+vol_text+"'","'"+fuel_text+"'")

        if plate_text=='' or model_text=='' or color_text=='' or vol_text=='' or fuel_text=='' or class_text=='':
            self.error_box.setText('Υπάρχουν κενά πεδία')
            self.error_box.exec_()
            return 0

        if len(plate_text)>9:
            self.error_box.setText('Ο αριθμός πινακίδας πρέπει να περιέχει το πολύ 9 χαρακτήρες')
            self.error_box.exec_()
            self.plate.setStyleSheet("QLineEdit{background: red;}")
            return 0

        if len(model_text)>30:
            self.error_box.setText('Το μοντέλο που επιλέξατε ξεπερνά τους 30 χαρακτήρες')
            self.error_box.exec_()
            self.model.setStyleSheet("QLineEdit{background: red;}")
            return 0

        if len(color_text)>30:
            self.error_box.setText('Το χρώμα που επιλέξατε ξεπερνά τους 30 χαρακτήρες')
            self.error_box.exec_()
            self.color.setStyleSheet("QLineEdit{background: red;}")
            return 0

        try:
            int(vol_text)
        except:
            self.error_box.setText('Ο κυβισμός πρέπει να είναι ακέραιος αριθμός')
            self.error_box.exec_()
            self.vol.setStyleSheet("QLineEdit{background: red;}")
            return 0
        

        if mode=='insert':
            sql = "SELECT 1 FROM OXHMA WHERE ar_pinakidas='%s'" % plate_text
            curs.execute(sql)
            plate_check=curs.fetchall()
            if plate_check!=[]:
                self.error_box.setText('Υπάρχει ήδη όχημα με αυτό τον αριθμό πινακίδας')
                self.error_box.exec_()
                self.plate.setStyleSheet("QLineEdit{background: red;}")
                return 0


        if mode=='insert':
            self.error_box.setText('Επιτυχής εισαγωγή')
            self.error_box.exec_()
        
        else:
            self.error_box.setText('Επιτυχής ενημέρωση')
            self.error_box.exec_()

        self.plate.setStyleSheet("QLineEdit{background: white;}")
        self.vol.setStyleSheet("QLineEdit{background: white;}")
        self.color.setStyleSheet("QLineEdit{background: white;}")
        self.model.setStyleSheet("QLineEdit{background: white;}")
        self.trigger.emit()

#Βλέπε φόρμα πακέτων υπηρεσιών
    def fill_lines(self,data_tuple):
        data_tuple=data_tuple[0]
        self.plate.setText(data_tuple[0])
        self.model.setText(str(data_tuple[2]))
        self.color.setText(str(data_tuple[3]))
        self.vol.setText(str(data_tuple[4]))

#Κλάση που αρχικοποιει το παράθυρο με τη φόρμα σταθμών
class Depot_Form_Window(QWidget):
####################Μορφοποίηση############################## 
    def __init__(self,parent=None):
        super(Depot_Form_Window,self).__init__(parent)

        self.error_box=QMessageBox(self)


        self.depot_lbl = QLabel('Εισάγετε τη περιοχή του σταθμού')
        
        self.depot = QLineEdit(self)
        
        self.go_for = QPushButton('Ολοκλήρωση',self)
        self.delete = QPushButton('Διαγραφή',self)
        self.save = QPushButton('Αποθήκευση',self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.depot_lbl)
        vbox.addWidget(self.depot)
        vbox.addStretch(1)
        vbox.addWidget(self.delete)
        vbox.addWidget(self.save)
        vbox.addWidget(self.go_for)
        
        self.setLayout(vbox)
############################################################

#Εισαγωγή ενός νέου σταθμού       
    def save_depot(self):
        depot_txt = self.depot.text()
        sql = "INSERT INTO STATHMOS(perioxh) VALUES(%s)" % ("'"+depot_txt+"'")
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()

#Διαγραφή ενός σταθμού
    def delete_depot(self):
        depot_txt = self.depot.text()
        sql = "DELETE FROM STATHMOS WHERE perioxh='%s'" % depot_txt
        try:
            curs.execute(sql)
        except:
            self.error_box.setText('Παρουσιάστηκε πρόβλημα')
            self.error_box.exec_()

#Κλάση που αρχικοποιεί το παράθυρο της φόρμας εκπτώσεων
class Discount_Form_Window(QWidget):
####################Μορφοποίηση############################## 
    trigger = pyqtSignal()

    def __init__(self,parent=None):
        super(Discount_Form_Window,self).__init__(parent)

        self.error_box=QMessageBox(self)

        self.code_lbl = QLabel('Εισάγετε τον κωδικό έκπτωσης',self)
        self.code = QLineEdit(self)

        self.percent_lbl = QLabel('Εισάγετε το ποσοστό έκπτωσης: 0%',self)
        self.percent = QSlider(Qt.Horizontal,self)
        self.percent.setRange(0,100)
        self.percent.setFocusPolicy(Qt.NoFocus)
        self.percent.setPageStep(5)
        
        self.go_for = QPushButton('Ολοκλήρωση',self)
        self.save = QPushButton('Αποθήκευση',self)


        


        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.code_lbl)
        self.vbox.addWidget(self.code)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.percent_lbl)
        self.vbox.addWidget(self.percent)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.save)
        self.vbox.addWidget(self.go_for)

        self.setLayout(self.vbox)
    
        self.percent.valueChanged.connect(self.print_percent)
############################################################

#Παρουσιάζει το ποσοστό έκπτωσης δίπλα στο slide bar (GUI)
    def print_percent(self):
        val = self.percent.value()
        txt = 'Εισάγετε το ποσοστό έκπτωσης: {} %'.format(str(val))
        self.percent_lbl.setText(txt)

#Αποθηκεύει μια νέα έκπτωση στη βάση
    def save_discount(self):
        code_txt = self.code.text()
        percent = self.percent.value()
        sql = "INSERT INTO EKPTWSH(kod_ekptwshs,pososto) VALUES(%s,%s)" % ("'"+code_txt+"'","'"+str(percent)+"'")
        try:
            curs.execute(sql)
        except:
            pass

#Βλέπε φόρμα πακέτων-υπηρεσιών
    def save_vals(self,mode='insert'):
        self.code_text = self.code.text()
        self.percent_val = self.percent.value()

        if self.code_text=='':
            self.error_box.setText('Υπάρχουν κενά πεδία')
            self.error_box.exec_()
            return 0
            
    
        if len(self.code_text)>8:
                self.error_box.setText('Ο κωδικός που επιλέξατε ξεπερνά τους 8 χαρακτήρες')
                self.error_box.exec_()
                self.code.setStyleSheet("QLineEdit{background: red;}")
                return 0

        if mode == 'insert':
            sql = "SELECT 1 FROM EKPTWSH WHERE kod_ekptwshs = '%s'" % self.code_text
            curs.execute(sql)
            check_code = curs.fetchall()
            if check_code!=[]:
                self.error_box.setText('Ο κωδικός έκπτωσης υπάρχει ήδη')
                self.error_box.exec_()
                self.code.setStyleSheet("QLineEdit{background: red;}")
                return 0 
            
            
            else:
                self.error_box.setText('Επιτυχής εισαγωγή')
                self.error_box.exec_()
                self.code.setStyleSheet("QLineEdit{background: white;}")
        else:
            self.error_box.setText('Επιτυχής ενημέρωση')
            self.error_box.exec_()
            self.code.setStyleSheet("QLineEdit{background: white;}")
    
        self.trigger.emit()
  



#Κύρια κλάση προγράμματος. Σε αυτή περιέχονται συναρτήσεις που αρχικοποιούν τα παράθυρα τα οποία
#περιγράψαμε παραπάνω. Μέσα σε κάθε μια από αυτές τις συναρτήσεις γίνεται και η διαχείριση των σημάτων
#του γραφικού περιβάλλοντος, δηλαδή ποια συνάρτηση εκτελέιται αν πατηθει το χ κουμπί κλπ.
#Κρίνουμε πως δεν έχει ιδιαίτερο ενδιαφέρον ως προς τη διαχείριση της βάσης και για αυτό δεν δίνονται σχόλια
class Main_Window(QMainWindow):

    def __init__(self,parent=None):
        super(Main_Window,self).__init__(parent)

        self.setGeometry(0,0,500,500)
        self.setWindowTitle('Application')
        self.initUI()
        self.conn = conn

    def initUI(self):

        self.MainWGUI = Main_Window_UI(self)
        self.setCentralWidget(self.MainWGUI)
        self.MainWGUI.car_button.clicked.connect(self.start_Car_Update_Window)
        self.MainWGUI.type_button.clicked.connect(self.start_Car_Type_Update_Window)
        self.MainWGUI.package_button.clicked.connect(self.start_Package_Update_Window)
        self.MainWGUI.service_button.clicked.connect(self.start_Service_Update_Window)
        self.MainWGUI.discount_button.clicked.connect(self.start_Discount_Update_Window)
        self.MainWGUI.reserve_button.clicked.connect(self.start_Reservation_Info_Window)
        self.MainWGUI.payment_button.clicked.connect(self.start_Payment_Window)
        self.MainWGUI.exit_button.clicked.connect(self.exit_app)
        self.show()

    def start_Car_Update_Window(self):
        self.CUW = Car_Update_Window(self)
        self.setCentralWidget(self.CUW)
        self.CUW.go_for.clicked.connect(self.initUI)

        self.CUW.insert.clicked.connect(lambda : self.Car_Form('insert'))

        self.CUW.delete.clicked.connect(lambda :self.CUW.delete_entry())

        
        self.CUW.update.clicked.connect(lambda :self.CUW.get_table_keys())
        self.CUW.update.clicked.connect(lambda : self.CUW.fetch_old())
        self.CUW.update.clicked.connect(lambda :self.Car_Form('update'))
        self.show()

    def start_Car_Type_Update_Window(self):
        self.CTUW = Car_Type_Update_Window(self)
        self.setCentralWidget(self.CTUW)
        self.CTUW.go_for.clicked.connect(self.initUI)
       
        self.CTUW.insert.clicked.connect(lambda : self.Car_Type_Form('insert'))
        
        self.CTUW.delete.clicked.connect(lambda : self.CTUW.delete_entry())

        
        self.CTUW.update.clicked.connect(lambda : self.CTUW.get_table_keys())
        self.CTUW.update.clicked.connect(lambda : self.CTUW.fetch_old())
        self.CTUW.update.clicked.connect(lambda : self.Car_Type_Form('update'))
        self.show()

    def start_Package_Update_Window(self):
        self.PUW = Package_Update_Window(self)
        self.setCentralWidget(self.PUW)
        self.PUW.go_for.clicked.connect(self.initUI)

        self.PUW.insert.clicked.connect(lambda : self.Package_Form('insert'))
        self.PUW.delete.clicked.connect(lambda : self.PUW.delete_entry())

        
        self.PUW.update.clicked.connect(lambda : self.PUW.get_table_keys())
        self.PUW.update.clicked.connect(lambda : self.PUW.fetch_old())
        self.PUW.update.clicked.connect(lambda : self.Package_Form('update'))
        self.show()

    def start_Service_Update_Window(self):
        self.SUW = Service_Update_Window(self)
        self.setCentralWidget(self.SUW)
        self.SUW.go_for.clicked.connect(self.initUI)
        self.SUW.insert.clicked.connect(lambda : self.Service_Form('insert'))
        self.SUW.delete.clicked.connect(lambda : self.SUW.delete_entry())

        
        self.SUW.update.clicked.connect(lambda : self.SUW.get_table_keys())
        self.SUW.update.clicked.connect(lambda : self.SUW.fetch_old())
        self.SUW.update.clicked.connect(lambda : self.Service_Form('update'))
        self.show()


    def start_Discount_Update_Window(self):
        self.DUW = Discount_Update_Window(self)
        self.setCentralWidget(self.DUW)

        self.DUW.go_for.clicked.connect(self.initUI)
        self.DUW.insert.clicked.connect(lambda : self.Discount_Form('insert'))

        self.DUW.delete.clicked.connect(self.DUW.delete_entry)

        
        self.DUW.update.clicked.connect(self.DUW.get_table_keys)
        self.DUW.update.clicked.connect(self.DUW.fetch_old)
        self.DUW.update.clicked.connect(lambda : self.Discount_Form('update'))

        self.show()

    def start_Reservation_Info_Window(self):
        self.RIF = Reservation_Info(self)
        self.setCentralWidget(self.RIF)

        self.RIF.go_for.clicked.connect(self.initUI)
        self.RIF.current.clicked.connect(self.RIF.fetch_current)
        self.RIF.completed.clicked.connect(self.RIF.fetch_completed)
        self.RIF.due.clicked.connect(self.RIF.fetch_due)
        self.RIF.trigger.connect(self.start_Reservation_Info_Plus)


    def start_Reservation_Info_Plus(self):
        self.RIP = Reservation_Info_Plus(self)
        self.setCentralWidget(self.RIP)

        self.RIP.fetch_data(self.RIF.selected)
        self.RIP.go_for.clicked.connect(self.start_Reservation_Info_Window)
        self.RIP.person.clicked.connect(self.start_Person_Info)
        self.RIP.car.clicked.connect(self.start_Car_Info)


    def start_Payment_Window(self):
        self.pay = Payment_Window(self)
        self.setCentralWidget(self.pay)

        self.pay.go_for.clicked.connect(self.initUI)
        self.pay.calc.clicked.connect(self.pay.calculate)
        
    def start_Person_Info(self):
        self.PI = Person_Info(self.RIP.username,self.RIP.firstname,self.RIP.lastname)
        self.setCentralWidget(self.PI)

        self.PI.go_for.clicked.connect(self.start_Reservation_Info_Plus)

    def start_Car_Info(self):
        self.CI = Car_Info(self.RIP.plate)
        self.setCentralWidget(self.CI)
        self.CI.go_for.clicked.connect(self.start_Reservation_Info_Plus)


    def Service_Form(self,mode):
        self.PSF = Package_Service_Form_Window(self)
        self.setCentralWidget(self.PSF)

        if mode=='update':
            self.PSF.fill_lines(self.SUW.update_data_tuple)

        self.PSF.go_for.clicked.connect(self.start_Service_Update_Window)
        
        
        if mode=='insert':
            self.PSF.save.clicked.connect(lambda : self.PSF.save_texts())
            self.PSF.trigger.connect(lambda : self.SUW.insert_to_db(self.PSF.title_text,self.PSF.text_contents,self.PSF.cost_value))
        elif mode=='update':
            self.PSF.save.clicked.connect(lambda : self.PSF.save_texts(mode='update'))
            self.PSF.trigger.connect(lambda : self.SUW.update_entry(self.SUW.cont_list[0],self.PSF.title_text,self.PSF.text_contents,self.PSF.cost_value))
            self.PSF.trigger.connect(self.start_Service_Update_Window)

    def Package_Form(self,mode):
        self.PSF = Package_Service_Form_Window(self)
        self.setCentralWidget(self.PSF)

        
        if mode=='update':
            self.PSF.fill_lines(self.PUW.update_data_tuple)

        self.PSF.go_for.clicked.connect(self.start_Package_Update_Window)
        
        
        if mode=='insert':
            self.PSF.save.clicked.connect(lambda : self.PSF.save_texts())
            self.PSF.trigger.connect(lambda : self.PUW.insert_to_db(self.PSF.title_text,self.PSF.text_contents,self.PSF.cost_value))
        elif mode=='update':
            self.PSF.save.clicked.connect(lambda : self.PSF.save_texts(mode='update'))
            self.PSF.trigger.connect(lambda : self.PUW.update_entry(self.PUW.cont_list[0],self.PSF.title_text,self.PSF.text_contents,self.PSF.cost_value))
            self.PSF.trigger.connect(self.start_Package_Update_Window)


    def Car_Type_Form(self,mode='insert'):
        self.CTF = Car_Type_Form_Window(self)
        self.setCentralWidget(self.CTF)

        

        if mode=='update':
            self.CTF.fill_lines(self.CTUW.update_data_tuple)

        self.CTF.go_for.clicked.connect(self.start_Car_Type_Update_Window)
        


        if mode=='insert':
            self.CTF.save.clicked.connect(lambda : self.CTF.save_texts())
            self.CTF.trigger.connect(lambda : self.CTUW.insert_to_db(self.CTF.type_desc_text,self.CTF.cost_value,self.CTF.pass_seats_text,self.CTF.photo_text))
        elif mode == 'update':
            self.CTF.save.clicked.connect(lambda : self.CTF.save_texts(mode='update'))
            self.CTF.trigger.connect(lambda : self.CTUW.update_entry(self.CTUW.cont_list[0],self.CTF.type_desc_text,self.CTF.cost_value,self.CTF.pass_seats_text,self.CTF.photo_text))
            self.CTF.trigger.connect(self.start_Car_Type_Update_Window)

    def Car_Form(self,mode = 'insert'):
        self.CF = Car_Form_Window(self)
        self.setCentralWidget(self.CF)

        self.CF.plus.clicked.connect(self.Depot_Form)

        if mode=='update':
            self.CF.fill_lines(self.CUW.update_data_tuple)

        self.CF.go_for.clicked.connect(lambda : self.start_Car_Update_Window())

        
        
        if mode=='insert':
            self.CF.save.clicked.connect(lambda : self.CF.save_vals())
            self.CF.trigger.connect(lambda :self.CUW.insert_to_db(self.CF.data_tuple,self.CF.depot_text))
        
        if mode=='update':
            self.CF.save.clicked.connect(lambda : self.CF.save_vals(mode='update'))
            self.CF.trigger.connect(lambda :self.CUW.update_entry(self.CUW.cont_list[0],self.CF.data_tuple,self.CF.depot_text))
            self.CF.trigger.connect(self.start_Car_Update_Window)

    def Depot_Form(self):
        self.DFW =Depot_Form_Window(self)
        self.setCentralWidget(self.DFW)


        self.DFW.go_for.clicked.connect(self.Car_Form)
        self.DFW.save.clicked.connect(lambda : self.DFW.save_depot())
        self.DFW.delete.clicked.connect(self.DFW.delete_depot)

    def Discount_Form(self,mode='insert'):
        self.DF = Discount_Form_Window(self)
        self.setCentralWidget(self.DF)
        
        self.DF.go_for.clicked.connect(self.start_Discount_Update_Window)
        if mode=='insert':
            self.DF.save.clicked.connect(lambda : self.DF.save_vals())
            self.DF.trigger.connect(lambda : self.DF.save_discount())
        elif mode=='update':
            self.DF.save.clicked.connect(lambda : self.DF.save_vals(mode='update'))
            self.DF.trigger.connect(lambda : self.DUW.update_entry(self.DUW.cont_list[0],self.DF.code_text,self.DF.percent_val))
            self.DF.trigger.connect(self.start_Discount_Update_Window)

    def exit_app(self):
        sys.exit()


#Συνάρτηση που πραγματοποιει τη σύνδεση με τη βάση δεδομένων
def connect_to_database():
    global conn
    global curs
    conn = mysql.connector.connect(
    host = '150.140.186.221',
    user = 'db20_up1059386',
    password = 'up1059386',
    database = 'project_db20_up1059386',
    autocommit = True
    )

    curs = conn.cursor()
    
#Η κύρια συνάρτηση στην οποία τρέχει η εφαρμογή
def main():
    connect_to_database()
    app = QApplication(sys.argv)
    main_window = Main_Window()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
