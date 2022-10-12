

# TODO  
# rezipper avec les dossier et sous dosseir OK
# suppprimer dosseir OK
# mettre la fonction js avec les variables, propre avec retour à la ligne OK
# récupérer bon format de date : dabord convert vers python date, puis de pythondate vers js date OK
# input de départ pour upload le bon fichier OK
# enregistrer fichier au même endroit avec nom différent OK
# github
# gestion des erreurs (mauvais format, input vide, autres erreurs, caractères spéciaux dans nom de fichier)
# appli executable sur différents Os

import os
import sys
import zipfile


from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import shutil


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(420, 300))    
        self.setWindowTitle("Scorm Date Generator") 

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Date :')
        self.nameLabel.move(20, 80)

        self.date = QDateEdit(self)
        # setting geometry of the date edit 
        self.date.setGeometry(100, 80, 200, 30)

        # date
        d = QDate(2020, 6, 10)
 
        # setting date to the date edit
        self.date.setDate(d)


        self.scormLabel = QLabel(self)
        self.scormLabel.setText('Scorm file :')
        self.scorm_message = QLineEdit(self)

        self.scorm_message.move(100, 20)
        self.scorm_message.resize(200, 32)
        self.scormLabel.move(20, 20)


        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Message :')
        self.line_message = QLineEdit(self)

        self.line_message.move(100, 80)
        self.line_message.resize(200, 32)
        self.nameLabel.move(20, 80)

        self.line_message.move(100, 140)
        self.line_message.resize(200, 32)
        self.nameLabel.move(20, 140)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.click_method)
        pybutton.resize(200,32)
        pybutton.move(100, 200)        

        pybutton = QPushButton('browse', self)
        pybutton.clicked.connect(self.browse_scorm)
        pybutton.resize(60,32)
        pybutton.move(320, 20)        

    def browse_scorm(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                        'All Files (*.*)')
        if path != ('', ''):
            print(path[0])

            self.scorm_message.setText(path[0])
            print(self.scorm_message.text())
            


    def click_method(self):
        self.update_scorm_date(self.date.date().toPyDate(), self.line_message.text(),self.scorm_message.text())



    def update_scorm_date(self, new_date, new_message, scorm_name):

        week_table = {
            "lun.": "Mon",
            "mar.": "Tue",
            "mer.": "Wed",
            "jeu.": "Thu",
            "ven.": "Fri",
            "sam.": "Sat",
            "dim.": "Sun"
        }

        month_table = {
            "janv.": "Jan",
            "févr.": "Feb",
            "mars": "Mar",
            "avril": "Apr",
            "mai": "May",
            "juin": "Jun",
            "juil.": "Jul",
            "août": "Aug",
            "sept.": "Thu",
            "oct.": "Oct",
            "nov.": "Nov",
            "déc.": "Dec"
        }

        week_str = new_date.strftime("%a")
        month_str = new_date.strftime("%b")
        for day in week_table:
            week_str = week_str.replace(day, week_table[day])
        for month in month_table:
            month_str = month_str.replace(month, month_table[month])
        day_int = new_date.strftime("%d")
        year_int = new_date.strftime("%Y")

        file_name_date = "EXP-" + week_str + "-" + month_str + "-" + day_int + "-" + year_int + "-"
        scorm_expiration_date = week_str + " " + month_str + " " + day_int + " " + year_int
        print(scorm_expiration_date)

        folder_name = scorm_name.replace('.zip', '')
        file_name = scorm_name.rsplit('/', 1)[-1]
        path = scorm_name.replace(file_name, '')

        #extract firectory from zip file
        with zipfile.ZipFile(scorm_name, 'r') as zipObject:
            zipObject.extractall(path)

        #replace date with input values
        with open('expDateFunction.txt') as dataFile:
            data = dataFile.read()
            js_data = data.replace('SCORM_EXP_MSG', new_message).replace('SCORM_EXP_DATE', str(scorm_expiration_date))

        with open(folder_name + '/lms/scormdriver.js','a',encoding = 'utf-8') as f:
            f.write("\n")
            f.write(js_data)

        #replace the old zip files with the updated one
        zf = zipfile.ZipFile(path + file_name_date + file_name, "w")
        for dirname, subdirs, files in os.walk(folder_name):
            updated_dirname = dirname.replace(path,'')
            zf.write(updated_dirname)
            for filename in files:
                zf.write(os.path.join(updated_dirname, filename))
        zf.close()

        shutil.rmtree(folder_name, ignore_errors=False, onerror=None)

        #FOR DEV
        self.close()

        print("**************************** end of process ***************************")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )