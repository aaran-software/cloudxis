Here's the direct one-liner bash command to zip and copy the frappe-bench directory to /home/devops/shared:
```
cd /home/devops && zip -r frappe-bench.zip frappe-bench && mkdir -p /home/devops/shared && mv frappe-bench.zip /home/devops/shared/
``

 bench get-app https://github.com/frappe/lms --branch develop
 bench --site dev.aaranerp.com install-app lms

npm install frappe-ui

 
 bench get-app https://github.com/frappe/gameplan --branch develop
 bench --site erp.logicx.in install-app gameplan
 
 bench get-app https://github.com/frappe/wiki 
 bench --site soft.aaranerp.com install-app wiki
 
 
  bench get-app https://github.com/frappe/lending --branch develop
  bench --site dev.aaranerp.com install-app lending

  bench get-app https://github.com/frappe/helpdesk --branch develop
  bench --site dev.aaranerp.com install-app helpdesk
  
  bench --site erp.tmnext.in install-app helpdesk
  
  bench get-app https://github.com/frappe/print_designer  --branch develop
  bench --site erp.aaranerp.com install-app print_designer 
  
  bench get-app https://github.com/frappe/education  --branch develop
  bench --site dev.aaranerp.com install-app education 
  
  bench get-app https://github.com/frappe/blogs  --branch develop
  bench --site dev.aaranerp.com install-app blogs 

  bench get-app https://github.com/frappe/payments
  bench --site dev.aaranerp.com install-app payments
  
  bench get-app https://github.com/frappe/webshop  --branch develop
  bench --site dev.aaranerp.com install-app webshop 



npm install @iconify-json/lucide
# or if you're using yarn
yarn add @iconify-json/lucide
# or pnpm
pnpm add @iconify-json/lucide


rm -rf node_modules
rm pnpm-lock.yaml # or yarn.lock
pnpm install # or yarn install