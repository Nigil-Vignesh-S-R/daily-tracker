DARK = {
    # surfaces
    "BG": "#121315", "PANEL": "#1A1B1F", "CARD": "#212227", "INPUT": "#1C1D21",
    "BAR": "#0E0F11", "RAIL": "#1A1B1F", "DOCK_BG": "#1C1D21",
    # lines and states
    "BORDER": "#2D2F36", "BORDER_STRONG": "#40434D", "HOVER": "#2A2C33",
    "TRACK": "#2A2C33", "GRID": "#26282E", "PRESS_BG": "#33363E", "DISABLED_BG": "#2A2C33",
    # text
    "TEXT": "#E8E9EC", "TEXT2": "#A2A5AE", "MUTED": "#727683",
    # gold accent
    "GOLD": "#FBB03B", "GOLD_SOFT": "rgba(251,176,59,28)", "GOLD_SOFT2": "rgba(251,176,59,52)",
    "GOLD_BORDER": "rgba(251,176,59,120)",
    "GOLD_BTN": "#FBB03B", "GOLD_BTN_HOVER": "#FFC25E", "GOLD_BTN_PRESS": "#E39F2E",
    "GOLD_BTN_TEXT": "#1A1B1F",
    # blue (primary actions)
    "BLUE": "#3B82F6", "BLUE_HOVER": "#5C9BF8", "BLUE_PRESS": "#2563EB",
    "BLUE_BORDER": "#2F5FB3", "BLUE_SOFT": "rgba(59,130,246,50)",
    # green / red
    "GREEN": "#16A34A", "GREEN_HOVER": "#1FB955", "GREEN_PRESS": "#12823B",
    "RED": "#B91C1C", "RED_HOVER": "#DC2626", "RED_PRESS": "#991B1B", "RED_TEXT": "#F87171",
    # github button stays light in dark mode (its icon is dark)
    "GITHUB_BG": "#E6E8EC", "GITHUB_HOVER": "#F3F4F6", "GITHUB_PRESS": "#D2D5DB",
    "GITHUB_TEXT": "#1A1B1F",
    # tooltips
    "TIP_BG": "#2B2D34", "TIP_TEXT": "#F2F3F5",
    # checkboxes
    "CHECK_IMG": "./icons/check.svg", "CROSS_IMG": "./icons/cross.svg",
    "FUTURE_BG": "#1C1D21", "FUTURE_BORDER": "#34363E",
    "UNCHK_BG": "rgba(220,38,38,55)", "UNCHK_BORDER": "rgba(220,38,38,150)",
    "UNCHK_HOVER_BG": "rgba(239,68,68,80)", "UNCHK_HOVER_BORDER": "rgba(239,68,68,200)",
    "UNCHK_PRESS_BG": "rgba(239,68,68,100)",
    "CHK_BG": "rgba(22,163,74,90)", "CHK_BORDER": "rgba(22,163,74,220)",
    "CHK_HOVER_BG": "rgba(34,197,94,110)", "CHK_HOVER_BORDER": "rgba(34,197,94,225)",
}
LIGHT = {
    # Cool blue-grey surfaces
    "BG": "#E8EEF5",
    "PANEL": "#F0F4F9",
    "CARD": "#E4EBF4",
    "INPUT": "#EEF3F9",
    "BAR": "#E4EBF4",
    "RAIL": "#F0F4F9",
    "DOCK_BG": "#EDF2F8",
    # Borders and interactions
    "BORDER": "#C3DCF5",
    "BORDER_STRONG": "#CFD9E5",
    "HOVER": "#E5EDF7",
    "TRACK": "#DCE5F0",
    "GRID": "#C3DCF5",
    "PRESS_BG": "#D9E3F0",
    "DISABLED_BG": "#E5EBF3",
    # Typography
    "TEXT": "#26364B",
    "TEXT2": "#65778F",
    "MUTED": "#91A0B3",
    # violet accent - darker burnt orange
    "GOLD": "#6D28D9",
    "GOLD_SOFT": "rgba(109,40,217,18)",
    "GOLD_SOFT2": "rgba(109,40,217,32)",
    "GOLD_BORDER": "rgba(109,40,217,115)",
    "GOLD_BTN": "#6D28D9",
    "GOLD_BTN_HOVER": "#7C3AED",
    "GOLD_BTN_PRESS": "#5B21B6",
    "GOLD_BTN_TEXT": "#FFFFFF",
    # Blue primary
    "BLUE": "#397EF2",
    "BLUE_HOVER": "#5592F6",
    "BLUE_PRESS": "#2867D5",
    "BLUE_BORDER": "#A9C5EF",
    "BLUE_SOFT": "rgba(57,126,242,28)",
    # Success
    "GREEN": "#188653",
    "GREEN_HOVER": "#219B63",
    "GREEN_PRESS": "#126D43",
    # Danger - deeper crimson red
    "RED": "#B83232",
    "RED_HOVER": "#CC3F3F",
    "RED_PRESS": "#A52626",
    "RED_TEXT": "#AE2929",
    # GitHub
    "GITHUB_BG": "#6D28D9",
    "GITHUB_HOVER": "#7C3AED",
    "GITHUB_PRESS":  "#5B21B6",
    "GITHUB_TEXT": "#FFFFFF",
    # Tooltips
    "TIP_BG": "#26364B",
    "TIP_TEXT": "#F5F8FC",
    # Checkbox icons
    "CHECK_IMG": "./icons/checkL.svg",
    "CROSS_IMG": "./icons/crossL.svg",
    # Future checkboxes
    "FUTURE_BG": "#EDF2F8",
    "FUTURE_BORDER": "#D5E0ED",
    # Unchecked
    "UNCHK_BG": "rgba(184,50,50,24)",
    "UNCHK_BORDER": "rgba(184,50,50,170)",
    "UNCHK_HOVER_BG": "rgba(184,50,50,45)",
    "UNCHK_HOVER_BORDER": "rgba(184,50,50,210)",
    "UNCHK_PRESS_BG": "rgba(184,50,50,65)",
    # Checked
    "CHK_BG": "rgba(24,134,83,38)",
    "CHK_BORDER": "rgba(24,134,83,185)",
    "CHK_HOVER_BG": "rgba(24,134,83,55)",
    "CHK_HOVER_BORDER": "rgba(24,134,83,220)",
}
_TEMPLATE = """
QWidget{
    background-color:@BG;
    color:@TEXT;
    font-family:"Segoe UI";
    font-size:14px;
}
QStackedWidget{
    background-color:@BG;
    border-radius:0px;
}
QFrame{
    background-color:@PANEL;
    border-radius:8px;
}
QFrame#inner_frames{
    background-color:@CARD;
    border:1px solid @BORDER;
    border-radius:8px;
    padding-top:15px;
    padding-bottom:15px;
}
QFrame#centerFrame{
    border:1px solid @BLUE_BORDER;
}
QLabel{
    background:transparent;
    border:none;
    color:@TEXT;
    font-size:20px;
    font-style:italic;
    font-weight:400;
}
QLabel#sideHeaders{
    min-height:50px;
}
QLabel#statName{
    color:@TEXT2;
    font-size:15px;
    font-weight:400;
}
QLabel#statValue{
    color:@TEXT;
    font-size:16px;
    font-weight:500;
}
QLabel#progress{
    color:@BLUE;
    font-size:16px;
    font-weight:500;
}
QLabel#streak{
    color:@GOLD;
    font-size:16px;
    font-weight:500;
}
QLabel#streakDays{
    color:@GOLD;
    font-size:60px;
    font-weight:450;
    font-style:italic;
}
QLabel#daysLabel{
    color:@TEXT2;
    font-size:20px;
    font-weight:400;
    padding-top:18px;
}
QLabel#keepLabel{
    color:@MUTED;
    font-size:15px;
    font-weight:400;
    padding-left:30px;
}
QLabel#percentLabel, QLabel#finishedLabel{
    color:@BLUE;
    font-size:20px;
    font-weight:500;
}
QLabel#dateLabel{
    color:@TEXT2;
    font-size:16px;
    font-weight:400;
}
QLabel#todayLabel{
    color:@GOLD;
    font-size:26px;
    font-weight:500;
}
QLabel#notesHeader{
    color:@GOLD;
    font-size:19px;
    font-weight:500;
}
QLabel#errorLabel{
    color:@RED_TEXT;
    font-size:13px;
    font-weight:400;
}
QTextEdit{
    background-color:@INPUT;
    color:@TEXT;
    border:1px solid @BORDER;
    border-radius:7px;
    padding:10px;
    selection-background-color:@BLUE;
    font-size:15px;
}
QTextEdit:focus{
    border:1px solid @BLUE;
}
QLineEdit{
    background-color:@INPUT;
    color:@TEXT;
    font-size:15px;
    min-height:24px;
    border:1px solid @BORDER;
    border-radius:7px;
    padding:8px;
    selection-background-color:@BLUE;
}
QLineEdit:focus{
    border:1px solid @BLUE;
}
QListWidget{
    background-color:@INPUT;
    color:@TEXT;
    border:1px solid @BORDER;
    border-radius:7px;
    font-size:16px;
    padding:8px;
    outline:none;
}
QListWidget::item{
    padding:10px;
    min-height:24px;
    border-radius:7px;
}
QListWidget::item:hover{
    background-color:@HOVER;
}
QListWidget::item:selected{
    background-color:@BLUE;
    color:#FFFFFF;
}
QProgressBar{
    border:none;
    border-radius:6px;
    background:@TRACK;
    height:12px;
}
QProgressBar::chunk{
    background:@BLUE;
    border-radius:6px;
}
QCalendarWidget QWidget{
    background-color:@CARD;
}
QCalendarWidget QToolButton{
    background-color:@CARD;
    color:@GOLD;
    border:none;
    border-radius:6px;
    padding:4px;
    font-size:18px;
    font-weight:500;
}
QCalendarWidget QToolButton:hover{
    background-color:@HOVER;
}
QCalendarWidget QToolButton:pressed{
    background-color:@PRESS_BG;
}
QCalendarWidget QMenu{
    background-color:@CARD;
    color:@TEXT;
}
QCalendarWidget QAbstractItemView{
    selection-background-color:@BLUE;
    selection-color:#FFFFFF;
    outline:none;
}
QCalendarWidget QTableView{
    background-color:@CARD;
    alternate-background-color:@CARD;
}
QCalendarWidget QHeaderView{
    background-color:@CARD;
}
QCalendarWidget QTableView QHeaderView::section{
    background-color:@CARD;
    color:@GOLD;
    padding:6px;
    border:none;
}
QPushButton{
    border:none;
    border-radius:7px;
    padding:8px;
    font-size:14px;
    font-weight:500;
    min-height:40px;
}
QPushButton#saveBtn{
    background-color:@GREEN;
    color:#FFFFFF;
    font-size:15px;
}
QPushButton#saveBtn:hover{
    background-color:@GREEN_HOVER;
}
QPushButton#saveBtn:pressed{
    background-color:@GREEN_PRESS;
}
QPushButton#saveBtn:disabled{
    background-color:@DISABLED_BG;
    color:@MUTED;
}
QPushButton#add_habit{
    background-color:@BLUE;
    color:#FFFFFF;
}
QPushButton#add_habit:hover{
    background-color:@BLUE_HOVER;
}
QPushButton#add_habit:pressed{
    background-color:@BLUE_PRESS;
}
QPushButton#add_habit:disabled{
    background-color:@DISABLED_BG;
    color:@MUTED;
}
QPushButton#delete_habit{
    background-color:@RED;
    color:#FFFFFF;
}
QPushButton#delete_habit:hover{
    background-color:@RED_HOVER;
}
QPushButton#delete_habit:pressed{
    background-color:@RED_PRESS;
}
QPushButton#delete_habit:disabled{
    background-color:@DISABLED_BG;
    color:@MUTED;
}
QTableWidget{
    background-color:@BG;
    color:@TEXT;
    border:1px solid @BORDER;
    border-radius:7px;
    gridline-color:@GRID;
    font-size:14px;
    selection-background-color:transparent;
    outline:none;
}
QHeaderView::section{
    background-color:@CARD;
    color:@GOLD;
    border:none;
    border-right:1px solid @BORDER;
    border-bottom:1px solid @BORDER;
    padding:6px;
    font-size:14px;
    font-weight:500;
}
QTableWidget::item:selected{
    background-color:@BLUE_SOFT;
    color:@TEXT;
}
QScrollBar:horizontal{
    background:@TRACK;
    height:10px;
    border:none;
    border-radius:5px;
}
QScrollBar::handle:horizontal{
    background:@BLUE;
    border-radius:5px;
    min-width:24px;
}
QScrollBar::handle:horizontal:hover{
    background:@BLUE_HOVER;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal{
    width:0px;
}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{
    background:none;
}
QScrollBar:vertical{
    background:@TRACK;
    width:10px;
    border:none;
    border-radius:5px;
}
QScrollBar::handle:vertical{
    background:@BLUE;
    border-radius:5px;
    min-height:24px;
}
QScrollBar::handle:vertical:hover{
    background:@BLUE_HOVER;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical{
    height:0px;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{
    background:none;
}
QCheckBox{
    background:transparent;
}
QCheckBox::indicator{
    width:18px;
    height:18px;
    border:2px solid @UNCHK_BORDER;
    border-radius:5px;
    background-color:@UNCHK_BG;
    image:url("@CROSS_IMG");
}
QCheckBox::indicator:hover{
    border:2px solid @UNCHK_HOVER_BORDER;
    background-color:@UNCHK_HOVER_BG;
}
QCheckBox::indicator:pressed{
    background-color:@UNCHK_PRESS_BG;
}
QCheckBox::indicator:checked{
    background-color:@CHK_BG;
    border:2px solid @CHK_BORDER;
    image:url("@CHECK_IMG");
}
QCheckBox::indicator:checked:hover{
    background-color:@CHK_HOVER_BG;
    border:2px solid @CHK_HOVER_BORDER;
}
QCheckBox::indicator[future="true"]{
    background-color:@FUTURE_BG;
    border:2px solid @FUTURE_BORDER;
    image:none;
}
QCheckBox::indicator[before_creation="true"]{
    background-color:@FUTURE_BG;
    border:2px solid @FUTURE_BORDER;
    image:none;
}
QFrame#bottomBar{
    background-color:@BAR;
    border-radius:0px;
    border-top:1px solid @BORDER;
}
QLabel#bottomBarText{
    color:@TEXT2;
    font-size:14px;
    font-weight:400;
}
QPushButton#themeToggleBtn{
    background:transparent;
    border:none;
    border-radius:20px;
    padding:0px;
    min-height:0px;
}
QPushButton#themeToggleBtn:hover{
    background-color:@GOLD_SOFT;
}
QPushButton#themeToggleBtn:pressed{
    background-color:@GOLD_SOFT2;
}
QWidget#barSection{
    background:transparent;
}
QFrame#navDock{
    background-color:@DOCK_BG;
    border:1px solid @BORDER;
    border-radius:20px;
}
QFrame#dockIndicator{
    background-color:@GOLD_SOFT2;
    border:1px solid @GOLD_BORDER;
    border-radius:6px;
}
QPushButton#dockBtn{
    background:transparent;
    border:none;
    border-radius:6px;
    padding:0px;
    min-height:0px;
}
QPushButton#dockBtn:hover{
    background-color:@GOLD_SOFT;
}
QLabel#dockTip{
    background-color:@TIP_BG;
    color:@TIP_TEXT;
    border:1px solid @BORDER;
    border-radius:7px;
    padding:4px 10px;
    font-size:13px;
    font-weight:500;
}
QFrame#iconRail{
    background-color:@RAIL;
    border-right:1px solid @BORDER;
    border-radius:0px;
}
QPushButton#railBtn{
    background-color:transparent;
    border:none;
    border-radius:7px;
    padding:0px;
    min-height:0px;
}
QPushButton#railBtn:hover{
    background-color:@GOLD_SOFT;
}
QFrame#navOverlay{
    background-color:@RAIL;
    border-right:1px solid @BORDER;
    border-radius:0px;
}
QPushButton#navBtn{
    background-color:transparent;
    border:none;
    border-radius:6px;
    text-align:left;
    padding:8px;
    color:@TEXT;
    font-size:16px;
    font-weight:500;
    min-height:0px;
}
QPushButton#navBtn:hover{
    background-color:@GOLD_SOFT;
}
QLabel#settingsTitle, QLabel#settingsLabel{
    color:@TEXT;
    font-size:24px;
    font-weight:500;
}
QLabel#settingsSubtitle{
    color:@TEXT2;
    font-size:15px;
    font-weight:400;
}
QFrame#settingsCard{
    background-color:@CARD;
    border:1px solid @BORDER;
    border-radius:6px;
    padding:16px;
}
QLabel#cardTitle{
    color:@GOLD;
    font-size:17px;
    font-weight:500;
}
QLabel#settingRowTitle{
    color:@TEXT;
    font-size:15px;
    font-weight:500;
}
QLabel#settingRowDesc{
    color:@TEXT2;
    font-size:13px;
    font-weight:400;
}
QPushButton#themeOption{
    background-color:@INPUT;
    border:1px solid @BORDER;
    color:@TEXT2;
    border-radius:6px;
    padding:8px 16px;
    min-height:0px;
    font-size:14px;
    font-weight:500;
}
QPushButton#themeOption:hover{
    background-color:@HOVER;
    border:1px solid @BORDER_STRONG;
    color:@TEXT;
}
QPushButton#themeOption[active="true"]{
    background-color:@GOLD_SOFT;
    border:1px solid @GOLD;
    color:@GOLD;
}
QPushButton#exportBtn{
    background-color:@GOLD_BTN;
    color:@GOLD_BTN_TEXT;
    border:none;
    border-radius:6px;
    padding:8px 16px;
    min-height:0px;
    font-size:14px;
    font-weight:500;
}
QPushButton#exportBtn:hover{
    background-color:@GOLD_BTN_HOVER;
}
QPushButton#exportBtn:pressed{
    background-color:@GOLD_BTN_PRESS;
}
QPushButton#exportBtn:disabled{
    background-color:@DISABLED_BG;
    color:@MUTED;
}
QLabel#aboutTitle{
    color:@TEXT;
    font-size:17px;
    font-weight:500;
}
QLabel#versionBadge{
    color:@GOLD;
    background-color:@GOLD_SOFT;
    border:1px solid @GOLD_BORDER;
    border-radius:6px;
    padding:2px 8px;
    font-size:12px;
    font-weight:500;
    max-width:85px;
}
QPushButton#githubBtn{
    background-color:@GITHUB_BG;
    border:none;
    color:@GITHUB_TEXT;
    border-radius:6px;
    padding:8px 16px;
    min-height:0px;
    font-size:14px;
    font-weight:500;
}
QPushButton#githubBtn:hover{
    background-color:@GITHUB_HOVER;
}
QPushButton#githubBtn:pressed{
    background-color:@GITHUB_PRESS;
}
QFrame#statCardBig{
    background-color:@CARD;
    border:1px solid @BORDER;
    border-radius:6px;
    padding:14px;
}
QFrame#statCardBig:hover{
    border:1px solid @BORDER_STRONG;
}
QLabel#statCardIconCircle{
    background-color:@GOLD_SOFT;
    border:1px solid @GOLD_BORDER;
    border-radius:20px;
}
QLabel#statCardTitle{
    background:transparent;
    border:none;
    color:@TEXT2;
    font-size:14px;
    font-weight:400;
}
QLabel#statCardValue{
    background:transparent;
    border:none;
    color:@TEXT;
    font-size:30px;
    font-weight:500;
}
QLabel#statCardSub{
    background:transparent;
    border:none;
    color:@GOLD;
    font-size:13px;
    font-weight:400;
}
QFrame#statsCard{
    background-color:@CARD;
    border:1px solid @BORDER;
    border-radius:6px;
    padding:16px;
}
QFrame#statsCard:hover{
    border:1px solid @BORDER_STRONG;
}
QInputDialog, QMessageBox{
    background-color:@PANEL;
}
QInputDialog QLabel, QMessageBox QLabel{
    color:@TEXT;
    font-size:15px;
    font-weight:400;
}
QInputDialog QLineEdit{
    background-color:@INPUT;
    color:@TEXT;
    border:1px solid @BORDER;
    border-radius:6px;
    padding:8px;
    font-size:15px;
}
QInputDialog QLineEdit:focus{
    border:1px solid @BLUE;
}
QInputDialog QPushButton, QMessageBox QPushButton{
    background-color:@BLUE;
    color:#FFFFFF;
    border-radius:6px;
    padding:6px 18px;
    min-height:30px;
    min-width:70px;
    font-size:14px;
}
QInputDialog QPushButton:hover, QMessageBox QPushButton:hover{
    background-color:@BLUE_HOVER;
}
QToolTip{
    background-color:@TIP_BG;
    color:@TIP_TEXT;
    border:1px solid @BORDER;
    padding:4px 8px;
    font-size:13px;
}
"""
def _build(tokens):
    css = _TEMPLATE
    # longest names first so @TEXT2 is replaced before @TEXT, @BLUE_HOVER before @BLUE, ...
    for name in sorted(tokens, key=len, reverse=True):
        css = css.replace("@" + name, tokens[name])
    return css
def get_dark_stylesheet():
    return _build(DARK)
def get_light_stylesheet():
    return _build(LIGHT) 