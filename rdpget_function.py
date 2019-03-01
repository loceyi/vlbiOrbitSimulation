# %RDPGET Get ODE OPTIONS parameters.
# %   VAL = RDPGET(OPTIONS,'NAME') extracts the value of the named property
# %   from integrator options structure OPTIONS, returning an empty matrix if
# %   the property value is not specified in OPTIONS.  [] is a valid OPTIONS
# %   argument.
# %
# %   VAL = RDPGET(OPTIONS,'NAME',DEFAULT) extracts the named property as
# %   above, but returns VAL = DEFAULT if the named property is not specified
# %   in OPTIONS. For example
# %
# %       val = rdpget(opts,'RelTol',1e-4);
# %
# %   returns val = 1e-3 if the RelTol property is not specified in opts.
# %
# %   See also RDPSET, RADAU,DOP45 and DOP853
# % ------------------------------------------------------------------------
import os

def rdpget(options,name,default,*flag):

    '''

    :param options: 输入必须是字典类型
    :param name: 需要提取value的key的名字
    :param default: 默认值，如果options中没有对应key的value，这给这个name一个值
    :param flag:
    :return:
    '''



    Fcn_Name='rdpget'

    nargin=3+len(flag)

    if nargin==4 and flag=='fast' :#快速模式，不进行这些错误判断


        o=getknownfield(options,name,default)

        return o

    else:
        pass

    if not isinstance(options,dict):

        print(Fcn_Name,':options input is not in the form of dictionary')

        os._exit(0)

    else:

        pass

    if len(options)==0:

        o=default

        return o

    else:

        pass

    Names = ['AbsTol', 'RelTol', 'InitialStep', 'MaxStep', 'MaxNbrStep',
             'Refine','OutputFcn', 'OutputSel','FacL', 'FacR','NormControl',
             'Safe','MassFcn', 'EventsFcn','StiffTest','Beta',
             'Complex',
             'NbrInd1', 'NbrInd2', 'NbrInd3',
             'JacFcn', 'JacRecompute',
             'Start_Newt', 'MaxNbrNewton',
             'NbrStg', 'MinNbrStg', 'MaxNbrStg',
             'Quot1', 'Quot2',
             'Vitu', 'Vitd',
             'hhou', 'hhod', 'Gustafsson']

    names=[string.lower() for string in Names]#all elements into lower case


















    return Julian_date


def getknownfield(s,f,d):
    #  GETKNOWNFIELD Get field f from struct s, or else yield defaultd .

    if f in s:

        v=s[f]
        #判断v是否是空列表，v可能是数，或者空列表
        if isinstance(v,list):

            if len(v)==0 :

                v=d

            else:

                pass



        else:

            pass

        return v


    else:

        pass








def test():
    s={'a':[],'b':2}
    f='a'
    d=0
    jd=getknownfield(s,f,d)
    print(jd)



if __name__ == "__main__":

    test()
