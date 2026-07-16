@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM qa-entry.cmd — Append a QA entry to a reviewer's qa-log.md
REM
REM Usage: qa-entry.cmd <ReviewerNumber> "<UserQuestion>"
REM Example: qa-entry.cmd 3 "Why did you rate the evaluation as weak?"
REM ============================================================

set "REVIEWER_NUM=%~1"
set "USER_QUESTION=%~2"
set "BASE_DIR=review\reviews\reviewer%REVIEWER_NUM%"
set "QA_LOG=%BASE_DIR%\qa-log.md"
set "REVIEW_MD=%BASE_DIR%\review.md"

REM --- Validate inputs ---
if "%REVIEWER_NUM%"=="" (
    echo ERROR: Reviewer number required.
    echo Usage: qa-entry.cmd ^<N^> "^<question^>"
    exit /b 1
)
if "%USER_QUESTION%"=="" (
    echo ERROR: User question required.
    echo Usage: qa-entry.cmd ^<N^> "^<question^>"
    exit /b 1
)

REM --- Check that review exists ---
if not exist "%REVIEW_MD%" (
    echo ERROR: No review found for Reviewer %REVIEWER_NUM% at %REVIEW_MD%
    echo Run Step 2 first to generate reviews.
    exit /b 1
)

REM --- Ensure directory and qa-log.md exist ---
if not exist "%BASE_DIR%" mkdir "%BASE_DIR%"
if not exist "%QA_LOG%" (
    echo # QA Log — Reviewer %REVIEWER_NUM% > "%QA_LOG%"
    echo. >> "%QA_LOG%"
    echo Generated: %DATE% %TIME% >> "%QA_LOG%"
    echo. >> "%QA_LOG%"
    echo --- >> "%QA_LOG%"
    echo. >> "%QA_LOG%"
)

REM --- Determine next Q number ---
set "QNUM=1"
if exist "%QA_LOG%" (
    for /f "tokens=2 delims=Q" %%a in ('findstr /r "^## Q[0-9]" "%QA_LOG%" 2^>nul') do (
        set "LAST_Q=%%a"
    )
    if defined LAST_Q (
        for /f "tokens=1 delims=:" %%b in ("!LAST_Q!") do (
            set /a QNUM=%%b + 1
        )
    )
)

REM --- Get current date ---
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set "DT=%%I"
set "DATE_STR=%DT:~0,4%-%DT:~4,2%-%DT:~6,2%"

REM --- Append QA entry ---
(
    echo ## Q%QNUM%: %DATE_STR%
    echo.
    echo **User Question:**
    echo %USER_QUESTION%
    echo.
    echo **Reviewer Response:**
    echo ^<TO BE FILLED BY AGENT — respond in Reviewer %REVIEWER_NUM%'s voice^>
    echo.
    echo **Internal Reasoning:**
    echo ^<TO BE FILLED BY AGENT — record why Reviewer %REVIEWER_NUM% answered this way^>
    echo.
    echo ---
    echo.
) >> "%QA_LOG%"

echo QA entry Q%QNUM% appended to %QA_LOG%
echo Next: agent must fill Reviewer Response and Internal Reasoning.
exit /b 0
