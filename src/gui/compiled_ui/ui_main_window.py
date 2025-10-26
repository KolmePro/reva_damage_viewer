# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, Qt)
from PySide6.QtGui import (QAction, QIcon)
from PySide6.QtWidgets import (QCheckBox, QFrame, QGridLayout,
                               QGroupBox, QHBoxLayout, QLabel,
                               QMenuBar, QSizePolicy, QSpacerItem,
                               QStatusBar, QTableView, QToolBar, QVBoxLayout,
                               QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 835)
        MainWindow.setMinimumSize(QSize(1200, 800))
        icon = QIcon(QIcon.fromTheme(u"accessories-calculator"))
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QSize(36, 36))
        self.action_set_game_folder = QAction(MainWindow)
        self.action_set_game_folder.setObjectName(u"action_set_game_folder")
        icon1 = QIcon(QIcon.fromTheme(u"folder"))
        self.action_set_game_folder.setIcon(icon1)
        self.action_load_last_log = QAction(MainWindow)
        self.action_load_last_log.setObjectName(u"action_load_last_log")
        self.action_load_last_log.setEnabled(True)
        icon2 = QIcon(QIcon.fromTheme(u"media-skip-forward"))
        self.action_load_last_log.setIcon(icon2)
        self.action_load_last_log.setMenuRole(QAction.MenuRole.NoRole)
        self.action_clear_selection = QAction(MainWindow)
        self.action_clear_selection.setObjectName(u"action_clear_selection")
        icon3 = QIcon(QIcon.fromTheme(u"edit-clear"))
        self.action_clear_selection.setIcon(icon3)
        self.action_clear_selection.setMenuRole(QAction.MenuRole.NoRole)
        self.central_widget = QWidget(MainWindow)
        self.central_widget.setObjectName(u"central_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.horizontalLayout_4 = QHBoxLayout(self.central_widget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.verticalWidget = QWidget(self.central_widget)
        self.verticalWidget.setObjectName(u"verticalWidget")
        self.verticalWidget.setMinimumSize(QSize(400, 0))
        self.verticalWidget.setMaximumSize(QSize(400, 16777215))
        self.verticalLayout = QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.verticalWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.cb_attack_o = QCheckBox(self.groupBox)
        self.cb_attack_o.setObjectName(u"cb_attack_o")
        self.cb_attack_o.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_o, 6, 0, 1, 1)

        self.cb_attack_p = QCheckBox(self.groupBox)
        self.cb_attack_p.setObjectName(u"cb_attack_p")
        self.cb_attack_p.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_p, 5, 0, 1, 1)

        self.cb_attack_block = QCheckBox(self.groupBox)
        self.cb_attack_block.setObjectName(u"cb_attack_block")
        self.cb_attack_block.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_block, 3, 0, 1, 1)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 1, 0, 1, 2)

        self.cb_outgoing_spirit_damage = QCheckBox(self.groupBox)
        self.cb_outgoing_spirit_damage.setObjectName(u"cb_outgoing_spirit_damage")
        self.cb_outgoing_spirit_damage.setChecked(True)

        self.gridLayout.addWidget(self.cb_outgoing_spirit_damage, 0, 0, 1, 1)

        self.cb_attack_m = QCheckBox(self.groupBox)
        self.cb_attack_m.setObjectName(u"cb_attack_m")
        self.cb_attack_m.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_m, 5, 1, 1, 1)

        self.cb_attack_common = QCheckBox(self.groupBox)
        self.cb_attack_common.setObjectName(u"cb_attack_common")
        self.cb_attack_common.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_common, 2, 0, 1, 1)

        self.cb_attack_combo = QCheckBox(self.groupBox)
        self.cb_attack_combo.setObjectName(u"cb_attack_combo")
        self.cb_attack_combo.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_combo, 3, 1, 1, 1)

        self.cb_attack_critical = QCheckBox(self.groupBox)
        self.cb_attack_critical.setObjectName(u"cb_attack_critical")
        self.cb_attack_critical.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_critical, 2, 1, 1, 1)

        self.cb_incoming_spirit_damage = QCheckBox(self.groupBox)
        self.cb_incoming_spirit_damage.setObjectName(u"cb_incoming_spirit_damage")
        self.cb_incoming_spirit_damage.setChecked(True)

        self.gridLayout.addWidget(self.cb_incoming_spirit_damage, 0, 1, 1, 1)

        self.line_3 = QFrame(self.groupBox)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_3, 4, 0, 1, 2)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.groupBox_2 = QGroupBox(self.verticalWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 0, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 2, 2, 1, 1)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 0, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 3, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 1, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 2, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 4, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 2, 4, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 2, 3, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)


        self.horizontalLayout_4.addWidget(self.verticalWidget)

        self.line = QFrame(self.central_widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.damage_table_view = QTableView(self.central_widget)
        self.damage_table_view.setObjectName(u"damage_table_view")

        self.verticalLayout_2.addWidget(self.damage_table_view)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.central_widget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolbar = QToolBar(MainWindow)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setMinimumSize(QSize(0, 0))
        self.toolbar.setMovable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 33))
        MainWindow.setMenuBar(self.menubar)

        self.toolbar.addAction(self.action_load_last_log)
        self.toolbar.addAction(self.action_set_game_folder)
        self.toolbar.addAction(self.action_clear_selection)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440 \u0443\u0440\u043e\u043d\u0430", None))
        self.action_set_game_folder.setText(QCoreApplication.translate("MainWindow", u"&\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u043f\u0430\u043f\u043a\u0443 \u0441 \u0438\u0433\u0440\u043e\u0439", None))
#if QT_CONFIG(tooltip)
        self.action_set_game_folder.setToolTip(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0430\u043f\u043a\u0443 \u0441 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043d\u043e\u0439 \u0438\u0433\u0440\u043e\u0439.", None))
#endif // QT_CONFIG(tooltip)
        self.action_load_last_log.setText(QCoreApplication.translate("MainWindow", u"$\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0438\u0439 \u043b\u043e\u0433", None))
#if QT_CONFIG(tooltip)
        self.action_load_last_log.setToolTip(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0438\u0439 \u043b\u043e\u0433 \u0447\u0430\u0442\u0430", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_load_last_log.setShortcut(QCoreApplication.translate("MainWindow", u"F5", None))
#endif // QT_CONFIG(shortcut)
        self.action_clear_selection.setText(QCoreApplication.translate("MainWindow", u"&\u0421\u043d\u044f\u0442\u044c \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u0438\u0435", None))
#if QT_CONFIG(tooltip)
        self.action_clear_selection.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u043d\u044f\u0442\u044c \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u0441\u043e \u0432\u0441\u0435\u0445 \u0441\u0442\u0440\u043e\u0447\u0435\u043a \u0443\u0440\u043e\u043d\u0430.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_clear_selection.setShortcut(QCoreApplication.translate("MainWindow", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0438\u043b\u044c\u0442\u0440\u044b", None))
        self.cb_attack_o.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u044b\u0447\u043d\u044b\u0439", None))
        self.cb_attack_p.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0438\u043b\u0430 \u0430\u0442\u0430\u043a\u0438", None))
        self.cb_attack_block.setText(QCoreApplication.translate("MainWindow", u"\u0411\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f", None))
        self.cb_outgoing_spirit_damage.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0440\u043e\u043d \u043e\u0442 \u0434\u0443\u0445\u043e\u0432", None))
        self.cb_attack_m.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0438\u043b\u0430 \u0437\u0430\u043a\u043b\u0438\u043d\u0430\u043d\u0438\u0439", None))
        self.cb_attack_common.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u044b\u0447\u043d\u044b\u0435 \u0430\u0442\u0430\u043a\u0438", None))
        self.cb_attack_combo.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043c\u0431\u043e-\u0443\u0434\u0430\u0440\u044b", None))
        self.cb_attack_critical.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0440\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0443\u0434\u0430\u0440\u044b", None))
        self.cb_incoming_spirit_damage.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0440\u043e\u043d \u043f\u043e \u0434\u0443\u0445\u0430\u043c", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0440\u0435\u0434\u043d\u0438\u0439", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0434\u0438\u0430\u043d\u043d\u044b\u0439", None))
        self.toolbar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

