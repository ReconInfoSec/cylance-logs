# Cylance Detections

A Python/Flask application that polls the Cylance API on a schedule and logs detections.

```
pip install -r requirements.txt
cp init.d/cylance-detections.service /etc/systemd/system/cylance-detections.service
systemctl daemon-reload
systemctl enable cylance-detections
systemctl start cylance-detections
```
