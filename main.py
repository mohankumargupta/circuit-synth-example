from circuit_synth import *
from pathlib import Path
import shutil

# power:+5V
# power:+3.3V
# power:PWR_FLAG

VREGULATOR_TOREX = Component(
    symbol="SamacSys_Parts:XC6220B331MR-G",
    footprint="SamacSys_Parts:SOT95P280X130-5N",
    datasheet="https://www.torexsemi.com/file/xc6220/XC6220.pdf",
    description="TOREX - XC6220B331MR-G - IC, LDO, 1A, 3.3V, SOT-25"
)

USB_CONNECTOR = Component(
    symbol="SamacSys_Parts:USB4135-GF-A", 
    footprint="SamacSys_Parts:USB4135GFA",
)

C_10uF_0603 = Component(
    symbol="Device:C", ref="C", value="10uF", footprint="Capacitor_SMD:C_0201_0603Metric"
)

C_01uF_0603 = Component(
    symbol="Device:C", ref="C", value="0.1uF", footprint="Capacitor_SMD:C_0201_0603Metric"
)

# Helper function to create nets in schematic
class SchematicNet:
    def __init__(self, source, name=None, is_global=False, power_symbol=None):
        self._user_defined_name = name
        
        # 1. Resolve Net Object
        if isinstance(source, str):
            self.net = Net(source)
        elif hasattr(source, 'net'): 
            self.net = source.net
        else:
            self.net = source

        # 2. Rename
        if name:
            self.net.name = name
            
        # 3. Handle Global/Power Settings
        if power_symbol:
            # If a symbol is provided, it implies the net is a global power net
            self.net.is_power = True
            self.net.power_symbol = power_symbol
        elif is_global:
            # If just is_global is True, default to the standard VCC arrow
            self.net.is_power = True
            self.net.power_symbol = "power:VCC"

    @property
    def name(self):
        return self.net.name

    @name.setter
    def name(self, new_name):
        self._user_defined_name = new_name
        self.net.name = new_name

    def __iadd__(self, other):
        if isinstance(other, SchematicNet):
            self.net += other.net
        else:
            self.net += other

        if self._user_defined_name:
            self.net.name = self._user_defined_name
            
        return self

    
def usb_power_supply():    
    # Create main nets
    NET_5V = Net("5V")
    NET_3V3 = Net("3V3")
    GND = Net("GND")

    # Create nets from regulator
    regulator_nets = {
        "vin": SchematicNet("REGULATOR_VIN"),
        "vss": SchematicNet("REGULATOR_VSS"),
        "ce": SchematicNet("REGULATOR_CE"),
        "vout": SchematicNet("REGULATOR_VOUT"),
    }

    # create components

    regulator_ic1 = VREGULATOR_TOREX()
    regulator_ic1.ref = "IC1"
    regulator_ic1.rotation = 90

    capacitor_c5 = C_10uF_0603()
    capacitor_c5.ref = "C5"

    capacitor_c7 = C_01uF_0603()
    capacitor_c7.ref = "C7"

    # Connect regulator nets
    regulator_nets["vout"] += regulator_ic1[5]
    regulator_nets["vout"] += capacitor_c5[1]

    # Add wires
    capacitor_c5[1] += capacitor_c7[1]


def usb_connector_circuit():
    # 1. Define the Ground Net with the proper symbol
    #    This ensures it uses the "arrow/triangle" symbol shown in your image.
    NET_GND = SchematicNet("GND")

    # 2. Define the Component
    #    (Assuming you have this symbol in your library)
    usb_conn = USB_CONNECTOR()
    usb_conn.ref = "J1"

    # 3. Connect the pins shown in the image
    #    In SKiDL/Circuit-Synth, you can access pins by their name (string).
    NET_GND += usb_conn["MP1"]
    NET_GND += usb_conn["MP2"]

    # Connect the Mounting Pins (Shield)
    # gnd_net += usb_conn["MP1"]
    # gnd_net += usb_conn["MP2"]
    # gnd_net += usb_conn["MP3"]
    # gnd_net += usb_conn["MP4"]
    
    # # Connect the Ground Pin (B12)
    # gnd_net += usb_conn["B12"]




def rc_delay():
    vcc = Net("+3.3V") 
    gnd = Net("GND")
    en  = Net("EN")

    # 2. Define the Components
    # R3: 10k Resistor
    # We use the standard KiCad symbol "Device:R"
    r3 = Component(
        symbol="Device:R", 
        ref="R3",           # Explicitly naming it R3 to match your schematic
        value="10k",
        footprint="Resistor_SMD:R_0603_1608Metric" # Example 0603 footprint
    )

    # C12: 1uF Capacitor
    # We use the standard KiCad symbol "Device:C"
    c12 = Component(
        symbol="Device:C", 
        ref="C12",          # Explicitly naming it C12
        value="1uF",
        footprint="Capacitor_SMD:C_0603_1608Metric" # Example 0603 footprint
    )

    # 3. Connect the Circuit
    # R3 Pin 1 -> +3.3V
    r3[1] += vcc
    
    # R3 Pin 2 -> EN
    r3[2] += en

    # C12 Pin 1 -> EN
    c12[1] += en

    # C12 Pin 2 -> GND
    c12[2] += gnd    

def uart_circuit():
    # 1. Define the Nets
    # Matching the labels in your schematic: RXD, TXD, and GND
    rxd = Net("RXD")
    txd = Net("TXD")
    gnd = Net("GND")

    # 2. Define the Component
    # J3: 3-pin Connector
    # We use the standard KiCad symbol "Connector_Generic:Conn_01x03"
    j3 = Component(
        symbol="Connector_Generic:Conn_01x03",
        ref="J3",
        value="UART_Header",
        # We must choose a footprint. A standard 2.54mm (0.1") pin header is common for UART.
        footprint="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical"
    )

    # 3. Connect the pins based on the schematic
    # Pin 3 -> RXD
    j3[3] += rxd

    # Pin 2 -> TXD
    j3[2] += txd

    # Pin 1 -> GND
    j3[1] += gnd

@circuit
def main_circuit():
    uart_circuit()
    #rc_delay()
    #usb_connector_circuit()
    #usb_power_supply()
    

if __name__ == "__main__":
    project_name = "first_circuit"
    project_folder = Path(".") / project_name
    if project_folder.exists():
        shutil.rmtree(project_folder)
        
    circuit = main_circuit()
    circuit.generate_kicad_project(project_name, generate_pcb=False, force_regenerate=False )

