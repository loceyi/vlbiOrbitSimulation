
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
        AbsTolDef = 1e-6 # General parameters
        RelTolDef = 1e-3
        InitialStepDef = 1e-2
        MaxStepDef = self.tspan[-1] - self.tspan(0)
        MaxNbrStepDef = float('inf')
        MassFcnDef = []
        EventsFcnDef = []
        RefineDef = 1
        OutputFcnDef = []
        OutputSelDef = np.linspace(1,Ny,num=Ny,endpoint=True,retstep=False,dtype=float)
        ComplexDef = False
        NbrInd1Def = 0
        NbrInd2Def = 0
        NbrInd3Def = 0
        JacFcnDef = []; # Implicit solver parameters 空列表
        JacRecomputeDef = 1e-3
        Start_NewtDef = False
        MaxNbrNewtonDef = 7
        NbrStgDef = 3
        MinNbrStgDef = 3# 1 3 5 7
        MaxNbrStgDef = 7 # 1 3 5 7
        SafeDef = 0.9
        Quot1Def = 1
        Quot2Def = 1.2
        FacLDef = 0.2
        FacRDef = 8.0
        VituDef = 0.002
        VitdDef = 0.8
        hhouDef = 1.2
        hhodDef = 0.8
        GustafssonDef = True

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

        for n in range(1,OpNames.shape[0]+1):

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

                print(Solver_Name, ': WWrong input "MaxStep" must be a number')

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
                    print(Solver_Name, ': WWrong input "Refine"" must be a number')

                    os._exit(0)




        ##-------------------OutPutFcn

        #列表中可以存函数地址

        if len(Op_dict['OutputFcn'])!=0:

            for data in Op_dict['OutputFcn']:

                if not isfunction(data):

                    print(Solver_Name, ': OutputFcn must be valid functions')

                    os._exit(0)






























































































    def radausolver(self):
        print("我的年龄：%s"%self.age)


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