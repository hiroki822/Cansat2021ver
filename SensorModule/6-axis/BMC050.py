from smbus import SMBus
import time

ACC_ADDRESS = 0x19
ACC_REGISTER_ADDRESS = 0x02
MAG_ADDRESS = 0x13
MAG_REGISTER_ADDRESS = 0x42

i2c = SMBus(1)


def bmc050_setup():
    # --- BMC050Setup --- #
    # Initialize ACC
    try:
        i2c.write_byte_data(ACC_ADDRESS, 0x0F, 0x03)
        time.sleep(0.1)
        i2c.write_byte_data(ACC_ADDRESS, 0x10, 0x0F)
        time.sleep(0.1)
        i2c.write_byte_data(ACC_ADDRESS, 0x11, 0x00)
        time.sleep(0.1)
    except:
        time.sleep(0.1)
        print("BMX055 Setup Error")
        i2c.write_byte_data(ACC_ADDRESS, 0x0F, 0x03)
        time.sleep(0.1)
        i2c.write_byte_data(ACC_ADDRESS, 0x10, 0x0F)
        time.sleep(0.1)
        i2c.write_byte_data(ACC_ADDRESS, 0x11, 0x00)
        time.sleep(0.1)

    # Initialize MAG
    try:
        data = i2c.read_byte_data(MAG_ADDRESS, 0x4B)
        if(data == 0):
            i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x83)
            time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x01)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4C, 0x38)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4E, 0x84)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x51, 0x04)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x52, 0x0F)
        time.sleep(0.1)
    except:
        time.sleep(0.1)
        print("BMC050 Setup Error")
        data = i2c.read_byte_data(MAG_ADDRESS, 0x4B)
        if(data == 0):
            i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x83)
            time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4B, 0x01)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4C, 0x38)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x4E, 0x84)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x51, 0x04)
        time.sleep(0.1)
        i2c.write_byte_data(MAG_ADDRESS, 0x52, 0x0F)
        time.sleep(0.1)


def acc_dataRead():
    # --- Read Acc Data --- #
    accData = [0, 0, 0, 0, 0, 0]
    value = [0.0, 0.0, 0.0]
    for i in range(6):
        try:
            accData[i] = i2c.read_byte_data(
                ACC_ADDRESS, ACC_REGISTER_ADDRESS+i)
        except:
            pass
            # print("error")

    for i in range(3):
        value[i] = (accData[2*i+1] * 16) + (int(accData[2*i] & 0xF0) / 16)
        value[i] = value[i] if value[i] < 2048 else value[i] - 4096
        value[i] = value[i] * 0.0098 * 1

    return value


def mag_dataRead():
    # --- Read Mag Data --- #
    magData = [0, 0, 0, 0, 0, 0, 0, 0]
    value = [0.0, 0.0, 0.0]
    for i in range(8):
        try:
            magData[i] = i2c.read_byte_data(
                MAG_ADDRESS, MAG_REGISTER_ADDRESS + i)
        except:
            pass
            # print("error")

    for i in range(3):
        if i != 2:
            value[i] = ((magData[2*i+1] * 256) + (magData[2*i] & 0xF8)) / 8
            if value[i] > 4095:
                value[i] = value[i] - 8192
        else:
            value[i] = ((magData[2*i+1] * 256) | (magData[2*i] & 0xF8)) / 2
            if value[i] > 16383:
                value[i] = value[i] - 32768

    return value


def bmc050_read():
    # --- Read BMC050 Data --- #
    accx, accy, accz = acc_dataRead()
    magx, magy, magz = mag_dataRead()

    value = [accx, accy, accz, magx, magy, magz]

    # --- Round Data --- #
    for i in range(len(value)):
        if value[i] is not None:
            value[i] = round(value[i], 4)

    return value


if __name__ == '__main__':
    try:
        bmc050_setup()
        time.sleep(0.2)
        while 1:
            bmxData = bmc050_read()
            print(bmxData)
            time.sleep(1)

    except KeyboardInterrupt:
        print()
    except Exception as e:
        print()
        print(e.message)
