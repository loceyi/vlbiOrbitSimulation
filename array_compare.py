def intersection(nums1, nums2):
    """
            :type nums1: List[int]
            :type nums2: List[int]
            :rtype: List[int]
            """
    setNums1 = set(nums1)
    setNums2 = set(nums2)

    result = []
    for x in setNums2:
        if x in setNums1:
            result.append(x)

    return result


#  
#  
# 用set来把list的重复元素过滤掉，然后判断是否存在，把结果保存起来
# http: // www.waitingfy.com / archives / 3724
#
#  
#  
#
# ---------------------
# 作者：瓦力冫
# 来源：CSDN
# 原文：https: // blog.csdn.net / fox64194167 / article / details / 80466689
# 版权声明：本文为博主原创文章，转载请附上博文链接！