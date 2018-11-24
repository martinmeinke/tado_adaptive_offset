## A script to adapt your tado devices temperature offsets according to the outside temperature

### Problem

Tado Smart Radiator Thermostats measure the Temerature close to the Radiator. The Tado app allows for setting a constant temperature offset per measurement device, which one might use to account for the difference between room temperature, and the temperature measured at the radiator. 

Still, a constant offset is not working pretty wall, as the offset usually varies with the outside temperature & temperature of the radiator.



### Solution

This script allows for adaptively setting the offset temperature for the Tado devices in your home.
Simply enter your Tado credentials, and adapt the `OFFSET_CONFIG` at the top of the script. You can find the device identifiers in the Tado app.






### Limitations

Although we can set floating point offsets using the Tado REST API, it seems like the floored values are actually used when controlling the room temperature.

(Eg. setting an offset of 0.7° and a target temperature of 23° results in a room temperature of 22.3°)



Thanks to http://blog.scphillips.com/posts/2017/01/the-tado-api-v2/