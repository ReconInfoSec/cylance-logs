# cylance-logs

Integrates with Cylance Protect API and logs events.

```
pip install -r requirements.txt
cp init.d/cylance-protect.service /etc/systemd/system/cylance-protect.service
systemctl daemon-reload
systemctl enable cylance-protect
systemctl start cylance-protect
```
