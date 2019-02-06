# this function removes spaces from a list. (after splitting a string)
def remove_spaces (list_1):
    list_of_data_without_spaces=[]
    for item_list in list_1:
        my_list = []
        for item_of_list in item_list:
            if item_of_list==" " or item_of_list=="":
                continue
            else:
                my_list.append(item_of_list)
        list_of_data_without_spaces.append(my_list)

    return list_of_data_without_spaces

def calcuate_xi_squre (y_list,a,b,dy_list,x_list,n):
    xi_squre=0
    for index in range(0,n):
        item_in_index=((y_list[index]-(a*x_list[index]+b))/dy_list[index])**2
        xi_squre=xi_squre+item_in_index
    return xi_squre

def calculate_xi_squre_red(xi_squre,n):
    xi_squre_red=xi_squre/(n-2)
    return xi_squre_red


#calculating average z
def calculating_avg(z,dy_squre):
    up_sum=0
    down_sum=0
    for index in range (0,len(z)):
        item_in_index_up=z[index]/dy_squre[index]
        up_sum=up_sum+item_in_index_up
        item_in_index_down=1/dy_squre[index]
        down_sum=down_sum+item_in_index_down
    return up_sum/down_sum

# this function calculates f(x) with a given a and b
def calculatin_fx_list (a,b,x_list):
    fx_list=[]
    for item in x_list:
        fx_of_y=(a*item)+b
        fx_list.append(fx_of_y)
    return fx_list

# this function gets a list of the axis names and extract the names of the axis as they should appear in the linear fit
def fixing_axis_names (axis_names_list, axis):
    axis_name = 1
    for item in axis_names_list:
        if item[0] == axis:
            axis_name = item
    colon_index_in_axis_name=axis_name.index(":")
    axis_fixed=axis_name[colon_index_in_axis_name+1:]
    return axis_fixed.title()

 ################main program############
def fit_linear(filename):
    file=open(filename,"r")
    data=file.readlines()
    index_of_space=data.index("\n")
    data_without_axis=data[0:index_of_space]  #data without axis names
    axis_names=[] #not splited!!
    new_data_without_axis=[]    #will be list without axis, stripped(),lower()

    # creating a list of the axis names
    for line in data:
        line=line.lower().strip()
        if "x" and "axis" in line:
            axis_names.append(line)
        if "y" and "axis" in line:
            axis_names.append(line)

    x_axis=fixing_axis_names(axis_names,"x")
    y_axis=fixing_axis_names(axis_names,"y")

#fixing the "data_without_axis" list
    for line in data_without_axis:
        line = line.lower()
        line = line.strip()
        line=line.split(" ")
        new_data_without_axis.append(line)
    new_data_without_axis = remove_spaces(new_data_without_axis) # list without spaces and ready for use (only data)

    data_dict = {} #creating a data dictionary


    #########for columns
    if new_data_without_axis[0][1]=="dx" or new_data_without_axis[0][1]=="dy" or new_data_without_axis[0][1]=="x" or new_data_without_axis[0][1]=="y" :
        #convert string to float
        for t in range (1,len(new_data_without_axis)):
            for k in range (0,len(new_data_without_axis[t])):
                new_data_without_axis[t][k]=float(new_data_without_axis[t][k])
        print(new_data_without_axis)
        #check if all items in "data" have the same length
        for p in range(0,len(new_data_without_axis)-1):
            if len(new_data_without_axis[p])!=len(new_data_without_axis[p+1]):
                print("Input file error: Data lists are not the same length.")
                return
        #check if uncertainties are positive
        index_dx=new_data_without_axis[0].index("dx")
        index_dy=new_data_without_axis[0].index("dy")
        for r in range(1,len(new_data_without_axis)):
            if new_data_without_axis[r][index_dx]<0 or new_data_without_axis[r][index_dy]<0:
                print("Input file error: Not all uncertainties are positive.")
                return

        # creat a dictionary with x,dx,y,dy as keys and the
        for w in range(0, 4):
            items_list = []
            for n in range(1, len(new_data_without_axis)):
                items_list.append(new_data_without_axis[n][w])
            data_dict[new_data_without_axis[0][w]] = items_list

    #in rows
    else :
        lenght=len(new_data_without_axis[0])
        for k in range(0,4):      #check if all items in "data" have the same length
            if len(new_data_without_axis[k])!=lenght:
                print("Input file error: Data lists are not the same length.")
                return
        for l in new_data_without_axis:
            float_list=[]
            for j in range(1,len(l)):
                float_list.append(float(l[j]))
            data_dict[l[0]]=float_list
        #check if uncertainties are positive
        uncertainties_x=data_dict["dx"]
        for item in uncertainties_x:
            if item<0:
                print("Input file error: Not all uncertainties are positive.")
                return
        uncertainties_y=data_dict["dy"]
        for item in uncertainties_y:
            if item<0:
                print("Input file error: Not all uncertainties are positive.")
                return


    # creating a list of x_squre_and dy_squre (for calculating chi2)
    dy_list=data_dict["dy"]
    dy_squre_list=[]
    for item in dy_list:
        item_squre=item**2
        dy_squre_list.append(item_squre)
    x_list=data_dict["x"]
    x_squre_list=[]
    for item in x_list:
        x_squre_list.append(item**2)
    y_list=data_dict["y"]
    dx_list=data_dict["dx"]

    #creating a list of x dot y for calculating chi2
    x_dot_y = []
    for index in range (0,len(x_list)):
        x_dot_y.append(y_list[index]*x_list[index])


    #calculating a,b,db,da
    import math
    a=(calculating_avg(x_dot_y,dy_squre_list)-(calculating_avg(x_list,dy_squre_list)*calculating_avg(y_list,dy_squre_list)))/(calculating_avg(x_squre_list,dy_squre_list)-(calculating_avg(x_list,dy_squre_list)**2))

    b=calculating_avg(y_list,dy_squre_list)-(a*(calculating_avg(x_list,dy_squre_list)))

    n=len(x_list)  #number of dots
    da=math.sqrt((calculating_avg(dy_squre_list,dy_squre_list))/(n*(calculating_avg(x_squre_list,dy_squre_list)-(calculating_avg(x_list,dy_squre_list)**2))))

    db=math.sqrt((calculating_avg(dy_squre_list,dy_squre_list)*calculating_avg(x_squre_list,dy_squre_list))/(n*(calculating_avg(x_squre_list,dy_squre_list)-(calculating_avg(x_list,dy_squre_list)**2))))
    print("a=",a,"+-",da)
    print("b=",b,"+-",db)

    # calculating xi_squre and xi_squre_reduced
    xi_squre=calcuate_xi_squre(y_list,a,b,dy_list,x_list,n)
    print("chi2=",xi_squre)
    xi_squre_red=calculate_xi_squre_red(xi_squre,n)
    print("chi2_reduced =",xi_squre_red)

    #creating a list of fx
    fx_list=calculatin_fx_list(a,b,x_list)

    #creating the plot:

    from matplotlib import pyplot as plt
    plt.plot(x_list,fx_list, "r")
    plt.errorbar(x_list, y_list, xerr=dx_list, yerr=dy_list, ecolor="b",fmt='None')
    plt.ylabel(y_axis)
    plt.xlabel(x_axis)
    #plt.show()
    plt.savefig("linear_fit.SVG")
    return








fit_linear("input_3")