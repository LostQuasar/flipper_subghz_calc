import re

HEADER = "Filetype: Flipper SubGhz Setting File\nVersion: 1\n"
STANDARD_FREQ = "Add_standard_frequencies: true\n"
CUSTOM_FREQ = 'Frequency: '

PRESET_NAME = 'Custom_preset_name: '
PRESET_MODULE = "Custom_preset_module: CC1101\n"
PRESET_DATA = 'Custom_preset_data:'
CRYSTAL_FRQUENCY = 26000000
MODEM_CONFIG = ''
TX_PREAMBLE = 0b111111000
TX_ZERO = 0b1110
TX_ONE = 0b0001
file_output = HEADER

# inp = input("Include standard frequencies? (Y/n)\n")
# inp = inp.lower().strip()[:1]
# if inp == 'y' or inp == '':
#     file_output += STANDARD_FREQ

# inp = input("Custom frequency? (in MHz)\n")
# if inp != '':
#     inp = int(float(inp) * float(1000000))
#     file_output += CUSTOM_FREQ + str(inp) + '\n'

# inp = input("Cusom Preset Name?\n")
# file_output += PRESET_NAME + re.sub(r" |\-", '_', inp.upper())[:8] + '\n'
# file_output += PRESET_MODULE


inp = input("Data rate (Baud) in Hertz?\n")
inp = int(inp)
if inp > 3910:
    for chanbw_e in range(0, 4): # 2 bits
        chanbw_m = round((CRYSTAL_FRQUENCY * 2**(-3-chanbw_e))/(inp*2) - 4)
        if chanbw_m < 4 and chanbw_m >= 0: # 2 bits
            break
    else:
        chanbw_m = 3
    # MINUMUM BANDWIDTH = 58 kHz
    for drate_e in range(0, 16): # 4 bits
        drate_m = round(((2 ** (21 - drate_e)) * inp / (CRYSTAL_FRQUENCY / 128)) - 256)
        if drate_m < 256 and drate_m >= 0:
            break
    dem_dcfilt_off = 1 if inp <= 250000 else 0
    mod_format = 3 #ASK/OOK
    manchester_en = 0

    print(
        "10 "
        + f"{int(bin(chanbw_e)[2:]+bin(chanbw_m)[2:],2):#0{3}x}"[2:].upper()
        + f"{drate_e:#0{3}x}"[2:].upper()
        + "\n11 "
        + f"{drate_m:#0{4}x}"[2:].upper()
    )
    

    print("Calculated Baud:", round(((256 + drate_m) * 2**drate_e) / (2**28) * CRYSTAL_FRQUENCY, 1))
    print("Calculated Bandwidth:", round((CRYSTAL_FRQUENCY)/(8*(4+chanbw_m)*2**chanbw_e), 1))
