@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM aggregate-report.cmd — Aggregate all reviews into a formatted report
REM
REM Usage: aggregate-report.cmd [output_path]
REM Default output: review\aggregate-report.md
REM ============================================================

set "OUTPUT=review\aggregate-report.md"
if not "%~1"=="" set "OUTPUT=%~1"

set "REVIEWERS_DIR=review\reviewers"
set "REVIEWS_DIR=review\reviews"
set "PROFILES=%REVIEWERS_DIR%\profiles.md"

REM --- Validate prerequisites ---
if not exist "%PROFILES%" (
    echo ERROR: Profiles not found at %PROFILES%. Run Step 1 first.
    exit /b 1
)

set REVIEW_COUNT=0
for /l %%i in (1,1,5) do (
    if exist "%REVIEWS_DIR%\reviewer%%i\review.md" set /a REVIEW_COUNT+=1
)
if %REVIEW_COUNT%==0 (
    echo ERROR: No reviews found. Run Step 2 first.
    exit /b 1
)

REM --- Get date ---
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set "DT=%%I"
set "DATE_STR=%DT:~0,4%-%DT:~4,2%-%DT:~6,2% %DT:~8,2%:%DT:~10,2%"

REM --- Build report ---
(
    echo # Aggregate Review Report
    echo.
    echo **Generated:** %DATE_STR%
    echo **Reviews collected:** %REVIEW_COUNT%/5
    echo.
    echo ---
    echo.
    echo ## Reviewer Overview
    echo.
    echo ^| # ^| Name ^| Domain ^| Expertise ^| Rating ^| Confidence ^|
    echo ^|---^|------^|--------^|-----------^|--------^|------------^|

    for /l %%i in (1,1,5) do (
        set "REVIEW=%REVIEWS_DIR%\reviewer%%i\review.md"
        if exist "!REVIEW!" (
            REM Extract name, domain, expertise, rating, confidence from review header
            for /f "tokens=2 delims=*" %%n in ('findstr /c:"**Reviewer:**" "!REVIEW!" 2^>nul') do set "NAME=%%n"
            set "NAME=!NAME: =!"
            for /f "tokens=2 delims=*" %%d in ('findstr /c:"Domain:" "!REVIEW!" 2^>nul') do set "DOMAIN=%%d"
            for /f "tokens=2 delims=*" %%e in ('findstr /c:"Expertise:" "!REVIEW!" 2^>nul') do set "EXPERTISE=%%e"
            for /f "tokens=2 delims=*" %%r in ('findstr /c:"**Overall Rating:**" "!REVIEW!" 2^>nul') do set "RATING=%%r"
            for /f "tokens=2 delims=*" %%c in ('findstr /c:"**Confidence:**" "!REVIEW!" 2^>nul') do set "CONFIDENCE=%%c"
            echo ^| %%i ^| !NAME! ^| !DOMAIN! ^| !EXPERTISE! ^| !RATING! ^| !CONFIDENCE! ^|
        ) else (
            echo ^| %%i ^| *(missing)* ^| - ^| - ^| - ^| - ^|
        )
    )

    echo.
    echo ---
    echo.
    echo ## Per-Reviewer Details
    echo.

    for /l %%i in (1,1,5) do (
        set "REVIEW=%REVIEWS_DIR%\reviewer%%i\review.md"
        set "QA_LOG=%REVIEWS_DIR%\reviewer%%i\qa-log.md"

        if exist "!REVIEW!" (
            echo ### Reviewer %%i
            echo.
            echo ^<details^>^<summary^>^<b^>Full Review^</b^>^</summary^>
            echo.
            type "!REVIEW!"
            echo.
            echo ^</details^>
            echo.

            if exist "!QA_LOG!" (
                echo ^<details^>^<summary^>^<b^>QA Log^</b^>^</summary^>
                echo.
                type "!QA_LOG!"
                echo.
                echo ^</details^>
                echo.
            )
            echo ---
            echo.
        ) else (
            echo ### Reviewer %%i - *(review not found)*
            echo.
        )
    )

    echo ## Rating Summary
    echo.
    for %%r in ("Accept" "Weak Accept" "Weak Reject" "Reject") do (
        set "COUNT=0"
        for /l %%j in (1,1,5) do (
            set "RV=%REVIEWS_DIR%\reviewer%%j\review.md"
            if exist "!RV!" (
                findstr /c:"%%~r" "!RV!" >nul 2>&1 && set /a COUNT+=1
            )
        )
        echo - %%~r: !COUNT!
    )

) > "%OUTPUT%"

echo Aggregate report written to: %OUTPUT%
echo Reviews collected: %REVIEW_COUNT%/5
exit /b 0
