import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Initialize the database connection
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    score = data.get('score')
    
    if not score:
        return jsonify({'message': 'No score provided'}), 400

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (score) VALUES (?)', (score,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Thank you for your feedback!'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
