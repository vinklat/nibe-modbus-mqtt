# nibe-modbus-mqtt

- MQTT bridge for a **Nibe heat pump** connected to the **Modbus**
- under development  

## done
- read metrics using READ_HOLDING_REGISTERS (0x03) modbus function
- Modbus 40 interface device + [arduino-modbus-rtu-tcp-gateway](https://github.com/budulinek/arduino-modbus-rtu-tcp-gateway) arduino device
- tested Nibe VVM 310 indoor unit + F3040 outdoor device

## todo
- Modbus registers config file
- write / change heat pump settings via WRITE_SINGLE_REGISTER (0x10)