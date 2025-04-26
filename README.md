# MerryMeals

MerryMeals is a food-related web application built using **Python Django** with a **PostgreSQL** (or **MySQL**) database, and a frontend designed in **HTML, CSS, and JavaScript**.

---

## Requirements

- Python
- Any Database (e.g., PostgreSQL, MySQL)

### If Using PostgreSQL
- Install **PostGIS** extension using **StackBuilder** to add spatial functions to PostgreSQL.

### If Using MySQL
- Spatial functions are **built-in** — no extra installation required.

---

## Steps to Run the Project

1. **Clone the repository**  
   ```bash
   git clone https://github.com/lipikagupta758/MerryMeals.git
   ```

2. **Create a virtual environment**  
   ```bash
   python -m venv <venv_name>
   ```

3. **Activate the virtual environment**  
   ```bash
   <venv_name>\Scripts\activate  # For Windows
   source <venv_name>/bin/activate  # For Linux/Mac
   ```

4. **Install project dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file**  
   - Add database and Google Auth API configurations.
   - Take reference from the provided `.env-sample`.
   - Ensure you create a database with the **same name** in your local system.
   - Verify that your **DB username and password** are correct.
   - Set `DB_HOST` as `localhost` if running locally.

6. **Email Configuration**
   - Enter your email ID and password in the `.env`.
   - For the password:
     - Go to your email settings.
     - Enable **2-Factor Authentication**.
     - Create an **App Password**.
     - Use the generated **16-digit code** as the email password.

7. **Google Auth API Key**
   - Create a project in **Google Cloud Console**.
   - Generate a **Google Auth API key** and add it in the `.env` file.

8. **Apply database migrations**  
   ```bash
   python manage.py migrate
   ```

9. **Run the development server**  
   ```bash
   python manage.py runserver
   ```

10. **Visit the application**  
    Open your browser and go to:
    ```
    http://127.0.0.1:8000/
    ```

---

## Tech Stack

- **Backend**: Python, Django
- **Database**: PostgreSQL / MySQL
- **Frontend**: HTML, CSS, JavaScript

---
