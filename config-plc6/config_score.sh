#!/usr/bin/env bash

echo "Partial Credit: 0"

score=0

# Check Dockerfile contains FROM keyword
if grep -q "^FROM" Dockerfile; then
    echo "Dockerfile contains a FROM instruction"
    ((score+=1))
else
    echo "Dockerfile does not contain a FROM instruction"
fi


# Check docker-compose file
file="docker-compose.yml"

echo "Checking keywords in $file..."

# Function to check keyword presence
check_keyword() {
    local keyword=$1
    if grep -qi "$keyword" "$file"; then
        echo "Found: $keyword"
        ((score+=1))
    else
        echo "Missing: $keyword"
    fi
}

# List of required keywords
# check_keyword "image"
check_keyword "mysql"
check_keyword "environment"
# check_keyword "volumes"
check_keyword "init.sql"
check_keyword "ports"
check_keyword "build"



# Start services in detached mode
if docker-compose up -d --build &> /dev/null; then
    echo "docker-compose started successfully"
    ((score+=1))
else
    echo "Failed to start docker-compose services"
fi

# 3. Wait for services to initialize
echo "Waiting for containers to initialize..."
sleep 15

# 4. Check if UI and DB containers are running
ui_running=$(docker ps --filter "name=banking-ui" --filter "status=running" -q)
db_running=$(docker ps --filter "name=mysql-db" --filter "status=running" -q)

if [ -n "$ui_running" ]; then
    echo "UI container is running"
    ((score+=1))
else
    echo "UI container not running:"
    # docker ps --format "table {{.Names}}\t{{.Status}}"
fi

if [ -n "$db_running" ]; then
    echo "DB container is running"
    ((score+=1))
else
    echo "DB container not running:"
    # docker ps --format "table {{.Names}}\t{{.Status}}"
fi


# 5. Test the UI with curl
echo "Testing UI endpoint (http://localhost:8080)..."
if curl -s --head http://localhost:8080 | grep "200 OK" > /dev/null; then
    echo "UI is accessible"
    ((score+=1))
else
    echo "UI is not accessible via curl"
fi


echo "Removing containers"
docker-compose down &> /dev/null


echo "----------------------"
echo "Total Score: $score/10"

((credit = score*100/10))
echo "Partial Credit: $credit%"
