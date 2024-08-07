import winreg
import os
import shutil
import subprocess
import ctypes

class Tweaks:
    # Métodos para ajustar configuraciones adicionales

    def crear_punto_de_restauracion(self):
        try:
            # Verificar el estado del servicio VSS
            print("Verificando el estado del servicio VSS...")
            command = ['powershell', '-Command', 'Get-Service -Name VSS']
            result = subprocess.run(command, capture_output=True, text=True)
            
            if 'Running' not in result.stdout:
                # El servicio VSS no está en ejecución, intentamos iniciarlo
                print("El servicio VSS no está en ejecución. Intentando iniciar...")
                command = ['powershell', '-Command', 'Start-Service -Name VSS; Set-Service -Name VSS -StartupType Automatic']
                result = subprocess.run(command, capture_output=True, text=True)

                if result.returncode == 0:
                    print("Servicio VSS habilitado y en ejecución.")
                else:
                    print("No se pudo iniciar el servicio VSS.")
                    print(result.stderr)
                    return  # Salir de la función si no se puede iniciar el servicio
            else:
                print("El servicio VSS ya está en ejecución.")
            
            # Intentar habilitar la protección del sistema en todas las unidades
            print("Habilitando la protección del sistema...")
            command = [
                'powershell', '-Command',
                'foreach ($drive in (Get-Volume | Where-Object { $_.DriveType -eq "Fixed" })) { Enable-ComputerRestore -Drive "$($drive.DriveLetter):" }'
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Protección del sistema habilitada en todas las unidades.")
            else:
                print("Error al habilitar la protección del sistema:")
                print(result.stderr)
                return  # Salir de la función si no se puede habilitar la protección
            
            # Crear punto de restauración
            print("Creando punto de restauración...")
            command = ['powershell', '-Command', "Checkpoint-Computer -Description 'Automatic Restore Point' -RestorePointType 'MODIFY_SETTINGS'"]
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                print("Punto de restauración creado con éxito.")
            else:
                print("Error al crear el punto de restauración:")
                print(result.stderr)
        
        except Exception as e:
            print(f"Error: {e}")


    def desactivar_ventanas_fluorescentes(self):
        # Desactivar ventanas fluorescentes (transparencia en las ventanas)
        print("Disabling fluorescent windows...")
        try:
            key = r"SOFTWARE\Microsoft\Windows\DWM"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "EnableTransparency", 0, winreg.REG_DWORD, 0)
                print("Fluorescent windows disabled.")
        except FileNotFoundError:
            print("Registry key not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def activar_tema_oscuro(self):
        try:
            print("Activando el tema oscuro...")
            command = (
                'powershell -Command "Set-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize\' '
                '-Name \'AppsUseLightTheme\' -Value 0 -Type DWord"'
            )
            subprocess.run(command, check=True, shell=True)
            print("Tema oscuro activado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al activar el tema oscuro: {e}")

    def desactivar_tema_oscuro(self):
        try:
            print("Desactivando el tema oscuro...")
            command = (
                'powershell -Command "Set-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize\' '
                '-Name \'AppsUseLightTheme\' -Value 1 -Type DWord"'
            )
            subprocess.run(command, check=True, shell=True)
            print("Tema oscuro desactivado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al desactivar el tema oscuro: {e}")

    def activar_numlock_al_inicio(self):
        try:
            print("Activando NumLock al inicio...")
            command = (
                'powershell -Command "Set-ItemProperty -Path \'HKCU:\\Control Panel\\Keyboard\' '
                '-Name \'InitialKeyboardIndicators\' -Value 2 -Type String"'
            )
            subprocess.run(command, check=True, shell=True)
            print("NumLock activado al inicio exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al activar NumLock al inicio: {e}")

    def desactivar_numlock_al_inicio(self):
        try:
            print("Desactivando NumLock al inicio...")
            command = (
                'powershell -Command "Set-ItemProperty -Path \'HKCU:\\Control Panel\\Keyboard\' '
                '-Name \'InitialKeyboardIndicators\' -Value 0 -Type String"'
            )
            subprocess.run(command, check=True, shell=True)
            print("NumLock desactivado al inicio exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al desactivar NumLock al inicio: {e}")

    def activar_teclas_adhesivas(self):
        try:
            print("Activando teclas adhesivas...")
            command = (
                'powershell -Command "Set-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Accessibility\' '
                '-Name \'StickyKeys\' -Value 1 -Type DWord"'
            )
            subprocess.run(command, check=True, shell=True)
            print("Teclas adhesivas activadas exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al activar teclas adhesivas: {e}")

    def desactivar_teclas_adhesivas(self):
        try:
            print("Desactivando teclas adhesivas...")
            command = (
                'powershell -Command "Set-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Accessibility\' '
                '-Name \'StickyKeys\' -Value 0 -Type DWord"'
            )
            subprocess.run(command, check=True, shell=True)
            print("Teclas adhesivas desactivadas exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al desactivar teclas adhesivas: {e}")

    def mostrar_archivos_ocultos(self):
        try:
            print("Mostrando archivos ocultos...")
            command = (
                'powershell -Command "Set-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\' '
                '-Name \'Hidden\' -Value 1 -Type DWord"'
            )
            subprocess.run(command, check=True, shell=True)
            print("Archivos ocultos ahora son visibles.")
        except subprocess.CalledProcessError as e:
            print(f"Error al mostrar archivos ocultos: {e}")

    def ocultar_archivos_ocultos(self):
        try:
            print("Ocultando archivos ocultos...")
            command = (
                'powershell -Command "Set-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\' '
                '-Name \'Hidden\' -Value 2 -Type DWord"'
            )
            subprocess.run(command, check=True, shell=True)
            print("Archivos ocultos ahora están ocultos.")
        except subprocess.CalledProcessError as e:
            print(f"Error al ocultar archivos ocultos: {e}")

    def mostrar_extensiones_de_archivos(self):
        # Muestra las extensiones de los archivos en el Explorador de archivos
        print("Showing file extensions...")
        try:
            key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "HideFileExt", 0, winreg.REG_DWORD, 0)
                print("File extensions are now visible.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def ocultar_extensiones_de_archivos(self):
        # Oculta las extensiones de los archivos en el Explorador de archivos
        print("Hiding file extensions...")
        try:
            key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "HideFileExt", 0, winreg.REG_DWORD, 1)
                print("File extensions are now hidden.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def is_preference_enabled(self, preference_name):
        # Implementar la lógica para comprobar si una preferencia está habilitada
        if preference_name == "Tema Oscuro para Windows":
            return self._is_dark_theme_enabled()
        elif preference_name == "NumLock al Iniciar":
            return self._is_numlock_enabled()
        elif preference_name == "Teclas Adhesivas":
            return self._is_sticky_keys_enabled()
        elif preference_name == "Mostrar Archivos Ocultos":
            return self._are_hidden_files_visible()
        elif preference_name == "Mostrar Extensiones de Archivos":
            return self._are_file_extensions_visible()
        return False

    def _is_dark_theme_enabled(self):
        # Comprobar si el tema oscuro está habilitado en el registro
        try:
            key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
                value = winreg.QueryValueEx(reg_key, "AppsUseLightTheme")[0]
                return value == 0  # 0 indica que el tema oscuro está habilitado
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def _is_numlock_enabled(self):
        # Comprobar si NumLock está habilitado al inicio en el registro
        try:
            key = r"Control Panel\\Keyboard"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
                value = winreg.QueryValueEx(reg_key, "InitialKeyboardIndicators")[0]
                return value == "2"  # "2" indica que NumLock está habilitado
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def _is_sticky_keys_enabled(self):
        # Comprobar si las teclas adhesivas están habilitadas en el registro
        try:
            key = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Accessibility"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
                value = winreg.QueryValueEx(reg_key, "StickyKeys")[0]
                return value == 1  # 1 indica que las teclas adhesivas están habilitadas
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def _are_hidden_files_visible(self):
        # Comprobar si los archivos ocultos son visibles en el Explorador de archivos
        try:
            key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
                value = winreg.QueryValueEx(reg_key, "Hidden")[0]
                return value == 1  # 1 indica que los archivos ocultos son visibles
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def _are_file_extensions_visible(self):
        # Comprobar si las extensiones de los archivos son visibles en el Explorador de archivos
        try:
            key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as reg_key:
                value = winreg.QueryValueEx(reg_key, "HideFileExt")[0]
                return value == 0  # 0 indica que las extensiones de los archivos son visibles
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def ejecutar_limpieza_de_disco(self):
        # Ejecutar la limpieza de disco utilizando PowerShell
        try:
            print("Ejecutando limpieza de disco...")
            # Comando de PowerShell para iniciar la limpieza de disco
            clean_command = 'powershell -Command "Start-Process cleanmgr -ArgumentList \'/sagerun:1\' -NoNewWindow -Wait"'
            subprocess.run(clean_command, check=True, shell=True)
            print("Limpieza de disco completada exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar la limpieza de disco: {e}")

    def desactivar_seguimiento_de_ubicacion(self):
        # Crear la clave del registro si no existe
        try:
            print("Desactivando el seguimiento de ubicación...")
            
            # Comando para crear la clave del registro
            create_registry_key_command = (
                'powershell -Command "New-Item -Path \'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\LocationAndSensors\' '
                '-Force"'
            )
            subprocess.run(create_registry_key_command, check=True, shell=True)
            
            # Comando para desactivar el seguimiento de ubicación
            disable_location_tracking_command = (
                'powershell -Command "Set-ItemProperty -Path \'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\LocationAndSensors\' '
                '-Name \'DoNotAllowLocation\' -Value 1 -Type DWord"'
            )
            subprocess.run(disable_location_tracking_command, check=True, shell=True)
            
            print("Seguimiento de ubicación desactivado exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al desactivar el seguimiento de ubicación: {e}")

