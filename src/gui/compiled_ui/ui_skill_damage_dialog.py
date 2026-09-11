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
    QDialogButtonBox, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

class Ui_SkillDamageDialog(object):
    def setupUi(self, SkillDamageDialog):
        if not SkillDamageDialog.objectName():
            SkillDamageDialog.setObjectName(u"SkillDamageDialog")
        SkillDamageDialog.setSizeGripEnabled(True)
        SkillDamageDialog.resize(1200, 580)
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

        self.summary_panel = QWidget(SkillDamageDialog)
        self.summary_panel.setObjectName(u"summary_panel")
        self.summary_panel.setStyleSheet(u"QFrame[summaryCard=\"true\"] {\n"
" background-color: palette(base);\n"
" border: 1px solid palette(mid);\n"
" border-radius: 8px;\n"
"}\n"
"QFrame#total_damage_card { border-top: 3px solid #6f9ed8; }\n"
"QLabel { background: transparent; border: none; }\n"
"QLabel[summaryRole=\"value\"] { font-size: 22px; font-weight: 600; }\n"
"QLabel[summaryRole=\"detail\"] { font-size: 12px; }\n"
"QLabel#summary_label { font-weight: 600; }")
        self.summary_layout = QVBoxLayout(self.summary_panel)
        self.summary_layout.setSpacing(8)
        self.summary_layout.setObjectName(u"summary_layout")
        self.summary_layout.setContentsMargins(0, 8, 0, 0)
        self.summary_label = QLabel(self.summary_panel)
        self.summary_label.setObjectName(u"summary_label")
        self.summary_label.setWordWrap(True)

        self.summary_layout.addWidget(self.summary_label)

        self.summary_cards_layout = QHBoxLayout()
        self.summary_cards_layout.setSpacing(10)
        self.summary_cards_layout.setObjectName(u"summary_cards_layout")
        self.total_damage_card = QFrame(self.summary_panel)
        self.total_damage_card.setObjectName(u"total_damage_card")
        self.total_damage_card.setProperty(u"summaryCard", True)
        self.total_damage_layout = QVBoxLayout(self.total_damage_card)
        self.total_damage_layout.setObjectName(u"total_damage_layout")
        self.total_damage_title = QLabel(self.total_damage_card)
        self.total_damage_title.setObjectName(u"total_damage_title")

        self.total_damage_layout.addWidget(self.total_damage_title)

        self.total_damage_value = QLabel(self.total_damage_card)
        self.total_damage_value.setObjectName(u"total_damage_value")
        self.total_damage_value.setProperty(u"summaryRole", u"value")
        self.total_damage_value.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.total_damage_layout.addWidget(self.total_damage_value)

        self.total_damage_detail = QLabel(self.total_damage_card)
        self.total_damage_detail.setObjectName(u"total_damage_detail")
        self.total_damage_detail.setProperty(u"summaryRole", u"detail")

        self.total_damage_layout.addWidget(self.total_damage_detail)


        self.summary_cards_layout.addWidget(self.total_damage_card)

        self.total_dps_card = QFrame(self.summary_panel)
        self.total_dps_card.setObjectName(u"total_dps_card")
        self.total_dps_card.setProperty(u"summaryCard", True)
        self.total_dps_layout = QVBoxLayout(self.total_dps_card)
        self.total_dps_layout.setObjectName(u"total_dps_layout")
        self.total_dps_title = QLabel(self.total_dps_card)
        self.total_dps_title.setObjectName(u"total_dps_title")

        self.total_dps_layout.addWidget(self.total_dps_title)

        self.total_dps_value = QLabel(self.total_dps_card)
        self.total_dps_value.setObjectName(u"total_dps_value")
        self.total_dps_value.setProperty(u"summaryRole", u"value")
        self.total_dps_value.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.total_dps_layout.addWidget(self.total_dps_value)

        self.total_dps_detail = QLabel(self.total_dps_card)
        self.total_dps_detail.setObjectName(u"total_dps_detail")
        self.total_dps_detail.setProperty(u"summaryRole", u"detail")

        self.total_dps_layout.addWidget(self.total_dps_detail)


        self.summary_cards_layout.addWidget(self.total_dps_card)

        self.total_attacks_card = QFrame(self.summary_panel)
        self.total_attacks_card.setObjectName(u"total_attacks_card")
        self.total_attacks_card.setProperty(u"summaryCard", True)
        self.total_attacks_layout = QVBoxLayout(self.total_attacks_card)
        self.total_attacks_layout.setObjectName(u"total_attacks_layout")
        self.total_attacks_title = QLabel(self.total_attacks_card)
        self.total_attacks_title.setObjectName(u"total_attacks_title")

        self.total_attacks_layout.addWidget(self.total_attacks_title)

        self.total_attacks_value = QLabel(self.total_attacks_card)
        self.total_attacks_value.setObjectName(u"total_attacks_value")
        self.total_attacks_value.setProperty(u"summaryRole", u"value")
        self.total_attacks_value.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.total_attacks_layout.addWidget(self.total_attacks_value)

        self.total_attacks_detail = QLabel(self.total_attacks_card)
        self.total_attacks_detail.setObjectName(u"total_attacks_detail")
        self.total_attacks_detail.setProperty(u"summaryRole", u"detail")

        self.total_attacks_layout.addWidget(self.total_attacks_detail)


        self.summary_cards_layout.addWidget(self.total_attacks_card)

        self.total_critical_card = QFrame(self.summary_panel)
        self.total_critical_card.setObjectName(u"total_critical_card")
        self.total_critical_card.setProperty(u"summaryCard", True)
        self.total_critical_layout = QVBoxLayout(self.total_critical_card)
        self.total_critical_layout.setObjectName(u"total_critical_layout")
        self.total_critical_title = QLabel(self.total_critical_card)
        self.total_critical_title.setObjectName(u"total_critical_title")

        self.total_critical_layout.addWidget(self.total_critical_title)

        self.total_critical_value = QLabel(self.total_critical_card)
        self.total_critical_value.setObjectName(u"total_critical_value")
        self.total_critical_value.setProperty(u"summaryRole", u"value")
        self.total_critical_value.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.total_critical_layout.addWidget(self.total_critical_value)

        self.total_critical_detail = QLabel(self.total_critical_card)
        self.total_critical_detail.setObjectName(u"total_critical_detail")
        self.total_critical_detail.setProperty(u"summaryRole", u"detail")

        self.total_critical_layout.addWidget(self.total_critical_detail)


        self.summary_cards_layout.addWidget(self.total_critical_card)

        self.total_misses_card = QFrame(self.summary_panel)
        self.total_misses_card.setObjectName(u"total_misses_card")
        self.total_misses_card.setProperty(u"summaryCard", True)
        self.total_misses_layout = QVBoxLayout(self.total_misses_card)
        self.total_misses_layout.setObjectName(u"total_misses_layout")
        self.total_misses_title = QLabel(self.total_misses_card)
        self.total_misses_title.setObjectName(u"total_misses_title")

        self.total_misses_layout.addWidget(self.total_misses_title)

        self.total_misses_value = QLabel(self.total_misses_card)
        self.total_misses_value.setObjectName(u"total_misses_value")
        self.total_misses_value.setProperty(u"summaryRole", u"value")
        self.total_misses_value.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.total_misses_layout.addWidget(self.total_misses_value)

        self.total_misses_detail = QLabel(self.total_misses_card)
        self.total_misses_detail.setObjectName(u"total_misses_detail")
        self.total_misses_detail.setProperty(u"summaryRole", u"detail")

        self.total_misses_layout.addWidget(self.total_misses_detail)


        self.summary_cards_layout.addWidget(self.total_misses_card)

        self.total_average_card = QFrame(self.summary_panel)
        self.total_average_card.setObjectName(u"total_average_card")
        self.total_average_card.setProperty(u"summaryCard", True)
        self.total_average_layout = QVBoxLayout(self.total_average_card)
        self.total_average_layout.setObjectName(u"total_average_layout")
        self.total_average_title = QLabel(self.total_average_card)
        self.total_average_title.setObjectName(u"total_average_title")

        self.total_average_layout.addWidget(self.total_average_title)

        self.total_average_value = QLabel(self.total_average_card)
        self.total_average_value.setObjectName(u"total_average_value")
        self.total_average_value.setProperty(u"summaryRole", u"value")
        self.total_average_value.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.total_average_layout.addWidget(self.total_average_value)

        self.total_average_detail = QLabel(self.total_average_card)
        self.total_average_detail.setObjectName(u"total_average_detail")
        self.total_average_detail.setProperty(u"summaryRole", u"detail")

        self.total_average_layout.addWidget(self.total_average_detail)


        self.summary_cards_layout.addWidget(self.total_average_card)

        self.summary_cards_layout.setStretch(0, 1)
        self.summary_cards_layout.setStretch(1, 1)
        self.summary_cards_layout.setStretch(2, 1)
        self.summary_cards_layout.setStretch(3, 1)
        self.summary_cards_layout.setStretch(4, 1)
        self.summary_cards_layout.setStretch(5, 1)

        self.summary_layout.addLayout(self.summary_cards_layout)


        self.verticalLayout.addWidget(self.summary_panel)

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
        self.scope_label.setText(QCoreApplication.translate("SkillDamageDialog", u"\u0410\u043d\u0430\u043b\u0438\u0437 \u0432\u0441\u0435\u0445 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0435\u043c\u044b\u0445 \u0437\u0430\u043f\u0438\u0441\u0435\u0439 \u0441 \u0443\u0447\u0451\u0442\u043e\u043c \u0444\u0438\u043b\u044c\u0442\u0440\u043e\u0432 \u0438 \u0432\u0440\u0435\u043c\u0435\u043d\u0438.", None))
#if QT_CONFIG(tooltip)
        self.scope_label.setToolTip(QCoreApplication.translate("SkillDamageDialog", u"\u0428\u0430\u043d\u0441\u044b \u0438 \u0441\u0440\u0435\u0434\u043d\u0438\u0439 \u0443\u0440\u043e\u043d \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b \u043f\u043e \u0432\u0441\u0435\u043c \u0430\u0442\u0430\u043a\u0430\u043c \u0443\u043c\u0435\u043d\u0438\u044f \u0432 \u0432\u044b\u0431\u043e\u0440\u043a\u0435, \u0432\u043a\u043b\u044e\u0447\u0430\u044f \u043f\u0440\u043e\u043c\u0430\u0445\u0438.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.summary_panel.setToolTip(QCoreApplication.translate("SkillDamageDialog", u"\u041e\u0431\u0449\u0438\u0435 \u0448\u0430\u043d\u0441\u044b \u0438 \u0441\u0440\u0435\u0434\u043d\u0438\u0439 \u0443\u0440\u043e\u043d \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u044b\u0432\u0430\u044e\u0442\u0441\u044f \u043e\u0442 \u043e\u0431\u0449\u0435\u0433\u043e \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u0430 \u0430\u0442\u0430\u043a, \u0432\u043a\u043b\u044e\u0447\u0430\u044f \u043f\u0440\u043e\u043c\u0430\u0445\u0438.", None))
#endif // QT_CONFIG(tooltip)
        self.summary_label.setText(QCoreApplication.translate("SkillDamageDialog", u"\u0418\u0442\u043e\u0433\u043e \u043f\u043e \u0432\u044b\u0431\u043e\u0440\u043a\u0435", None))
        self.total_damage_title.setText(QCoreApplication.translate("SkillDamageDialog", u"\u041e\u0431\u0449\u0438\u0439 \u0443\u0440\u043e\u043d", None))
        self.total_damage_value.setText(QCoreApplication.translate("SkillDamageDialog", u"0", None))
        self.total_damage_detail.setText(QCoreApplication.translate("SkillDamageDialog", u"\u043f\u043e \u0432\u0441\u0435\u043c \u0443\u043c\u0435\u043d\u0438\u044f\u043c", None))
#if QT_CONFIG(tooltip)
        self.total_dps_card.setToolTip(QCoreApplication.translate("SkillDamageDialog", u"\u041e\u0431\u0449\u0438\u0439 \u0443\u0440\u043e\u043d / \u0432\u0440\u0435\u043c\u044f \u043c\u0435\u0436\u0434\u0443 \u043f\u0435\u0440\u0432\u043e\u0439 \u0438 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u0437\u0430\u043f\u0438\u0441\u044c\u044e \u0443\u0440\u043e\u043d\u0430 \u0432 \u0432\u044b\u0431\u043e\u0440\u043a\u0435, \u0432\u043a\u043b\u044e\u0447\u0430\u044f \u043f\u0430\u0443\u0437\u044b \u0438 \u043e\u0442\u0440\u0430\u0436\u0451\u043d\u043d\u044b\u0439 \u0443\u0440\u043e\u043d. \u041f\u0440\u0438 \u043d\u0443\u043b\u0435\u0432\u043e\u0439 \u0434\u043b\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u043f\u043e\u043a\u0430\u0437\u0430\u043d \u043f\u0440\u043e\u0447\u0435\u0440\u043a.", None))
#endif // QT_CONFIG(tooltip)
        self.total_dps_title.setText(QCoreApplication.translate("SkillDamageDialog", u"DPS", None))
        self.total_dps_value.setText(QCoreApplication.translate("SkillDamageDialog", u"\u2014", None))
        self.total_dps_detail.setText(QCoreApplication.translate("SkillDamageDialog", u"\u0443\u0440\u043e\u043d \u0432 \u0441\u0435\u043a\u0443\u043d\u0434\u0443", None))
        self.total_attacks_title.setText(QCoreApplication.translate("SkillDamageDialog", u"\u0410\u0442\u0430\u043a\u0438", None))
        self.total_attacks_value.setText(QCoreApplication.translate("SkillDamageDialog", u"0", None))
        self.total_attacks_detail.setText(QCoreApplication.translate("SkillDamageDialog", u"\u0432\u043a\u043b\u044e\u0447\u0430\u044f \u043f\u0440\u043e\u043c\u0430\u0445\u0438", None))
        self.total_critical_title.setText(QCoreApplication.translate("SkillDamageDialog", u"\u041a\u0440\u0438\u0442\u044b", None))
        self.total_critical_value.setText(QCoreApplication.translate("SkillDamageDialog", u"0", None))
        self.total_critical_detail.setText(QCoreApplication.translate("SkillDamageDialog", u"0.0% \u0432\u0441\u0435\u0445 \u0430\u0442\u0430\u043a", None))
        self.total_misses_title.setText(QCoreApplication.translate("SkillDamageDialog", u"\u041f\u0440\u043e\u043c\u0430\u0445\u0438", None))
        self.total_misses_value.setText(QCoreApplication.translate("SkillDamageDialog", u"0", None))
        self.total_misses_detail.setText(QCoreApplication.translate("SkillDamageDialog", u"0.0% \u0432\u0441\u0435\u0445 \u0430\u0442\u0430\u043a", None))
        self.total_average_title.setText(QCoreApplication.translate("SkillDamageDialog", u"\u0421\u0440\u0435\u0434\u043d\u0438\u0439 \u0443\u0440\u043e\u043d", None))
        self.total_average_value.setText(QCoreApplication.translate("SkillDamageDialog", u"0", None))
        self.total_average_detail.setText(QCoreApplication.translate("SkillDamageDialog", u"\u043d\u0430 \u043e\u0434\u043d\u0443 \u0430\u0442\u0430\u043a\u0443", None))
    # retranslateUi

