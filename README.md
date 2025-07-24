# 🗺️ Campus Navigation System - Flask + Folium

An interactive **campus navigation tool** built with **Python**, **Flask**, and **Folium**, designed to help users find optimal paths within a campus using a web-based interface.

---

## 🚀 Features

- 🌍 **Dynamic Map Rendering** with [Folium](https://python-visualization.github.io/folium/)
- 🖥️ **Web Interface** using [Flask](https://flask.palletsprojects.com/)
- 📍 **Dropdown-based Location Selection** for easy navigation
- 🧭 **Shortest Path Visualization** using GeoJSON route data

---

## 🛠️ Installation & Setup

Get started in just a few steps! 🔧💻

### 📦 Step 1: Clone the Repository

```
git clone https://github.com/darshitk19/Campus_navigation_system.git
cd Campus_navigation_system
```
### ⚙️ Step 2: Install Dependencies
# Preferred: use requirements file
pip install -r requirements.txt
Or, install manually:

pip install flask folium
▶️ Running the Application
Launch the Flask server locally:

python app.py
Then open your browser and visit:


http://127.0.0.1:5000
You'll see an interactive dropdown-based map UI for navigation. 🗺️

📁 Project Structure
```
Campus_navigation_system/
├── app.py                # Main Flask application logic
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
│
├── data/
│   └── PATHS/            # GeoJSON route files for navigation
│
├── templates/            # HTML templates for Flask rendering
│   └── index.html        # Main UI with map and dropdowns
│
└── static/               # Static assets (CSS, JS, icons)
    └── style.css         # (Optional) Custom styles

```
📌 Notes
✅ Ensure .geojson path files are inside the data/PATHS/ folder.

✅ Start and end location names in the dropdown should match those defined in the backend mapping.

✅ Routes are visualized dynamically using Folium on each request.


### 📸 Screenshots

# 🧭 UI with Dropdown & Map
![Campus_navigation_system](IMAGES/Screenshot%202025-07-24%20135738.png)

# 📍 Route Highlight Example
![Campus_navigation_system](IMAGES/Screenshot%202025-07-24%20135752.png)




### 👤 Author
Darshit Kachhadiya
