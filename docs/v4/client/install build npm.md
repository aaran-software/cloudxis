sudo -u www-data python3 ideploy.py \
  --install-node y \
  --update-npm y \
  --npm-install y \
  --build-npm y


sudo -u www-data python3 ideploy.py --npm-install y --build-npm n


sudo -u www-data python3 ideploy.py --npm-install n --build-npm y
