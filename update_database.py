#!/usr/bin/env python3
"""
Helper script to process simulation logs and update the database.
Run this after completing a simulation to update the database for Streamlit Cloud.
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime
import glob

def process_simulation_logs():
    """Process the latest simulation log and update the database."""
    
    # Find the latest collision log
    log_files = glob.glob("simulations/*_collision_log.csv")
    if not log_files:
        print("No collision logs found in simulations/ directory")
        return
    
    latest_log = max(log_files, key=os.path.getctime)
    print(f"Processing: {latest_log}")
    
    # Read the collision log
    df = pd.read_csv(latest_log)
    
    # Extract date from filename (format: YYYYMMDD_HHMMSS_collision_log.csv)
    filename = os.path.basename(latest_log)
    date_str = filename.split('_')[0] + '_' + filename.split('_')[1]
    
    # Connect to database
    conn = sqlite3.connect('data/daily_stats.db')
    
    try:
        # Process the data and update database
        # This is a simplified version - you may need to adapt based on your database schema
        
        # Get unique players and their stats
        player_stats = df.groupby('Particle').agg({
            'Force Received': 'sum',
            'Killed': 'sum'
        }).reset_index()
        
        # Calculate kills (when opponent was killed)
        kills_df = df[df['Killed'] == True].groupby('Opponent').size().reset_index(name='kills')
        kills_df.columns = ['player', 'kills']
        
        # Merge with player stats
        final_stats = player_stats.merge(kills_df, left_on='Particle', right_on='player', how='left')
        final_stats['kills'] = final_stats['kills'].fillna(0)
        final_stats['deaths'] = final_stats['Killed']
        
        # Insert into database (adjust table names and columns as needed)
        for _, row in final_stats.iterrows():
            conn.execute("""
                INSERT OR REPLACE INTO player_stats 
                (date, player, kills, deaths, damage_received) 
                VALUES (?, ?, ?, ?, ?)
            """, (date_str, row['Particle'], int(row['kills']), int(row['deaths']), row['Force Received']))
        
        # Find the winner (last player alive)
        last_entries = df.tail(10)  # Check last few entries
        winner = None
        for _, row in last_entries.iterrows():
            if not row['Killed']:
                winner = row['Particle']
                break
        
        if winner:
            # Update daily summary
            conn.execute("""
                INSERT OR REPLACE INTO daily_summary 
                (date, num_players, winner) 
                VALUES (?, ?, ?)
            """, (date_str, len(final_stats), winner))
        
        conn.commit()
        print(f"✅ Database updated successfully for date: {date_str}")
        print(f"📊 Processed {len(final_stats)} players")
        print(f"🏆 Winner: {winner}")
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    process_simulation_logs()
