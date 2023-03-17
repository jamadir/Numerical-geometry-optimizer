import math




print("Start")

hub = 16        #in mm
Last = 50       # in Newton

rangeA = 500    #max Länge in mm
rangeB = 500



startA = 5      #start Länge in mm
startB = 5

stepAB = 5      #schrittweite
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

        fx = 2*Last*(math.sin(math.radians(degb)))/(math.sin(math.radians(180-dega-degb)))*math.cos(deg0)
    except:
        fx = -1
    return round(fx,2)

def komma(zahl):
    kommazahl = str(zahl).replace(".", ",");
    return kommazahl



A = startA
B = startB
#C = 500
x = 1

yval = [[[0 for i in range(rangeB+rangeA+1)]for i in range(rangeB+1)]for i in range(rangeA+1)]

yvalmax = [[0 for i in range(rangeB+1)]for i in range(rangeA+1)]
xvalmax = [[0 for i in range(rangeB+1)]for i in range(rangeA+1)]
xvalhub = [[0 for i in range(rangeB+1)]for i in range(rangeA+1)]
xvalforce = [[0 for i in range(rangeB+1)]for i in range(rangeA+1)]

forceminval = 10000
Avalforcemin = [0 for i in range(2)]


imaxt = 0
imax = [[0 for i in range(rangeB+1)]for i in range(rangeA+1)]

outputf = open("output.csv", "w")
outputf.write("A;B;Fmin;imax\n")

while(A <= rangeA):
    while(B <= rangeB):
        while(x <= B+A):
            #Go through X
            temp = yauxpal(A,B,x)
            yval[A][B][x] = temp
            if(temp > yvalmax[A][B]): #If new max
                yvalmax[A][B] = temp
                xvalmax[A][B] = x

            if(temp > yvalmax[A][B] - hub): #If last xhub
                xvalhub[A][B] = x

            #print(" A:", A, " B:", B, " x:", x," y:", yval[A][B][x])
            if(x == 1):
                x = 0
            x = x+stepx


        x = xvalmax[A][B]-stepAB #xmax precise
        if(x < 0 or x > rangeA+rangeB-4):
            x = 0
        while(x <= xvalmax[A][B]+stepAB):
            temp = yauxpal(A,B,x)
            yval[A][B][x] = temp
            if(temp > yvalmax[A][B]):
                yvalmax[A][B] = temp
                xvalmax[A][B] = x
            #print("closem:", x, "\ttemp:", temp)
            x = x + 1


        x = xvalhub[A][B]-stepAB #xhub precise
        if(x < 0 or x > rangeA+rangeB-4):
            x = 0
        while(x <= xvalhub[A][B]+stepAB):
            temp = yauxpal(A,B,x)
            yval[A][B][x] = temp
            if(temp < yvalmax[A][B]-hub):
                xvalhub[A][B] = x
                xvalforce[A][B] = xforceauxpal(A,B,x)
                break
            if(temp<=0):
                xvalhub[A][B] = -1
                break
            #print("closeh:", x, "\ttemp:", temp)
            x = x + 1


        x = xvalmax[A][B]
        imaxt = yauxpal(A,B,x)
        while(x <= xvalhub[A][B]):
            temp = yauxpal(A,B,x)

            if(imax[A][B] < abs(imaxt-temp)):
                imax[A][B] = round(abs(imaxt-temp),2)

            imaxt = temp
            x = x + 1

        imaxt = 0

        if(xvalforce[A][B] < forceminval and xvalforce[A][B] > 0):
            forceminval = xvalforce[A][B]
            Avalforcemin[0] = A
            Avalforcemin[1] = B


        print(" A:", A, "\tB:", B,"\t\txmax:", xvalmax[A][B], "\txhub:", xvalhub[A][B], "\txforce", xvalforce[A][B], "\tymax:", yvalmax[A][B], "\timax:", imax[A][B])
        x = 1
        B = B+stepAB

    if(forceminval == 10000):
        forceminval = -1
    print("forcemin: " + str(komma(forceminval)) + "\t Lengths: " + str(Avalforcemin[0]) + "\t" + str(Avalforcemin[1]) + "\timax:" + str(imax[Avalforcemin[0]][Avalforcemin[1]]) )
    outputf.write("{};{};{};{}\n".format(str(Avalforcemin[0]), str(Avalforcemin[1]), str(komma(forceminval)), str(komma(imax[Avalforcemin[0]][Avalforcemin[1]]))))
    B = startB
    A = A + stepAB
    forceminval = 10000





