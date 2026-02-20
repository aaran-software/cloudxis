#!/bin/sh

APP_ROOT="/var/www/html"
APP_NAME="codexsun"
APP_DIR="$APP_ROOT/$APP_NAME"
REPO="https://github.com/aaran-software/codexsun.git"
BRANCH="main"

echo "======================================"
echo "🚀 Container starting..."
echo "======================================"

cd "$APP_ROOT" || exit 1

# Fix git safe directory
git config --global --add safe.directory "$APP_ROOT"

# ----------------------------------------
# Remove ONLY project folder (not html)
# ----------------------------------------
if [ -d "$APP_DIR" ]; then
    echo "🧹 Removing existing project..."
    rm -rf "$APP_DIR"
fi

# ----------------------------------------
# Clone repository
# ----------------------------------------
echo "📦 Cloning repository..."
git clone -b "$BRANCH" "$REPO" "$APP_NAME" || exit 1

cd "$APP_DIR" || exit 1

# ----------------------------------------
# Install dependencies
# ----------------------------------------
echo "📦 Installing Composer..."
composer install --no-interaction --prefer-dist --optimize-autoloader || exit 1

# ----------------------------------------
# Setup ENV
# ----------------------------------------
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

sed -i 's/DB_CONNECTION=.*/DB_CONNECTION=sqlite/' .env

mkdir -p database
touch database/database.sqlite
chmod -R 775 database

php artisan key:generate --force

# ----------------------------------------
# Install NPM + Build
# ----------------------------------------
# ----------------------------------------
# Smart Frontend Dependency Handling
# ----------------------------------------

if [ -f "pnpm-lock.yaml" ]; then
    echo "📦 PNPM project detected"

    # Remove npm lock if exists
    if [ -f "package-lock.json" ]; then
        echo "🧹 Removing package-lock.json (conflict with pnpm)"
        rm -f package-lock.json
    fi

    # Remove old node_modules to avoid corruption
    if [ -d "node_modules" ]; then
        echo "🧹 Removing old node_modules"
        rm -rf node_modules
    fi

    echo "📦 Running pnpm install..."
    pnpm install || exit 1

    echo "🏗 Running pnpm build..."
    pnpm run build || exit 1

elif [ -f "package-lock.json" ]; then
    echo "📦 NPM project detected"

    # Remove old node_modules for clean install
    if [ -d "node_modules" ]; then
        echo "🧹 Removing old node_modules"
        rm -rf node_modules
    fi

    echo "📦 Running npm install..."
    npm install || exit 1

    echo "🏗 Running npm build..."
    npm run build || exit 1
else
    echo "ℹ️ No frontend lockfile detected, skipping frontend build"
fi


# ----------------------------------------
# Optimize
# ----------------------------------------
php artisan config:cache
php artisan route:cache
php artisan view:cache

echo "✅ Starting Supervisor..."

exec /usr/bin/supervisord -c /etc/supervisord.conf
