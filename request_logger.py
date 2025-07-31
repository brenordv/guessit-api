import sqlite3
import datetime
from typing import Dict, List, Optional, Any, Union


class RequestLogger:
    """
    A class to log requests to the /api/guess endpoint and provide statistics.
    
    This class logs each request in a SQLite database table called 'requests' with
    the following columns:
    - filename: what the endpoint received
    - requester_ip: the IP of the client that made the request
    - title: from the guessit result, the title
    - year: from the guessit result, the year
    - type: from the guessit result, the type
    - error: in case of error, the error will be saved here
    - timestamp: timestamp for the request, in UTC
    """
    
    def __init__(self, db_path: str = "requests.db"):
        """
        Initialize the RequestLogger with an SQLite database.
        
        Args:
            db_path: Path to the SQLite database file. Defaults to "requests.db".
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the SQLite database with the required table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create the requests table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            requester_ip TEXT NOT NULL,
            title TEXT,
            year INTEGER,
            type TEXT,
            error TEXT,
            timestamp TIMESTAMP NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def log(self, filename: str, requester_ip: str, 
            title: Optional[str] = None, year: Optional[int] = None, 
            type_: Optional[str] = None, error: Optional[str] = None):
        """
        Log a request to the database.
        
        Args:
            filename: The filename that was analyzed
            requester_ip: The IP address of the requester
            title: The title extracted from the filename (optional)
            year: The year extracted from the filename (optional)
            type_: The type extracted from the filename (optional)
            error: Any error that occurred during processing (optional)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current UTC timestamp
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # Insert the request data into the database
        cursor.execute('''
        INSERT INTO requests (filename, requester_ip, title, year, type, error, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (filename, requester_ip, title, year, type_, error, timestamp))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self, num_requests: int = 100) -> Dict[str, Any]:
        """
        Get statistics about the requests.
        
        Args:
            num_requests: Number of recent requests to return. Defaults to 100.
            
        Returns:
            A dictionary with the following keys:
            - total: Total number of requests ever made to the API
            - total_24h: Total number of requests in the past 24 hours
            - recent_requests: List of the most recent N requests
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        # Get total number of requests
        cursor.execute('SELECT COUNT(*) as count FROM requests')
        total = cursor.fetchone()['count']
        
        # Get total number of requests in the past 24 hours
        twenty_four_hours_ago = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=1)).isoformat()
        cursor.execute('SELECT COUNT(*) as count FROM requests WHERE timestamp >= ?', (twenty_four_hours_ago,))
        total_24h = cursor.fetchone()['count']
        
        # Get the most recent N requests
        cursor.execute('''
        SELECT filename, requester_ip, title, year, type, error, timestamp
        FROM requests
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (num_requests,))
        
        recent_requests = []
        for row in cursor.fetchall():
            recent_requests.append({
                'filename': row['filename'],
                'requester_ip': row['requester_ip'],
                'title': row['title'],
                'year': row['year'],
                'type': row['type'],
                'error': row['error'],
                'timestamp': row['timestamp']
            })
        
        conn.close()
        
        return {
            'total': total,
            'total_24h': total_24h,
            'recent_requests': recent_requests
        }