#!/bin/bash
# Script to reset MySQL root password for /usr/local/mysql/ installation

echo "═══════════════════════════════════════════════════════════════"
echo "  MySQL Password Reset Script"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "This will reset the root password for your MySQL installation."
echo ""

# Step 1: Stop MySQL
echo "Step 1: Stopping MySQL..."
sudo /usr/local/mysql/support-files/mysql.server stop 2>/dev/null || echo "MySQL may already be stopped"

# Step 2: Start MySQL in safe mode
echo ""
echo "Step 2: Starting MySQL in safe mode (no password required)..."
sudo mysqld_safe --skip-grant-tables --skip-networking --datadir=/usr/local/mysql/data &

echo "Waiting 5 seconds for MySQL to start..."
sleep 5

# Step 3: Get new password
echo ""
echo "Step 3: Setting new root password..."
echo "Enter your NEW MySQL root password:"
read -s NEW_PASSWORD

# Step 4: Reset password
mysql -u root << EOF
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY '$NEW_PASSWORD';
FLUSH PRIVILEGES;
EXIT;
EOF

# Step 5: Stop safe mode
echo ""
echo "Step 4: Stopping MySQL safe mode..."
sudo mysqladmin shutdown

# Step 6: Start MySQL normally
echo ""
echo "Step 5: Starting MySQL normally..."
sudo /usr/local/mysql/support-files/mysql.server start

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Password reset complete!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Your new MySQL root password is: $NEW_PASSWORD"
echo ""
echo "Now update your .env file:"
echo "  DATABASE_URL=mysql+pymysql://root:$NEW_PASSWORD@localhost:3306/fairfares"
echo ""
