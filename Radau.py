
import numpy as np
from inspect import isfunction
import os
from rdpget_function import rdpget
from scipy import sparse
import math
#解stiff differential equation
# %     Numerical solution of a stiff (or differential algebraic) system of
# # %     first order ordinary differential equations:
# # %                   Mass*y' = OdeFcn(t,y).
# # %     The system can be (linearly) implicit (mass-matrix Mass ~= I)
# # %     or explicit (Mass = I)
# # %     The code is based on implicit Runge-Kutta methods (Radau IIa)
# # %     with variable order (1, 5, 9, 13), with step size control and
# # %     continuous output.
# # %
# # %     AUTHORS: E. HAIRER AND G. WANNER
# # %              UNIVERSITE DE GENEVE, DEPT. DE MATHEMATIQUES
# # %              CH-1211 GENEVE 24, SWITZERLAND
# # %              E-MAIL:  Ernst.Hairer@math.unige.ch
# # %                       Gerhard.Wanner@math.unige.ch
# # %
# # %     For a description of the related code Radau5 see the book
# # %         E. HAIRER AND G. WANNER, SOLVING ORDINARY DIFFERENTIAL
# # %         EQUATIONS II. STIFF AND DIFFERENTIAL-ALGEBRAIC PROBLEMS.
# # %         SPRINGER SERIES IN COMPUTATIONAL MATHEMATICS 14,
# # %         SPRINGER-VERLAG 1991, SECOND EDITION 1996.
# # %
# # %     Matlab version:
# # %     Denis Bichsel
# # %     Rue des Deurres 58
# # %     2000 Neuch鈚el
# # %     Suisse
# # %     dbichsel@infomaniak.ch
# # %     Version of end 2015
# # %
# # % RADAU solve stiff differential equations, with variable order method.
# # %
# # % [tout,yout] = radau(OdeFcn,tspan,y0) with tspan = [t0, tfinal]
# # %   solve the system of first order differential (or differential -
# # %   algebraic) equations y' = OdeFcn(t,y) from t0 to tfinal with initial
# # %   conditions y0. OdeFcn is the name (or function handle) of the function
# # %   which defines the system.
# # %  Input
# # %   y0:      must be a column vector of initial conditions
# # %   OdeFcn:  must return a column vector
# # %   tspan:   is a vector with at least two component, t0 and tfinal
# # %   tspan may also be a monotonic vector t0 < t1 < t2 ... < tfinal or
# # %   t0 > t1 > t2 ... > tfinal.
# # %   If tspan is a two components vector, the solver returns the solution
# # %   at points evaluated by the solver.
# # %   If tspan is a vector with more than two components, the solutions are
# # %   only returned at these tspan values.
# # %
# # % [tout,yout] = radau(OdeFcn,tspan,y0,options) solves as above with
# # %   default integration parameters replaced by values in options, an
# # %   argument created with the RDPSET function. See RDPSET for details.
# # %
# # % [tout,yout] = radau(OdeFcn,tspan,y0,options,varargin) solves as above
# # %   with parameters in varargin. These parameters may be used in OdeFcn,
# # %   JacFcn and or in MassFcn.
# # %
# # % radau(OdeFcn,tspan,y0) or
# # % radau(OdeFcn,tspan,y0,options) or
# # % radau(OdeFcn,tspan,y0,options,varargin)
# # %   If radau is called without output parameters, radau calls odeplot to
# # %   show graphical solution.
# # %
# # % RADAU also solves problems M*y' = F(t,y) with a constant mass matrix M.
# # %   Define a function which define the mass matrix and let it know to RADAU
# # %   via the options (see RDPSET and the examples)(default = identity).
# # %
# # % The jacobian of the system may be defined analytically and the name
# # %   or the handle of this function may be given to RADAU via RDPSET
# # %   (default numerical jacobian).
# # %
# # % [tout,yout,Stats] = radau(OdeFcn,tspan,y0) or
# # % [tout,yout,Stats] = radau(OdeFcn,tspan,y0,options) or
# # % [tout,yout,Stats] = radau(OdeFcn,tspan,y0,options,varargin)
# # %   solve the system like above and let know some informations on the
# # %   calculations:
# # %  Stats.Stat gives the the following global informations.
# # %   FcnNbr:     The call number to the OdeFcn.
# # %   JacNbr:     The call number to the jacobian.
# # %   DecompNbr:  The number of LU decompositions
# # %   SolveNbr:   The number of non-linear system resolutions.
# # %   StepNbr:    The number of main steps.
# # %   AccptNbr:   The number of accepted steps
# # %   StepRejNbr: The number of rejected steps
# # %   NewtRejNbr: The number of rejected Newton procedure.
# # %
# # % Stats.Dyn gives the following dynamical information
# # %   Dyn.haccept_t:      Times when the step sizes are accepted
# # %   Dyn.haccepted_Step: Steps when the step sizes are accepted
# # %   Dyn.haccept:        Values of the accepted step sizes
# # %   Dyn.hreject_t:      Times when the steps are rejected
# # %   Dyn.hreject_Step:   Steps when the step sizes are rejected
# # %   Dyn.hreject:        Values of the rejected step sizes
# # %   Dyn.Newt_t:         Times when Newton is iterated
# # %   Dyn.Newt_Step:      Steps when Newton is iterated
# # %   Dyn.NewtNbr:        Number of Newton iterations
# # %   Dyn.NbrStg_t:       Times when the numbers of stages are read
# # %   Dyn.NbrStg_Step:    Steps when the numbers of stages are read
# # %   Dyn.NbrStg:         Number of stages
# # %
# # % -------------------------------------------------------------------------

class radau:    #定义类，并起一个名字



    ##--------------------Declaration of global variables

    global T
    global TI
    global ValP
    global C
    global Dd
    global T_1
    global TI_1
    global C1
    global ValP1
    global Dd1
    global T_3
    global TI_3
    global C3
    global ValP3
    global Dd3
    global T_5
    global TI_5
    global C5
    global ValP5
    global Dd5
    global T_7
    global TI_7
    global C7
    global ValP7
    global Dd7





    #OdeFcn传入一个函数,self是类特有的属性
    def __init__(self,OdeFcn,tspan,y0,*options_varagin):

        #构造函数，类接收外部传入参数全靠构造函数,外加一个可变参数
        self.OdeFcn = OdeFcn#必须是函数类型
        self.tspan = tspan#必须是array类型
        self.y0 = y0#y0必须是array类型
        self.options=options_varagin[0]#options必须是字典类型，对应的key value设置为列表类型
        self.varagin=options_varagin[1]
        self.nargin=3+len(options_varagin)
    def radau_main(self):    #类的方法


        Solver_Name = 'radau'
        Ny = len(self.y0)
        # ---------------------------
        # Default options values
        AbsTolDef = [1e-6] # General parameters
        RelTolDef = [1e-3]
        InitialStepDef = [1e-2]
        MaxStepDef = [self.tspan[-1] - self.tspan(0)]
        MaxNbrStepDef = [float('inf')]
        MassFcnDef = []
        EventsFcnDef = []
        RefineDef = [1]###############默认为一个数
        OutputFcnDef = []###########默认只放一个函数
        OutputSelDef = np.linspace(1,Ny,num=Ny,endpoint=True,retstep=False,dtype=float)
        ComplexDef = [False]
        NbrInd1Def = [0]
        NbrInd2Def = [0]
        NbrInd3Def = [0]
        JacFcnDef = []   # Implicit solver parameters 空列表
        JacRecomputeDef = [1e-3]
        Start_NewtDef = [False]
        MaxNbrNewtonDef = [7]
        NbrStgDef = [3]
        MinNbrStgDef = [3]  # 1 3 5 7 #默认为一个数
        MaxNbrStgDef = [7]  # 1 3 5 7#默认为一个数
        SafeDef = [0.9]
        Quot1Def = [1]
        Quot2Def = [1.2]
        FacLDef = [0.2]
        FacRDef = [8.0]
        VituDef = [0.002]
        VitdDef = [0.8]
        hhouDef = [1.2]
        hhodDef = [0.8]
        GustafssonDef = [True]

        OpDefault=[AbsTolDef,   RelTolDef,       InitialStepDef,\
                           MaxStepDef,   MaxNbrStepDef,\
                           MassFcnDef,   EventsFcnDef,    RefineDef,\
                           OutputFcnDef, OutputSelDef,    ComplexDef,\
                           NbrInd1Def,   NbrInd2Def,      NbrInd3Def,\
                           JacFcnDef,    JacRecomputeDef,\
                           Start_NewtDef,MaxNbrNewtonDef,\
                           NbrStgDef,    MinNbrStgDef,    MaxNbrStgDef,\
                           SafeDef,\
                           Quot1Def,     Quot2Def,\
                           FacLDef,      FacRDef,\
                           VituDef,      VitdDef,\
                           hhouDef,      hhodDef,\
                           GustafssonDef]

        OpNames=['AbsTol','RelTol','InitialStep','MaxStep','MaxNbrStep',
                 'MassFcn','EventsFcn','Refine',
                 'OutputFcn','OutputSel','Complex',
                 'NbrInd1','NbrInd2','NbrInd3',
                 'JacFcn','JacRecompute',
                 'Start_Newt','MaxNbrNewton',
                 'NbrStg','MinNbrStg','MaxNbrStg',
                 'Safe',
                 'Quot1','Quot2',
                 'FacL','FacR',
                 'Vitu','Vitd',
                 'hhou','hhod','Gustafsson']


        if  not(isfunction(self.OdeFcn)) :

            print('First input argument must be a valid function')
            os._exit(0)


        elif not isinstance(self.tspan,np.ndarray) or len(self.tspan)<2:

            print('Third input argument must be in ndarray type')
            os._exit(0)

        elif not isinstance(self.y0,np.ndarray):

            print('Initial conditions argument must be in ndarray type')
            os._exit(0)

        #  OdeFcn tspan y options are all good.

        #用字典去代替matlab中的一维结构数组

        if self.nargin<4:

            options_dict={}
        Arg_In=self.nargin>4
        Arg_dict={'In':Arg_In}

        Op_dict={}

        for n in range(1,len(OpNames)+1):

            Op_dict[OpNames[n-1]]=rdpget(self.options,OpNames[n-1],OpDefault[n-1])


        #####--------------AbsTol

        ##Judgement of AbsTol, AbsTol should be of length 1 or length of input y0


        if not(len(Op_dict['AbsTol'])==1) and not(len(Op_dict['AbsTol'])==Ny):


            print(Solver_Name, ': AbsTol vector must be of length 1 or',Ny)

            os._exit(0)

        ##getting each data in AbsTol when its length is 1 or Ny
        for data in Op_dict['AbsTol'] :

            if not(isinstance(data,int)) and not(isinstance(data,float)):


                print(Solver_Name, ': Wrong data type in AbsTol ,AbsTol must be a positive number')

                os._exit(0)

            else:

                pass

            if data <=0 :

                print(Solver_Name,': Absolute tolerance are too small.')

                os._exit(0)

            else:

                pass

        #Extend Op_dict_AbsTol from list to matrix,like Op.AbsTol = Op.AbsTol + zeros(size(y0)) in matlab
        Op_dict_AbsTol_matrix=[]
        for i in range(1,Ny+1):

            b=Op_dict['AbsTol']

            Op_dict_AbsTol_matrix.extend(b)



        Op_dict['AbsTol']=np.array(Op_dict_AbsTol_matrix)



        ###---------RelTol




        ##Judgement of RelTol, RelTol should be of length 1 or length of input y0

        if not (len(Op_dict['RelTol']) == 1) and not (len(Op_dict['RelTol']) == Ny):
            print(Solver_Name, ': RelTol vector must be of length 1 or', Ny)
            os._exit(0)

        ##getting each data in AbsTol when its length is 1 or Ny
        for data in Op_dict['RelTol']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong data type in RelTol ,RelTol must be a positive number')

                os._exit(0)

            else:

                pass

            if data <= 10*np.spacing(1):

                print(Solver_Name, ': Relative  tolerance are too small.')

                os._exit(0)

            else:

                pass

        # Extend Op_dict_AbsTol from list to matrix,like Op.RelTol = Op.RelTol + zeros(size(y0)) in matlab
        Op_dict_RelTol_matrix = []
        for i in range(1, Ny + 1):
            b = Op_dict['RelTol']

            Op_dict_RelTol_matrix.extend(b)

        Op_dict['RelTol'] = np.array(Op_dict_RelTol_matrix)



        ###-----------Initial Step Size

        for data in Op_dict['InitialStep']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': WWrong input "InitialStep" must be a number')

                os._exit(0)

            else:

                pass




        ##-----------Maximal Step Size



        for data in Op_dict['MaxStep']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': WWrong input "MaxStep" must be a number')

                os._exit(0)

            else:

                pass




        ##----------Maximal Number of Steps




        for data in Op_dict['MaxNbrStep']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "MaxStep" must be a number')

                os._exit(0)

            elif data <=0:

                print(Solver_Name,': Wrong input "MaxNbrStep" ,elements in MaxNbrStep must be > 0')

                os._exit(0)


        ##-----------------Mass (原代码中省略)



        ##-----------------Events



        if len(Op_dict['EventsFcn'])==0:

            EventsExist=0

        else:

            EventsExist=1


        ##------------------Refine


        if len(Op_dict['Refine'])!=0:

            for data in Op_dict['Refine']:

                if not (isinstance(data, int)) and not (isinstance(data, float)):
                    print(Solver_Name, ': Wrong input "Refine"" must be a number')

                    os._exit(0)




        ##-------------------OutPutFcn

        #列表中可以存函数地址
        Op_dict_outputfcn_str=[]
        if len(Op_dict['OutputFcn'])!=0:

            for data in Op_dict['OutputFcn']:

                if not isfunction(data):

                    print(Solver_Name, ': OutputFcn must be valid functions')

                    os._exit(0)

                else:

                    Op_dict_outputfcn_str.append(str(data.__name__)) #name前后都是由两个下划线组成的
        else:

            pass

            Op_dict['OutputFcn']=Op_dict_outputfcn_str
            #like  Op.OutputFcn = func2str(Op.OutputFcn) in matlab
            #把原本存的函数地址全部替换为函数名字符串



        ##---------------OutputSel


        if len(Op_dict['OutputSel'])!=0:

            IndComp=[]
            for c in range(1,Ny+1):

                IndComp.append(c)

            for n in range(0,len(Op_dict['OutputSel'])):


                if Op_dict['OutputSel'][n] not in IndComp:


                    print(Solver_Name,': OutputSel must be an integer in 1 .. ',Ny)

                    os._exit(0)

                else:

                    pass

        else:


            pass



        ##--------------Complex

        #Complex中必须是bool类型


        for data in Op_dict['Complex']:

            if not isinstance(data,bool):

                print(Solver_Name, ': Complex must be in the type ''bool')

                os._exit(0)

        #相当于Op.RealXY = ~Op.Complex
        Op_dict['RealXY']= []

        for data in Op_dict['Complex']:


            Op_dict['RealXY'].append(not(data))




        ##----------------Index1 Index2 Index3


        counter=0 #Set counter to see if all the elements in Op_dict['NbrInd1'] are zero
        for data in Op_dict['NbrInd1']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "NbrInd1" must be a number')

                os._exit(0)

            elif data <0:

                print(Solver_Name,': Wrong input "NbrInd1" ,elements in NbrInd1 must be > 0')

                os._exit(0)

            elif data==0:

                counter=counter+1

        if counter == len(Op_dict['NbrInd1']):

            Op_dict['NbrInd1']=[Ny] #一个数也存成list



        for data in Op_dict['NbrInd2']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "NbrInd2" must be a number')

                os._exit(0)

            elif data <0:

                print(Solver_Name,': Wrong input "NbrInd2" ,elements in NbrInd1 must be > 0')

                os._exit(0)

            else:

                pass

        for data in Op_dict['NbrInd3']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "NbrInd3" must be a number')

                os._exit(0)

            elif data < 0:

                print(Solver_Name, ': Wrong input "NbrInd3" ,elements in NbrInd1 must be > 0')

                os._exit(0)

            else:

                pass
        if len(Op_dict['NbrInd2'])==len(Op_dict['NbrInd3']):


            if len(Op_dict['NbrInd1'])==1:

                Op_dict_NbrInd1=Op_dict['NbrInd1']*len(Op_dict['NbrInd2'])

                temporary_parameter=[Op_dict_NbrInd1[i]+Op_dict['NbrInd2'][i]+Op_dict['NbrInd3'][i]
                                     for i in range(0,len(Op_dict['NbrInd2']))]

            elif len(Op_dict['NbrInd1'])==len(Op_dict['NbrInd2']):

                temporary_parameter = [Op_dict['NbrInd1'][i] + Op_dict['NbrInd2'][i] + Op_dict['NbrInd3'][i]
                                       for i in range(0, len(Op_dict['NbrInd2']))]

            else:

                print(Solver_Name,':NbrInd1 dimension must agree with Ind2,3')

                os._exit(0)



        else:

            if len(Op_dict['NbrInd2'])==1:


                if len(Op_dict['NbrInd1'])==1:


                    Op_dict_NbrInd1 = Op_dict['NbrInd1'] * len(Op_dict['NbrInd3'])
                    Op_dict_NbrInd2 = Op_dict['NbrInd2'] * len(Op_dict['NbrInd3'])

                    temporary_parameter = [Op_dict_NbrInd1[i] + Op_dict_NbrInd2[i] +
                                           Op_dict['NbrInd3'][i]
                                           for i in range(0, len(Op_dict['NbrInd3']))]

                else:

                    if len(Op_dict['NbrInd1'])==len(Op_dict['NbrInd3']):



                        Op_dict_NbrInd2 = Op_dict['NbrInd2'] * len(Op_dict['NbrInd3'])

                        temporary_parameter = [Op_dict['NbrInd1'][i] + Op_dict_NbrInd2[i] +
                                               Op_dict['NbrInd3'][i]
                                               for i in range(0, len(Op_dict['NbrInd3']))]


                    else:

                        print(Solver_Name, ':NbrInd1 dimension must agree with Ind3 when Ind2=1 and '
                                           'Ind3!=1')

                        os._exit(0)


            else:

                if len(Op_dict['NbrInd3'])==1:

                    if len(Op_dict['NbrInd1']) == 1:

                        Op_dict_NbrInd1 = Op_dict['NbrInd1'] * len(Op_dict['NbrInd2'])
                        Op_dict_NbrInd3 = Op_dict['NbrInd3'] * len(Op_dict['NbrInd2'])

                        temporary_parameter = [Op_dict_NbrInd1[i] + Op_dict_NbrInd3[i] +
                                               Op_dict['NbrInd2'][i]
                                               for i in range(0, len(Op_dict['NbrInd2']))]

                    else:

                        if len(Op_dict['NbrInd1']) == len(Op_dict['NbrInd2']):

                            Op_dict_NbrInd3 = Op_dict['NbrInd3'] * len(Op_dict['NbrInd2'])

                            temporary_parameter = [Op_dict['NbrInd1'][i] + Op_dict_NbrInd3[i] +
                                                   Op_dict['NbrInd2'][i]
                                                   for i in range(0, len(Op_dict['NbrInd2']))]


                        else:

                            print(Solver_Name, ':NbrInd1 dimension must agree with Ind2 when Ind3=1 and '
                                               'Ind2!=1')

                            os._exit(0)

                else:

                    print(Solver_Name, ':NbrInd2 dimension must agree with Ind3 when they are not zero')

                    os._exit(0)

        counter = 0
        for i in range(0, len(temporary_parameter)):

            if temporary_parameter[i] == Ny:

                pass


            else:

                print(Solver_Name, ': Curious input for NbrInd1 + NbrInd2 + NbrInd3 ~= Ny')

                os._exit(0)




        ##--------------Jacobian


        if len(Op_dict['JacFcn'])==0:

            Op_dict['JacAnalytic']=False

        else:

            Op_dict['JacAnalytic']=True


        ##---------------JacRecompute


        for data in Op_dict['JacRecompute']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "JacRecompute" must be numeric {0.001}')

                os._exit(0)

            elif abs(data) >= 1 :

                print(Solver_Name,': Curious input for "JacRecompute" ',data)

                os._exit(0)

            else:

                pass



        ##-------------------Start_Newt
        #Predict: switch for starting values of newton iterations.


        if len(Op_dict['Start_Newt']) >0:



            for data in Op_dict['Start_Newt']:

                if not isinstance(data,bool):

                    print(Solver_Name, ': Start_Newt must be logical')

                    os._exit(0)

                else:

                    pass


        else:

            pass





        ##------------Maximal Number of Newton Iteration



        for data in Op_dict['MaxNbrNewton']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "MaxNbrNewton" must be a positive number >= 4')

                os._exit(0)

            elif data < 4 :

                print(Solver_Name,': Wrong input "MaxNbrNewton" ',data,', must be > =4')

                os._exit(0)

            else:

                pass





        ##--------------Number of Stages (Min Initial Max)


        Stage=[1,3,5,7]

        for data in Op_dict['NbrStg']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "NbrStg" must be in [ 1 3 5 7]')

                os._exit(0)

            elif data not in Stage :

                print(Solver_Name,': Wrong input "NbrStg" must be in [ 1 3 5 7]')

                os._exit(0)

            else:

                pass


        for data in Op_dict['MinNbrStg']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "MinNbrStg" must be in [ 1 3 5 7]')

                os._exit(0)

            elif data not in Stage:

                print(Solver_Name,': Wrong input "MinNbrStg" must be in [ 1 3 5 7]')

                os._exit(0)

            else:

                pass



        for data in Op_dict['MaxNbrStg']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "MaxNbrStg" must be in [ 1 3 5 7]')

                os._exit(0)

            elif data not in Stage :

                print(Solver_Name,': Wrong input "MaxNbrStg" must be in [ 1 3 5 7]')

                os._exit(0)

            else:

                pass
        counter =0
        for data in Op_dict['MinNbrStg']:

            if data > Op_dict['MaxNbrStg'][counter]:

                print(Solver_Name, ':  Wrong input MaxNbrStg >= MinNbrStg please')

                os._exit(0)

            else:

                counter=counter+1


        counter=0
        for data in Op_dict['NbrStg']:

            if data > Op_dict['MaxNbrStg'][counter] or data < Op_dict['MinNbrStg'][counter]:

                print(Solver_Name, ':   Curious input for "NbrStg"')

                os._exit(0)

            else:

                counter=counter+1


        ##------------Safe Safety factor in step size prediction



        for data in Op_dict['Safe']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ':  Wrong input "Safe" must be a positive number')

                os._exit(0)

            elif data<=0.001 or data>=1:

                print(Solver_Name,':  Curious input for Safe,',data,' must be in 0.001~1')

                os._exit(0)

            else:

                pass

        #  --------------- QUOT1 AND QUOT2: IF QUOT1 < HNEW / HOLD < QUOT2, STEPSIZE = CONST.
        # work(5: 6) = [quot1;quot2], parameters for step size selection
        # if quot1 < hnew / hold < quot2, then the step size is not changed.
        # this saves, together with a large work(3), LU-decompositions and
        # computing time for large systems. for small systems one may have
        # quot1 = 1, quot2 = 1.2, for large full systems quot1 = 0.99, quot2 =
        # 2 might be good.defaults quot1 = 1, quot2 = 1.2.




        for data in Op_dict['Quot1']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ':   Wrong input "Quot1"  must be numeric')

                os._exit(0)

            elif data >1:

                print(Solver_Name,': Curious input for Quot1 = ', data, ' must be in <= 1')

                os._exit(0)

            else:

                pass



        for data in Op_dict['Quot2']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ':   Wrong input "Quot2"  must be numeric')

                os._exit(0)

            elif data >1:

                print(Solver_Name,': Curious input for Quot2 = ', data, ' must be in <= 1')

                os._exit(0)

            else:

                pass




        ##------------FacL, Facr : parameters for step size selection


        for data in Op_dict['FacL']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "FacL" must be numeric default 0.2')

                os._exit(0)

            elif data >1:

                print(Solver_Name,': Curious input for "FacL" default 0.2')

                os._exit(0)

            else:

                pass

        for data in Op_dict['FacR']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "FacR" must be numeric default 8')

                os._exit(0)

            elif data < 1:

                print(Solver_Name, ': Curious input for "FacR" default 8')

                os._exit(0)

            else:

                pass




        ##-------------Vitu Vitd Hhou Hhod parameters for order selection strategy

        for data in Op_dict['Vitu']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "Vitu" must be numeric default 0.002')

                os._exit(0)

            else:

                pass


        for data in Op_dict['Vitd']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "Vitd" must be numeric default 0.8')

                os._exit(0)

            else:

                pass


        for data in Op_dict['hhou']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "hhou" must be numeric default 1.2')

                os._exit(0)

            else:

                pass




        for data in Op_dict['hhod']:

            if not (isinstance(data, int)) and not (isinstance(data, float)):

                print(Solver_Name, ': Wrong input "Vitu" must be numeric default 0.8')

                os._exit(0)

            else:

                pass



        ##------------Gustafsson

        for data in Op_dict['Gustafsson']:

            if not isinstance(data, bool):

                print(Solver_Name, ': Wrong input "Gustafsson" must be logical')

                os._exit(0)

            else:

                pass



        solver54=['radausolver',self.OdeFcn,self.tspan,self.y0,Op_dict]



        if Arg_dict['In']:

            solver54=[solver54,self.varagin]



        ###------------------------------------------------------------------------------------
        ###Tests on outputs
        ###------------------------------------------------------------------------------------


        y=self.y0
        varargout=radau.radausolver(y,Op_dict)



        OutputNbr=len(varargout)


        if len(OutputNbr)==0:

            Op_dict['Stats']=False

            if len(Op_dict['OutputFcn'])==0:

                Op_dict['OutputFcn']=rdpget(self.options,'OutputFcn','odeplot')

            else:

                pass


        elif OutputNbr==2:

            Op_dict['Stats'] = False

        elif OutputNbr==3:

            Op_dict['Stats'] = True


        elif OutputNbr==5:

            Op_dict['Stats'] = False

            if not EventsExist:

                print(Solver_Name,': Events not set, too much output')

                os._exit(0)


            else:

                pass


        elif OutputNbr==6:

            Op_dict['Stats'] = True

            if not EventsExist:

                print(Solver_Name, ': Events and Stats must be set for 6 outputs')

                os._exit(0)


            else:

                pass


        else:

            print(Solver_Name, ': Outputs number not correct')

            os._exit(0)



        solverradau=['radausolver',self.OdeFcn,self.tspan,self.y0,Op_dict]

        if Arg_dict['In']:


            solverradau=[solverradau,self.varagin]


        else:

            pass


        if OutputNbr ==0:

            varargout=[]


        else:

            pass


        return varargout




    def radausolver(self,y,Op_dict):

        global T
        global TI
        global ValP
        global C
        global Dd




        Solver_Name='radausolver'

        ##----------------Input Parameters


        #Time Properties

        tspan=self.tspan

        ntspan=len(tspan)

        t=tspan[0]

        tfinal=tspan[ntspan-1]

        PosNeg=np.sign(tfinal-t)

        #Number of equations, y is a column vector

        Ny=len(y)

        #Options parameters

        #--General options

        RelTol=Op_dict['RelTol']
        AbsTol=Op_dict['AbsTol']
        h=Op_dict['InitialStep']
        hmax=Op_dict['MaxStep']
        MassFcn=Op_dict['MassFcn'][0]#都先默认最多包含一个函数
        EventsFcn=Op_dict['EventsFcn'][0]
        OutputFcn=Op_dict['OutputFcn'][0]
        OutputSel=Op_dict['OutputSel']



        RealYN=[]  #RealYN = ~Op.Complex
        for data in Op_dict['Complex']:

            RealYN.append(not(data))

        NbrInd1=Op_dict['NbrInd1']
        NbrInd2=Op_dict['NbrInd2']
        NbrInd3=Op_dict['NbrInd3']
        Refine=Op_dict['Refine']
        MaxNbrStep=Op_dict['MaxNbrStep']

        #--Parameters for implicit procedure

        MaxNbrNewton=Op_dict['MaxNbrNewton']
        Start_Newt=Op_dict['Start_Newt']
        JacFcn=Op_dict['JacFcn'][0]##############################
        JacAnalytic=Op_dict['JacAnalytic']
        Thet=Op_dict['JacRecompute']
        Safe=Op_dict['Safe']
        Quot1=Op_dict['Quot1']
        Quot2=Op_dict['Quot2']

        FacL=[]
        for data in Op_dict['FacL']:

            FacL.append(1/data)

        FacR = []
        for data in Op_dict['FacR']:
            FacR.append(1 / data)


        #--Order selection parameters

        NbrStg=Op_dict['NbrStg']
        MinNbrStg=Op_dict['MinNbrStg']
        MaxNbrStg=Op_dict['MaxNbrStg']
        Vitu=Op_dict['Vitu']
        Vitd=Op_dict['Vitd']
        hhou=Op_dict['hhou']
        hhod=Op_dict['hhod']
        Gustafsson=Op_dict['Gustafsson']

        #--Initialisation of Stat parameters

        Stat={}

        Stat['FcnNbr']=0
        Stat['JacNbr'] = 0
        Stat['DecompNbr'] = 0
        Stat['SolveNbr'] = 0
        Stat['StepNbr'] = 0
        Stat['AccptNbr'] = 0
        Stat['StepRejNbr'] = 0
        Stat['NewRejNbr'] = 0

        #Initialisation of Dyn parameters

        Dyn={}

        Dyn['Jac_t']=[]
        Dyn['Jac_Step'] = []
        Dyn['haccept_t'] = []
        Dyn['haccept_Step'] = []
        Dyn['haccept'] = []
        Dyn['hreject_t'] = []
        Dyn['hreject_Step'] = []
        Dyn['hreject'] = []
        Dyn['Newt_t'] = []
        Dyn['Newt_Step'] = []
        Dyn['NewtNbr'] = []
        Dyn['NbrStg_t'] = [t]
        Dyn['NbrStg_Step'] = [0]
        Dyn['NbrStg'] = [NbrStg]

        StatsExist=False
        nargout=3###############################################################

        if nargout==3 or nargout ==6:

            StatsExist=True
            Dyn['haccept_t'] = []
            Dyn['haccept_Step'] = []
            Dyn['haccept'] = []
            Dyn['hreject_t'] = []
            Dyn['hreject_Step'] = []
            Dyn['hreject'] = []

        else:


            pass

        #----------Arguments

        Arg={}
        Arg['In']=(abs(self.nargin)>4)



        if isfunction(self.OdeFcn):

            OdeError=str(self.OdeFcn.__name__)

        else:

            OdeError=self.OdeFcn


        Arg['Ode']=abs(nargin(self.OdeFcn))>2######################################

        if Arg['Ode'] and not(Arg['In']):#########################

            print(Solver_Name,':  ',OdeError,', parameters are missing')

            os._exit(0)


        else:

            pass

        ##--------------------MassFcn with arguments or not
        #先默认MassFcn最多包含一个函数

        if len(MassFcn) ==0:
            data=[]
            for i in range(1,Ny+1):

                data.append(1)



            row = list(range(1,Ny+1))
            col = list(range(1,Ny+1))
            c = sparse.coo_matrix((data, (row, col)), shape=(Ny+1,Ny+1))


        else:

            if nargin(MassFcn)==0:#############################

                Mass=MassFcn()

            else:

                if isfunction(MassFcn):


                    MassError=str(MassFcn.__name__)

                else:

                    MassError=MassFcn

                if not(Arg['In']) :

                    print(Solver_Name, ':  ',MassError, ', parameters are missing')

                    os._exit(0)

                else:

                    Mass=MassFcn(self.varagin)


        ##-----------------------JacFcn with arguments or not
        #默认JacFcn最多含一个函数


        if len(JacFcn)!=0:


            if isfunction(JacFcn):

                JacError=str(JacFcn.__name__)

            else:


                JacError=JacFcn

            Arg['Jac']=(abs(nargin(JacFcn))>2)######################################

            if Arg['Jac']:

                if Arg['Jac'] and not(Arg['In']):

                    print(Solver_Name,':  ',JacError,', parameters are missing')

                else:

                    pass

            else:

                pass


        else:

            pass


        ##----------------------------------------set the output flag and output buffer




        if ntspan==2:



            if Refine[0]<=1:

                Outflag=1
                nBuffer=100
                nout=0
                tout=np.zeros([nBuffer,1])
                yout=np.zeros([nBuffer,Ny])

            else:

                Outflag=2
                nBuffer=10*Refine[0]
                nout=0
                tout=np.zeros([nBuffer,1])
                yout=np.zeros([nBuffer,Ny])


        else:


            Outflag=3
            nout=0
            nout3=0
            tout=np.zeros([ntspan,1])
            yout=np.zeros([ntspan,Ny])

            if Refine[0]>1:

                Refine[0]=1

                print('Warning！',Solver_Name,': Refine set equal 1, because length(tspan) > 2 ')

            else:

                pass



        OutputFcnExist=False

        if not len(OutputFcn)==0:

            OutputFcnExist=True

            #Initialize the OutputFcn

            OutputFcnArg=[OutputFcn,[t,tfinal],y[OutputSel],'init']

            OutputFcnResult=OutputFcn[0]([t,tfinal],y[OutputSel],'init')

        else:

            pass

        #Initialiation of internal constants

        UnExpStepRej=False
        UnExpNewRej=False
        Keep=False
        ChangeNbr=0
        ChangeFlag=False
        Theta=0
        Thetat=0  #Change orderparameter
        Variab=((MaxNbrStg[0]-MinNbrSt[0])!=0)


        InitNbrStg=True
        radau.Coertv(NbrStg,NbrStg,RealYN,InitNbrStg)










































    def ntrprad(self):
        print("我的职业：%s"%self.profession)


    def NumJac(self):
        print("我的职业：%s"%self.profession)


    def DecomRC(self):
        print("我的职业：%s"%self.profession)


    def Solvrad(self):
        print("我的职业：%s"%self.profession)


    def Estrad(self):
        print("我的职业：%s"%self.profession)


    def OutFcnSolout2(self):
        print("我的职业：%s"%self.profession)


    def OutFcnSolout3(self):
        print("我的职业：%s"%self.profession)


    def EventZeroFcn(self):
        print("我的职业：%s"%self.profession)


    def Coertv(self,MinNbrStg,MaxNbrStg,RealYN,Init):

        '''

        :param MaxNbrStg:
        :param RealYN:
        :param Init:
        :return:
        '''


        global T
        global TI
        global C
        global ValP
        global Dd
        global T_1
        global TI_1
        global C1
        global ValP1
        global Dd1
        global T_3
        global TI_3
        global C3
        global ValP3
        global Dd3
        global T_5
        global TI_5
        global C5
        global ValP5
        global Dd5
        global T_7
        global TI_7
        global C7
        global ValP7
        global Dd7

        Fcn_Name='Coertv'


        if Init:
            for NbrStg in range(MinNbrStg[0],MaxNbrStg[0]+1):

                if NbrStg==1:

                    radau.Coertv1(RealYN)

                elif NbrStg==3:

                    radau.Coertv3(RealYN)

                elif NbrStg==5:

                    radau.Coertv5(RealYN)

                elif NbrStg==7:

                    radau.Coertv7(RealYN)



        else:

            if MinNbrStg[0]!= MaxNbrStg[0]:

                print(Fcn_Name, 'Th Number of steps is wrong')

            else:

                pass

            NbrStg=MinNbrStg[0]

            if NbrStg==1:

                T = T_1
                TI = TI_1
                ValP = ValP1
                C = C1
                Dd = Dd1

            elif NbrStg==3:

                T = T_3
                TI = TI_3
                ValP = ValP3
                C = C3
                Dd = Dd3

            elif NbrStg==5:

                T = T_5
                TI = TI_5
                ValP = ValP5
                C = C5
                Dd = Dd5

            elif NbrStg==7:

                T = T_7
                TI = TI_7
                ValP = ValP7
                C = C7
                Dd = Dd7

        return






    def Coertv1(self,RealYN):
        # Implict Euler'method
        global T_1
        global TI_1
        global C1
        global ValP1
        global Dd1

        C1 = 1
        T_1 = 1
        TI_1 = 1
        ValP1 = 1
        Dd1 = -1



    def Coertv3(self,RealYN):

        '''

        :param RealYN:
        :return:
        '''

        global T_3
        global TI_3
        global C3
        global ValP3
        global Dd3
        global Ta3
        global TIa3

        Sq6=np.sqrt(6)
        C3=[(4.0 - Sq6)/10.0,(4.0 + Sq6)/10.0,1]

        Dd=[-(13 + 7*Sq6)/3,(-13 + 7*Sq6)/3,-1.0/3]
        Dd3=Dd[:]

        if RealYN:

            T3=np.array([[9.1232394870892942792e-02,-0.14125529502095420843,-3.0029194105147424492e-02]
                            ,[0.24171793270710701896,0.20412935229379993199,0.38294211275726193779]
                            ,[0.96604818261509293619,1,0]])

            TI3=np.array([[4.3255798900631553510,0.33919925181580986954,0.54177053993587487119]
                             ,[-4.1787185915519047273,-0.32768282076106238708,0.47662355450055045196]
                             ,[-0.50287263494578687595,2.5719269498556054292,-0.59603920482822492497]])

            ST9=math.pow(9,1/3)

            ValP=[(6.0+ST9*(ST9-1))/30.0,(12.0-ST9*(ST9-1))/60.0,ST9*(ST9+1)*np.sqrt(3.0)/60.0]
            Cno=math.pow(ValP[1],2)+math.pow(ValP[2],2)
            ValP3=[1.0/ValP[0],ValP[1]/Cno,ValP[2]/Cno]

        else:

            CP3 = np.array([[1,C3[0],C3[0]**2],
                            [1,C3[1],C3[1]**2],
                            [1,C3[2],C3[2]**2]])

            CQ3 = np.array([[C3[0],math.pow(C3[0],2)/2,math.pow(C3[0],3)/3],
                   [C3[1],math.pow(C3[1],2)/2,math.pow(C3[1],3)/3],
                   [C3[2],math.pow(C3[2],2)/2,math.pow(C3[2],3)/3]])

            A3=np.dot(CQ3,np.linalg.inv(CP3))

            D3,T3= np.linalg.eig(A3)
            D3=np.array([[D3[0],0,0],[0,D3[1],0],[0,0,D3[2]]])
            D3=np.dot(np.eye(3,dtype=float),np.linalg.inv(D3))
            TI3=np.dot(np.linalg.inv(T3),np.eye(3,dtype=float))
            ValP3=[D3[0,0],D3[1,1],D3[2,2]]

        T_3=np.array([[T3[0,0], T3[1,0], T3[2,0]],
                      [T3[0,1], T3[1,1], T3[2,1]],
                      [T3[0,2], T3[1,2], T3[2,2]]])

        TI_3=np.array([[TI3[0,0], TI3[1,0], TI3[2,0]],
                      [TI3[0,1], TI3[1,1], TI3[2,1]],
                      [TI3[0,2], TI3[1,2], TI3[2,2]]])





    def Coertv5(self,RealYN):

        global T_5
        global TI_5
        global C5
        global ValP5
        global Dd5

        C5=[0.5710419611451768219312e-01,0.2768430136381238276800e+00,0.5835904323689168200567e+00,
            0.8602401356562194478479e+00,1.0]

        Dd5=[-0.2778093394406463730479e+02,0.3641478498049213152712e+01,-0.1252547721169118720491e+01,
             0.5920031671845428725662e+00,-0.2000000000000000000000e+00]

        if RealYN:

            #T5是局部变量，不能被外部获取
            T5=np.array([[-0.1251758622050104589014e-01,-0.1024204781790882707009e-01,0.4767387729029572386318e-01,
                          -0.1147851525522951470794e-01,-0.1401985889287541028108e-01],
                         [-0.1491670151895382429004e-02,0.5017286451737105816299e-01,-0.9433181918161143698066e-01,
                          -0.7668830749180162885157e-02,0.2470857842651852681253e-01],
                         [-0.7298187638808714862266e-01,-0.2305395340434179467214e+00,0.1027030453801258997922e+00,
                          0.1939846399882895091122e-01,0.8180035370375117083639e-01],
                         [-0.3800914400035681041264e+00,0.3778939022488612495439e+00,0.4667441303324943592896e+00,
                          0.4076011712801990666217e+00,0.1996824278868025259365e+00],
                         [-0.9219789736812104884883e+00,1,0,1,0]])

            TI5=np.array([[-0.3004156772154440162771e+02,-0.1386510785627141316518e+02,-0.3480002774795185561828e+01,
                           0.1032008797825263422771e+01,-0.8043030450739899174753e+00],
                          [0.5344186437834911598895e+01,0.4593615567759161004454e+01,-0.3036360323459424298646e+01,
                           0.1050660190231458863860e+01,-0.2727786118642962705386e+00],
                          [0.3748059807439804860051e+01,-0.3984965736343884667252e+01,-0.1044415641608018792942e+01,
                           0.1184098568137948487231e+01,-0.4499177701567803688988e+00],
                          [-0.3304188021351900000806e+02,-0.1737695347906356701945e+02,-0.1721290632540055611515e+00,
                           -0.9916977798254264258817e-01,0.5312281158383066671849e+00],
                          [-0.8611443979875291977700e+01,0.9699991409528808231336e+01,0.1914728639696874284851e+01,
                           0.2418692006084940026427e+01,-0.1047463487935337418694e+01]])

            ValP5=[0.6286704751729276645173e+01,0.3655694325463572258243e+01,0.6543736899360077294021e+01,
                   0.5700953298671789419170e+01,0.3210265600308549888425e+01]


        else:


            CP5=np.array([[1,C5[0],C5[0]**2,C5[0]**3,C5[0]**4],
                          [1,C5[1],C5[1]**2,C5[1]**3,C5[1]**4],
                          [1,C5[2],C5[2]**2,C5[2]**3,C5[2]**4],
                          [1,C5[3],C5[3]**2,C5[3]**3,C5[3]**4],
                          [1,C5[4],C5[4]**2,C5[4]**3,C5[4]**4]])

            CQ5 = np.array([[C5[0],(C5[0]**2)/2,(C5[0]**3)/3,(C5[0]**4)/4,(C5[0]**5)/5],
                            [C5[1],(C5[1]**2)/2,(C5[1]**3)/3,(C5[1]**4)/4,(C5[1]**5)/5],
                            [C5[2],(C5[2]**2)/2,(C5[2]**3)/3,(C5[2]**4)/4,(C5[2]**5)/5],
                            [C5[3],(C5[3]**2)/2,(C5[3]**3)/3,(C5[3]**4)/4,(C5[3]**5)/5],
                            [C5[4],(C5[4]**2)/2,(C5[4]**3)/3,(C5[4]**4)/4,(C5[4]**5)/5]])

            A5=np.dot(CQ5,np.linalg.inv(CP5))

            D5,T5= np.linalg.eig(A5)
            D5=np.array([[D5[0],0,0,0,0],[0,D5[1],0,0,0],[0,0,D5[2],0,0],[0,0,0,D5[3],0],[0,0,0,0,D5[4]]])
            D5=np.dot(np.eye(5,dtype=float),np.linalg.inv(D5))
            TI5=np.dot(np.linalg.inv(T5),np.eye(5,dtype=float))
            ValP5=[D5[0,0],D5[1,1],D5[2,2],D5[3,3],D5[4,4]]



        T_5=np.array([[T5[0,0], T5[1,0], T5[2,0], T5[3,0], T5[4,0]],
                      [T5[0,1], T5[1,1], T5[2,1], T5[3,1], T5[4,1]],
                      [T5[0,2], T5[1,2], T5[2,2], T5[3,2], T5[4,2]],
                      [T5[0,3], T5[1,3], T5[2,3], T5[3,3], T5[4,3]],
                      [T5[0,4], T5[1,4], T5[2,4], T5[3,4], T5[4,4]]
                      ])

        TI_5=np.array([[TI5[0,0], TI5[1,0], TI5[2,0], TI5[3,0], TI5[4,0]],
                      [TI5[0,1], TI5[1,1], TI5[2,1], TI5[3,1], TI5[4,1]],
                      [TI5[0,2], TI5[1,2], TI5[2,2], TI5[3,2], TI5[4,2]],
                      [TI5[0,3], TI5[1,3], TI5[2,3], TI5[3,3], TI5[4,3]],
                      [TI5[0,4], TI5[1,4], TI5[2,4], TI5[3,4], TI5[4,4]]
                      ])


        return



    def Coertv7(self,RealYN):

        global T_7
        global TI_7
        global C7
        global ValP7
        global Dd7




        C7=[0.2931642715978489197205e-01,0.1480785996684842918500e+00,0.3369846902811542990971e+00,
            0.5586715187715501320814e+00,0.7692338620300545009169e+00,0.9269456713197411148519e+00,
            1]

        Dd7=[-0.5437443689412861451458e+02,0.7000024004259186512041e+01,-0.2355661091987557192256e+01,
             0.1132289066106134386384e+01,-0.6468913267673587118673e+00,0.3875333853753523774248e+00,
             -0.1428571428571428571429e+00]


        if RealYN:

            #T7是局部变量，不能被外部获取
            T7=np.array([[-0.2153754627310526422828e-02,0.2156755135132077338691e-01,0.8783567925144144407326e-02,
                          -0.4055161452331023898198e-02,0.4427232753268285479678e-02,-0.1238646187952874056377e-02,
                          -0.2760617480543852499548e-02],
                         [0.1600025077880428526831e-02,-0.3813164813441154669442e-01,-0.2152556059400687552385e-01,
                          0.8415568276559589237177e-02,-0.4031949570224549492304e-02,-0.6666635339396338181761e-04,
                          0.3185474825166209848748e-02],
                         [-0.4059107301947683091650e-02,0.5739650893938171539757e-01,0.5885052920842679105612e-01,
                          -0.8560431061603432060177e-02,-0.6923212665023908924141e-02,-0.2352180982943338340535e-02,
                          0.4169077725297562691409e-03],
                         [-0.1575048807937684420346e-01,-0.3821469359696835048464e-01,-0.1657368112729438512412e+00,
                          -0.3737124230238445741907e-01,0.8239007298507719404499e-02,0.3115071152346175252726e-02,
                          0.2511660491343882192836e-01],
                         [-0.1129776610242208076086e+00,-0.2491742124652636863308e+00,0.2735633057986623212132e+00,
                          0.5366761379181770094279e-02,0.1932111161012620144312e+00,0.1017177324817151468081e+00,
                          0.9504502035604622821039e-01],
                         [-0.4583810431839315010281e+00,0.5315846490836284292051e+00,0.4863228366175728940567e+00,
                          0.5265742264584492629141e+00,0.2755343949896258141929e+00,0.5217519452747652852946e+00,
                          0.1280719446355438944141e+00],
                         [-0.8813915783538183763135e+00,1,0,1,0,1,0]])

            TI7=np.array([[-0.2581319263199822292761e+03,-0.1890737630813985089520e+03,-0.4908731481793013119445e+02,
                           -0.4110647469661428418112e+01,-0.4053447889315563304175e+01,0.3112755366607346076554e+01,
                           -0.1646774913558444650169e+01],
                          [-0.3007390169451292131731e+01,-0.1101586607876577132911e+02,0.1487799456131656281486e+01,
                           0.2130388159559282459432e+01,-0.1816141086817565624822e+01,0.1134325587895161100083e+01,
                           -0.4146990459433035319930e+00],
                          [-0.8441963188321084681757e+01,-0.6505252740575150028169e+00,0.6940670730369876478804e+01,
                           -0.3205047525597898431565e+01,0.1071280943546478589783e+01,-0.3548507491216221879730e+00,
                           0.9198549132786554154409e-01],
                          [0.7467833223502269977153e+02,0.8740858897990081640204e+02,0.4024158737379997877014e+01,
                           -0.3714806315158364186639e+01,-0.3430093985982317350741e+01,0.2696604809765312378853e+01,
                           -0.9386927436075461933568e+00],
                          [0.5835652885190657724237e+02,-0.1006877395780018096325e+02,-0.3036638884256667120811e+02,
                           -0.1020020865184865985027e+01,-0.1124175003784249621267e+00,0.1890640831000377622800e+01,
                           - 0.9716486393831482282172e+00],
                          [-0.2991862480282520966786e+03,-0.2430407453687447911819e+03,-0.4877710407803786921219e+02,
                           -0.2038671905741934405280e+01,0.1673560239861084944268e+01,-0.1087374032057106164456e+01,
                           0.9019382492960993738427e+00],
                          [-0.9307650289743530591157e+02,0.2388163105628114427703e+02,0.3927888073081384382710e+02,
                           0.1438891568549108006988e+02,-0.3510438399399361221087e+01,0.4863284885566180701215e+01,
                           -0.2246482729591239916400e+01]])

            ValP7=[0.8936832788405216337302e+01,0.4378693561506806002523e+01,0.1016969328379501162732e+02,
                   0.7141055219187640105775e+01,0.6623045922639275970621e+01,0.8511834825102945723051e+01,
                   0.3281013624325058830036e+01]


        else:


            CP7=np.array([[1,C7[0],C7[0]**2,C7[0]**3,C7[0]**4,C7[0]**5,C7[0]**6],
                          [1,C7[1],C7[1]**2,C7[1]**3,C7[1]**4,C7[1]**5,C7[1]**6],
                          [1,C7[2],C7[2]**2,C7[2]**3,C7[2]**4,C7[2]**5,C7[2]**6],
                          [1,C7[3],C7[3]**2,C7[3]**3,C7[3]**4,C7[3]**5,C7[3]**6],
                          [1,C7[4],C7[4]**2,C7[4]**3,C7[4]**4,C7[4]**5,C7[4]**6],
                          [1,C7[5],C7[5]**2,C7[5]**3,C7[5]**4,C7[5]**5,C7[5]**6],
                          [1,C7[6],C7[6]**2,C7[6]**3,C7[6]**4,C7[6]**5,C7[6]**6]])

            CQ7 = np.array([[C7[0],(C7[0]**2)/2,(C7[0]**3)/3,(C7[0]**4)/4,(C7[0]**5)/5,(C7[0]**6)/6,(C7[0]**7)/7],
                            [C7[1],(C7[1]**2)/2,(C7[1]**3)/3,(C7[1]**4)/4,(C7[1]**5)/5,(C7[1]**6)/6,(C7[1]**7)/7],
                            [C7[2],(C7[2]**2)/2,(C7[2]**3)/3,(C7[2]**4)/4,(C7[2]**5)/5,(C7[2]**6)/6,(C7[2]**7)/7],
                            [C7[3],(C7[3]**2)/2,(C7[3]**3)/3,(C7[3]**4)/4,(C7[3]**5)/5,(C7[3]**6)/6,(C7[3]**7)/7],
                            [C7[4],(C7[4]**2)/2,(C7[4]**3)/3,(C7[4]**4)/4,(C7[4]**5)/5,(C7[4]**6)/6,(C7[4]**7)/7],
                            [C7[5],(C7[5]**2)/2,(C7[5]**3)/3,(C7[5]**4)/4,(C7[5]**5)/5,(C7[5]**6)/6,(C7[5]**7)/7],
                            [C7[6],(C7[6]**2)/2,(C7[6]**3)/3,(C7[6]**4)/4,(C7[6]**5)/5,(C7[6]**6)/6,(C7[6]**7)/7]])

            A7=np.dot(CQ7,np.linalg.inv(CP7))

            D7,T7= np.linalg.eig(A7)
            D7=np.array([[D7[0],0,0,0,0,0,0],[0,D7[1],0,0,0,0,0],[0,0,D7[2],0,0,0,0],[0,0,0,D7[3],0,0,0],[0,0,0,0,D7[4],0,0],
                         [0, 0, 0, 0, 0,D7[5], 0],[0,0,0,0,0,0,D7[6]]])
            D7=np.dot(np.eye(7,dtype=float),np.linalg.inv(D7))
            TI7=np.dot(np.linalg.inv(T7),np.eye(7,dtype=float))
            ValP7=[D7[0,0],D7[1,1],D7[2,2],D7[3,3],D7[4,4],D7[5,5],D7[6,6]]


            #计算结果与matlab有出入，或许因为计算精度不同
        T_7=np.array([[T7[0,0], T7[1,0], T7[2,0], T7[3,0], T7[4,0],T7[5,0], T7[6,0]],
                      [T7[0,1], T7[1,1], T7[2,1], T7[3,1], T7[4,1],T7[5,1], T7[6,1]],
                      [T7[0,2], T7[1,2], T7[2,2], T7[3,2], T7[4,2],T7[5,2], T7[6,2]],
                      [T7[0,3], T7[1,3], T7[2,3], T7[3,3], T7[4,3],T7[5,3], T7[6,3]],
                      [T7[0,4], T7[1,4], T7[2,4], T7[3,4], T7[4,4],T7[5,4], T7[6,4]],
                      [T7[0,5], T7[1,5], T7[2,5], T7[3,5], T7[4,5],T7[5,5], T7[6,5]],
                      [T7[0,6], T7[1,6], T7[2,6], T7[3,6], T7[4,6],T7[5,6], T7[6,6]]
                      ])

        TI_7=np.array([[TI7[0,0],TI7[1,0], TI7[2,0], TI7[3,0], TI7[4,0],TI7[5,0], TI7[6,0]],
                      [TI7[0,1], TI7[1,1], TI7[2,1], TI7[3,1], TI7[4,1],TI7[5,1], TI7[6,1]],
                      [TI7[0,2], TI7[1,2], TI7[2,2], TI7[3,2], TI7[4,2],TI7[5,2], TI7[6,2]],
                      [TI7[0,3], TI7[1,3], TI7[2,3], TI7[3,3], TI7[4,3],TI7[5,3], TI7[6,3]],
                      [TI7[0,4], TI7[1,4], TI7[2,4], TI7[3,4], TI7[4,4],TI7[5,4], TI7[6,4]],
                      [TI7[0,5], TI7[1,5], TI7[2,5], TI7[3,5], TI7[4,5],TI7[5,5], TI7[6,5]],
                      [TI7[0,6], TI7[1,6], TI7[2,6], TI7[3,6], TI7[4,6],TI7[5,6], TI7[6,6]]])


        return



# test = cltdy('sober',25,'DevOps')    #类的实例化，将参数传入类中，传入参数可以多但不可以少于类构造函数的参数(self参数除外，self是将实例化的变量名传入类)
# print("这是类实例化后的内存地址：%s"%test)
# test.printing_name()    #调用实例化后类中的方法
# test.name = 'moon'    #可以修改构造函数中参数的值
# test.printing_name()
# test.printing_pfsn()
# print(test.n)
# test.n = 2000    #修改类属性，只针对test实例化生效
#
# print(test.n,'\n====================')
#
# t2 = cltdy('jack',22,'student')    #实例化类对象，命名t2
# print(t2.n)
# t2.printing_age()



def test1():


    RealYN=True
    self=0
    radau.Coertv5(self,RealYN)
    print(T_5)




if __name__ == "__main__":

    test1()
