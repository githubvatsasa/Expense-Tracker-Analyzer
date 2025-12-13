#!/usr/bin/env python3
# Expense Tracker and Analyzer Application
# Track, categorize, and analyze personal expenses

import sqlite3
import json
from datetime import datetime
from typing import List, Dict

class ExpenseTracker:
    """Main Expense Tracker application class"""
    
    def __init__(self, db_name='expenses.db'):
        """Initialize the expense tracker with database connection"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.initialize_database()
    
    def initialize_database(self):
        """Create database and tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        # Create expenses table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create categories table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )
        ''')
        
        # Create budget table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                limit_amount REAL NOT NULL,
                month TEXT NOT NULL
            )
        ''')
        
        self.conn.commit()
    
    def add_expense(self, date: str, category: str, description: str, amount: float, payment_method: str = 'Cash'):
        """Add a new expense to the tracker"""
        try:
            self.cursor.execute('''
                INSERT INTO expenses (date, category, description, amount, payment_method)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, category, description, amount, payment_method))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding expense: {e}")
            return False
    
    def get_expenses_by_category(self, category: str) -> List[Dict]:
        """Get all expenses for a specific category"""
        self.cursor.execute('''
            SELECT * FROM expenses WHERE category = ? ORDER BY date DESC
        ''', (category,))
        rows = self.cursor.fetchall()
        return [self._row_to_dict(row) for row in rows]
    
    def get_monthly_summary(self, month: str) -> Dict:
        """Get spending summary for a month"""
        self.cursor.execute('''
            SELECT category, SUM(amount) FROM expenses 
            WHERE strftime('%Y-%m', date) = ? 
            GROUP BY category
        ''', (month,))
        rows = self.cursor.fetchall()
        return {row[0]: row[1] for row in rows}
    
    def _row_to_dict(self, row) -> Dict:
        """Convert database row to dictionary"""
        return {
            'id': row[0],
            'date': row[1],
            'category': row[2],
            'description': row[3],
            'amount': row[4],
            'payment_method': row[5]
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    """Main application entry point"""
    tracker = ExpenseTracker()
    print("Expense Tracker Application Started")
    # Add your main logic here
    tracker.close()


if __name__ == '__main__':
    main()
