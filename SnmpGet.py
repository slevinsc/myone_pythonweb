#!/usr/bin/env python
#encoding=utf-8


import sys,re,time,json
import thread,threading
sys.path.append('E:\\223\\osa')
from pysnmp.entity.rfc3413.oneliner import cmdgen
from ctrlpy.etc.config import snmp_handle_func
from pysnmp.proto.rfc1902 import ObjectName
from ctrlpy.lib.osaUtil import save_log

#oid=ObjectName('1.3.6.1.4.1.2021.11.9.0')
#print oid
def change_dict(snmp_get):
    '''
    把snmp获取来的数据转为字典
    '''
    snmp_dict={}
    for key in snmp_get:        #print f
        snmp_index=key[0][0][-1]
        snmp_values=str(key[0][1])
        snmp_change={snmp_index:snmp_values}
        snmp_dict.update(snmp_change)
    return snmp_dict

	
def memory_handle(agent,ip,key,port):
    total_oid=ObjectName('.1.3.6.1.4.1.2021.4.5.0')
    use_oid=ObjectName('.1.3.6.1.4.1.2021.4.6.0')
    run_mem_total=ger_snmp_get(agent,ip,key,port,total_oid)
    run_mem_use= ger_snmp_get(agent,ip,key,port,use_oid)
    return {'memory':{'used':str(run_mem_use[0][1]),'total':str(run_mem_total[0][1])}}
    	

	
def user_login(agent,ip,key,port):
    login_oid=ObjectName('.1.3.6.1.2.1.25.1.5.0')
    user_login =ger_snmp_get(agent,ip,key,port,login_oid)
    return {'user_login':str(user_login[0][1])}
	#return user_login
	
	
	#return "{'run_mem_use':%s}}"%(ger_snmp(agent,ip,key,port,oid))
def loadstat(agent,ip,key,port):
    load_one_oid=ObjectName('.1.3.6.1.4.1.2021.10.1.3.1')
    load_five_oid=ObjectName('.1.3.6.1.4.1.2021.10.1.3.2')
    load_fifteen_oid=ObjectName('.1.3.6.1.4.1.2021.10.1.3.3')
    load_one =ger_snmp_get(agent,ip,key,port,load_one_oid)
    load_five =ger_snmp_get(agent,ip,key,port,load_five_oid)
    load_fifteen =ger_snmp_get(agent,ip,key,port,load_fifteen_oid)
    return {'loadstat':{'fifteen':str(load_fifteen[0][1]),'five':str(load_five[0][1]),'one':str(load_one[0][1])}}
    

def process_num(agent,ip,key,port):
	process_oid=ObjectName('.1.3.6.1.2.1.25.1.6.0')
	process_num =ger_snmp_get(agent,ip,key,port,process_oid)
	return {'process_num':str(process_num[0][1])}
	

def constat(agent,ip,key,port):
	tcp_oid=ObjectName('1.3.6.1.2.1.6.13.1.2')
	udp_oid=ObjectName('1.3.6.1.2.1.7.5.1.1')
	constat_tcp =ger_snmp_next(agent,ip,key,port,tcp_oid)
	constat_udp =ger_snmp_next(agent,ip,key,port,udp_oid)
	count_tcp=0
	count_udp=0
	for row in constat_tcp:
		count_tcp+=1
	for row in constat_udp:
		count_udp+=1
	return {'constat':{'udp':str(count_udp),'tcp':str(count_tcp),'all':str(int(count_tcp)+int(count_udp))}}
	


def disk_Handle_sau(agent,ip,key,port):
    '''
    获取每个逻辑分区的计算单位
    '''
    sau_oid=ObjectName('.1.3.6.1.2.1.25.2.3.1.4')
    sau_get=ger_snmp_next(agent,ip,key,port,sau_oid)
    sau=change_dict(sau_get)
    return sau

def disk_Handle_description(agent,ip,key,port):
    '''
    获取正在使用的逻辑分区
    '''
    description={}
    description_oid=ObjectName('.1.3.6.1.2.1.25.2.3.1.3')
    description_get=ger_snmp_next(agent,ip,key,port,description_oid)
    for key in description_get:
        description_key=key[0][0][-1]
        description_value=str(key[0][1])
        if re.match('/',description_value):
            #print re.match('/',description_value).group()
            #print   description_value       
            y={description_key:description_value}
            description.update(y)
    return description
           
def disk_stat(agent,ip,key,port):
    total_total={}
    description= disk_Handle_description(agent,ip,key,port)
    sau= disk_Handle_sau(agent,ip,key,port)
    use_oid=ObjectName('.1.3.6.1.2.1.25.2.3.1.6')
    total_oid=ObjectName('.1.3.6.1.2.1.25.2.3.1.5')
    use_get=ger_snmp_next(agent,ip,key,port,use_oid)
    use=change_dict(use_get)
    total_get=ger_snmp_next(agent,ip,key,port,total_oid)
    total=change_dict(total_get)
    for id in description.keys():
        z={str(description[id]):{'total':str(int(total[id])*int(sau[id])/1048576),'use':str(int(use[id])*int(sau[id])/1048576)}}        
        total_total.update(z)
    return {'disk':total_total}

    
def system_info(agent,ip,key,port):
    '''
    获取系统的位数，看是64位还是32位
    '''
    system_oid=ObjectName('1.3.6.1.2.1.1.1')
    system_get=ger_snmp_next(agent,ip,key,port,system_oid)
    system_name = system_get[0][0][1]
    #print system_name
    system_bit= str(system_name).split()[11]
    return system_bit
    #print  system_next
       
def network_eth(agent,ip,key,port):
    '''
    获取正在使用的网卡
    '''
    active_eth={}
    statu_oid=ObjectName('.1.3.6.1.2.1.2.2.1.8')
    statu_get=ger_snmp_next(agent,ip,key,port,statu_oid)
    status_vals=change_dict(statu_get)
    Description_oid=ObjectName('.1.3.6.1.2.1.2.2.1.2')
    Description_get=ger_snmp_next(agent,ip,key,port,Description_oid)
    Description_vals=change_dict(Description_get)
    for key in status_vals:
        if status_vals[key]!='2' and not re.match('lo',Description_vals[key]):
            result_eth={key:Description_vals[key]}
            active_eth.update(result_eth)
    return active_eth
            
def diffrent_value(agent,ip,key,port,in_flow_oid,out_flow_oid):
    '''
        计算一分钟内网卡的流量
    '''
    network_stat={}
    in_flow_one=ger_snmp_next(agent,ip,key,port,in_flow_oid)
    out_flow_one=ger_snmp_next(agent,ip,key,port,out_flow_oid)
    time.sleep(60)
    in_flow_two=ger_snmp_next(agent,ip,key,port,in_flow_oid)
    out_flow_two=ger_snmp_next(agent,ip,key,port,out_flow_oid)
    in_flow_one_dict=change_dict(in_flow_one)
    in_flow_two_dict=change_dict(in_flow_two)        
    out_flow_one_dict=change_dict(out_flow_one)
    out_flow_two_dict=change_dict(out_flow_two)
    active_eth=network_eth(agent,ip,key,port)
    for k in active_eth:
        in_flow_value=int(in_flow_two_dict[k])-int(in_flow_one_dict[k])
        out_flow_value=int(out_flow_two_dict[k])-int(out_flow_one_dict[k])
        flow_total={active_eth[k]:{'inbond':float(in_flow_value/1024),'outbond':float(out_flow_value/1024)}}
        network_stat.update(flow_total)
    return network_stat         
     
def network_stat(agent,ip,key,port):
    
    system_bit=system_info(agent,ip,key,port)
    #print system_bit
    if system_bit=='x86_64':
        in_flow_oid=ObjectName('.1.3.6.1.2.1.31.1.1.1.6')
        out_flow_oid=ObjectName('.1.3.6.1.2.1.31.1.1.1.10')
        network_stat=diffrent_value(agent,ip,key,port,in_flow_oid,out_flow_oid)       
        return {'network':network_stat}        
    else:
        in_flow_oid=ObjectName('.1.3.6.1.2.1.2.2.1.10')
        out_flow_oid=ObjectName('.1.3.6.1.2.1.2.2.1.16')
        network_stat=diffrent_value(agent,ip,key,port,in_flow_oid,out_flow_oid)       
        return {'network':network_stat}

def cpu_user_get(agent,ip,key,port):
    cpu_user_oid=ObjectName('.1.3.6.1.4.1.2021.11.9.0')
    cpu_get=ger_snmp_get(agent,ip,key,port,cpu_user_oid)
    return {'cpu_user':str(cpu_get[0][1])}

def disk_dev(agent,ip,key,port):
    active_disk={}
    dev_oid=ObjectName('1.3.6.1.4.1.2021.13.15.1.1.2')
    dev_io_get=ger_snmp_next(agent,ip,key,port,dev_oid)
    dev_get=change_dict(dev_io_get)
    for key in dev_get:
        if re.match('[s|h]d[a-z]$',dev_get[key]):
            dev_dict={key:dev_get[key]}
            active_disk.update(dev_dict)
    return active_disk




def disk_io_get(agent,ip,key,port):
    disk_io_total={}
    read_oid='.1.3.6.1.4.1.2021.13.15.1.1.5.'
    write_oid='.1.3.6.1.4.1.2021.13.15.1.1.6.'
    active_disk=disk_dev(agent,ip,key,port)
    print active_disk
    for key_index in active_disk:                
        read_oid_get=ObjectName(str(read_oid)+str(key_index))
        write_oid_get=ObjectName(str(write_oid)+str(key_index))
        #print read_oid_get
        read_io_get=ger_snmp_get(agent,ip,key,port,read_oid_get)
        write_io_get=ger_snmp_get(agent,ip,key,port,write_oid_get)
        #print read_io_get
        if read_io_get[0][1] == 0 or write_io_get[0][1] == 0:
            continue
        
        disk_io = {active_disk[key_index]:{'read_io':str(read_io_get[0][1]),'write_io':str(write_io_get[0][1])}}
        disk_io_total.update(disk_io)
    return disk_io_total
        #print write_io_get
    

def ger_snmp_get(agent,ip,key,port,oid):
    if port is None:
        port = 161
    cg=cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cg.getCmd(
        cmdgen.CommunityData(agent, key,1),
        cmdgen.UdpTransportTarget((ip, port)),
        #cmdgen.UdpTransportTarget((ip, port),timeout=15,retries=3)
        oid
    )
    if varBindTable:
        return varBindTable
    else:
        save_log('ERROR', ip+errorIndication)        
        sys.exit(0)

def ger_snmp_next(agent,ip,key,port,oid):
    if port is None:
        port = 161
    
    cg=cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cg.nextCmd(
        cmdgen.CommunityData(agent, key,1),
        cmdgen.UdpTransportTarget((ip, port)),
        #cmdgen.UdpTransportTarget((ip, port),timeout=15,retries=3)
        oid
    )
    if varBindTable:
        return varBindTable
    else:
        save_log('ERROR', ip+errorIndication)
        sys.exit(0)	

def handle_func(agent,ip,key,port):
    info ={}
    for x in snmp_handle_func:
        func=x+'(agent,ip,key,port)'
        y=eval(func)
        info.update(y)
    return info


def DicttoJson(agent,ip,key,port):
    dct=handle_func(agent,ip,key,port)
    #print dct
    encodedjson = json.dumps(dct)       
    return encodedjson

        


