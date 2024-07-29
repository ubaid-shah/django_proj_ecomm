Referance: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu

# Step 1: Create an EC2 instance 

## Connect to your EC2
```bash
ssh -i "KP.pem" ubuntu@ec2-55-90-207-22.compute-1.amazonaws.com
```

## Install and upgrade Ubuntu
```bash
sudo apt-get upgrade
```
## Install the pip
```bash
sudo apt-get install python3-pip
```

## Install venv
```bash
sudo apt install python3-venv python3-dev libpq-dev nginx curl
```
## Create and activate the venv
```bash
python3 -m venv env

source env/bin/activate
```

## Clone the git repo
```bash
git clone https://github.com/user-name/repo.git
```

# Step 2: Install Nginx server in EC2

## Install Ngninx
```bash
sudo apt-get install -y nginx
```

## Install gunicorn
```bash
pip install gunicorn psycopg2-binary
```

## Step — Creating systemd Socket and Service Files for Gunicorn
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```
```bash
type the foolowing code :

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

```bash
sudo nano /etc/systemd/system/gunicorn.service
```
```bash
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/myprojectdir
ExecStart=/home/ubuntu/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
```bash
sudo systemctl status gunicorn.socket

output:
● gunicorn.socket - gunicorn socket
     Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor preset: enabled)
     Active: active (listening) since Mon 2022-04-18 17:53:25 UTC; 5s ago
   Triggers: ● gunicorn.service
     Listen: /run/gunicorn.sock (Stream)
     CGroup: /system.slice/gunicorn.socket

Apr 18 17:53:25 django systemd[1]: Listening on gunicorn socket.
```

```bash
file /run/gunicorn.sock

Output
/run/gunicorn.sock: socket
```
```bash
sudo journalctl -u gunicorn.socket
```
```bash
sudo systemctl status gunicorn

Output
○ gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
     Active: inactive (dead)
TriggeredBy: ● gunicorn.socket
```
```bash
curl --unix-socket /run/gunicorn.sock localhost
```

```bash
sudo systemctl status gunicorn

Output
● gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
     Active: active (running) since Mon 2022-04-18 17:54:49 UTC; 5s ago
TriggeredBy: ● gunicorn.socket
   Main PID: 102674 (gunicorn)
      Tasks: 4 (limit: 4665)
     Memory: 94.2M
        CPU: 885ms
     CGroup: /system.slice/gunicorn.service
             ├─102674 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
             ├─102675 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
             ├─102676 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
             └─102677 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application

Apr 18 17:54:49 django systemd[1]: Started gunicorn daemon.
Apr 18 17:54:49 django gunicorn[102674]: [2022-04-18 17:54:49 +0000] [102674] [INFO] Starting gunicorn 20.1.0
Apr 18 17:54:49 django gunicorn[102674]: [2022-04-18 17:54:49 +0000] [102674] [INFO] Listening at: unix:/run/gunicorn.sock (102674)
Apr 18 17:54:49 django gunicorn[102674]: [2022-04-18 17:54:49 +0000] [102674] [INFO] Using worker: sync
Apr 18 17:54:49 django gunicorn[102675]: [2022-04-18 17:54:49 +0000] [102675] [INFO] Booting worker with pid: 102675
Apr 18 17:54:49 django gunicorn[102676]: [2022-04-18 17:54:49 +0000] [102676] [INFO] Booting worker with pid: 102676
Apr 18 17:54:50 django gunicorn[102677]: [2022-04-18 17:54:50 +0000] [102677] [INFO] Booting worker with pid: 102677
Apr 18 17:54:50 django gunicorn[102675]:  - - [18/Apr/2022:17:54:50 +0000] "GET / HTTP/1.1" 200 10697 "-" "curl/7.81.0"
```

```bash
sudo journalctl -u gunicorn
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

```bash
sudo nano /etc/nginx/sites-available/myproject
```
```bash
type the following code:

server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/myprojectdir;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

```bash
sudo nginx -t
```

```bash
sudo systemctl restart nginx
```

```
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```
