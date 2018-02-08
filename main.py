import pyb
import micropython
import utime
import time
import controller_Ng_Kropp_Fitter as controller
import encoder_Ng_Kropp_Fitter as encode
import motor_Ng_Kropp_Fitter as driver

def do_it(location, end):
    enc.zero()
    ctr.set_setpoint(location)
    for i in range(0,end):
        ctr.err_calc(enc.read())
        actuation = ctr.do_work()
        drv.set_duty_cycle(actuation)
        utime.sleep_ms(10)

drv = driver.MotorDriver()
enc = encode.MotorEncoder()
ctr = controller.MotorController(.04, 7000)   ##Initializes controller with gain=1 and location = 50
while input() is not 'q':
    do_it(2750, 50)

fh = open("eric.csv", "w")
for x in ctr.return_data():
    fh.write(str(x))
fh.close()

