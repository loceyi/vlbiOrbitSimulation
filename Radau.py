
import numpy as np
from inspect import isfunction
import os
from rdpget_function import rdpget
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
        RefineDef = [1]
        OutputFcnDef = []
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
        MinNbrStgDef = [3]  # 1 3 5 7
        MaxNbrStgDef = [7]  # 1 3 5 7
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

        Arg_dict={'In':self.nargin}

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



        if Arg_dict['In']>3:

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

        if Arg_dict['In']>3:


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
        MassFcn=Op_dict['MassFcn']
        EventsFcn=Op_dict['EventsFcn']
        OutputFcn=Op_dict['OutputFcn']
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
        JacFcn=Op_dict['JacFcn']
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


    def Coertv(self):
        print("我的职业：%s"%self.profession)


    def Coertv1(self):
        print("我的职业：%s"%self.profession)


    def Coertv3(self):
        print("我的职业：%s"%self.profession)


    def Coertv5(self):
        print("我的职业：%s"%self.profession)


    def Coertv7(self):
        print("我的职业：%s"%self.profession)

test = cltdy('sober',25,'DevOps')    #类的实例化，将参数传入类中，传入参数可以多但不可以少于类构造函数的参数(self参数除外，self是将实例化的变量名传入类)
print("这是类实例化后的内存地址：%s"%test)
test.printing_name()    #调用实例化后类中的方法
test.name = 'moon'    #可以修改构造函数中参数的值
test.printing_name()
test.printing_pfsn()
print(test.n)
test.n = 2000    #修改类属性，只针对test实例化生效

print(test.n,'\n====================')

t2 = cltdy('jack',22,'student')    #实例化类对象，命名t2
print(t2.n)
t2.printing_age()