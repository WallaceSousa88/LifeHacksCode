import os
import re
import time
import json
import folium
import requests
from bs4 import BeautifulSoup, Tag

def get_ip(ip, json_file='ip_info.json'):
    try:
        url = f'https://ipapi.co/{ip}/json/'
        response = requests.get(url, verify=False)
        data = response.json()
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"IP info saved to '{json_file}'")
    except Exception as e:
        print(f"Error fetching IP info: {e}")

def wait_file(file_name, timeout=10):
    start = time.time()
    while not os.path.exists(file_name):
        if time.time() - start > timeout:
            raise TimeoutError(f"File '{file_name}' not found after {timeout} seconds.")
        time.sleep(0.5)

def make_map(json_file='ip_info.json', html_file='ip_map.html'):
    wait_file(json_file)
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    lat = data.get('latitude')
    lon = data.get('longitude')
    if lat is None or lon is None:
        raise ValueError("Latitude or longitude not found in JSON.")
    map_obj = folium.Map(location=[0, 0], zoom_start=2, max_bounds=True)
    folium.Marker(
        location=[lat, lon],
        popup=f"{data.get('city')}, {data.get('region')}, {data.get('country_name')}",
        icon=folium.Icon(color='red')
    ).add_to(map_obj)
    map_obj.save(html_file)
    print(f"Map saved as '{html_file}'.")

def fix_html(html_file='ip_map.html'):
    wait_file(html_file)
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    map_div = soup.find('div', class_='folium-map')
    if isinstance(map_div, Tag) and 'id' in map_div.attrs:
        old_id = str(map_div.attrs['id'])
        map_div.attrs['id'] = 'map'
        for script in soup.find_all('script'):
            if isinstance(script, Tag):
                content = script.string
                if isinstance(content, str) and old_id in content:
                    script.clear()
                    script.append(content.replace(old_id, 'map'))
    for style in soup.find_all('style'):
        style.decompose()
    style_tag = soup.new_tag('style')
    style_tag.string = """
    html, body {
        height: 100%;
        width: 100%;
        margin: 0;
        padding: 0;
    }
    #map {
        position: absolute;
        top: 0;
        bottom: 0;
        right: 0;
        left: 0;
        height: 100%;
        width: 100%;
    }
    """
    if soup.head:
        soup.head.append(style_tag)
    for script in soup.find_all('script'):
        if isinstance(script, Tag):
            content = script.string
            if isinstance(content, str) and 'L.map(' in content:
                lines = content.splitlines()
                new_lines = []
                for line in lines:
                    line = line.replace(',,', ',')
                    if '"zoom":' in line:
                        line = re.sub(r'"zoom":\s*\d+', '"zoom": 3', line)
                    if '"minZoom":' in line:
                        line = re.sub(r'"minZoom":\s*\d+', '"minZoom": 3', line)
                    elif '"zoom": 3' in line and '"minZoom":' not in line:
                        line = line.replace(
                            '"zoom": 3',
                            '"zoom": 3, "minZoom": 3, "maxBounds": [[-85, -180], [85, 180]], "maxBoundsViscosity": 1.0'
                        )
                    new_lines.append(line)
                script.clear()
                script.append('\n'.join(new_lines))
    for script in soup.find_all('script'):
        if isinstance(script, Tag):
            content = script.string
            if isinstance(content, str) and 'L.tileLayer' in content:
                lines = content.splitlines()
                new_lines = []
                for line in lines:
                    if '"noWrap": false' in line:
                        line = line.replace('"noWrap": false', '"noWrap": true')
                    new_lines.append(line)
                script.clear()
                script.append('\n'.join(new_lines))
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"HTML updated successfully in '{html_file}'.")

if __name__ == '__main__':
    get_ip('187.69.91.52')
    wait_file('ip_info.json')
    make_map()
    wait_file('ip_map.html')
    fix_html()
