import serial
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

ser = serial.Serial('/dev/cu.usbserial-1440', 9600, timeout=1) 

def load_data():
    with open('a.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('a.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    data_dict = load_data()

    if ser.is_open:
        try:
            # Read the latest line and decode it
            data = ser.readline().decode('utf-8').strip()

            # Print received data for debugging
            print(f"Received Data: {data}")

            # Ensure data is in the correct format
            if "Water Level" in data and "Servo Status" in data:
                # Split data safely and check parts
                parts = data.split(" | ")

                if len(parts) == 2:
                    water_level = parts[0].split(":")[1].strip()
                    servo_status = parts[1].split(":")[1].strip()

                    # Update the level (allowing for floating-point numbers)
                    try:
                        data_dict['level'] = float(water_level)  # Use float instead of int
                    except ValueError:
                        return jsonify({'error': 'Invalid Water Level Format'})

                    # Save the updated data back to the JSON file
                    save_data(data_dict)

                    return jsonify(data_dict)
                else:
                    return jsonify({'error': 'Invalid Data Format: Missing Parts'})

            else:
                return jsonify({'error': 'Invalid Data Format: Missing Water Level or Servo Status'})

        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Serial port not open'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
