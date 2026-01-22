#### starting from a **clean Ubuntu 24.04 LTS**.

---

### ✅ Step-by-Step: Install Docker

---

## 🧱 1. Update and Install System Essentials

```bash
sudo apt update && sudo apt upgrade -y
```

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

---

## 🐳 2. Install Docker Engine (Latest Stable)

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

✅ Verify Docker works:

```bash
sudo docker version
```