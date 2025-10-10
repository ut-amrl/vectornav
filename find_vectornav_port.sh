#!/bin/bash

echo "=== Finding VectorNav Device ==="
echo

echo "1. List all USB serial devices:"
ls -la /dev/ttyUSB* 2>/dev/null || echo "No ttyUSB devices found"
echo

echo "2. Show USB device tree with vendor/product IDs:"
lsusb | grep -E "(FTDI|0403:6001)" || echo "No FTDI devices found"
echo

echo "3. Check which ttyUSB devices respond to VectorNav commands:"
for port in /dev/ttyUSB*; do
    if [ -c "$port" ]; then
        echo "Testing $port..."
        timeout 3 python3 -c "
import serial
import time
try:
    s = serial.Serial('$port', 115200, timeout=1)
    time.sleep(0.1)
    s.write(b'\$VNRRG,01*XX\r\n')  # VectorNav model info command
    time.sleep(0.5)
    response = s.read_all()
    s.close()
    if b'VN-' in response:
        print('  ✓ VectorNav device found!')
    elif response and len(response) > 5:
        print('  ✗ Other device (not VectorNav)')
        print('  Response: Binary data (%d bytes)' % len(response))
    else:
        print('  ✗ No response')
except Exception as e:
    print('  ✗ Error:', e)
" 2>/dev/null
        echo
    fi
done

echo "4. Check dmesg for recent USB serial device connections:"
echo "Recent FTDI/ttyUSB connections:"
dmesg 2>/dev/null | grep -E "(ttyUSB|FTDI|ftdi_sio)" | tail -5 || echo "Cannot read dmesg (need sudo)"
echo

echo "5. Show device attributes for FTDI devices:"
for port in /dev/ttyUSB*; do
    if [ -c "$port" ]; then
        echo "Device: $port"
        udevadm info --name="$port" --attribute-walk 2>/dev/null | grep -E "(ATTRS{idVendor}|ATTRS{idProduct}|ATTRS{product})" | head -3
        echo
    fi
done
