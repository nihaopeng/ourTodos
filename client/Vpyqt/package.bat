pyinstaller -D -w main.py

set dist_dir=dist\main\
set backend_dir=%dist_dir%_internal\backend\
set figures_dir=%dist_dir%ui\src\
set toml_file=backend\config.toml
set figures_source_dir=ui\src
set wav_dir=%dist_dir%ui\wav\
set wav_source_dir=ui\wav

echo "target backend directory: %backend_dir%"
if not exist "%backend_dir%" (
    echo 正在创建目标文件夹...
    mkdir "%backend_dir%"
)
echo "target figures directory: %figures_dir%"
if not exist "%figures_dir%" (
    echo 正在创建目标文件夹...
    mkdir "%figures_dir%"
)

echo "moving config.toml to backend directory"
copy  %toml_file% %backend_dir%
echo "moving figures and wav to figures directory"
xcopy /E /I /Y %figures_source_dir% %figures_dir%
xcopy /E /I /Y %wav_source_dir% %wav_dir%