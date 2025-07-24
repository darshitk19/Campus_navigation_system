import json
import os
import glob

class PathLoader:
    def __init__(self, path_dir):
        self.path_dir = path_dir
        self.paths = self.load_paths()

    def load_paths(self):
        all_paths = {}
        for filename in os.listdir(self.path_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.path_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    key = f"{data['start']} - {data['end']}"
                    all_paths[key] = data
        return all_paths

    def get_all_paths(self):
        return self.paths

    def get_all_locations(self):
        locations = set()
        for path in self.paths.values():
            locations.add(path['start'])
            locations.add(path['end'])
        return sorted(locations)

