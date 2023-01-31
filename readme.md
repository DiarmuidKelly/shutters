# Shutters controller
Controller for automating shutters, sycned with dawn and dusk times. Operating a uWSGI in emperor mode using systemd. To add new services create directories inside ```/opt/``` with ```<project>.ini``` to launch the flask app.

### TODO:
- [ ] Separate web service from shutters service. Placing web serice on port ```80``` as ```www-data``` user and group. Then add variable for port on shutters services. This should allow one UI for multiple backend services.

## Setup commands
### General Setup
Install requirements 
```bash
pip3 install -r requirements.txt
```

## [Emperor Setup](https://uwsgi-docs.readthedocs.io/en/latest/Emperor.html)

Copy the contents of opt/ to ```/opt/```. Create symbolic link to service in user systemd 
```bash
ln -s /opt/emperor/emperor.uwsgi.service /etc/systemd/system/emperor.uwsgi.service
```

### Run Emperor
```bash
systemctl daemon-reload
systemctl enable emperor.uwsgi.service
systemctl start emperor.uwsgi.service
systemctl status emperor.uwsgi.service
```
```bash
systemctl daemon-reload
systemctl restart emperor.uwsgi.service
```