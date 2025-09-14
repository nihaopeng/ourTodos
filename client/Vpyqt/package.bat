pyinstaller -w main.py -n main
pyinstaller -F -w updater.py -n ourTodos -i ui\src\task.ico

set dist_dir=dist\main\
set core_dir=%dist_dir%_internal\core\
set figures_dir=%dist_dir%ui\src\
set toml_file=core\config.toml
set figures_source_dir=ui\src
set wav_dir=%dist_dir%ui\wav\
set wav_source_dir=ui\wav

echo "target core_ directory: %core_dir%"
if not exist "%core_dir%" (
    echo 正在创建目标文件夹...
    mkdir "%core_dir%"
)
echo "target figures directory: %figures_dir%"
if not exist "%figures_dir%" (
    echo 正在创建目标文件夹...
    mkdir "%figures_dir%"
)

echo "moving config.toml to  directory"
copy  %toml_file% %core_dir%
echo "moving figures and wav to figures directory"
xcopy /E /I /Y %figures_source_dir% %figures_dir%
xcopy /E /I /Y %wav_source_dir% %wav_dir%
copy dist\ourTodos.exe %dist_dir%ourTodos.exe