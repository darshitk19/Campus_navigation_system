from flask import Flask, render_template, request
import folium
import os
import json

app = Flask(__name__)

# Building codes mapped to names
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

    for filename in available_files:
        if filename.endswith('.geojson') and '_to_' in filename:
            parts = filename[:-8].split('_to_')
            if len(parts) == 2:
                valid_paths.add((parts[0], parts[1]))

    start_points = sorted(set(start for start, _ in valid_paths if start in BUILDING_NAMES))

    destinations_by_start = {
        start: sorted(
            [(end, BUILDING_NAMES.get(end, end)) for s, end in valid_paths if s == start and end in BUILDING_NAMES]
        ) for start in start_points
    }

    return render_template(
        'index.html',
        destinations_by_start=destinations_by_start,
        building_names=BUILDING_NAMES,
        destinations=BUILDING_NAMES
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

    path_file = f'paths/{start}_to_{end}.geojson'
    if not os.path.exists(path_file):
        return f"Path file '{start}_to_{end}.geojson' not found in paths/ folder."

    with open(path_file) as f:
        path_data = json.load(f)

    if not path_data.get('features'):
        return "GeoJSON has no features."

    # Combine all coordinates from all LineString features
    all_coords = []
    for feature in path_data['features']:
        if feature['geometry']['type'] == 'LineString':
            all_coords.extend(feature['geometry']['coordinates'])

    if not all_coords:
        return "No coordinates found in GeoJSON."

    # Add the full path as one layer
    folium.GeoJson(
        path_data,
        name='Path',
        popup=folium.Popup(f'{BUILDING_NAMES.get(start)} to {BUILDING_NAMES.get(end)}', max_width=250)
    ).add_to(m)

    start_coords = all_coords[0][::-1]
    end_coords = all_coords[-1][::-1]

    # Start marker
    folium.Marker(start_coords, icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(
        location=start_coords,
        icon=folium.DivIcon(html=f"""
            <div style="white-space: nowrap; font-size:12px; font-weight:bold; color:white; background-color:green; padding:3px 8px; border-radius:5px;">
                {BUILDING_NAMES.get(start)}
            </div>
        """)
    ).add_to(m)

    # End marker
    folium.Marker(end_coords, icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(
        location=end_coords,
        icon=folium.DivIcon(html=f"""
            <div style="white-space: nowrap; font-size:12px; font-weight:bold; color:white; background-color:red; padding:3px 8px; border-radius:5px;">
                {BUILDING_NAMES.get(end)}
            </div>
        """)
    ).add_to(m)

    # Title
    title_html = f"<h3 align='center' style='font-size:20px'><b>{BUILDING_NAMES.get(start)} to {BUILDING_NAMES.get(end)}</b></h3>"
    m.get_root().html.add_child(folium.Element(title_html))

    return render_template('map.html', map=m._repr_html_())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
