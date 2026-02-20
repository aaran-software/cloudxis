#!/bin/bash

# ==================================================
# CODEXSUN FULL INSTALL + RUN SCRIPT
# Laravel + Octane + FrankenPHP
# ==================================================

set -e

PROJECT_DIR="app/codexsun"
REPO_URL="https://github.com/aaran-software/codexsun.git"
PORT=8000

echo "🚀 Starting Codexsun Setup..."

# --------------------------------------------------
# Install required packages
# --------------------------------------------------
echo "📦 Installing system packages..."
apt update
apt install -y git curl unzip zip sqlite3 nano \
    libzip-dev libsqlite3-dev \
    nodejs npm

# Try PHP extensions (ignore if already installed)
docker-php-ext-install zip pdo pdo_mysql pdo_sqlite bcmath intl pcntl 2>/dev/null || true

# --------------------------------------------------
# Create project directory
# --------------------------------------------------
echo "📁 Creating project directory..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# --------------------------------------------------
# Clone repository
# --------------------------------------------------
if [ ! -f artisan ]; then
    echo "📥 Cloning repository..."
    git clone $REPO_URL .
fi

# --------------------------------------------------
# Install Composer if missing
# --------------------------------------------------
if ! command -v composer &> /dev/null
then
    echo "🎵 Installing Composer..."
    curl -sS https://getcomposer.org/installer | php
    mv composer.phar /usr/local/bin/composer
fi

composer --version

# --------------------------------------------------
# Install PHP dependencies
# --------------------------------------------------
echo "📦 Installing Composer dependencies..."
composer install

# --------------------------------------------------
# Install Node dependencies
# --------------------------------------------------
echo "📦 Installing NPM packages..."
npm install

# --------------------------------------------------
# Setup .env
# --------------------------------------------------
if [ ! -f .env ]; then
    echo "⚙️ Creating .env..."
    cp .env.example .env
fi

# --------------------------------------------------
# Setup SQLite database
# --------------------------------------------------
echo "🗄 Creating SQLite database..."
mkdir -p database
touch database/database.sqlite

sed -i 's/^DB_CONNECTION=.*/DB_CONNECTION=sqlite/' .env
sed -i 's|^DB_DATABASE=.*|DB_DATABASE=database/database.sqlite|' .env

# --------------------------------------------------
# Generate app key
# --------------------------------------------------
echo "🔑 Generating application key..."
php artisan key:generate

# --------------------------------------------------
# Run migrations + seed
# --------------------------------------------------
echo "🧱 Running migrations..."
php artisan migrate:fresh --seed


composer require laravel/octane
php artisan octane:install

# --------------------------------------------------
# Build frontend
# --------------------------------------------------
echo "🏗 Building frontend..."
npm run build

# --------------------------------------------------
# Stop old Octane if running
# --------------------------------------------------
echo "🛑 Stopping old Octane..."
php artisan octane:stop 2>/dev/null || true
pkill -f frankenphp 2>/dev/null || true

# --------------------------------------------------
# Start Octane with FrankenPHP
# --------------------------------------------------
echo "🚀 Starting Octane on port $PORT ..."
php artisan octane:start \
    --server=frankenphp \
    --host=0.0.0.0 \
    --port=$PORT


php artisan octane:start \
    --server=frankenphp \
    --host=0.0.0.0 \
    --port=7021