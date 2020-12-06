GlowScript 2.9 VPython
#Eric Zhou
#3/9/20

#Graphs
Pos_Graph = graph(width = 800, height = 200, title = "Position", xtitle = "time (s)", ytitle = "height (m)")
pCurve = gcurve(color = color.blue, label = "x")

Vel_Graph = graph(width = 800, height = 200, title= "Velocity", xtitle = "time (s)", ytitle = "velocity (m/s)")
vCurve = gcurve(color= color.red, label = "v")

Acc_Graph = graph(width = 800, height = 200, title= "Acceleration", xtitle = "time (s)", ytitle = "acceleration (m/s/s)")
aCurve = gcurve(color= color.purple, label = "a")

Force_Graph = graph(width = 800, height = 200, title= "Force", xtitle = "time (s)", ytitle = "Newtons (n)")
fCurve = gcurve(color= color.orange, label = "f")

#Variables
rMass = 13000 #kg
rocketLength = 14 #m
fuelR = -130 #kg/s
burnTime = 65 #s
Cd = 0.245
Uex = 1880 #m/s
p = 1.225 #0°C, kg/m^3
A = pi * (1.651/2)**2
G = 6.67e-11 #Nm^2/kg^2
Me = 5.972e24 #kg
earthRadius = 6378100 #m, Source: https://en.wikipedia.org/wiki/Earth_radius

#Constant Force
Fthrust = -Uex * fuelR

#Initialization
t = 0
dt = 0.1
v = 0
h = 0
vMax = 0
peak = False #testing whether or not rocket has reached its highest height

#Toggles
AirDensity = True
varying_AirDensity = True
varying_Gravity = True

#Helper Method
def airDensity(h): 
    p0 = 1.2203
    a1 = -1.130781e-4
    a2 = 3.56536e-9
    a3 = -3.74861e-14
    return p0 + (a1 * h) + (a2 * h**2) + (a3 * h**3)

#Calculations
while (h >= 0):
    d = earthRadius + h + (rocketLength/2) #Distance between the Earth and the rocket's centers, h must be updated every dt
    
    #Force of Gravity
    if (varying_Gravity):
        Fg = G * Me * rMass / d**2
    else:
        Fg = rMass * 9.8 #rMass is updated every dt
    
    #Force of Rocket Thrust while engine is still burning
    if (t <= burnTime):
        F = Fthrust - Fg
    else:
        F = -Fg
    
    #Accounting for force of air resistance under different circumstances
    if (AirDensity):
        if (varying_AirDensity and h < 40000):
            Fd = 0.5 * Cd * A * airDensity(h) * v**2
        else if (not varying_AirDensity):
            Fd = 0.5 * Cd * A * p * v**2
            
        #Making sure drag force is always opposing velocity   
        if (v > 0):
            F += -Fd
        else:
            F += Fd 
    else:
        Fd = 0
    
    #Decreasing mass if engine is still burning
    if (t <= burnTime):
        rMass += (fuelR * dt)
    
    #Updating variables
    a = F / rMass
    v += a * dt
    h += v * dt
    
    #Plotting data
    pCurve.plot(t,h)
    vCurve.plot(t,v)
    aCurve.plot(t,a)
    fCurve.plot(t,F)
    
    #Finding max velocity
    if (abs(v) > vMax):
        vMax = abs(v)
    #When v is 0, pos-time graph must be a absolute maximum value, changing velocity/slope from (+) -> (-)
    if (t > 0 and int(v) == 0 and not peak):
        print("Max Height: {0:.2f}".format(h) + " m")
        peak = True
        
    t += dt

print("Max Velocity: {0:.2f}".format(vMax) + " m/s")
print("Flight Time: {0:.2f}".format(t) + " s")
