"""
Landline Adapter - Parent Web Portal
Run on Raspberry Pi, accessible at http://kidphone.local
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-in-production')

# Data files
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
WHITELIST_FILE = os.path.join(DATA_DIR, 'whitelist.json')
CALL_LOG_FILE = os.path.join(DATA_DIR, 'call_log.json')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

# Default config
DEFAULT_CONFIG = {
    'password': 'kidphone',  # Change this!
    'quiet_hours': {
        'enabled': False,
        'start': '21:00',
        'end': '07:00'
    },
    'phone_name': "Kid's Phone"
}


def load_json(filepath, default):
    """Load JSON file or return default if not exists."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return default


def save_json(filepath, data):
    """Save data to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def get_whitelist():
    """Get the whitelist of approved numbers."""
    return load_json(WHITELIST_FILE, [])


def save_whitelist(whitelist):
    """Save the whitelist."""
    save_json(WHITELIST_FILE, whitelist)


def get_config():
    """Get app configuration."""
    return load_json(CONFIG_FILE, DEFAULT_CONFIG)


def save_config(config):
    """Save app configuration."""
    save_json(CONFIG_FILE, config)


def get_call_log():
    """Get call history."""
    return load_json(CALL_LOG_FILE, [])


def log_call(number, name, allowed, duration=0):
    """Log a call attempt."""
    log = get_call_log()
    log.insert(0, {
        'timestamp': datetime.now().isoformat(),
        'number': number,
        'name': name,
        'allowed': allowed,
        'duration': duration
    })
    # Keep last 100 calls
    save_json(CALL_LOG_FILE, log[:100])


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============== Routes ==============

@app.route('/')
def index():
    """Redirect to dashboard or login."""
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    error = None
    if request.method == 'POST':
        config = get_config()
        if request.form['password'] == config.get('password', 'kidphone'):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        error = 'Invalid password'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """Logout."""
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard."""
    config = get_config()
    whitelist = get_whitelist()
    call_log = get_call_log()[:10]  # Last 10 calls
    return render_template('dashboard.html', 
                          config=config, 
                          whitelist=whitelist,
                          call_log=call_log)


@app.route('/whitelist')
@login_required
def whitelist_page():
    """Whitelist management page."""
    whitelist = get_whitelist()
    return render_template('whitelist.html', whitelist=whitelist)


@app.route('/whitelist/add', methods=['POST'])
@login_required
def whitelist_add():
    """Add a number to whitelist."""
    number = request.form.get('number', '').strip()
    name = request.form.get('name', '').strip()
    
    if number:
        whitelist = get_whitelist()
        # Check if already exists
        if not any(w['number'] == number for w in whitelist):
            whitelist.append({
                'number': number,
                'name': name or number,
                'added': datetime.now().isoformat()
            })
            save_whitelist(whitelist)
    
    return redirect(url_for('whitelist_page'))


@app.route('/whitelist/remove/<number>')
@login_required
def whitelist_remove(number):
    """Remove a number from whitelist."""
    whitelist = get_whitelist()
    whitelist = [w for w in whitelist if w['number'] != number]
    save_whitelist(whitelist)
    return redirect(url_for('whitelist_page'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Settings page."""
    config = get_config()
    
    if request.method == 'POST':
        config['phone_name'] = request.form.get('phone_name', "Kid's Phone")
        config['quiet_hours']['enabled'] = 'quiet_enabled' in request.form
        config['quiet_hours']['start'] = request.form.get('quiet_start', '21:00')
        config['quiet_hours']['end'] = request.form.get('quiet_end', '07:00')
        
        # Update password if provided
        new_password = request.form.get('new_password', '').strip()
        if new_password:
            config['password'] = new_password
        
        save_config(config)
        return redirect(url_for('settings'))
    
    return render_template('settings.html', config=config)


@app.route('/call-log')
@login_required
def call_log_page():
    """Full call history."""
    call_log = get_call_log()
    return render_template('call_log.html', call_log=call_log)


# ============== API Endpoints ==============
# These are called by the Asterisk/Pi SIP processor

@app.route('/api/check/<number>')
def api_check_number(number):
    """
    Check if a number is allowed.
    Called by Asterisk AGI or Pi SIP processor.
    Returns: {"allowed": true/false, "name": "Contact Name"}
    """
    whitelist = get_whitelist()
    config = get_config()
    
    # Check quiet hours
    if config['quiet_hours']['enabled']:
        now = datetime.now().time()
        start = datetime.strptime(config['quiet_hours']['start'], '%H:%M').time()
        end = datetime.strptime(config['quiet_hours']['end'], '%H:%M').time()
        
        if start <= now or now <= end:
            return jsonify({'allowed': False, 'reason': 'quiet_hours'})
    
    # Check whitelist
    for contact in whitelist:
        if contact['number'] == number:
            return jsonify({'allowed': True, 'name': contact['name']})
    
    return jsonify({'allowed': False, 'reason': 'not_whitelisted'})


@app.route('/api/log-call', methods=['POST'])
def api_log_call():
    """
    Log a call attempt.
    Called by Asterisk AGI or Pi SIP processor.
    """
    data = request.json or {}
    log_call(
        number=data.get('number', 'unknown'),
        name=data.get('name', 'Unknown'),
        allowed=data.get('allowed', False),
        duration=data.get('duration', 0)
    )
    return jsonify({'status': 'ok'})


@app.route('/api/whitelist')
def api_whitelist():
    """Get full whitelist (for Pi SIP processor to cache)."""
    return jsonify(get_whitelist())


if __name__ == '__main__':
    # Create default config if needed
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    
    # Run on all interfaces so it's accessible on local network
    app.run(host='0.0.0.0', port=80, debug=True)
