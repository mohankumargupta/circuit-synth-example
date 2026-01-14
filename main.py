from circuit_synth import *
from pathlib import Path
import shutil

VREGULATOR_TOREX = Component(
    symbol="SamacSys_Parts:XC6220B331MR-G",
    footprint="SamacSys_Parts:SOT95P280X130-5N",
    datasheet="https://www.torexsemi.com/file/xc6220/XC6220.pdf",
    description="TOREX - XC6220B331MR-G - IC, LDO, 1A, 3.3V, SOT-25"
)

C_10uF_0603 = Component(
    symbol="Device:C", ref="C", value="10uF", footprint="Capacitor_SMD:C_0603"
)

C_01uF_0603 = Component(
    symbol="Device:C", ref="C", value="0.1uF", footprint="Capacitor_SMD:C_0603"
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
    # Create main nets
    _5v = Net("5V")
    _3v3 = Net("3V3")
    GND = Net("GND")

    # Create dictionaries of nets instead of buses
    usb_nets = {"d_minus": Net("USB_DM"), "d_plus": Net("USB_DP")}  # D-  # D+

    spi_nets = {
        "miso": Net("SPI_MISO"),  # MISO
        "mosi": Net("SPI_MOSI"),  # MOSI
        "sck": Net("SPI_SCK"),  # SCK
        "cs": Net("SPI_CS"),  # CS
    }

    int_nets = {"int1": Net("INT1"), "int2": Net("INT2")}


    regulator_ic1 = VREGULATOR_TOREX()
    regulator_ic1.ref = "IC1"

    capacitor_c5 = C_10uF_0603()
    capacitor_c5.ref = "C5"

    capacitor_c7 = C_01uF_0603()
    capacitor_c7.ref = "C7"

    # Connections
    # connect pin 5 of VREG to capacitors
    regulator_ic1[5] += capacitor_c5[1]
    regulator_ic1[5] += capacitor_c7[1]

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

