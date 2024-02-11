from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

app = Flask(__name__)

# Note: Using a local SQLite database here for simplicity
# Define the base directory for the database file
db_dir = Path('/var/app_data/counter_service')

# Create directories and setting the path for SQLite database.
db_dir.mkdir(parents=True, exist_ok=True)

# Define the full path to the database file
db_file = db_dir / 'counter.db'

# Configure the Flask app to use the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'

# Disabling 'SQLALCHEMY_TRACK_MODIFICATIONS' helps to reduce memory usage and improve performance
# by not setting up internal event listeners for state changes - a feature not needed for this application.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Define the Counter model
class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)


# Ensure the database and the counter table exist
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def get_count():
    """Handle GET requests to return the current count."""
    counter = Counter.query.first()
    if counter is None:
        counter = Counter(count=0)
        db.session.add(counter)
        db.session.commit()
    return render_template('counter.html', count=counter.count)


@app.route('/', methods=['POST'])
def increment_count():
    """Handle POST requests to increment the count by 1."""
    counter = Counter.query.first()
    if not counter:
        counter = Counter(count=1)
    else:
        counter.count += 1
    db.session.add(counter)
    db.session.commit()
    return jsonify(message='Count incremented by 1'), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the service is running."""
    try:
        # Run a simple database query to ensure connectivity:
        Counter.query.first()
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        # Log the error and return a service unavailable status code if there's an issue
        app.logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy'}), 503


if __name__ == '__main__':
    # For debugging purposes
    app.run(debug=True, port=5000, host='0.0.0.0')
