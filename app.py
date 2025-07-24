from flask import Flask, render_template, request
import folium
import os
import json

app = Flask(__name__)

# Mapping of building shortcuts to full names
BUILDING_NAMES = {
    'admin': 'Admin Building',
    'arip': 'Ashok & Rita Patel Institute of Physiotherapy',
    'bd': 'Bapubhai Desaibhai Patel Institute of Paramedical Sciences',
    'cmpica': 'Chandaben Mohanbhai Patel Institute of Computer Applications',
    'cscm': 'CSPIT – Civil Engineering',
    'csec': 'CSPIT – Electronics & Communication',
    'dep': 'Devang Patel Institute of Advance Technology and Research (DEPSTAR)',
    'gh3': 'Girls Hostel 3',
    'hospital': 'Charusat Hospital',
    'iiim': 'Indukaka Ipcowala Institute of Management',
    'jcph': 'J.C. Patel Hostel',
    'kkh': 'Kalson Kashiba Hostel',
    'mtin': 'Manikaka Topawala Institute of Nursing',
    'nidhisha': 'Food Plaza',
    'pd': 'P.D. Patel Institute of Applied Sciences',
    'rpcp': 'Ramanbhai Patel College of Pharmacy',
    'back': 'Back Gate',
    'front': 'Front Gate'
}


@app.route('/')
def index():
    available_files = os.listdir('paths')
    valid_paths = set()

    # Extract valid (start, end) pairs
    for filename in available_files:
        if filename.endswith('.geojson') and '_to_' in filename:
            parts = filename[:-8].split('_to_')  # remove ".geojson"
            if len(parts) == 2:
                valid_paths.add((parts[0], parts[1]))

    # Get unique start points (like front, back, admin, etc.)
    start_points = sorted(set(start for start, _ in valid_paths if start in BUILDING_NAMES))

    # Build destination mapping for each start
    destinations_by_start = {
        start: sorted(
            [(end, BUILDING_NAMES.get(end, end)) for s, end in valid_paths if s == start and end in BUILDING_NAMES]
        ) for start in start_points
    }

    return render_template(
    'index.html',
    destinations_by_start=destinations_by_start,
    building_names=BUILDING_NAMES,
    destinations=BUILDING_NAMES   # ✅ Fix here
)



@app.route('/map')
def show_map():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return "Invalid input."

    map_center = [22.6000, 72.8200]
    m = folium.Map(
        location=map_center,
        zoom_start=17,
        min_zoom=16,
        max_zoom=18,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Tiles © Esri'
    )

    # Path file
    path_file = f'paths/{start}_to_{end}.geojson'
    if not os.path.exists(path_file):
        return f"Path file '{start}_to_{end}.geojson' not found in paths/ folder."

    with open(path_file) as f:
        path_data = json.load(f)
        folium.GeoJson(path_data, name='Path').add_to(m)

    start_name = BUILDING_NAMES.get(start, start)
    end_name = BUILDING_NAMES.get(end, end)

    # Get coordinates from GeoJSON
    start_coords = path_data['features'][0]['geometry']['coordinates'][0][::-1]
    end_coords = path_data['features'][0]['geometry']['coordinates'][-1][::-1]

    # Add start marker + label
    folium.Marker(start_coords, icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(
        location=start_coords,
        icon=folium.DivIcon(html=f"""
        <div style="white-space: nowrap; font-size:12px; font-weight:bold; color:white; background-color:green; padding:3px 8px; border-radius:5px;">
            {start_name}
        </div>
        """)
    ).add_to(m)

    # Add end marker + label
    folium.Marker(end_coords, icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(
        location=end_coords,
         icon=folium.DivIcon(html=f"""
        <div style="white-space: nowrap; font-size:12px; font-weight:bold; color:white; background-color:red; padding:3px 8px; border-radius:5px;">
            {end_name}
        </div>
        """)
    ).add_to(m)

    # Title
    title_html = f"<h3 align='center' style='font-size:20px'><b>{start_name} to {end_name}</b></h3>"
    m.get_root().html.add_child(folium.Element(title_html))

    return render_template('map.html', map=m._repr_html_())

if __name__ == '__main__':
    app.run(debug=True)
