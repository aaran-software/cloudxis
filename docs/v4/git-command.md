


git config --global user.name "Sundar"
git config --global user.email "Sundar@aaransoftware.com"

git init -b main



git push -u origin develop


git branch -m main develop
git fetch origin
git branch -u origin/develop develop
git remote set-head origin -a

git pull --no-rebase origin develop

git push -u origin develop --force

git add .
git commit

git config pull.rebase true

git config --global pull.rebase false


git fetch origin
git diff origin/develop..develop

git pull --rebase origin develop


 git reset --soft HEAD~1