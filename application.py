import streamlit as st
import serial
import time
"""
# Application de numérisation d'objet en 3D
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


USB0 = st.sidebar.checkbox("ttyUSBO");
USB1 = st.sidebar.checkbox("ttyUSB1");

if USB0:
    grbl_serial = open_com("/dev/ttyUSB0");
elif USB1:
    grbl_serial = open_com("/dev/ttyUSB1");

if st.button("Lancer les moteurs")


if st.button("")
