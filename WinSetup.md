# Windows Setup Guide - Fair Fares Application

Complete step-by-step guide for setting up the Fair Fares application on Windows.

---

## Table of Contents

1. [Prerequisites Installation](#1-prerequisites-installation)
2. [Database Setup](#2-database-setup)
3. [Backend Setup](#3-backend-setup)
4. [Frontend Setup](#4-frontend-setup)
5. [Running the Application](#5-running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites Installation

### Step 1.1: Install Python 3.8 or Higher

1. **Download Python:**
   - Visit: https://www.python.org/downloads/
   - Click "Download Python 3.x.x" (latest version)
   - Or direct link: https://www.python.org/downloads/windows/

2. **Install Python:**
   - Run the downloaded installer (e.g., `python-3.11.x-amd64.exe`)
   - ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" at the bottom of the installer
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation:**
   - Open **Command Prompt** (Press `Win + R`, type `cmd`, press Enter)
   - Or open **PowerShell** (Press `Win + X`, select "Windows PowerShell")
   - Run:
     ```cmd
     python --version
     ```
   - You should see: `Python 3.x.x`
   - Also verify pip is installed:
     ```cmd
     pip --version
     ```

### Step 1.2: Install Node.js 16 or Higher

1. **Download Node.js:**
   - Visit: https://nodejs.org/
   - Download the **LTS version** (recommended)
   - Or direct link: https://nodejs.org/en/download/
   - Choose "Windows Installer (.msi)" for 64-bit

2. **Install Node.js:**
   - Run the downloaded installer (e.g., `node-v20.x.x-x64.msi`)
   - Click "Next" through the installation wizard
   - Accept the license agreement
   - Keep default installation path
   - Click "Install"
   - Wait for installation to complete
   - Click "Finish"

3. **Verify Installation:**
   - Open a **new** Command Prompt or PowerShell window
   - Run:
     ```cmd
     node --version
     ```
   - You should see: `v20.x.x` (or similar)
   - Verify npm is installed:
     ```cmd
     npm --version
     ```

### Step 1.3: Install MySQL 8.0 or Higher

1. **Download MySQL:**
   - Visit: https://dev.mysql.com/downloads/installer/
   - Choose "MySQL Installer for Windows"
   - Download the **full installer** (recommended) or web installer
   - Or direct link: https://dev.mysql.com/downloads/windows/installer/8.0.html

2. **Install MySQL:**
   - Run the downloaded installer (e.g., `mysql-installer-community-8.0.x.x.msi`)
   - Choose "Developer Default" or "Server only" installation type
   - Click "Execute" to install required components
   - Wait for all components to install
   - Click "Next" through configuration

3. **Configure MySQL:**
   - **Type and Networking**: Keep defaults (Standalone, TCP/IP, Port 3306)
   - **Authentication Method**: Choose "Use Strong Password Encryption"
   - **Accounts and Roles**: 
     - Set a **root password** (remember this password!)
     - You can add additional users later if needed
   - **Windows Service**: 
     - Check "Configure MySQL Server as a Windows Service"
     - Service name: `MySQL80` (default)
     - Check "Start the MySQL Server at System Startup"
   - **Apply Configuration**: Click "Execute"
   - Wait for configuration to complete
   - Click "Finish"

4. **Verify MySQL Installation:**
   - Open Command Prompt or PowerShell
   - Navigate to MySQL bin directory (usually `C:\Program Files\MySQL\MySQL Server 8.0\bin`)
   - Or add MySQL to PATH:
     - Press `Win + X` → System → Advanced system settings
     - Click "Environment Variables"
     - Under "System variables", find "Path" and click "Edit"
     - Click "New" and add: `C:\Program Files\MySQL\MySQL Server 8.0\bin`
     - Click "OK" on all dialogs
   - Test MySQL:
     ```cmd
     mysql --version
     ```
   - You should see: `mysql Ver 8.0.x`

5. **Start MySQL Service (if not running):**
   - Press `Win + R`, type `services.msc`, press Enter
   - Find "MySQL80" in the list
   - Right-click → "Start" (if not already running)
   - Or use Command Prompt (as Administrator):
     ```cmd
     net start MySQL80
     ```

---

## 2. Database Setup

### Step 2.1: Create the Database

1. **Open Command Prompt or PowerShell**

2. **Login to MySQL:**
   ```cmd
   mysql -u root -p
   ```
   - Enter your MySQL root password when prompted
   - If you get "mysql is not recognized", use the full path:
     ```cmd
     "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
     ```

3. **Create the database:**
   ```sql
   CREATE DATABASE fairfares;
   ```

4. **Verify database was created:**
   ```sql
   SHOW DATABASES;
   ```
   - You should see `fairfares` in the list

5. **Exit MySQL:**
   ```sql
   exit;
   ```

### Step 2.2: Create Database Tables

1. **Open Command Prompt or PowerShell**

2. **Login to MySQL and select the database:**
   ```cmd
   mysql -u root -p fairfares
   ```
   - Enter your MySQL root password

3. **Create the tables:**
   ```sql
   CREATE TABLE IF NOT EXISTS user (
       srcode VARCHAR(50) PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       college VARCHAR(255) NOT NULL,
       password VARCHAR(255) NOT NULL,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE IF NOT EXISTS user_fares (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_srcode VARCHAR(50) NOT NULL,
       district INT NOT NULL,
       start_location VARCHAR(255) NOT NULL,
       destination VARCHAR(255) NOT NULL,
       include_trike BOOLEAN DEFAULT FALSE,
       total_fare FLOAT NOT NULL,
       trike_fare FLOAT DEFAULT 0.0,
       fare_details TEXT,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (user_srcode) REFERENCES user(srcode)
   );
   ```

4. **Verify tables were created:**
   ```sql
   SHOW TABLES;
   ```
   - You should see both `user` and `user_fares` tables

5. **Exit MySQL:**
   ```sql
   exit;
   ```

**Alternative Method (Using a SQL file):**

1. Create a file `setup_tables.sql` in the `backend` folder with the SQL commands above
2. Run:
   ```cmd
   mysql -u root -p fairfares < backend\setup_tables.sql
   ```

---

## 3. Backend Setup

### Step 3.1: Navigate to Backend Directory

1. **Open Command Prompt or PowerShell**

2. **Navigate to your project folder:**
   ```cmd
   cd C:\Users\YourUsername\Desktop\finalproject\backend
   ```
   - Replace `YourUsername` with your actual Windows username
   - Or navigate to wherever you extracted/cloned the project

### Step 3.2: Create Virtual Environment

1. **Create the virtual environment:**
   ```cmd
   python -m venv venv
   ```
   - This creates a folder named `venv` in the backend directory

2. **Activate the virtual environment:**
   
   **For Command Prompt (cmd):**
   ```cmd
   venv\Scripts\activate
   ```
   
   **For PowerShell:**
   ```powershell
   venv\Scripts\Activate.ps1
   ```
   
   - If you get an execution policy error in PowerShell, run:
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
     Then try activating again.
   
   - When activated, you should see `(venv)` at the beginning of your command prompt

### Step 3.3: Install Python Dependencies

1. **Make sure virtual environment is activated** (you should see `(venv)` in your prompt)

2. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```
   - This may take a few minutes
   - Wait for all packages to install successfully

3. **Verify installation:**
   ```cmd
   pip list
   ```
   - You should see packages like `fastapi`, `uvicorn`, `sqlalchemy`, etc.

### Step 3.4: Create .env File

1. **Navigate to the backend directory** (if not already there)

2. **Create the .env file:**
   
   **Method 1: Using Notepad**
   - Open Notepad
   - Type the following (replace `your_password` with your actual MySQL root password):
     ```
     DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/fairfares
     ```
   - Save the file as `.env` in the `backend` folder
   - ⚠️ **Important**: In the "Save As" dialog:
     - File name: `.env` (with the dot at the beginning)
     - Save as type: "All Files (*.*)"
     - Encoding: UTF-8

   **Method 2: Using Command Prompt (PowerShell)**
   ```powershell
   cd backend
   echo "DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/fairfares" > .env
   ```
   - Replace `your_password` with your actual MySQL root password
   - Then edit the file in Notepad to verify it's correct

   **Method 3: Using Command Prompt (cmd)**
   ```cmd
   cd backend
   (echo DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/fairfares) > .env
   ```
   - Replace `your_password` with your actual MySQL root password

3. **Verify .env file exists:**
   ```cmd
   dir .env
   ```
   - You should see the `.env` file listed

### Step 3.5: Verify Fare Guide CSV File

1. **Check that the CSV file exists:**
   ```cmd
   dir data\fare_guide.csv
   ```
   - The file should be at: `backend\data\fare_guide.csv`
   - If it doesn't exist, make sure you have the complete project files

### Step 3.6: Create Test User (Optional)

1. **Make sure virtual environment is activated** (you should see `(venv)`)

2. **Make sure you're in the backend directory**

3. **Run the test user creation script:**
   ```cmd
   python create_test_user.py
   ```

4. **Expected output:**
   ```
   Test user created successfully!
   SRCODE: TEST001
   Password: test123

   You can now login with these credentials.
   ```

### Step 3.7: Start the Backend Server

1. **Make sure virtual environment is activated** (you should see `(venv)`)

2. **Make sure you're in the backend directory**

3. **Start the server:**
   ```cmd
   uvicorn app:app --reload --port 8000
   ```

4. **Expected output:**
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

5. **Keep this terminal window open** - the server needs to keep running

6. **Test the backend:**
   - Open a web browser
   - Go to: http://localhost:8000
   - You should see: `{"message":"Fair Fares API","status":"running"}`
   - API documentation: http://localhost:8000/docs

---

## 4. Frontend Setup

### Step 4.1: Open a New Terminal Window

1. **Open a new Command Prompt or PowerShell window**
   - Keep the backend server running in the first terminal
   - Use this new terminal for frontend setup

### Step 4.2: Navigate to Frontend Directory

1. **Navigate to the frontend folder:**
   ```cmd
   cd C:\Users\YourUsername\Desktop\finalproject\frontend
   ```
   - Replace `YourUsername` with your actual Windows username
   - Adjust path to match your project location

### Step 4.3: Install Node.js Dependencies

1. **Install all required packages:**
   ```cmd
   npm install
   ```
   - This may take several minutes
   - Wait for installation to complete
   - You should see `node_modules` folder created

2. **Verify installation:**
   ```cmd
   npm list --depth=0
   ```
   - You should see packages like `react`, `vite`, `axios`, etc.

### Step 4.4: Start the Frontend Development Server

1. **Start the development server:**
   ```cmd
   npm run dev
   ```

2. **Expected output:**
   ```
   VITE v5.x.x  ready in xxx ms

   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ➜  press h + enter to show help
   ```

3. **Keep this terminal window open** - the frontend server needs to keep running

---

## 5. Running the Application

### Step 5.1: Verify Both Servers Are Running

You should have **two terminal windows open**:

1. **Backend Terminal:**
   - Shows: `Uvicorn running on http://127.0.0.1:8000`
   - Status: Running

2. **Frontend Terminal:**
   - Shows: `Local: http://localhost:5173/`
   - Status: Running

### Step 5.2: Access the Application

1. **Open a web browser** (Chrome, Firefox, Edge, etc.)

2. **Navigate to:**
   ```
   http://localhost:5173
   ```

3. **You should see the Fair Fares login page**

### Step 5.3: Create an Account or Login

**Option A: Create a New Account**
1. Click "Sign Up" link on the login page
2. Fill in the form:
   - **SRCODE**: (e.g., `USER001`)
   - **Name**: (e.g., `John Doe`)
   - **College**: (e.g., `Computer Science`)
   - **Password**: (choose a password)
3. Click "Sign Up"
4. You'll be redirected to the login page

**Option B: Use Test Account**
- If you created the test user earlier:
  - **SRCODE**: `TEST001`
  - **Password**: `test123`

### Step 5.4: Test the Application

1. **Login** with your credentials
2. You should be redirected to the **Home** page
3. Navigate to **"Track"** to calculate fares
4. Navigate to **"My Dashboard"** to view your fare history

---

## Troubleshooting

### Python Issues

**Problem: `python` is not recognized**
- **Solution**: 
  - Reinstall Python and make sure to check "Add Python to PATH"
  - Or manually add Python to PATH:
    - Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python3x\` to PATH
    - Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python3x\Scripts\` to PATH

**Problem: `pip` is not recognized**
- **Solution**: 
  - Use `python -m pip` instead of just `pip`
  - Or reinstall Python with "Add Python to PATH" checked

**Problem: Virtual environment activation fails**
- **Solution (PowerShell)**: 
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- **Solution (cmd)**: Use `venv\Scripts\activate.bat` instead

### Node.js Issues

**Problem: `node` is not recognized**
- **Solution**: 
  - Restart your terminal/Command Prompt after installing Node.js
  - Or restart your computer
  - Verify Node.js is in PATH: `C:\Program Files\nodejs\`

**Problem: `npm install` fails**
- **Solution**: 
  - Delete `node_modules` folder and `package-lock.json`
  - Run `npm install` again
  - Try: `npm cache clean --force` then `npm install`

**Problem: Port 5173 already in use**
- **Solution**: 
  - Close other applications using port 5173
  - Or change port in `vite.config.js`:
    ```javascript
    server: {
      port: 3000  // Use a different port
    }
    ```

### MySQL Issues

**Problem: `mysql` is not recognized**
- **Solution**: 
  - Use full path: `"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p`
  - Or add MySQL to PATH:
    - Add: `C:\Program Files\MySQL\MySQL Server 8.0\bin` to PATH

**Problem: Can't connect to MySQL**
- **Solution**: 
  - Check if MySQL service is running:
    - Press `Win + R`, type `services.msc`
    - Find "MySQL80" and make sure it's "Running"
  - Start MySQL service:
    ```cmd
    net start MySQL80
    ```
    (Run Command Prompt as Administrator)

**Problem: Access denied for user 'root'**
- **Solution**: 
  - Verify you're using the correct root password
  - Reset MySQL root password if needed (search online for instructions)

**Problem: Database doesn't exist**
- **Solution**: 
  - Make sure you created the database: `CREATE DATABASE fairfares;`
  - Verify: `SHOW DATABASES;` should list `fairfares`

### Backend Issues

**Problem: Backend won't start**
- **Checklist**:
  - ✅ MySQL service is running
  - ✅ Database `fairfares` exists
  - ✅ Tables `user` and `user_fares` are created
  - ✅ `.env` file exists with correct `DATABASE_URL`
  - ✅ Virtual environment is activated
  - ✅ All dependencies are installed (`pip install -r requirements.txt`)
  - ✅ Port 8000 is not in use by another application

**Problem: Module not found errors**
- **Solution**: 
  - Make sure virtual environment is activated
  - Reinstall dependencies: `pip install -r requirements.txt`

**Problem: Database connection error**
- **Solution**: 
  - Check `.env` file has correct format:
    ```
    DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/fairfares
    ```
  - Verify MySQL is running
  - Test connection manually:
    ```cmd
    mysql -u root -p fairfares
    ```

**Problem: CSV file not found**
- **Solution**: 
  - Verify file exists: `backend\data\fare_guide.csv`
  - Check file path in error message
  - Make sure you're running the server from the `backend` directory

### Frontend Issues

**Problem: Frontend won't start**
- **Checklist**:
  - ✅ Node.js is installed and in PATH
  - ✅ Dependencies are installed (`npm install`)
  - ✅ Port 5173 is available
  - ✅ Backend server is running on port 8000

**Problem: Can't connect to backend API**
- **Solution**: 
  - Verify backend is running: http://localhost:8000
  - Check `frontend\src\services\api.js` has correct URL
  - Check browser console for CORS errors
  - Verify CORS settings in `backend\app.py`

**Problem: Blank page or errors in browser**
- **Solution**: 
  - Open browser Developer Tools (F12)
  - Check Console tab for errors
  - Check Network tab for failed requests
  - Verify both servers are running

### General Issues

**Problem: Port already in use**
- **Solution**: 
  - Find what's using the port:
    ```cmd
    netstat -ano | findstr :8000
    netstat -ano | findstr :5173
    ```
  - Kill the process or use different ports

**Problem: File paths with spaces**
- **Solution**: 
  - Use quotes around paths: `cd "C:\Users\My Name\Desktop\finalproject"`
  - Or avoid spaces in folder names

**Problem: Antivirus blocking**
- **Solution**: 
  - Add project folder to antivirus exclusions
  - Allow Python and Node.js in firewall

---

## Quick Reference Commands

### Backend Commands
```cmd
# Navigate to backend
cd backend

# Activate virtual environment (cmd)
venv\Scripts\activate

# Activate virtual environment (PowerShell)
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app:app --reload --port 8000
```

### Frontend Commands
```cmd
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### MySQL Commands
```cmd
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE fairfares;

# Use database
USE fairfares;

# Show tables
SHOW TABLES;

# Exit MySQL
exit;
```

---

## Next Steps

Once everything is running:

1. ✅ Test all features (signup, login, fare calculation, dashboard)
2. ✅ Check API documentation: http://localhost:8000/docs
3. ✅ Review the main README.md for more information
4. ✅ Consider implementing security improvements before production deployment

---

## Getting Help

If you encounter issues not covered here:

1. Check the main `SETUP.md` file for additional troubleshooting
2. Check browser console (F12) for frontend errors
3. Check backend terminal for error messages
4. Verify all prerequisites are correctly installed
5. Ensure all services (MySQL, backend, frontend) are running

---

**Good luck with your setup! 🚀**
