import sqlite3
from typing import List, Dict, Any
import config

def get_connection() -> sqlite3.Connection:
    """Establish a connection to the local SQLite Database."""
    # Connecting to SQLite. If the file doesn't exist, it will be created automatically.
    return sqlite3.connect(config.SQLITE_DB_PATH, check_same_thread=False)

def execute_query(query: str) -> List[Dict[str, Any]]:
    """
    Execute a readonly SQL query against the local SQLite database and return the results
    as a list of dictionaries.
    """
    conn = None
    try:
        conn = get_connection()
        # Ensure rows act like dictionaries for easy access and serialization
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        
        if cursor.description is None:
            # Query did not return rows (e.g. INSERT, UPDATE)
            conn.commit()
            return [{"status": "Query executed successfully, no rows returned."}]
        
        results = []
        for row in cursor.fetchall():
            results.append(dict(row))
            
        return results
    except Exception as e:
        raise RuntimeError(f"Database query execution failed: {e}")
    finally:
        if conn:
            conn.close()
