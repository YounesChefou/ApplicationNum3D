import streamlit as st
import serial
import time
"""
# GRBL 2 axis probe test
"""
#----------------------------------------
# Initialize serial port
#----------------------------------------
def open_com(p):
    try:
        ser_port = serial.Serial(port=p, timeout=0.5, baudrate=115200)
    except serial.SerialException:
        ser_port = None
    return ser_port
#----------------------------------------
# Send only one G code to the xy table
#----------------------------------------
def send_g(line, ser_port):
    if not(ser_port) : return("Serial not opened !")
    ser_port.reset_input_buffer()
    ser_port.write((line + "\n").encode())
    resp = ""
    while True:
        l = ser_port.readline().decode()
        if l=="": break
        resp = resp + l
    return resp
#----------------------------------------
# Send only one G code to the xy table
#----------------------------------------
def show_status(ser_port):
    if not(ser_port) : return("Serial not opened !")
    ser_port.reset_input_buffer()
    ser_port.write((line + "\n").encode())
    resp = ""
    while True:
        l = ser_port.readline().decode()
        if l=="": break
        resp = resp + l
    return resp
#========================================
grbl_serial = open_com("/dev/ttyUSB0") # For Raspberry Pi zero X OR /dev/ttyAMA0, "COMxx" on Windows PC
if st.sidebar.button("Display config"):
    """
    ## $I - View build info
    """
    ret = send_g("$I", grbl_serial)
    st.text(ret)
    """
    ## $$ - View and write Grbl settings
    """
    ret = send_g("$$", grbl_serial)
    st.text(ret)
    """
    ## $# - View gcode parameters
    """
    ret = send_g("$#", grbl_serial)
    st.text(ret)
µsteps = 16
step_x_0  = round(400*µsteps/360, 3)
speed_x_0 = round(100000, 3)
accel_x_0 = round(100000, 3)
step_y_0  = round(10*20*µsteps/30, 3)
speed_y_0 = round(2000, 3)
accel_y_0 = round(200, 3)
if st.sidebar.button("Reset EEPROM"):
    """
    ## 0x18 (ctrl-x) : Soft-Reset
    """
    ret = send_g("\0x18", grbl_serial)
    st.text(ret)
    """
    ## Reset EEPROM Configuration
    """
    "$RST=$ 	Erases and restores the $$ Grbl settings back to defaults"
    st.text(send_g("$RST=$", grbl_serial))
    "$H - Run homing cycle"
    st.text(send_g("$H", grbl_serial))
    "$X - Kill alarm lock"
    st.text(send_g("$X", grbl_serial))
    "$32=1 	Laser mode, boolean"
    st.text(send_g("$32=1", grbl_serial))
    "$100=17.778 	X steps/° 0.9/16=17.778"
    st.text(send_g("$100="+str(step_x_0), grbl_serial))
    "$101=17.778 	X steps/° 0.9/16=17.778"
    st.text(send_g("$101="+str(step_y_0), grbl_serial))
    "$110=100000 	X Max rate, °/min, 555 RPM"
    st.text(send_g("$110="+str(speed_x_0), grbl_serial))
    "$111=100000 	Y Max rate, °/min, 555 RPM"
    st.text(send_g("$111="+str(speed_y_0), grbl_serial))
    "$120=100000 	X Acceleration, °/sec²"
    st.text(send_g("$120="+str(accel_x_0), grbl_serial))
    "$121=100000 	Y Acceleration, °/sec²"
    st.text(send_g("$121="+str(accel_y_0), grbl_serial))
    "$130=400 	X Max travel, °"
    st.text(send_g("$130=400", grbl_serial))
    "$131=400 	Y Max travel, °"
    st.text(send_g("$131=100", grbl_serial))

speed_x    = st.sidebar.slider("Speed X (°/min):", 10000, 300000, speed_x_0, 10000)
accel_x    = st.sidebar.slider("Accel X (°/s²):",  10000, 300000, accel_x_0, 10000)
speed_y    = st.sidebar.slider("Speed Y (mm/min):",  100,  10000, speed_y_0,   100)
accel_y    = st.sidebar.slider("Accel Y (mm/s²):",    10,   2000, accel_y_0,    10)

if st.sidebar.button("Update Speed/Accel"):
    """
    ## Set Speed/Accel. config
    """
    "$110="+str(speed_x)+" 	X Max rate, °/min"
    st.text(send_g("$110="+str(speed_x), grbl_serial))
    "$111="+str(speed_y)+" 	Y Max rate, mm/min"
    st.text(send_g("$111="+str(speed_y), grbl_serial))
    "$120="+str(accel_x)+" 	X Acceleration, °/sec²"
    st.text(send_g("$120="+str(accel_x), grbl_serial))
    "$121="+str(accel_y)+" 	Y Acceleration, mm/sec²"
    st.text(send_g("$121="+str(accel_y), grbl_serial))
motion_allowed = st.sidebar.checkbox("Motion allowed", False)
if st.sidebar.button("Depth homing"):
    """
    ## Depth homing
    """
    st.text(send_g("G0Y-10", grbl_serial))
depth    = st.sidebar.slider("Depth (mm):",0, 50, 1, 5)
if motion_allowed:
    """
    ## Head depth
    """
    sequence = "G1Y"+str(depth)+"F10000"
    sequence
    st.text(send_g(sequence, grbl_serial))
center    = st.sidebar.slider("Center (°):",0, 360, 180, 10)
range     = st.sidebar.slider("Range (°):", 0, 180, 60, 10)
nb_cycles = st.sidebar.slider("Cycles :",  0, 15,5, 1)
if motion_allowed:
    """
    ## Oscillating motion
    """
    send_g("G0X0", grbl_serial)
    if nb_cycles > 0:
        send_g("G1X"+str(center)+"F500000", grbl_serial)
        sequence = ("G1X"+str(int(center-range/2))+"\nG1X"+str(int(center+range/2))+"\n")*nb_cycles
        sequence
        send_g(sequence, grbl_serial)
        st.text(send_g("G0X0", grbl_serial))
st.sidebar.button("Again")
