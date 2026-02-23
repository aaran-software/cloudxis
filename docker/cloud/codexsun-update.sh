#!/bin/sh

APP_DIR="/var/www/html"
BRANCH="main"

echo "======================================"
echo "🚀 Laravel Production Update Starting"
echo "======================================"

cd $APP_DIR || exit 1

# --------------------------------------
# 1️⃣ Stop Horizon Gracefully
# --------------------------------------
echo "🛑 Stopping Horizon safely..."
php artisan horizon:terminate || true
sleep 3

# --------------------------------------
# 2️⃣ Enable Maintenance Mode
# --------------------------------------
echo "🔧 Enabling maintenance mode..."
php artisan down || true

# --------------------------------------
# 3️⃣ Update Git to Latest
# --------------------------------------
echo "⬆ Updating Git..."
apk update && apk add --no-cache git || true

git config --global --add safe.directory $APP_DIR

echo "📥 Pulling latest code..."
git fetch origin
git reset --hard origin/$BRANCH

# --------------------------------------
# 4️⃣ Update Composer Itself
# --------------------------------------
echo "⬆ Updating Composer..."
composer self-update || true

# --------------------------------------
# 5️⃣ Update PHP Dependencies
# --------------------------------------
echo "📦 Running composer update..."
composer update --no-interaction --prefer-dist --optimize-autoloader

# --------------------------------------
# 6️⃣ Update Node / NPM (if exists)
# --------------------------------------
if [ -f "package.json" ]; then
    echo "⬆ Updating NPM..."
    npm install

    echo "🏗 Building frontend..."
    npm run build
fi

# --------------------------------------
# 7️⃣ Clear All Caches
# --------------------------------------
echo "🧹 Clearing caches..."
php artisan cache:clear || true
php artisan config:clear || true
php artisan route:clear || true
php artisan view:clear || true

# --------------------------------------
# 8️⃣ Optimize
# --------------------------------------
echo "⚡ Optimizing Laravel..."
php artisan config:cache
php artisan route:cache
php artisan view:cache
php artisan optimize

# --------------------------------------
# 9️⃣ Run Migrations Safely
# --------------------------------------
echo "🗄 Running migrations..."
php artisan migrate --force || true

# --------------------------------------
# 🔟 Disable Maintenance Mode
# --------------------------------------
echo "✅ Bringing application up..."
php artisan up || true

echo "======================================"
echo "🎉 Update Completed Successfully"
echo "======================================"
