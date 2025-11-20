import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium



class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GeoAdminMapApp2")
        self.setGeometry(100, 100, 800, 600)

        # Name temporary Folium map
        self.map_file = "map.html"
        self.browser = None

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Button to zoom to TEKO Bern
        bern_button = QPushButton("TEKO Bern")
        width = bern_button.fontMetrics().boundingRect("TEKO Bern").width() + 27
        bern_button.setMaximumWidth(width)

        # Create a horizontal layout to center the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(bern_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # WebView to display the map
        self.browser = QWebEngineView(None)
        bern_button.clicked.connect(self.zoom_to_teko_bern)  # type: ignore

        self.generate_and_load_map(46.801108267, 8.226663632, 8)
        layout.addWidget(self.browser)

    def generate_and_load_map(self, latitude, longitude, zoom):
        # Create a folium map
        ch_map = folium.Map(location=[latitude, longitude], zoom_start=zoom)
        # To generate the map without Open Street Map
        # map = folium.Map(location=[latitude, longitude], zoom_start=zoom, tiles=None)

        # Add WMS layer from geo.admin.ch
        folium.raster_layers.WmsTileLayer(
            url="https://wms.geo.admin.ch/",
            name="Swiss Topo Map",
            layers="ch.swisstopo.pixelkarte-farbe",
            fmt="image/png",
            transparent=True
        ).add_to(ch_map)

        # Save and load the updated map
        ch_map.save(self.map_file)
        self.browser.load(QUrl.fromLocalFile(os.path.abspath(self.map_file)))

    def zoom_to_teko_bern(self):
        self.generate_and_load_map(46.943452799, 7.432701655, 18)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MapApp()
    main_window.show()
    sys.exit(app.exec_())
