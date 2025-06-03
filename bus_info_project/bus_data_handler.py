# bus_data_handler.py

import pandas as pd

class BusRouteFinder:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def find_routes(self, origin, destination):
        results = []
        grouped = self.df.groupby(['route_name', 'direction_text'])

        for (route, direction), group in grouped:
            stops = group.sort_values('stop_number')
            stop_names = stops['stop_name'].tolist()

            if origin in stop_names and destination in stop_names:
                origin_idx = stop_names.index(origin)
                dest_idx = stop_names.index(destination)

                if origin_idx < dest_idx:
                    results.append({
                        'route_name': route,
                        'direction_text': direction,
                        'stops': stop_names[origin_idx:dest_idx + 1]
                    })

        return results
