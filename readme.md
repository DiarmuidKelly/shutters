## Setupn commands

Copy the contents of src/ to ```/opt/shutters/```. Create symbolic link to service in user systemd 
```bash
ln -s /opt/shutters/shutters.service /etc/systemd/user/shutters.service
```

Install requirements 
```bash
pip3 install -r requirements.txt
```


## Run
```bash
systemctl --user daemon-reload
systemctl --user enable shutters.service
systemctl --user start shutters.service
systemctl --user status shutters.service
```

```bash
systemctl --user restart shutters.service
```