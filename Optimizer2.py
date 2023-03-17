import math



print("Start")

hub = 16        #in mm
Last = 50       # in Newton

hebelfläche = 10 # in mm^2
beschleunigung = 30 # in m/s^2

dichte = 2.7 # in g/cm^3

startA = 50      #start Länge in mm
startB = 50
startx = 0

rangeA = 300    #max Länge in mm
rangeB = 300


stepAB = 1      #schrittweite
stepx = 5


#rangeC = 200

def yauxpal(A,B,x):     #berechnet y pos für A,B hebel und x Wagenabstand

    try:
        y = A*math.sin(math.acos(((B**2)-(A**2)-(x**2))/(-2*A*x)))
    except:
        y = -1
    return round(y,2)



def xforceauxpal (A,B,x):

    try:
        deg0 = (math.acos(((B**2)-(A**2)-(x**2))/(-2*A*x)))
        dega = math.degrees(math.radians(90-math.degrees(math.acos(((B**2)-(A**2)-(x**2))/(-2*A*x)))))
        degb = math.degrees(math.radians(90-math.degrees(math.acos(((A**2)-(B**2)-(x**2))/(-2*B*x)))))

        #fx = 2*Last*(math.sin(math.radians(degb)))/(math.sin(math.radians(180-dega-degb)))*math.cos(deg0)
        fs1 = Last*(math.sin(math.radians(degb)))/(math.sin(math.radians(180-dega-degb)))

        fs2 = math.sqrt(fs1**2-2*fs1*Last*math.cos(math.radians(dega))+Last**2)

        fx = fs1*math.cos(math.radians(90-dega))+fs2*math.cos(math.radians(90-degb))

    except:
        fx = -1


    return round(fx,2)



def Ddiff(A,B,x):

    dega = 0
    degb = 0
    try:
        #deg0 = (math.acos(((B**2)-(A**2)-(x**2))/(-2*A*x)))
        dega = math.degrees(math.acos(((B**2)-(A**2)-(x**2))/(-2*A*x)))
        degb = math.degrees(math.acos(((A**2)-(B**2)-(x**2))/(-2*B*x)))

        Ddist = abs(A*math.cos(math.radians(dega))-B*math.cos(math.radians(degb)))

    except:
        Ddist = -1

    return round(Ddist,2)



def komma(zahl):
    kommazahl = str(zahl).replace(".", ",");
    return kommazahl

def kkomma(zahl):
    kommazahl = str(zahl).replace(",", ".");
    return kommazahl







xvalforce = [[0 for i in range(rangeB+1)]for i in range(rangeA+1)]
yvalmax = [[0 for i in range(rangeB+1)]for i in range(rangeA+1)]
Dlager = [[0 for i in range(rangeB+1)]for i in range(rangeA+1)]
imax = [[0 for i in range(rangeB+1)]for i in range(rangeA+1)]


ymax = 0
ymin = 1000
Dlmax = 0
Dlmin = 1000

for A in range(startA, rangeA+1, stepAB):
    for B in range(startB, rangeB+1, stepAB):

        for x in range(startx, rangeA+rangeB+1, stepx):
            temp = yauxpal(A,B,x)

            if(temp > yvalmax[A][B]):
                yvalmax[A][B] = temp
                xvalmax = x

            if(temp > yvalmax[A][B] - hub): #If last xhub
                xvalhub = x
            else:
                break

        for x in range((xvalmax-stepx),(xvalmax+stepx),1):
            if(x<0):
                x = 0
            temp = yauxpal(A,B,x)

            if(temp > yvalmax[A][B]):
                yvalmax[A][B] = temp

        for x in range((xvalhub-stepx),(xvalhub+stepx),1):
            if(x<0):
                x = 0
            temp = yauxpal(A,B,x)

            if(temp > yvalmax[A][B] - hub): #If last xhub
                xvalhub = x
                Dlager[A][B] = Ddiff(A,B,x)
                imax[A][B] = round(temp - yauxpal(A,B,x+1),2)
                xvalforce[A][B] = xforceauxpal(A,B,x)

        if(yvalmax[A][B] > ymax):
            ymax = yvalmax[A][B]
        if(yvalmax[A][B] < ymin):
            ymin = yvalmax[A][B]
        if(Dlager[A][B] > Dlmax):
            Dlmax = Dlager[A][B]
        if(Dlager[A][B] < Dlmin):
            Dlmin = Dlager[A][B]



dyforce = [["" for i in range(int(Dlmax)+1)]for i in range(int(ymax)+1)]


for A in range(startA, rangeA+1, stepAB):
    for B in range(startB, rangeB+1, stepAB):

        print("A,B: " + str(A) + " " + str(B) +"\tFhub: " + str(xvalforce[A][B]) + "\tymax: " + str(yvalmax[A][B]) + "\tDlager: " + str(Dlager[A][B]) + "\timax: " + str(imax[A][B]) + "\tymax: " + str(ymax) + "\tDlmax: " + str(Dlmax))

        if(dyforce[int(yvalmax[A][B])][int(Dlager[A][B])] != ""):
            if(float(kkomma(dyforce[int(yvalmax[A][B])][int(Dlager[A][B])])) < ((xvalforce[A][B] + hebelfläche*0.1*dichte*A*0.001*beschleunigung + hebelfläche*0.1*dichte*B*0.001*beschleunigung))):
                dyforce[int(yvalmax[A][B])][int(Dlager[A][B])] = komma((xvalforce[A][B] + hebelfläche*0.1*dichte*A*0.001*beschleunigung + hebelfläche*0.1*dichte*B*0.001*beschleunigung))
        else:
            dyforce[int(yvalmax[A][B])][int(Dlager[A][B])] = komma((xvalforce[A][B] + hebelfläche*0.1*dichte*A*0.001*beschleunigung + hebelfläche*0.1*dichte*B*0.001*beschleunigung))

outputf = open("output.csv", "w")

for y in range(int(ymin),int(ymax)+1,stepAB):
    outputf.write(";{}".format(y))

outputf.write("\n")

for d in range(int(Dlmin),int(Dlmax)+1,1):

    outputf.write("{}".format(d))

    for y in range(int(ymin),int(ymax)+1,stepAB):

        outputf.write(";{}".format(dyforce[y][d]))

    outputf.write("\n")























