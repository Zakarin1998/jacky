from flask import Flask, request, jsonify, send_file
from monitor.price_monitor import PriceMonitor
from qr.qr_generator import generate_qr_with_logo
from config.settings import PORT, FLASK_ENV
import threading

app = Flask(__name__)
monitor = PriceMonitor()
# start monitor
threading.Thread(target=monitor.start, daemon=True).start()

@app.route('/api/price-status', methods=['GET'])
def price_status():
    return jsonify(monitor.get_last_status())

@app.route('/api/generate-qr', methods=['POST'])
def api_generate_qr():
    payload = request.get_json() or {}
    data = payload.get('data','')
    logo = payload.get('logo_path','')
    output='sticker.png'
    generate_qr_with_logo(data, logo, output_path=output)
    return send_file(output, mimetype='image/png')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=PORT, debug=(FLASK_ENV=='development'))