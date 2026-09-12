@echo off
echo.
echo  =========================================
echo    HealthAware AI - Healthcare Chatbot
echo  =========================================
echo.
echo  Starting Streamlit server...
echo  Open your browser at: http://localhost:8501
echo.
.venv\Scripts\python.exe -m streamlit run app.py --server.port 8501
pause
