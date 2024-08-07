import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QPushButton, QGroupBox, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QDesktopServices, QFont
from PyQt5.QtCore import QUrl, Qt
from tweaks import Tweaks

class TweakerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tweaks = Tweaks()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('E4sy TwE4ks')
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: white;
            }
            QCheckBox, QLabel {
                font-size: 14px;
                font-family: 'Arial', sans-serif;
                font-weight: bold;
                color: white;
            }
            QPushButton {
                background-color: #00aaff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 5px;
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0099cc;
            }
            QGroupBox {
                margin: 20px;
                padding: 10px;
                border: 1px solid #444444;
                border-radius: 5px;
                font-family: 'Arial', sans-serif;
                font-weight: bold;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        main_layout = QVBoxLayout()

        # Add title
        title_label = QLabel("E4sy TwE4ks")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Monospace"))
        title_label.setStyleSheet("color: #00ff00; font-size: 80px;")

        main_layout.addWidget(title_label)

        content_layout = QHBoxLayout()

        # Add essential tweaks section
        tweaks_box = QGroupBox("Essential Tweaks")
        tweaks_layout = QVBoxLayout()

        self.checkboxes = {
            'Crear Punto de Restauración': QCheckBox('Crear Punto de Restauración'),
            'Desactivar Telemetría': QCheckBox('Desactivar Telemetría'),
            'Desactivar Wifi Sense': QCheckBox('Desactivar Wifi Sense'),
            'Desactivar Historial de Actividad': QCheckBox('Desactivar Historial de Actividad'),
            'Eliminar Archivos Temporales': QCheckBox('Eliminar Archivos Temporales'),
            'Ejecutar Limpieza de Disco': QCheckBox('Ejecutar Limpieza de Disco'),
            'Desactivar Seguimiento de Ubicación': QCheckBox('Desactivar Seguimiento de Ubicación'),
            'Desactivar HomeGroup': QCheckBox('Desactivar HomeGroup'),
            'Desactivar Sensor de Almacenamiento': QCheckBox('Desactivar Sensor de Almacenamiento'),
            'Desactivar Hibernación': QCheckBox('Desactivar Hibernación'),
            'Desactivar GameDVR': QCheckBox('Desactivar GameDVR'),
            'Desactivar Teredo': QCheckBox('Desactivar Teredo'),
        }

        for cb in self.checkboxes.values():
            tweaks_layout.addWidget(cb)

        tweaks_box.setLayout(tweaks_layout)

        # Add a section for theme and other preferences
        preferences_box = QGroupBox("Preferences")
        preferences_layout = QVBoxLayout()

        self.preference_checkboxes = {
            'Tema Oscuro para Windows': QCheckBox('Tema Oscuro para Windows'),
            'NumLock al Iniciar': QCheckBox('NumLock al Iniciar'),
            'Teclas Adhesivas': QCheckBox('Teclas Adhesivas'),
            'Mostrar Archivos Ocultos': QCheckBox('Mostrar Archivos Ocultos'),
            'Mostrar Extensiones de Archivos': QCheckBox('Mostrar Extensiones de Archivos'),
        }

        for name, cb in self.preference_checkboxes.items():
            cb.setChecked(self.tweaks.is_preference_enabled(name))
            preferences_layout.addWidget(cb)

        preferences_box.setLayout(preferences_layout)

        # Add About section
        about_box = QGroupBox("About")
        about_layout = QVBoxLayout()

        # Crear el layout horizontal para el texto y el enlace
        about_text_layout = QHBoxLayout()
        about_label = QLabel("Desarrollado por: ")
        link = QLabel('<a href="https://github.com/Sxmpl3">Izan Cano González (aKa Sxmpl3)</a>')
        link.setOpenExternalLinks(True)

        # Añadir el label y el enlace al layout horizontal
        about_text_layout.addWidget(about_label)
        about_text_layout.addWidget(link)

        # Crear un contenedor para el layout horizontal
        about_container = QWidget()
        about_container.setLayout(about_text_layout)

        donate_button = QPushButton('Donate')
        donate_button.setFixedWidth(100)  # Hacer el botón más pequeño
        donate_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://google.com')))

        # Añadir el contenedor y el botón al layout vertical
        about_layout.addWidget(about_container)
        about_layout.addWidget(donate_button, alignment=Qt.AlignCenter)
        about_box.setLayout(about_layout)

        # Combine all sections in the main layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(tweaks_box)

        right_layout = QVBoxLayout()
        right_layout.addWidget(preferences_box)
        right_layout.addWidget(about_box)

        content_layout.addLayout(left_layout)
        content_layout.addLayout(right_layout)

        main_layout.addLayout(content_layout)

        # Create Apply button
        apply_button = QPushButton('Apply changes')
        apply_button.setFixedWidth(150)  # Ancho del botón más pequeño
        apply_button.clicked.connect(self.run_tweaks)

        # Add spacer to push the button to the bottom right
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(apply_button)

        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def run_tweaks(self):
        for name, cb in self.checkboxes.items():
            if cb.isChecked():
                function_name = self.get_function_name(name)
                if hasattr(self.tweaks, function_name):
                    method = getattr(self.tweaks, function_name)
                    method()  # Llamada correcta sin argumentos
                else:
                    print(f"Function {function_name} does not exist in Tweaks class.")

        for name, cb in self.preference_checkboxes.items():
            function_name = self.get_function_name(name)
            if cb.isChecked():
                if hasattr(self.tweaks, function_name):
                    method = getattr(self.tweaks, function_name)
                    method()  # Llamada correcta sin argumentos
                else:
                    print(f"Function {function_name} does not exist in Tweaks class.")
            else:
                disable_function_name = function_name.replace('activar', 'desactivar')
                if hasattr(self.tweaks, disable_function_name):
                    method = getattr(self.tweaks, disable_function_name)
                    method()
                else:
                    print(f"Function {disable_function_name} does not exist in Tweaks class.")

    def get_function_name(self, checkbox_name):
        function_map = {
            'Crear Punto de Restauración': 'crear_punto_de_restauracion',
            'Desactivar Telemetría': 'desactivar_telemetria',
            'Desactivar Wifi Sense': 'desactivar_wifi_sense',
            'Desactivar Historial de Actividad': 'desactivar_historial_de_actividad',
            'Eliminar Archivos Temporales': 'eliminar_archivos_temporales',
            'Ejecutar Limpieza de Disco': 'ejecutar_limpieza_de_disco',
            'Desactivar Seguimiento de Ubicación': 'desactivar_seguimiento_de_ubicacion',
            'Desactivar HomeGroup': 'desactivar_homegroup',
            'Desactivar Sensor de Almacenamiento': 'desactivar_sensor_de_almacenamiento',
            'Desactivar Hibernación': 'desactivar_hibernacion',
            'Desactivar GameDVR': 'desactivar_gamedvr',
            'Desactivar Teredo': 'desactivar_teredo',
            'Tema Oscuro para Windows': 'activar_tema_oscuro',
            'NumLock al Iniciar': 'activar_numlock_al_inicio',
            'Teclas Adhesivas': 'activar_teclas_adhesivas',
            'Mostrar Archivos Ocultos': 'mostrar_archivos_ocultos',
            'Mostrar Extensiones de Archivos': 'mostrar_extensiones_de_archivos',
        }
        return function_map.get(checkbox_name, '')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TweakerApp()
    window.show()
    sys.exit(app.exec_())