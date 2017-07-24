# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled3.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(266, 302)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(60, 260, 99, 27))
        self.pushButton.setObjectName("pushButton")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(Form)
        self.dateTimeEdit.setGeometry(QtCore.QRect(70, 10, 194, 27))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit_2 = QtWidgets.QDateTimeEdit(Form)
        self.dateTimeEdit_2.setGeometry(QtCore.QRect(70, 50, 194, 27))
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.dateTimeEdit_3 = QtWidgets.QDateTimeEdit(Form)
        self.dateTimeEdit_3.setGeometry(QtCore.QRect(70, 90, 194, 27))
        self.dateTimeEdit_3.setObjectName("dateTimeEdit_3")
        self.dateTimeEdit_4 = QtWidgets.QDateTimeEdit(Form)
        self.dateTimeEdit_4.setGeometry(QtCore.QRect(70, 130, 194, 27))
        self.dateTimeEdit_4.setObjectName("dateTimeEdit_4")
        self.dateTimeEdit_5 = QtWidgets.QDateTimeEdit(Form)
        self.dateTimeEdit_5.setGeometry(QtCore.QRect(70, 170, 194, 27))
        self.dateTimeEdit_5.setObjectName("dateTimeEdit_5")
        self.dateTimeEdit_6 = QtWidgets.QDateTimeEdit(Form)
        self.dateTimeEdit_6.setGeometry(QtCore.QRect(70, 210, 194, 27))
        self.dateTimeEdit_6.setObjectName("dateTimeEdit_6")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 70, 31, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 160, 31, 21))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 10, 21, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 21, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 170, 21, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 50, 31, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(40, 130, 31, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(40, 210, 31, 21))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Расписание"))
        self.pushButton.setText(_translate("Form", "Установить"))
        self.pushButton_2.setText(_translate("Form", "+"))
        self.pushButton_3.setText(_translate("Form", "+"))
        self.label.setText(_translate("Form", "C :"))
        self.label_2.setText(_translate("Form", "C :"))
        self.label_3.setText(_translate("Form", "C :"))
        self.label_4.setText(_translate("Form", "По :"))
        self.label_5.setText(_translate("Form", "По :"))
        self.label_6.setText(_translate("Form", "По :"))




