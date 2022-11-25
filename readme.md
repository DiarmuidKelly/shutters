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
systemctl restart emperor.uwsgi.service
```

## Alternative - Run shutters service directly
Copy the contents of src/ to ```/opt/shutters/```. Create symbolic link to service in user systemd 
```bash
ln -s /opt/shutters/shutters.service /etc/systemd/user/shutters.service
```


### Run shutters directly (Tested not working reliably)
```bash
systemctl --user daemon-reload
systemctl --user enable shutters.service
systemctl --user start shutters.service
systemctl --user status shutters.service
```

```bash
systemctl --user restart shutters.service
```