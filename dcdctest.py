#!/usr/bin/env python2

import serial
import serial.tools.list_ports
import time
from collections import OrderedDict
import pdu

ps = serial.Serial("/dev/ttyUSB1")
ld = serial.Serial("/dev/ttyUSB0")

onp = "outp on \r\n" #turn power supply on
onl = "inp on\r\n"

offp = "outp off\r\n"
offl = "inp off\r\n"

v56 = "VOLT:LEV 60\r\n" #set power supply to 48v
v48 = "VOLT:LEV 48\r\n" #set power supply to 48v
v24 = "VOLT:LEV 19\r\n" #set power supply to 48v
v19 = "VOLT:LEV 17\r\n" #set power supply to 48v

vol = "MEAS:VOLT:DC?\r\n" #command to read voltage of power supply
cur = "MEAS:CURR:DC?\r\n" #command to read current of power supply

c0 = "CURR:LEV 0.2\r\n"
c1 = "CURR:LEV 1\r\n"
c3 = "CURR:LEV 3\r\n"
c4 = "CURR:LEV 4\r\n"
c5 = "CURR:LEV 5\r\n"

pdu = pdu.pdi("http://172.23.5.188")

endsum = OrderedDict()

def identify_ports():
	ports = list(serial.tools.list_ports.comports(__device__))
	for p in ports:
		print(p)

def writeld(x):
	ld.write(x)
	rest()

def writeps(x):
	ps.write(x)
	rest()

def power_on():
	print("Now powering on\n")
	ld.write(c1)
	ld.write(onl)
	ps.write(onp)

def end():
	ld.write(c1)
	ps.write(offp)
	ld.write(offl)

def summary(x, y):
	endsum.update({x:y})

def bounds(x):
	num = abs(x - 12)
	if (num < 0.6):
             return("PASS")
	else:
            return("FAIL")

def rest():
	time.sleep(1)

def measure():
	output = ld.readline()
	return(float(output))


def full_test():
	end()
	rest()
	power_on()
	#identify_ports()
	#print("Current limit: ")
	#ld.write("CURR: LIM?\r\n")
	#out = measure()
	#print(out)
	time.sleep(3)
	print("a-input test")
	ab_input("a", 1)
	print("b-input test")
	ab_input("b", 2)
	print("c-input Test")
	test_c_input()
	test_auto_off()
	test_low_load()
	print("\n")
	print("Summary")
	for key in endsum:
		print(key + " " + endsum[key])

	pass_count()
	end()

def test_auto_off():
	test_name = ("17v 1A")
	print(test_name + " Automatic Power off Test")
	writeld(c1)
	writeps(v19)
	time.sleep(10)
	outc = c_current()
	print("Current: " + str(outc) + "A")
	writeld(vol)
	outv = measure()
	print(outv)
	def pass_criteria(x):
		if x > .002:
			return("FAIL")
		else:
			return("PASS")
	final = pass_criteria(outv)
	print(final)
	rest()
	summary("c " + test_name, final)

def test_low_load():
	test_name = ("48V 0.2A")
	print(test_name + " No Load Test")
	writeps(v48)
	writeld(c0)
	time.sleep(10)
	outc = c_current()
	print("Current: " + str(outc) + "A")
	writeld(vol)
	out = measure()
	print(out)
	def pass_criteria(x):
		if x > 13.9:
			return("FAIL")
		else:
			return("PASS")
	final = pass_criteria(out)
	print(final)
	summary("c " + test_name, final)


def test_c_input():
	power_on()
	summary("c-input","")
	print("Test 1.1: 60V")
	c_input(c1, v56, "1A", "60V")
	c_input(c3, v56, "3A", "60V")
	c_input(c5, v56, "5A", "60V")
	print("\n")
	print("Test 1.2: 48V")
	c_input(c1, v48, "1A", "48V")
	c_input(c3, v48, "3A", "48V")
	c_input(c5, v48, "5A", "48v")
	print("\n")
	print("Test 1.3: 20V")
	c_input(c1, v24, "1A", "19V")
	c_input(c3, v24, "3A", "19V")
	c_input(c4, v24, "4A", "19V")
	print("\n")

def c_input(commandld, commandps, valueld, valueps):
	print("Now testing " + valueps + " at " + valueld)
	writeld(commandld)
	writeps(commandps)
	outc = c_current()
	print("Current: " + str(outc) + "A")
	rating = out_results()
	summary("c " + valueps + " " + valueld, rating)

def ab_input(name, port):
    ps.write(offp)
    summary(name + "-input", "")
    pdu.setup()
    writeld(c1)
    pdu.on(port)
    print("Now testing 48V at 1A")
    time.sleep(3)
    rating = out_results()
    summary(name + " 48V 1A", rating)
    writeld(c3)
    print("Now testing 48V at 3A")
    out_results()
    summary(name + " 48V 3A", rating)
    writeld(c5)
    print("Now testing 48V at 5A")
    out_results()
    summary(name + " 48V 5A", rating)
    pdu.setup()
    print("\n")

def test_func(fake_int):
  print fake_int
  return fake_int + 3

def out_results():
	writeld(vol)
	outv = measure()
	rating = bounds(outv)
	result = (str(outv)+ "V " + rating)
	print(result)
	return(rating)

def c_current():
	writeps(cur)
	outc = ps.readline()
	return(float(outc))

def pass_count():
	countp = 0
	countf = 0
	for key in endsum:
		if (endsum[key] == ("PASS") or endsum[key] == ("")):
			countp = countp + 1
		else:
			countf = countf + 1
	print(str(countp) + " tests passed. " + str(countf) + " tests failed")

if __name__ == "__main__":
  try:
    full_test()
  except KeyboardInterrupt:
    print("\nScript stopped manually")
    end()
