from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform

class BluetoothApp(App):

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.status_label = Label(text="Welcome! Press Scan.", size_hint_y=0.1)
        scan_button = Button(text="List Paired Devices", on_press=self.list_paired_devices)
        
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(scan_button)
        return self.layout

    def list_paired_devices(self, instance):
        if platform != 'android':
            self.status_label.text = "This only works on Android."
            return

        from jnius import autoclass
        self.status_label.text = "Scanning..."
        try:
            BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
            default_adapter = BluetoothAdapter.getDefaultAdapter()
            paired_devices = default_adapter.getBondedDevices().toArray()
            
            if not paired_devices:
                self.status_label.text = "No paired devices found."
            else:
                device_names = [device.getName() for device in paired_devices]
                self.status_label.text = "Paired Devices:\n" + "\n".join(device_names)
        except Exception as e:
            self.status_label.text = f"Error: {e}"

if __name__ == '__main__':
    BluetoothApp().run()