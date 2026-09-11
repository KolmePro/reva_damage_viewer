# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'skill_damage_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QHeaderView, QLabel, QSizePolicy,
    QTableView, QVBoxLayout, QWidget)

class Ui_SkillDamageDialog(object):
    def setupUi(self, SkillDamageDialog):
        if not SkillDamageDialog.objectName():
            SkillDamageDialog.setObjectName(u"SkillDamageDialog")
        SkillDamageDialog.setSizeGripEnabled(True)
        SkillDamageDialog.resize(1200, 480)
        self.verticalLayout = QVBoxLayout(SkillDamageDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scope_label = QLabel(SkillDamageDialog)
        self.scope_label.setObjectName(u"scope_label")
        self.scope_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.scope_label)

        self.damage_table = QTableView(SkillDamageDialog)
        self.damage_table.setObjectName(u"damage_table")
        self.damage_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.damage_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.damage_table.setAlternatingRowColors(True)
        self.damage_table.setSortingEnabled(True)
        self.damage_table.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.damage_table)

        self.summary_label = QLabel(SkillDamageDialog)
        self.summary_label.setObjectName(u"summary_label")
        self.summary_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.summary_label)

        self.button_box = QDialogButtonBox(SkillDamageDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setStandardButtons(QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.button_box)


        self.retranslateUi(SkillDamageDialog)
        self.button_box.rejected.connect(SkillDamageDialog.reject)

        QMetaObject.connectSlotsByName(SkillDamageDialog)
    # setupUi

    def retranslateUi(self, SkillDamageDialog):
        SkillDamageDialog.setWindowTitle(QCoreApplication.translate("SkillDamageDialog", u"\u0410\u043d\u0430\u043b\u0438\u0437 \u0443\u0440\u043e\u043d\u0430", None))
        self.scope_label.setText(QCoreApplication.translate("SkillDamageDialog", u"\u0412\u0441\u0435 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0435\u043c\u044b\u0435 \u0441\u0442\u0440\u043e\u043a\u0438 \u0441 \u0443\u0447\u0451\u0442\u043e\u043c \u0444\u0438\u043b\u044c\u0442\u0440\u043e\u0432 \u0438 \u0432\u0440\u0435\u043c\u0435\u043d\u0438, \u043d\u0435\u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e \u043e\u0442 \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u0438\u044f \u0441\u0442\u0440\u043e\u043a. \u0428\u0430\u043d\u0441\u044b \u0438 \u0441\u0440\u0435\u0434\u043d\u0438\u0439 \u0443\u0440\u043e\u043d \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b \u043f\u043e \u0432\u0441\u0435\u043c \u0430\u0442\u0430\u043a\u0430\u043c \u0443\u043c\u0435\u043d\u0438\u044f, \u0432\u043a\u043b\u044e\u0447\u0430\u044f \u043f\u0440\u043e\u043c\u0430\u0445\u0438.", None))
        self.summary_label.setText(QCoreApplication.translate("SkillDamageDialog", u"\u041d\u0435\u0442 \u0437\u0430\u043f\u0438\u0441\u0435\u0439 \u043e \u043d\u0430\u043d\u0435\u0441\u0451\u043d\u043d\u043e\u043c \u0443\u0440\u043e\u043d\u0435.", None))
#if QT_CONFIG(tooltip)
        self.summary_label.setToolTip(QCoreApplication.translate("SkillDamageDialog", u"\u041e\u0431\u0449\u0438\u0435 \u0448\u0430\u043d\u0441\u044b \u0438 \u0441\u0440\u0435\u0434\u043d\u0438\u0439 \u0443\u0440\u043e\u043d \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u044b\u0432\u0430\u044e\u0442\u0441\u044f \u043e\u0442 \u043e\u0431\u0449\u0435\u0433\u043e \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u0430 \u0430\u0442\u0430\u043a, \u0432\u043a\u043b\u044e\u0447\u0430\u044f \u043f\u0440\u043e\u043c\u0430\u0445\u0438.", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

