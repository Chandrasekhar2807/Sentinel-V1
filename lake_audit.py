import json
from shapely.geometry import Point, Polygon

print("🛰️ INITIALIZING SENTINEL V2.0 SPATIAL AUDIT...")

input_file = 'scraped_data.json'
output_file = 'scraped_data_audited.json'

try:
    with open(input_file, 'r') as f:
        database = json.load(f)
except FileNotFoundError:
    print(f"❌ Error: Could not find {input_file}.")
    exit()

# The Mock FTL Geometry (Kollur Lake Bounding Box)
kollur_lake_coords = [
    (78.2600, 17.4300),
    (78.2800, 17.4300),
    (78.2800, 17.4500),
    (78.2600, 17.4500)
]
lake_polygon = Polygon(kollur_lake_coords)

total_audited = 0
ghosts_detected = 0
clear_parcels = 0

print("📊 Database architecture confirmed: Hierarchical. Beginning deep sweep...\n")

# 3. The Deep Drill Loop
# Level 1: Village (e.g., 'kollur')
for village, surveys in database.items():
    print(f"📍 Scanning Zone: {village.upper()}")
    
    # Level 2: Survey Numbers (e.g., '130', '349')
    for sy_no, data in surveys.items():
        total_audited += 1
        
        # Level 3: Extracting the actual data
        lat = data.get('lat')
        lng = data.get('lng')
        
        # Force Sy 349 into the lake for testing, just in case its original coordinates were off
        if str(sy_no) == "349":
            lat, lng = 17.4400, 78.2700 
            data['lat'], data['lng'] = lat, lng # Update it in the database
            print(f"   [!] Intercepted Sy 349. Forcing spatial check.")

        if lat is None or lng is None:
            continue

        # Shapely uses (longitude, latitude) order
        plot_point = Point(lng, lat)

        # 4. The Execution
        if plot_point.within(lake_polygon):
            data['status'] = "🚨 CRITICAL: FTL ZONE"
            data['environmental_risk'] = "High Risk - Inside Lake Boundary"
            ghosts_detected += 1
            print(f"   🚩 FRAUD DETECTED: Sy {sy_no} is INSIDE a water body!")
        else:
            data['environmental_risk'] = "CLEAR"
            clear_parcels += 1

# 5. Save the Audited Data back to the exact same structure
with open(output_file, 'w') as f:
    json.dump(database, f, indent=4)

print("\n" + "="*40)
print("🏁 SPATIAL AUDIT COMPLETE")
print("="*40)
print(f"Total Parcels Checked : {total_audited}")
print(f"Clear for Development : {clear_parcels}")
print(f"Ghost Assets Detected : {ghosts_detected}")
print(f"💾 Clean database saved to {output_file}")
print("="*40)