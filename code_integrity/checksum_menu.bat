@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Настройки
set "CPVERIFY_PATH=cpverify.exe"
set "CHECKSUM_FILE=checksums.txt"

:menu
cls
echo ==============================
echo Меню проверки контрольных сумм
echo ==============================
echo 1. Вычислить и сохранить контрольную сумму файла
echo 2. Показать сохранённые контрольные суммы
echo 3. Проверить контрольную сумму файла
echo 4. Выход
echo.
choice /c 1234 /n /m "Выберите действие (1-4): "

if errorlevel 4 exit /b
if errorlevel 3 goto :verify
if errorlevel 2 goto :show
if errorlevel 1 goto :save

:save
cls
set /p "file_path=Введите полный путь к файлу: "
if not exist "!file_path!" (
    echo Файл не найден!
    pause
    goto menu
)

:: Проверяем, есть ли уже запись для этого пути (с кавычками!)
set "quoted_path=*"%file_path%""
set "exists="
if exist "%CHECKSUM_FILE%" (
    for /f "usebackq delims=" %%L in ("%CHECKSUM_FILE%") do (
        for /f "tokens=1,* delims= " %%H in ("%%L") do (
            if "%%I" == "!quoted_path!" (
                set "exists=1"
                goto :already_exists
            )
        )
    )
)

:already_exists
if defined exists (
    echo Контрольная сумма для этого файла уже сохранена.
    pause
    goto menu
)

echo Вычисление контрольной суммы...
for /f "tokens=*" %%a in ('""%CPVERIFY_PATH%" -mk -alg GR3411_2012_256 "!file_path!" 2^>nul"') do set "hash=%%a"
if not defined hash (
    echo Ошибка при вычислении хеша. Убедитесь, что cpverify.exe доступен.
    pause
    goto menu
)

:: Сохраняем: <hash> *"<file_path>"
>>"%CHECKSUM_FILE%" echo !hash! *"!file_path!"
echo Контрольная сумма сохранена.
pause
goto menu

:show
cls
echo Сохранённые контрольные суммы:
echo -------------------------------
if not exist "%CHECKSUM_FILE%" (
    echo Файл с контрольными суммами отсутствует.
) else (
    type "%CHECKSUM_FILE%"
)
echo.
pause
goto menu

:verify
cls
set /p "file_path=Введите путь к файлу для проверки: "
if not exist "!file_path!" (
    echo Файл не найден!
    pause
    goto menu
)

:: Вычисляем текущую контрольную сумму
for /f "tokens=*" %%a in ('""%CPVERIFY_PATH%" -mk -alg GR3411_2012_256 "!file_path!" 2^>nul"') do set "current_hash=%%a"
if not defined current_hash (
    echo Ошибка при вычислении хеша.
    pause
    goto menu
)

set "quoted_path=*"%file_path%""
set "saved_hash="
set "found="

if exist "%CHECKSUM_FILE%" (
    for /f "usebackq delims=" %%L in ("%CHECKSUM_FILE%") do (
        for /f "tokens=1,* delims= " %%H in ("%%L") do (
            if "%%I" == "!quoted_path!" (
                set "saved_hash=%%H"
                set "found=1"
                goto :compare
            )
        )
    )
)

:compare
if not defined found (
    echo Контрольная сумма для этого файла не найдена в базе.
    pause
    goto menu
)

if "!current_hash!" == "!saved_hash!" (
    echo УСПЕХ: Контрольные суммы совпадают.
) else (
    echo ОШИБКА: Контрольные суммы НЕ совпадают!
    echo Сохранённая: !saved_hash!
    echo Текущая:     !current_hash!
)
pause
goto menu