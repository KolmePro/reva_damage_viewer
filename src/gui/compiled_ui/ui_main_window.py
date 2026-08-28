# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QSizePolicy,
    QSpacerItem, QStatusBar, QTableView, QToolBar,
    QToolButton, QVBoxLayout, QWidget)

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
        self.action_load_log_file = QAction(MainWindow)
        self.action_load_log_file.setObjectName(u"action_load_log_file")
        self.action_load_log_file.setMenuRole(QAction.MenuRole.NoRole)
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
        self.cb_your_effects = QCheckBox(self.groupBox)
        self.cb_your_effects.setObjectName(u"cb_your_effects")
        self.cb_your_effects.setChecked(True)

        self.gridLayout.addWidget(self.cb_your_effects, 9, 0, 1, 1)

        self.cb_attack_m = QCheckBox(self.groupBox)
        self.cb_attack_m.setObjectName(u"cb_attack_m")
        self.cb_attack_m.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_m, 14, 1, 1, 1)

        self.cb_not_your_effects = QCheckBox(self.groupBox)
        self.cb_not_your_effects.setObjectName(u"cb_not_your_effects")
        self.cb_not_your_effects.setChecked(True)

        self.gridLayout.addWidget(self.cb_not_your_effects, 9, 1, 1, 1)

        self.line_4 = QFrame(self.groupBox)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_4, 10, 0, 1, 2)

        self.line_7 = QFrame(self.groupBox)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_7, 1, 0, 1, 2)

        self.cb_attack_o = QCheckBox(self.groupBox)
        self.cb_attack_o.setObjectName(u"cb_attack_o")
        self.cb_attack_o.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_o, 15, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)

        self.le_your_nickname = QLineEdit(self.groupBox)
        self.le_your_nickname.setObjectName(u"le_your_nickname")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.le_your_nickname.sizePolicy().hasHeightForWidth())
        self.le_your_nickname.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.le_your_nickname, 0, 1, 1, 1)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout.addWidget(self.label_20, 2, 0, 1, 1)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 8, 0, 1, 2)

        self.cb_outgoing_your_damage = QCheckBox(self.groupBox)
        self.cb_outgoing_your_damage.setObjectName(u"cb_outgoing_your_damage")
        self.cb_outgoing_your_damage.setChecked(True)

        self.gridLayout.addWidget(self.cb_outgoing_your_damage, 6, 0, 1, 1)

        self.le_attacker_name = QLineEdit(self.groupBox)
        self.le_attacker_name.setObjectName(u"le_attacker_name")
        sizePolicy1.setHeightForWidth(self.le_attacker_name.sizePolicy().hasHeightForWidth())
        self.le_attacker_name.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.le_attacker_name, 2, 1, 1, 1)

        self.cb_attack_critical = QCheckBox(self.groupBox)
        self.cb_attack_critical.setObjectName(u"cb_attack_critical")
        self.cb_attack_critical.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_critical, 11, 1, 1, 1)

        self.cb_incoming_spirit_damage = QCheckBox(self.groupBox)
        self.cb_incoming_spirit_damage.setObjectName(u"cb_incoming_spirit_damage")
        self.cb_incoming_spirit_damage.setChecked(True)

        self.gridLayout.addWidget(self.cb_incoming_spirit_damage, 7, 1, 1, 1)

        self.cb_attack_p = QCheckBox(self.groupBox)
        self.cb_attack_p.setObjectName(u"cb_attack_p")
        self.cb_attack_p.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_p, 14, 0, 1, 1)

        self.line_3 = QFrame(self.groupBox)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_3, 13, 0, 1, 2)

        self.cb_incoming_your_damage = QCheckBox(self.groupBox)
        self.cb_incoming_your_damage.setObjectName(u"cb_incoming_your_damage")
        self.cb_incoming_your_damage.setChecked(True)

        self.gridLayout.addWidget(self.cb_incoming_your_damage, 6, 1, 1, 1)

        self.cb_outgoing_spirit_damage = QCheckBox(self.groupBox)
        self.cb_outgoing_spirit_damage.setObjectName(u"cb_outgoing_spirit_damage")
        self.cb_outgoing_spirit_damage.setChecked(True)

        self.gridLayout.addWidget(self.cb_outgoing_spirit_damage, 7, 0, 1, 1)

        self.cb_attack_block = QCheckBox(self.groupBox)
        self.cb_attack_block.setObjectName(u"cb_attack_block")
        self.cb_attack_block.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_block, 12, 0, 1, 1)

        self.line_damage_range = QFrame(self.groupBox)
        self.line_damage_range.setObjectName(u"line_damage_range")
        self.line_damage_range.setFrameShape(QFrame.Shape.HLine)
        self.line_damage_range.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_damage_range, 5, 0, 1, 2)

        self.damage_range_group = QGroupBox(self.groupBox)
        self.damage_range_group.setObjectName(u"damage_range_group")
        self.damage_range_layout = QGridLayout(self.damage_range_group)
        self.damage_range_layout.setObjectName(u"damage_range_layout")
        self.label_minimum_damage = QLabel(self.damage_range_group)
        self.label_minimum_damage.setObjectName(u"label_minimum_damage")

        self.damage_range_layout.addWidget(self.label_minimum_damage, 0, 0, 1, 1)

        self.label_maximum_damage = QLabel(self.damage_range_group)
        self.label_maximum_damage.setObjectName(u"label_maximum_damage")

        self.damage_range_layout.addWidget(self.label_maximum_damage, 0, 2, 1, 1)

        self.le_minimum_damage = QLineEdit(self.damage_range_group)
        self.le_minimum_damage.setObjectName(u"le_minimum_damage")
        self.le_minimum_damage.setMaxLength(9)

        self.damage_range_layout.addWidget(self.le_minimum_damage, 0, 1, 1, 1)

        self.le_maximum_damage = QLineEdit(self.damage_range_group)
        self.le_maximum_damage.setObjectName(u"le_maximum_damage")
        self.le_maximum_damage.setMaxLength(9)

        self.damage_range_layout.addWidget(self.le_maximum_damage, 0, 3, 1, 1)

        self.btn_reset_damage_range = QToolButton(self.damage_range_group)
        self.btn_reset_damage_range.setObjectName(u"btn_reset_damage_range")
        self.btn_reset_damage_range.setAutoRaise(True)

        self.damage_range_layout.addWidget(self.btn_reset_damage_range, 0, 4, 1, 1)

        self.damage_range_layout.setColumnStretch(1, 1)
        self.damage_range_layout.setColumnStretch(3, 1)

        self.gridLayout.addWidget(self.damage_range_group, 6, 0, 1, 2)

        self.le_target_name = QLineEdit(self.groupBox)
        self.le_target_name.setObjectName(u"le_target_name")
        sizePolicy1.setHeightForWidth(self.le_target_name.sizePolicy().hasHeightForWidth())
        self.le_target_name.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.le_target_name, 3, 1, 1, 1)

        self.cb_attack_common = QCheckBox(self.groupBox)
        self.cb_attack_common.setObjectName(u"cb_attack_common")
        self.cb_attack_common.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_common, 11, 0, 1, 1)

        self.cb_attack_combo = QCheckBox(self.groupBox)
        self.cb_attack_combo.setObjectName(u"cb_attack_combo")
        self.cb_attack_combo.setChecked(True)

        self.gridLayout.addWidget(self.cb_attack_combo, 12, 1, 1, 1)

        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout.addWidget(self.label_21, 3, 0, 1, 1)

        self.label_22 = QLabel(self.groupBox)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout.addWidget(self.label_22, 4, 0, 1, 1)

        self.le_skill_name = QLineEdit(self.groupBox)
        self.le_skill_name.setObjectName(u"le_skill_name")
        sizePolicy1.setHeightForWidth(self.le_skill_name.sizePolicy().hasHeightForWidth())
        self.le_skill_name.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.le_skill_name, 4, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.groupBox_2 = QGroupBox(self.verticalWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_2.addWidget(self.label_14, 3, 1, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 6, 1, 1, 1)

        self.line_6 = QFrame(self.groupBox_2)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_6, 5, 1, 1, 4)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 7, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 6, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 6, 4, 1, 1)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_2.addWidget(self.label_10, 0, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 7, 3, 1, 1)

        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 3, 2, 1, 1)

        self.line_5 = QFrame(self.groupBox_2)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_2.addWidget(self.line_5, 2, 1, 1, 4)

        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_2.addWidget(self.label_17, 4, 1, 1, 1)

        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_2.addWidget(self.label_19, 4, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 6, 3, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 7, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 7, 4, 1, 1)

        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_2.addWidget(self.label_18, 3, 4, 1, 1)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_2.addWidget(self.label_12, 0, 3, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_2.addWidget(self.label_9, 0, 1, 1, 1)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 0, 4, 1, 1)

        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_2.addWidget(self.label_16, 3, 3, 1, 1)

        self.label_23 = QLabel(self.groupBox_2)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_2.addWidget(self.label_23, 1, 1, 1, 1)

        self.label_24 = QLabel(self.groupBox_2)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_2.addWidget(self.label_24, 1, 2, 1, 1)


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
        self.toolbar.addAction(self.action_load_log_file)
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
        self.action_load_log_file.setText(QCoreApplication.translate("MainWindow", u"&\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u043b\u043e\u0433...", None))
#if QT_CONFIG(tooltip)
        self.action_load_log_file.setToolTip(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0438 \u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u043b\u043e\u0433 \u0431\u043e\u044f", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_load_log_file.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_clear_selection.setText(QCoreApplication.translate("MainWindow", u"&\u0421\u043d\u044f\u0442\u044c \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u0438\u0435", None))
#if QT_CONFIG(tooltip)
        self.action_clear_selection.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u043d\u044f\u0442\u044c \u0432\u044b\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u0441\u043e \u0432\u0441\u0435\u0445 \u0441\u0442\u0440\u043e\u0447\u0435\u043a \u0443\u0440\u043e\u043d\u0430.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_clear_selection.setShortcut(QCoreApplication.translate("MainWindow", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0438\u043b\u044c\u0442\u0440\u044b", None))
        self.cb_your_effects.setText(QCoreApplication.translate("MainWindow", u"\u042d\u0444\u0444\u0435\u043a\u0442\u044b \u043d\u0430 \u0432\u0430\u0441", None))
        self.cb_attack_m.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0438\u043b\u0430 \u0437\u0430\u043a\u043b\u0438\u043d\u0430\u043d\u0438\u0439", None))
        self.cb_not_your_effects.setText(QCoreApplication.translate("MainWindow", u"\u042d\u0444\u0444\u0435\u043a\u0442\u044b \u043d\u0430 \u0434\u0440\u0443\u0433\u0438\u0445", None))
        self.cb_attack_o.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u044b\u0447\u043d\u044b\u0439", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0430\u0448 \u043d\u0438\u043a\u043d\u0435\u0439\u043c", None))
#if QT_CONFIG(tooltip)
        self.le_your_nickname.setToolTip(QCoreApplication.translate("MainWindow", u"\u0414\u043b\u044f \u0444\u0438\u043b\u044c\u0442\u0440\u0430\u0446\u0438\u0438 \u0432\u0445\u043e\u0434\u044f\u0449\u0435\u0433\u043e \u0438 \u0438\u0441\u0445\u043e\u0434\u044f\u0449\u0435\u0433\u043e \u0443\u0440\u043e\u043d\u0430.", None))
#endif // QT_CONFIG(tooltip)
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0442\u0430\u043a\u0443\u044e\u0449\u0438\u0439", None))
        self.cb_outgoing_your_damage.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0440\u043e\u043d \u043e\u0442 \u0432\u0430\u0441", None))
#if QT_CONFIG(tooltip)
        self.le_attacker_name.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0444\u0438\u043b\u044c\u0442\u0440\u043e\u0432\u0430\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u043f\u043e \u0438\u043c\u0435\u043d\u0438 \u0430\u0442\u0430\u043a\u0443\u044e\u0449\u0435\u0433\u043e.", None))
#endif // QT_CONFIG(tooltip)
        self.cb_attack_critical.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0440\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0443\u0434\u0430\u0440\u044b", None))
        self.cb_incoming_spirit_damage.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0440\u043e\u043d \u043f\u043e \u0434\u0443\u0445\u0430\u043c", None))
        self.cb_attack_p.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0438\u043b\u0430 \u0430\u0442\u0430\u043a\u0438", None))
        self.cb_incoming_your_damage.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0440\u043e\u043d \u043f\u043e \u0432\u0430\u043c", None))
        self.cb_outgoing_spirit_damage.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0440\u043e\u043d \u043e\u0442 \u0434\u0443\u0445\u043e\u0432", None))
        self.cb_attack_block.setText(QCoreApplication.translate("MainWindow", u"\u0411\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f", None))
        self.damage_range_group.setTitle(QCoreApplication.translate("MainWindow", u"\u0414\u0438\u0430\u043f\u0430\u0437\u043e\u043d \u0443\u0440\u043e\u043d\u0430", None))
        self.label_minimum_damage.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442", None))
        self.label_maximum_damage.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e", None))
#if QT_CONFIG(tooltip)
        self.le_minimum_damage.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u0442\u043e\u043b\u044c\u043a\u043e \u0430\u0442\u0430\u043a\u0438 \u0441 \u0443\u0440\u043e\u043d\u043e\u043c \u0441\u0442\u0440\u043e\u0433\u043e \u0431\u043e\u043b\u044c\u0448\u0435 \u0443\u043a\u0430\u0437\u0430\u043d\u043d\u043e\u0433\u043e \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_maximum_damage.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u0442\u043e\u043b\u044c\u043a\u043e \u0430\u0442\u0430\u043a\u0438 \u0441 \u0443\u0440\u043e\u043d\u043e\u043c \u0441\u0442\u0440\u043e\u0433\u043e \u043c\u0435\u043d\u044c\u0448\u0435 \u0443\u043a\u0430\u0437\u0430\u043d\u043d\u043e\u0433\u043e \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.btn_reset_damage_range.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c \u0434\u0438\u0430\u043f\u0430\u0437\u043e\u043d \u0443\u0440\u043e\u043d\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btn_reset_damage_range.setText("")
#if QT_CONFIG(tooltip)
        self.le_target_name.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0444\u0438\u043b\u044c\u0442\u0440\u043e\u0432\u0430\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u043f\u043e \u0438\u043c\u0435\u043d\u0438 \u0446\u0435\u043b\u0438.", None))
#endif // QT_CONFIG(tooltip)
        self.cb_attack_common.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u044b\u0447\u043d\u044b\u0435 \u0430\u0442\u0430\u043a\u0438", None))
        self.cb_attack_combo.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043c\u0431\u043e-\u0443\u0434\u0430\u0440\u044b", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u0426\u0435\u043b\u044c", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"\u0423\u043c\u0435\u043d\u0438\u0435", None))
#if QT_CONFIG(tooltip)
        self.le_skill_name.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0444\u0438\u043b\u044c\u0442\u0440\u043e\u0432\u0430\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u043f\u043e \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u044e \u0443\u043c\u0435\u043d\u0438\u044f.", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0438\u0437\u0438\u0447\u0435\u0441\u043a\u0438\u0439", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u0434\u0438\u0430\u043d\u043d\u044b\u0439", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u044b\u0447\u043d\u044b\u0439", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0440\u0435\u0434\u043d\u0438\u0439", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0440\u043e\u043d", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0442\u0430\u043a \u0432\u0441\u0435\u0433\u043e", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0433\u0438\u0447\u0435\u0441\u043a\u0438\u0439", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0440\u0438\u0442\u043e\u0432", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"n/a", None))
        self.toolbar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

