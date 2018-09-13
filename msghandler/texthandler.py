#--coding:gbk
from utils.sqlutils import getDB
def help():
    helptext = '输入6位区划代码，查询县级及以上单位数据。\n输入‘201803’、‘201806’格式的时期切换时期\n输入指标名称，查询全国数据。'
    return helptext

def singleindexquery(querytext):
    print(querytext)
    conn = getDB()
    cursor = conn.get_conn().cursor()
    retlst = []
    retstr = ""
    if querytext=='000000':
        print('Ok it`s all')
        sql = 'select d.value/unittimes,i.unitafterdivide,i.IndexName,i.indexid,d.period from datawarehouse d, indexdict i where d.tablekind=i.DataTable and d.period=i.period and d.DbfID=i.DbfID and d.qhdm="{qhdm}" and d.period="{Period}" and i.Indexname like "%{indexName}%"'.format(qhdm='000000000000',Period=201806,indexName=querytext)
    else:
        sql = 'select d.value,i.unitname,i.IndexName,i.indexid,d.period from datawarehouse d, indexdict i where d.tablekind=i.DataTable and d.period=i.period and d.DbfID=i.DbfID and d.qhdm="{qhdm}" and d.period="{Period}" and i.Indexname like "%{indexName}%"'.format(qhdm='000000000000',Period=201806,indexName=querytext)
    cursor.execute(sql)
    queryrst = cursor.fetchall()
    for res in queryrst:
        record = res[2]+' '+str(int(res[0]))+' '+res[1]
        retlst.append(record)
    for rec in retlst:
        retstr = retstr + rec +"\n"
    if queryrst !=():
        queryperiod = queryrst[0][4]
    if retstr != "":
        if queryperiod[4]=="0":
            retstr = queryperiod[0:4]+'年'+queryperiod[5]+'月'+'\n'+retstr
        else:
            retstr = queryperiod[0:4]+'年'+queryperiod[4:6]+'月'+'\n'+retstr
    if retstr=="":
        retstr="查找不到所要查询的指标，请使用其他关键词"
    return retstr

def querybyqhdm(qhdm,period):
    if len(qhdm)==6:
       queryqhdm=qhdm+'000000'
    conn = getDB()
    cursor = conn.get_conn().cursor()
    cursor.execute('select region_code,region_name from regioninfo where region_code="{qhdm}"'.format(qhdm=queryqhdm))
    qhinfo = cursor.fetchone()
    print(qhinfo)
    if  qhinfo == None:
        return '不存在此区划代码'
    if qhdm=='000000':
        sql = 'select i.indexname,d.value/i.unittimes,i.unitafterdivide from datawarehouse d,indexdict i where d.qhdm="{qhdm}" and d.MatchedIndex = i.indexID and d.year=i.year and d.tablekind=i.datatable and d.period="{period}"'.format(qhdm=queryqhdm,period=period)
    else:
        sql = 'select i.indexname,d.value,i.unitname from datawarehouse d,indexdict i where d.qhdm="{qhdm}" and d.MatchedIndex = i.indexID and d.year=i.year and d.tablekind=i.datatable and d.period="{period}"'.format(qhdm=queryqhdm,period=period)
    cursor.execute(sql)
    res = cursor.fetchall()
    retstr = str(qhinfo[1])+'  '+str(qhinfo[0][0:6])+'\n'+period[0:4]+'年'+period[4:6]+'月'+'\n\n'
    reslist = []
    for record in res:
        if int(record[1])!=0:
            res = record[0]+' '+str(int(round(record[1])))+' '+record[2]
            reslist.append(res)
    for index in reslist:
        retstr = retstr+ index+'\n'
    if len(retstr)<35:
        retstr = retstr+'无数据'
    return retstr

