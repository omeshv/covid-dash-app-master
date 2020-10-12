import numpy as np
import math


# This file contains function, `

# ##########################################################
# Function: getSpecDef
# Input: reportCount (INT), value from 1 to 12 currently
# Output: maxRows(int), maxCols (int) and specDef Array of Dataframe
# About: This function returns number of rows, columns required and the specification definition for
#        Graph subplots
# Author: Omesh Vashisth (eomevas)
# ############################################################
def getSpecDef(reportCount):
    maxRows = 4
    maxCols = 3
    specDef = None
    if reportCount == 1:
        maxRows = 2
        maxCols = 2
        specDef = [[{"rowspan": 2, "colspan": 2}, None],
                   [None, None]]
    elif reportCount == 2:
        maxRows = 1
        maxCols = 2
        specDef = [[{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}]]
    elif reportCount == 3:
        maxRows = 1
        maxCols = 3
        specDef = [[{}, {}, {}]]
    elif reportCount == 4:
        maxRows = 2
        maxCols = 2
        specDef = [[{}, {}],
                   [{}, {}]
                   ]
    elif reportCount == 5:
        maxRows = 2
        maxCols = 3
        specDef = [[{}, {}, {}],
                   [{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 2}, None]
                   ]
    elif reportCount == 6:
        maxRows = 2
        maxCols = 3
        specDef = [[{}, {}, {}],
                   [{}, {}, {}]
                   ]
    elif reportCount == 7:
        maxRows = 3
        maxCols = 3
        specDef = [[{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [{"rowspan": 2, "colspan": 1}, {"rowspan": 2, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [None, None, {"rowspan": 1, "colspan": 1}],
                   ]
    elif reportCount == 8:
        maxRows = 3
        maxCols = 3
        specDef = [[{"rowspan": 2, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [None, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   ]
    elif reportCount == 9:
        maxRows = 3
        maxCols = 3
        specDef = [[{}, {}, {}],
                   [{}, {}, {}],
                   [{}, {}, {}]
                   ]
    elif reportCount == 10:
        maxRows = 4
        maxCols = 3
        specDef = [[{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [{"rowspan": 2, "colspan": 1}, {"rowspan": 2, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [None, None, {"rowspan": 1, "colspan": 1}],
                   ]
    elif reportCount == 11:
        maxRows = 4
        maxCols = 3
        specDef = [[{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [{"rowspan": 2, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [None, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   ]
    elif reportCount == 12:
        maxRows = 4
        maxCols = 3
        specDef = [[{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}],
                   [{"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}, {"rowspan": 1, "colspan": 1}]
                   ]

    return maxRows, maxCols, specDef;


# END OF Function getSpecDef

# ##########################################################
# Function: getGraphDomain
# Input: graphType (String).
# Output: domain
# About: Returns domain name based on graphtype. Default to xy
# Author: Omesh Vashisth (eomevas)
# ############################################################
def getGraphDomain(graphType):
    domainType = 'xy'
    if graphType == 'Bar' or graphType == 'Line':
        domainType = 'xy'
    elif graphType == 'BarPolar':
        domainType = "polar"
    elif graphType == 'Pie' or graphType == 'Donut':
        domainType = "domain"
    elif graphType == 'Scatter3d':
        domainType = "scene"
    elif graphType == 'BarDual':
        domainType = "xy"
    elif graphType == 'LineDual':
        domainType = "xy"

    return domainType;


# ##########################################################
# Function: getGraphDomain_Axis
# Input: graphType (String).
# Output: domain
# About: Returns domain name based on graphtype. Default to xy
# Author: Omesh Vashisth (eomevas)
# ############################################################
def getGraphDomain_Axis(graphType):
    domainType = 'xy'
    secondryAxis = False
    if graphType == 'Bar' or graphType == 'Line':
        domainType = 'xy'
        secondryAxis = True
    elif graphType == 'BarPolar':
        domainType = "polar"
    elif graphType == 'Pie' or graphType == 'Donut':
        domainType = "domain"
    elif graphType == 'Scatter3d':
        domainType = "scene"
    elif graphType == 'BarDual':
        domainType = "xy"
        secondryAxis = True
    elif graphType == 'LineDual':
        domainType = "xy"
        secondryAxis = True

    return domainType, secondryAxis;


# End of function getGraphDomain()


# ##########################################################
# Function:  getRowAndColPos
# Input: currentSeq (INT),reportCount (INT)
# Output: rowPos(int), colPos(int)
# About: Returns row and column position based on identified location from total count of reports
#        Incase, Row and columns not found, returns -1,-1 (error position)
# Author: Omesh Vashisth (eomevas)
# ############################################################
def getRowAndColPos(currentSeq, reportCount):
    maxRow, maxCol, specDef = getSpecDef(reportCount)
    counter = 0
    for r in range(maxRow):
        for c in range(maxCol):
            if specDef[r][c] != None:
                counter = counter + 1
            if counter == currentSeq:
                return r + 1, c + 1
    return -1, -1


# end fuction getRowAndColPos()


# ##########################################################
# Function:  formatNumbers
# Input: number (INT),format(string).
#           value can be nD, where n is number and D is decimal,
#           nS defining max chars n and string. Autoconverts to K/M/B etc once n is breached
# Output: formattedNumber
# About: Returns fomatted number based on format selected
# Author: Omesh Vashisth (eomevas)
# ############################################################
def formatNumbers(num, formatStr):
    if 'D' in formatStr:
        prc = int(formatStr.replace('D', ''))
        return '{:.{prec}f}'.format(num, prec=prc)
    elif 'S' in formatStr:
        prc = int(formatStr.replace('S', ''))
        return '%{:.{prec}s}'.format(num, prec=prc)


# end fuction  formatNumbers()

# ##########################################################
# Function:  barColorWithCondition
# Input: dataFrame,conditionText
#           eg. Cyan, red>4000
# Output: colorArray
# About: Returns colorArray to be used for coloring the graph
# Author: Omesh Vashisth (eomevas)
# ############################################################
def barColorWithCondition(df, conditionText):
    delim = ''
    valArr = df['Value'].to_numpy()
    # print('Type of ValArr is:', type(valArr))
    # print('aRRAY is:', valArr)
    if "," in conditionText:
        baseCol = conditionText.split(",")
        baseCol[0] = baseCol[0].strip()
        color = np.array(baseCol[0] * np.array(df['Value']).shape[0])

        # now process red>4000
        arrComparitors = ['>=', '=>', '<=', '=<', '<', '>', '==', '=', '<', '>']
        for comparator in arrComparitors:
            if comparator in baseCol[1]:
                delim = comparator
        if delim != '':
            tArr = baseCol[1].split(delim)
            conditionalColor = tArr[0].strip()
            conditionalVal = float(tArr[1].strip())
            # print('Delim->', delim, ' Condition Color', conditionalColor, ' Conditional Value->', conditionalVal)
            if delim == '>=' or delim == '=>':
                color = np.where(valArr >= conditionalVal, conditionalColor, baseCol[0])
            elif delim == '<=' or delim == '=<':
                color = np.where(valArr <= conditionalVal, conditionalColor, baseCol[0])
            elif delim == '==' or delim == '=':
                color = np.where(valArr == conditionalVal, conditionalColor, baseCol[0])
            elif delim == '<':
                color = np.where(valArr < conditionalVal, conditionalColor, baseCol[0])
            elif delim == '>':
                color = np.where(valArr > conditionalVal, conditionalColor, baseCol[0])
                # color[valArr > conditionalVal] = conditionalColor
    else:
        color = np.array(conditionText.strip() * np.array(df['Value']).shape[0])
    return color


# end function barColorWithCondition

# ##########################################################
# Function:  barColorWithCondition
# Input: dataFrame,conditionText
#           eg. Cyan, red>4000
# Output: colorArray
# About: Returns colorArray to be used for coloring the graph
# Author: Omesh Vashisth (eomevas)
# ############################################################
def getTextFormat(inputFormat, df):
    divDict = {'': 1, 'K': 1000, 'M': 1000000, 'B': 1000000000, 'T': 1000000000000}
    df['Value'] = df['Value'].astype(float)
    if len(inputFormat) > 0:
            inputFormat = str(inputFormat)
    else:
        inputFormat = ''
    decType = 0
    formatType = ''
    for key in divDict.keys():
        if key in inputFormat and key != '':
            formatType = key
            #print('Key Found',key)
            break

    if '.1' in inputFormat:
        decType = 1
    elif '.2' in inputFormat:
        decType = 2
    elif '.3' in inputFormat:
        decType = 1

    #print('DecType->',decType)
    if decType == 0:
        df['Value'] = '{:.0f}'.format(df['Value'] / divDict[formatType])
    elif decType>0:
        #df['Value'] = '{:.{precision}f}'.format(df['Value'],decType)
        df['Value'] = df['Value'] / divDict[formatType]
        df['Value'] = df['Value'].apply(lambda x: '{:.{precision}f}'.format(x,precision=decType))
    return df
