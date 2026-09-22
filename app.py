from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# In-memory data (in a real app, use a database)
movies = [
    {"id": "dune2", "title": "Dune: Part Two", "emoji": "🏜️", "rating": "PG-13", "duration": "2h 46m"},
    {"id": "oppenheimer", "title": "Oppenheimer", "emoji": "⚛️", "rating": "R", "duration": "3h 0m"},
    {"id": "barbie", "title": "Barbie", "emoji": "💖", "rating": "PG-13", "duration": "1h 54m"},
    {"id": "godzilla", "title": "Godzilla x Kong", "emoji": "🦖", "rating": "PG-13", "duration": "1h 55m"},
    {"id": "insideout2", "title": "Inside Out 2", "emoji": "🧠", "rating": "PG", "duration": "1h 36m"},
    {"id": "fallguy", "title": "The Fall Guy", "emoji": "🎬", "rating": "PG-13", "duration": "2h 6m"}
]

# Pre-defined occupied seats (deterministic for demo)
OCCUPIED_SEATS = {
    'A3','A4','A6', 'B2','B5','B7', 'C1','C8','D4','D5','E2','E3','E7','F1','F6','F8'
}

@app.route('/')
def index():
    """Render the main booking page."""
    # Pass movies and occupied seats to the template
    return render_template('index.html', movies=movies, occupied_seats=list(OCCUPIED_SEATS))

@app.route('/api/book', methods=['POST'])
def book_tickets():
    """API endpoint to handle a booking request."""
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    movie_id = data.get('movie_id')
    selected_seats = data.get('seats', [])
    date = data.get('date')
    time = data.get('time')
    
    # Simple validation
    if not movie_id or not selected_seats:
        return jsonify({"success": False, "message": "Missing movie or seats"}), 400
    
    # Find movie
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        return jsonify({"success": False, "message": "Movie not found"}), 404
    
    # Check if any seat is already occupied (simulated concurrency check)
    for seat in selected_seats:
        if seat in OCCUPIED_SEATS:
            return jsonify({"success": False, "message": f"Seat {seat} is already taken."}), 409
    
    # Mark seats as occupied
    for seat in selected_seats:
        OCCUPIED_SEATS.add(seat)
    
    # Calculate total (example pricing logic)
    total = 0
    for seat in selected_seats:
        row = seat[0]
        price = 15.00 if row in ['A', 'B'] else 12.50
        total += price
    
    # Simulate a booking reference
    booking_ref = f"BK-{random.randint(10000, 99999)}"
    
    return jsonify({
        "success": True,
        "message": f"Booked {len(selected_seats)} ticket(s) for {movie['title']} on {date} at {time}.",
        "booking_ref": booking_ref,
        "total": round(total, 2),
        "seats": selected_seats
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
