echo "this is a convert script"

set login_ui=ui\login.ui
set login_py=uipy\loginForm.py

set register_ui=ui\register.ui
set register_py=uipy\registerForm.py

set settings_ui=ui\settings.ui
set settings_py=uipy\settingsForm.py

set todoList_ui=ui\todoList.ui
set todoList_py=uipy\todoListForm.py

set todoStatusCheck_ui=ui\todoStatusCheck.ui
set todoStatusCheck_py=uipy\todoStatusCheckForm.py

set coach_ui=ui\coach.ui
set coach_py=uipy\coachForm.py

set counter_ui=ui\counter.ui
set counter_py=uipy\counterForm.py

set rank_ui=ui\rank.ui
set rank_py=uipy\rankForm.py

set resources_qrc=ui\src\resources.qrc

pyside6-uic %login_ui% -o %login_py%
pyside6-uic %register_ui% -o %register_py%
pyside6-uic %settings_ui% -o %settings_py%
pyside6-uic %todoList_ui% -o %todoList_py%
pyside6-uic %todoStatusCheck_ui% -o %todoStatusCheck_py%
pyside6-uic %coach_ui% -o %coach_py%
pyside6-uic %counter_ui% -o %counter_py%
pyside6-uic %rank_ui% -o %rank_py%

pyside6-rcc %resources_qrc% -o resources_rc.py