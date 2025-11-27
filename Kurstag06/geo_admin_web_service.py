from flask import Flask, render_template_string
import folium


app = Flask(__name__)

def generate_map(latitude, longitude, zoom):
    ch_map = folium.Map(location=[latitude, longitude], zoom_start=zoom)
    folium.raster_layers.WmsTileLayer(
        url="https://wms.geo.admin.ch/",
        name="Swiss Topo Map",
        layers="ch.swisstopo.pixelkarte-farbe",
        fmt="image/png",
        transparent=True
    ).add_to(ch_map)
    return ch_map._repr_html_()

@app.route('/')
def home():
    map_html = generate_map(46.801108267, 8.226663632, 8)
    return render_template_string('<html><body><div style="text-align: center; margin-bottom: 8px;"><a href="/teko_bern"><button>TEKO Bern</button></div></a>{{ map_html|safe }}</body></html>', map_html=map_html)

@app.route('/teko_bern')
def teko_bern():
    map_html = generate_map(46.943452799, 7.432701655, 18)
    return render_template_string('<html><body><div style="text-align: center; margin-bottom: 8px;"><a href="/teko_bern"><button>TEKO Bern</button></div></a>{{ map_html|safe }}</body></html>', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
