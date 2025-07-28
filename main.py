from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend access

# PostgreSQL URL from Render
DATABASE_URL = "postgresql://nottherealepic:4u4lbsU8YdqcCnVsc0DYewLlOiaMabha@dpg-d1n08omr433s73b5jkg0-a.singapore-postgres.render.com/epicgiveaway_nw6s"

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

# Create table (if not exists)
cursor.execute('''
CREATE TABLE IF NOT EXISTS names (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')
conn.commit()

@app.route('/submit-name', methods=['POST'])
def submit_name():
    data = request.json
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    cursor.execute("INSERT INTO names (username) VALUES (%s);", (name,))
    conn.commit()
    return jsonify({'message': 'Name saved successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
