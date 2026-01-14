from circuit_synth import *
from pathlib import Path
import shutil

VREGULATOR_TOREX = Component(
    symbol="SamacSys_Parts:XC6220B331MR-G",
    footprint="SamacSys_Parts:SOT95P280X130-5N",
    datasheet="https://www.torexsemi.com/file/xc6220/XC6220.pdf",
    description="TOREX - XC6220B331MR-G - IC, LDO, 1A, 3.3V, SOT-25"
)


# @circuit(name="simple_led")
# def simple_led():
#     """
#     Simple LED circuit with current limiting resistor.
#     Perfect for getting started with Circuit-Synth!
#     """

#     # Create power nets
#     VCC_3V3 = Net('VCC_3V3')
#     GND = Net('GND')

#     # Create LED component
#     led = Component(
#         symbol="Device:LED",
#         ref="D1",
#         value="Red",
#         footprint="LED_SMD:LED_0603_1608Metric"
#     )

#     # Create current limiting resistor
#     resistor = Component(
#         symbol="Device:R",
#         ref="R1",
#         value="330",
#         footprint="Resistor_SMD:R_0603_1608Metric"
#     )

#     # Make connections
#     VCC_3V3 += resistor[1]     # Power to resistor
#     resistor[2] += led[1]      # Resistor to LED anode
#     led[2] += GND              # LED cathode to ground

# @circuit(name="usb_power_supply")
# def usb_power_supply():
#     # Create power nets
#     VCC_3V3 = Net('VCC_3V3')
#     GND = Net('GND')
#     ground = Component(
#         symbol="power:GND", 
#         ref="#PWR",        # Let KiCad assign the ref automatically
#     )
#     ground[1] += GND
#     vcc = Component(
#         symbol="power:VCC", 
#         ref="#PWR",        # Let KiCad assign the ref automatically
#     )
#     vcc[1] += VCC_3V3       
#     # R1 
#     resistor_r1 = Component(
#         symbol="Device:R",
#         ref="R1",
#         value="5.1k",
#         footprint="Resistor_SMD:R_0603_1608Metric",
    
#     )
    
        
#     # R1 to GND
#     resistor_r1[1] += VCC_3V3
#     resistor_r1[2] += GND


def usb_power_supply():
    regulator_ic1 = VREGULATOR_TOREX()
    regulator_ic1.ref = "IC1"


@circuit
def main_circuit():
    usb_power_supply()
    

if __name__ == "__main__":
    project_name = "first_circuit"
    project_folder = Path(".") / project_name
    if project_folder.exists():
        shutil.rmtree(project_folder)
        
    circuit = main_circuit()
    circuit.generate_kicad_project(project_name, generate_pcb=False )

