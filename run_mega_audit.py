import json
import time
import random
import os
from dharani_scraper import run_scraper 

def mega_audit():
    file_path = 'scraped_data.json'
    
    # 1. Load existing data
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                master_db = json.load(f)
            except:
                master_db = {"kollur": {}, "mokila": {}}
    else:
        master_db = {"kollur": {}, "mokila": {}}

    villages = ["kollur", "mokila"]
    
    for village in villages:
        if village not in master_db:
            master_db[village] = {}
            
        print(f"--- 🏗️ Auditing {village.upper()} ---")
        
        for sy in range(1, 501):
            sy_str = str(sy)
            
            # Skip if already exists and has real data
            if sy_str in master_db[village] and master_db[village][sy_str] is not None:
                continue 

            print(f"📡 Requesting Sy {sy}...")
            
            try:
                # 2. RUN SCRAPER
                # We pass (sy, sy) so it only audits this specific number
                full_batch_result = run_scraper(village, sy, sy)
                
                # 3. VERIFY AND EXTRACT
                if full_batch_result and sy_str in full_batch_result:
                    result = full_batch_result[sy_str]
                    master_db[village][sy_str] = result
                    
                    # 4. INSTANT SAVE
                    with open(file_path, 'w') as f:
                        json.dump(master_db, f, indent=4)
                    
                    print(f"✅ SAVED: Sy {sy} | Size now: {os.path.getsize(file_path)} bytes")
                else:
                    print(f"⚠️ Sy {sy} returned no data. Skipping...")

            except Exception as e:
                print(f"❌ ERROR on Sy {sy}: {e}")
                print("⏳ Connection throttled. Sleeping for 30 seconds...")
                time.sleep(30)
                continue 
            
            # STEALTH DELAY: Very important to prevent IP Ban
            time.sleep(random.uniform(5.5, 12.2))

if __name__ == "__main__":
    mega_audit()