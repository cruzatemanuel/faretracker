#!/bin/bash
# MySQL Password Reset Script for macOS Homebrew

echo "This script will help you reset your MySQL root password."
echo ""
echo "Step 1: Stop MySQL service"
brew services stop mysql

echo ""
echo "Step 2: Start MySQL in safe mode (skip grant tables)"
mysqld_safe --skip-grant-tables --skip-networking &

echo "Waiting 3 seconds for MySQL to start..."
sleep 3

echo ""
echo "Step 3: Connect to MySQL and reset password"
echo "Please enter your NEW MySQL root password:"
read -s NEW_PASSWORD

mysql -u root << EOF
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY '$NEW_PASSWORD';
FLUSH PRIVILEGES;
EOF

echo ""
echo "Step 4: Stop MySQL safe mode"
mysqladmin -u root -p"$NEW_PASSWORD" shutdown

echo ""
echo "Step 5: Start MySQL normally"
brew services start mysql

echo ""
echo "Password reset complete! Your new root password is: $NEW_PASSWORD"
echo "Please update your .env file with this password."
