from app import app
import ssl

app.run(debug = False, threaded=True, host='127.0.0.1', port=3000, passthrough_errors=True)
