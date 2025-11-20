# MySQL Setup Guide

## Option 1: Reset MySQL Root Password (Simpler Method)

1. Stop MySQL:
   ```bash
   brew services stop mysql
   ```

2. Start MySQL in safe mode:
   ```bash
   sudo mysqld_safe --skip-grant-tables --skip-networking &
   ```

3. Connect without password:
   ```bash
   mysql -u root
   ```

4. In MySQL, run:
   ```sql
   FLUSH PRIVILEGES;
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';
   FLUSH PRIVILEGES;
   EXIT;
   ```

5. Stop safe mode and restart normally:
   ```bash
   sudo mysqladmin shutdown
   brew services start mysql
   ```

## Option 2: Create a New MySQL User (Recommended for Development)

If you can't reset root password, create a new user:

1. Try to access MySQL (you may need to use sudo):
   ```bash
   sudo mysql -u root
   ```

2. If that works, create a new user:
   ```sql
   CREATE USER 'fairfares_user'@'localhost' IDENTIFIED BY 'fairfares_password123';
   CREATE DATABASE fairfares;
   GRANT ALL PRIVILEGES ON fairfares.* TO 'fairfares_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. Update your .env file:
   ```
   DATABASE_URL=mysql+pymysql://fairfares_user:fairfares_password123@localhost:3306/fairfares
   ```

## Option 3: Check if MySQL has a default password file

Some MySQL installations store credentials in:
- `~/.my.cnf`
- `/usr/local/etc/my.cnf`

Check these files for credentials.
