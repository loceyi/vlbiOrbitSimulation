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

    :param options: 输入必须是字典类型,而且如果options中的key没有给对应value时，则对应value位置要为空列表[]
    :param name: 需要提取value的key的名字
    :param default: 默认值，如果options中没有对应key的value，这给这个name一个值
    :param flag:如果有多个参数输入会自动存储为元组,即使只有一个输入也是存为元组
    :return:
    '''



    Fcn_Name='rdpget'

    nargin=3+len(flag)

    if nargin==4 and flag[0]=='fast' :#快速模式，不进行这些错误判断


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
    lowName=name.lower()

    #编写python中的strmatch
    j=[]
    count = 0
    for each_char in names:
        count += 1
        if lowName in each_char:

            j.append(count)

        else:

            pass



    if len(j)==0:


        print(Fcn_Name,'Invalid name input which does not exist in the known set parameters')

        os._exit(0)


    elif len(j)>1:

        #code of strmatch(exact) in matlab


        k = []
        count = 0
        for each_char in names:
            count += 1
            if lowName == each_char:

                k.append(count)

            else:

                pass

        if len(k)== 1:

            j=k


        else:
            #Pay attention to the difference with matlab: in python Names[0]is the first element,
            #but in matlab Names[1] is the first element,what contains in j is the order from 1 to n
            #so we need to  use j-1 to get the right position expression in Names
            #matches=Names[j[0]-1]


            print(Fcn_Name,':there are same properties names in Names ')

            os._exit(0)

    fieldnames_options=list(options.keys())#All the keys in options, and store it in fieldnames_options
                                           #in the form of list


    if Names[j[0]-1] in fieldnames_options:

        o= options[Names[j[0]-1]]

        if isinstance(o,list):

            if len(o)==0:

                o=default

            else:

                pass

        else:


            pass

    else:


        o=default



    return o


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

        v=d


    return v




def test1():
    s={'a':3,'b':2}
    f='a'
    d=0
    jd=getknownfield(s,f,d)
    print(jd)



if __name__ == "__main__":

    test1()






def test2():
    options={'RelTol':3,'AbsTol':2}
    name='AbsTol'
    default=0
    flag='fast'
    jd=rdpget(options, name, default, *flag)
    print(jd)



if __name__ == "__main__":

    test2()
