import array
import utime
import display
import leds
import color
import light_sensor
import os
import gpio
import ujson



FILENAME_CODES = "/apps/card10_tvbgone/codes.txt"

# we'll fake PWM, it's very naive

pwm_count = 0
pwm_period = 1000000/38000
pwm_on_time = 0
pwm_correction = 0

def pwm_pulse_send(pulses):
    on = True
    for p in pulses:
        if on:
            #disp.print("p1 %d" % p, posx=0, posy=30).update()
            #leds.set(9, [0,255,0])
            pwm_on_time = 0
			# we actually sleep twice
            period = int(pwm_period / 2);
            #if period > pwm_correction:
            #    period -= pwm_correction
            while pwm_on_time < p:
                #pwm_count += 1
                #disp.print("t %d" % pwm_on_time, posx=40, posy=30).update()
                #leds.set(10, [0,0,255])
                gpio.write(gpio.IR_LED, True)
                #leds.set(10, [0,255,255])
                #disp.print("t %d" % pwm_on_time, posx=40, posy=30).update()
                utime.sleep_us(period)
                #leds.set(10, [255,255,255])
                pwm_on_time += period

                #leds.set(10, [0,0,0])
                gpio.write(gpio.IR_LED, False)
                utime.sleep_us(period)
                pwm_on_time += period
            on = False
        else:
            #disp.print("p0 %d" % p, posx=0, posy=30).update()
            #leds.set(9, [0,0,0])
            gpio.write(gpio.IR_LED, False)
            utime.sleep_us(p)
            on = True
    gpio.write(gpio.IR_LED, False)
    #leds.set(9, [0,0,0])

c = 0
leds.clear()
utime.sleep(1)
with display.open() as disp:
    disp.clear().update()

#    if FILENAME_CODES in os.listdir("."):
    f = open(FILENAME_CODES, "r")
    try:
        # just in case
        #disp.print("STOP LS").update()
        light_sensor.stop()
        #disp.print("GPIO").update()
        gpio.set_mode(gpio.IR_LED, gpio.mode.OUTPUT)
        #disp.print("GPIO DONE").update()
        # Testing, 1, 2
        #gpio.write(gpio.IR_LED, True)
        #while True:
        #    gpio.write(gpio.IR_LED, True)
        #    gpio.write(gpio.IR_LED, False)
        #    c += 1

#        disp.print(" %d" % pwm_count, posx=0, posy=10).update()
#        pwm_pulse_send(array.array('H', [10000,10000]))
#        disp.print(" %d" % pwm_on_time, posx=0, posy=10).update()
#        while True:
#            c += 1

        for line in f:
            #disp.print(line).update()
            disp.print("l %d" % c).update()
            code = ujson.loads(line)
            #disp.print("%f" % code['delay']).update()
            #disp.print(str(code['freq'])).update()
            #disp.print(code).update()
            for pwm_correction in [0]:
                leds.set(8, [255,0,0])
                pwm_period = 1000000 / code['freq']
                disp.print("%f" % pwm_period, posx=0, posy=60).update()
    #            while True:
    #                c += 1
                # If this is a repeating code, extract details
                try:
                    repeat = code['repeat']
                    delay = code['repeat_delay']
                except KeyError:  # by default, repeat once only!
                    repeat = 1
                    delay = 0
                # The table holds the on/off pairs
                table = code['table']
                pulses = []  # store the pulses here
                # Read through each indexed element
                #disp.print("codes").update()
                for i in code['index']:
                    pulses += table[i]  # and add to the list of pulses
                pulses.pop()  # remove one final 'low' pulse

                for i in range(repeat):
                    #disp.print("%d" % i).update()
                    a = array.array('H', pulses)
                    #disp.print("a", posx=0, posy=30).update()
                    pwm_pulse_send(a)
                    #disp.print("z", posx=0, posy=30).update()
                    utime.sleep_ms(int(delay*1000))
                leds.clear()
                utime.sleep_ms(int(code['delay']*1000))

            c += 1
            #break

        disp.print("Thanks     Mitch!").update()

    except ValueError:
        disp.print("invalid codes.txt").update()
#    else:
#        disp.print("codes.txt not found").update()

    disp.close()

