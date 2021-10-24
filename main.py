from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi
import sys
import time
from BMICalc import bmi_calculator
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFrame, QMessageBox
import images_rc
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from datetime import date
from NUTRICalc import nutrition
from todatabaseconnection import createconnectionindb

currentdate = ""
currentcalburned = 0
value = 0
days = 0
winningdays = 0
currentstat = " "
currentcaloriesc = 0
currentsletaken = 0
currentwater = 0


def goto_screen_index(index_now):
    widget.setCurrentIndex(index_now)


class MainWindow(QMainWindow):
    # MainWindow Login Screen index 0
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("MainWindow.ui", self)
        self.pushButton_LogIn.clicked.connect(self.loginn)
        self.pushButton_NewUac.clicked.connect(lambda: goto_screen_index(1))
        self.pushButton.clicked.connect(lambda: goto_screen_index(2))

    def loginn(self):
        try:

            conn = createconnectionindb()
            uname = self.lineEdit_2.text()
            pasw = self.lineEdit.text()
            concursorobject = conn.cursor()
            concursorobject.execute('SELECT * FROM userid WHERE username = ? and password = ?',
                                    (uname, pasw))

            unamepswd = concursorobject.fetchone()
            concursorobject.fetchall()
            if unamepswd is None:
                raise Exception
            goto_screen_index(4)

            conn.commit()
            conn.close()

            print(unamepswd[7])



        except Exception as e:
            print("encounter error")


def history():
    conn = createconnectionindb()
    concursorobject = conn.cursor()
    concursorobject.execute('SELECT * FROM phistory WHERE id=1')

    unamepswd = concursorobject.fetchone()
    concursorobject.fetchall()
    global days, winningdays
    days = unamepswd[0]
    winningdays = unamepswd[1]


def nutrifitinitv():
    conn = createconnectionindb()
    concursorobject = conn.cursor()
    concursorobject.execute('SELECT * FROM userid WHERE did=1')

    unamepswd = concursorobject.fetchone()
    concursorobject.fetchall()
    weightuser = unamepswd[6]
    activityy = unamepswd[2]
    goall = unamepswd[7]
    bodytypee = unamepswd[3]
    global value
    value = nutrition(weightuser, activityy, goall, bodytypee)


class new_User(QFrame):
    # New_User index 1
    def __init__(self):
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        super(new_User, self).__init__()
        loadUi("NewUser.ui", self)
        self.pushButton_submit.clicked.connect(self.createnuer)
        self.pushButton_2.clicked.connect(lambda :goto_screen_index(0))
    def createnuer(self):
        try:
            conn = createconnectionindb()
            namefull = self.lineEdit.text()
            username = self.lineEdit_2.text()
            weight = self.lineEdit_3.text()
            blood_group = self.comboBox_2.currentText()
            body_type = self.comboBox.currentText()
            activity_now = self.comboBox_3.currentText()
            goal = self.comboBox_4.currentText()
            password = self.lineEdit_8.text()
            concursorobject = conn.cursor()

            concursorobject.execute("Delete from userid")
            conn.commit()
            concursorobject.fetchall()
            valuestoinsert = (username, password, activity_now, body_type, blood_group, namefull, weight, goal)
            concursorobject.execute(
                'INSERT INTO userid(username,password,activity,bodytype,bloodgrp,namefull,weight,goalw) VALUES(?, ?, ?, ?, ?, ?,?,?) '
                , valuestoinsert)

            conn.commit()

            QMessageBox.about(self,"","NEW USER CREATED")
            conn.close()

        except Exception as e:
            print("encounter error")


class changepassword(QFrame):
    # Change Password 2
    def __init__(self):
        super(changepassword, self).__init__()
        loadUi("changepassword.ui", self)
        self.pushButton.clicked.connect(self.passwordchange)
        self.pushButton_2.clicked.connect(lambda: goto_screen_index(0))

    def passwordchange(self):
        try:
            conn = createconnectionindb()
            namefull = self.lineEdit.text()
            bloodgroup = self.comboBox_2.currentText()
            pswrn = self.lineEdit_3.text()
            concursorobject = conn.cursor()
            concursorobject.execute('SELECT namefull,bloodgrp FROM userid WHERE namefull = ? and bloodgrp = ?',
                                    (namefull, bloodgroup))

            unamepswd = concursorobject.fetchone()
            concursorobject.fetchall()
            if unamepswd is None:
                raise Exception
            concursorobject.execute('UPDATE userid SET password = ? where namefull=?', (pswrn, namefull))

            conn.commit()
            conn.close()

        except Exception as e:
            print("encounter error")


class Gui_bmi(QFrame):
    # BMI index 4
    def __init__(self):
        super(Gui_bmi, self).__init__()
        loadUi("GUIbmi.ui", self)
        self.pushButtondaily.clicked.connect(lambda: goto_screen_index(3))
        self.pushButtonbmical.clicked.connect(lambda: goto_screen_index(4))
        self.pushButtonmeditation.clicked.connect(lambda: goto_screen_index(5))
        self.pushButtondiet.clicked.connect(lambda: goto_screen_index(6))
        self.pushButton_tips.clicked.connect(lambda: goto_screen_index(7))
        self.pushButton_progress.clicked.connect(lambda: goto_screen_index(8))
        self.pushButton_logout.clicked.connect(lambda: goto_screen_index(0))
        self.pushButton_BMICal.clicked.connect(self.wwbmi)
        self.pushButton_2.clicked.connect(self.initn)

    def initn(self):
        self.lcdNumber.display(0)
        self.spinBox.setValue(1)
        self.spinBox_2.setValue(1)
        self.lineEdit.setText("0")

    def wwbmi(self):
        height = (self.spinBox.value() * 12) + self.spinBox_2.value()
        height = height * 2.54
        weigt = self.lineEdit.text()
        weigt = int(weigt)
        test = int(bmi_calculator(height, weigt))
        print(test)
        self.lcdNumber.display(test)


class progressHistory(QFrame):
    # Progress history 8
    def __init__(self):
        super(progressHistory, self).__init__()
        loadUi("progressHistoryy.ui", self)
        self.pushButton_dailygoal.clicked.connect(lambda: goto_screen_index(3))
        self.pushButton_bmicalculator.clicked.connect(lambda: goto_screen_index(4))
        self.pushButton_meditation.clicked.connect(lambda: goto_screen_index(5))
        self.pushButton_dietplaner.clicked.connect(lambda: goto_screen_index(6))
        self.pushButton_both.clicked.connect(lambda: goto_screen_index(7))
        self.pushButton_progresshistory.clicked.connect(lambda: goto_screen_index(8))
        self.pushButton_logout.clicked.connect(lambda: goto_screen_index(0))
        self.label_4.setText(str(days))
        self.label_6.setText(str(winningdays))


def nutrifitinit():
    try:
        conn = createconnectionindb()
        concursorobject = conn.cursor()
        concursorobject.execute('SELECT * from currentnew WHERE id=1')
        unamepswd = concursorobject.fetchone()

        global currentcalburned, currentcaloriesc, currentwater, currentsletaken,currentstat

        currentcaloriesc = unamepswd[2]
        currentwater = unamepswd[0]
        currentcalburned = unamepswd[1]
        currentsletaken = unamepswd[3]
        currentstat=unamepswd[4]
        concursorobject.fetchall()
    except:
        print("Errorr")


def sectominsec(sc: int):
    mins = sc // 60
    secs = sc % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec


class meditation(QFrame):
    # meditation 5

    def __init__(self):
        super(meditation, self).__init__()
        self.time_left = 0
        loadUi("meditaton.ui", self)
        self.pushButton_dailygoal.clicked.connect(lambda: goto_screen_index(3))
        self.count = 0
        self.pushButton_bmicalculator.clicked.connect(lambda: goto_screen_index(4))
        self.pushButton_medtation.clicked.connect(lambda: goto_screen_index(5))
        self.pushButton_dietplanner.clicked.connect(lambda: goto_screen_index(6))
        self.pushButton_both.clicked.connect(lambda: goto_screen_index(7))
        self.pushButton_progresshistory.clicked.connect(lambda: goto_screen_index(8))
        self.pushButton_logout.clicked.connect(lambda: goto_screen_index(0))
        self.pushButton_starttimer.clicked.connect(lambda: self.strt())
        self.pushButton.clicked.connect(lambda: self.retimer())
        self.timer = QTimer(self)

    def strt(self):
        self.count = self.dial.value()
        self.time_left = self.count * 60
        self.timer.timeout.connect(self.nowtime)
        self.timer.start(1000)

    def nowtime(self):
        self.time_left = self.time_left - 1
        if self.time_left == 0:
            self.timer.stop()
        self.update_label()

    def update_label(self):
        minsec = sectominsec(self.time_left)
        self.label_4.setText(minsec)

    def retimer(self):
        self.dial.setValue(0)
        self.label_4.setText("00:00")
        self.timer.stop()


class tips(QFrame):
    # TIPS 7
    def __init__(self):
        super(tips, self).__init__()
        loadUi("tips.ui", self)
        self.lcdNumber.display(0)
        self.pushButton_dailygoal.clicked.connect(lambda: goto_screen_index(3))
        self.pushButton_bmicalculator.clicked.connect(lambda: goto_screen_index(4))
        self.pushButton_medtation.clicked.connect(lambda: goto_screen_index(5))
        self.pushButton_dietplanner.clicked.connect(lambda: goto_screen_index(6))
        self.pushButton_both.clicked.connect(lambda: goto_screen_index(7))
        self.pushButton_progresshistory.clicked.connect(lambda: goto_screen_index(8))
        self.pushButton_logout.clicked.connect(lambda: goto_screen_index(0))
        self.pushButton.clicked.connect(lambda: self.changelabelvalueone())
        self.pushButton_2.clicked.connect(lambda: self.clearthemeter())

    def changelabelvalueone(self):
        a = 1 + self.lcdNumber.value()
        self.lcdNumber.display(a)

    def clearthemeter(self):
        self.lcdNumber.display(0)


class dailygoal(QFrame):
    # Daily goal 3
    def __init__(self):
        super(dailygoal, self).__init__()
        loadUi("dailygoa.ui", self)
        self.pushButton_dailygoal.clicked.connect(lambda: goto_screen_index(3))
        self.pushButton_bmicalculator.clicked.connect(lambda: goto_screen_index(4))
        self.pushButton_medtation.clicked.connect(lambda: goto_screen_index(5))
        self.pushButton_dietplanner.clicked.connect(lambda: goto_screen_index(6))
        self.pushButton_both.clicked.connect(lambda: goto_screen_index(7))
        self.pushButton_progresshistory.clicked.connect(lambda: goto_screen_index(8))
        self.pushButton_logout.clicked.connect(lambda: goto_screen_index(0))
        self.label_2.setText(currentstat)
        self.lineEdit.setText(str(currentcaloriesc))
        self.lineEdit_2.setText(str(currentwater))
        self.lineEdit_3.setText(str(currentsletaken))
        self.lineEdit_4.setText(str(currentcalburned))

        self.label_10.setText("/" + str(value))
        self.pushButton_updatepercent_2.clicked.connect(self.updatewater)
        self.pushButton_updatepercent.clicked.connect(self.updatecaloriesburn)
    def updatewater(self):
        conn = createconnectionindb()
        concursorobject = conn.cursor()
        global currentwater, currentsletaken, currentcalburned, currentcaloriesc,value,currentstat
        currentwater = int(self.lineEdit_2.text())
        currentcalburned = int(self.lineEdit_4.text())
        currentcaloriesc = int(self.lineEdit.text())
        currentsletaken = int(self.lineEdit_3.text())
        if currentwater>=3 and currentsletaken>=7 and currentcalburned>=2400 and currentcaloriesc>=value:
            currentstat = "Achieved"
            self.lineEdit_2.setText(str(currentwater))
            self.lineEdit.setText(str(currentcaloriesc))
            self.lineEdit_3.setText(str(currentsletaken))
            self.lineEdit_4.setText(str(currentcalburned))
            self.label_2.setText(currentstat)
            concursorobject.execute("UPDATE currentnew  SET twater=? ,tcaloriesb=? ,tcaloriesco=?,tnidh=? ,tfull=? WHERE id=?",
                                    (currentwater, currentcalburned, currentcaloriesc, currentsletaken,currentstat, 1))
            conn.commit()
        else:
            currentstat = "Not 2Achieved"
            self.lineEdit_2.setText(str(currentwater))
            self.lineEdit.setText(str(currentcaloriesc))
            self.lineEdit_3.setText(str(currentsletaken))
            self.lineEdit_4.setText(str(currentcalburned))

            concursorobject.execute(
                "UPDATE currentnew  SET twater=? ,tcaloriesb=? ,tcaloriesco=?,tnidh=? ,tfull=? WHERE id=?",
                (currentwater, currentcalburned, currentcaloriesc, currentsletaken, currentstat, 1))
            conn.commit()

    def updatecaloriesburn(self):
        conn = createconnectionindb()
        global currentwater, currentsletaken, currentcalburned, currentcaloriesc, currentstat
        currentwater = int(self.lineEdit_2.text())
        currentcalburned = int(self.lineEdit_4.text())
        currentcaloriesc = int(self.lineEdit.text())
        currentsletaken = int(self.lineEdit_3.text())
        currentstat = self.label_2.text()
        concursorobject = conn.cursor()
        llt = concursorobject.execute('SELECT * FROM phistory WHERE id=1')
        lltt=llt.fetchone()

        llt.fetchall()
        tdays = (1 + int(lltt[0]))
        if currentstat == "Achieved":
            days = (1 + int(lltt[1]))
            concursorobject.execute('UPDATE phistory  SET daysno=? ,todayachieved=? WHERE id=1 ',
                                    (tdays,days)
                                    )
            conn.commit()
            currentwater = 0
            currentcalburned = 0
            currentcaloriesc = 0
            currentsletaken = 0
            currentstat ="Not Achieved"
            concursorobject.execute(
                "UPDATE currentnew  SET twater=? ,tcaloriesb=? ,tcaloriesco=?,tnidh=? ,tfull=? WHERE id=?",
                (currentwater, currentcalburned, currentcaloriesc, currentsletaken, currentstat, 1))
            conn.commit()
            self.lineEdit_4.setText("0")
            self.lineEdit_2.setText("0")
            self.lineEdit_3.setText("0")
            self.lineEdit.setText("0")
            self.label_2.setText(currentstat)
        else :
            days =int(lltt[1])
            concursorobject.execute('UPDATE phistory  SET daysno=? ,todayachieved=? WHERE id=1 ',
                                    (tdays, days)
                                    )
            conn.commit()
            currentwater = 0
            currentcalburned = 0
            currentcaloriesc =0
            currentsletaken = 0
            currentstat = "Not Achieved"
            days = lltt[1]
            concursorobject.execute(
                "UPDATE currentnew  SET twater=? ,tcaloriesb=? ,tcaloriesco=?,tnidh=? ,tfull=? WHERE id=?",
                (currentwater, currentcalburned, currentcaloriesc, currentsletaken, currentstat,1))
            conn.commit()
            self.lineEdit_4.setText("0")
            self.lineEdit_2.setText("0")
            self.lineEdit_3.setText("0")
            self.lineEdit.setText("0")
            self.label_2.setText(currentstat)

class diet(QFrame):
    # diet 6
    def __init__(self):
        super(diet, self).__init__()
        loadUi("diet..ui", self)
        self.pushButton_dailygoal.clicked.connect(lambda: goto_screen_index(3))
        self.pushButton_bmicalculator.clicked.connect(lambda: goto_screen_index(4))
        self.pushButton_meditation.clicked.connect(lambda: goto_screen_index(5))
        self.pushButton_dietplanner.clicked.connect(lambda: goto_screen_index(6))
        self.pushButton_both.clicked.connect(lambda: goto_screen_index(7))
        self.pushButton_progresshistory.clicked.connect(lambda: goto_screen_index(8))
        self.label_6.setText("/" + str(value))
        self.pushButton_logout.clicked.connect(lambda: goto_screen_index(0))
        self.pushButton.clicked.connect(self.caloriestogett)
        self.pushButton_3.clicked.connect(self.caloriestoget)
        self.pushButton_4.clicked.connect(self.caloriestogetth)
        self.pushButton_2.clicked.connect(self.addcal)
        self.pushButton_5.clicked.connect(self.addcalo)
        self.pushButton_6.clicked.connect(self.addcaloo)

    def addcaloo(self):
        cal = int(self.label_10.text())
        tes = int(self.label.text())
        self.label.setText(str(tes + cal))

    def addcalo(self):
        cal = int(self.label_9.text())
        tes = int(self.label.text())
        self.label.setText(str(tes + cal))

    def addcal(self):
        cal = int(self.label_8.text())
        tes = int(self.label.text())
        self.label.setText(str(tes + cal))

    def caloriestoget(self):
        conn = createconnectionindb()

        tname = self.comboBox_3.currentText()

        concursorobject = conn.cursor()
        concursorobject.execute('SELECT tcalorie FROM meat WHERE tname= ?',
                                (tname,))

        unamepswd = concursorobject.fetchone()
        concursorobject.fetchall()
        ffcal = unamepswd[0]
        repet = self.comboBox_6.currentText()
        repet = int(repet)
        self.label_9.setText(str(ffcal * repet))

    def caloriestogetth(self):
        conn = createconnectionindb()

        tname = self.comboBox_4.currentText()

        concursorobject = conn.cursor()
        concursorobject.execute('SELECT tcalorie FROM meat WHERE tname= ?',
                                (tname,))

        unamepswd = concursorobject.fetchone()
        concursorobject.fetchall()
        ffcal = unamepswd[0]
        repet = self.comboBox_7.currentText()
        repet = int(repet)
        self.label_10.setText(str(ffcal * repet))

    def caloriestogett(self):
        conn = createconnectionindb()

        tname = self.comboBox_2.currentText()

        concursorobject = conn.cursor()
        concursorobject.execute('SELECT tcalorie FROM meat WHERE tname= ?',
                                (tname,))

        unamepswd = concursorobject.fetchone()
        concursorobject.fetchall()
        ffcal = unamepswd[0]
        repet = self.comboBox_5.currentText()
        repet = int(repet)
        self.label_8.setText(str(ffcal * repet))
    # self.pushButton.clicked.connect(a=self.comboBox.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    # create objects of the windows
    nutrifitinit()
    nutrifitinitv()
    history()
    # outer widgets
    main_window_login_obj = MainWindow()
    new_user_obj = new_User()
    change_password_obj = changepassword()

    # internal widgets
    daily_goal_obj = dailygoal()
    BMI_obj = Gui_bmi()
    meditaion_ = meditation()
    diet_planner_obj = diet()
    tips_obj = tips()
    progress_history_obj = progressHistory()

    # add widgets to the pos

    # outer widgets
    widget.addWidget(main_window_login_obj)
    widget.addWidget(new_user_obj)
    widget.addWidget(change_password_obj)

    # internal widgets
    widget.addWidget(daily_goal_obj)
    widget.addWidget(BMI_obj)
    widget.addWidget(meditaion_)
    widget.addWidget(diet_planner_obj)
    widget.addWidget(tips_obj)
    widget.addWidget(progress_history_obj)

    # start the application
    # widget.setFixedHeight(1982)
    # widget.setFixedWidth(1080)
    widget.show()
    sys.exit(app.exec_())
