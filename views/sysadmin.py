# (C) Copyright 2021 Hewlett Packard Enterprise Development LP.

from flask import current_app, Blueprint, json, request
from werkzeug.datastructures import ImmutableMultiDict
import time
sysadmin = Blueprint('sysadmin', __name__)

from datetime import datetime, time
from flask import render_template

import classes.classes as classes

@sysadmin.route("/useradmin",methods=['GET','POST'])
def useradmin():
    authOK=classes.checkAuth("sysuseraccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        # Obtain the relevant information from the database
        if "selectauthsource" in formresult:
            if formresult['selectauthsource']=="ldap":
                result=classes.userldapAction(formresult)
            else:
                result=classes.userdbAction(formresult)
        else:
            result=classes.userdbAction(formresult)
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            return render_template("useradmin.html",result=result['userresult'],roleresult=result['roleresult'],formresult=formresult,totalentries=int(result['totalentries']),pageoffset=int(result['pageoffset']),entryperpage=int(result['entryperpage']), authOK=authOK, sysvars=sysvars)
        else:
            return render_template("noaccess.html", authOK=authOK, sysvars=sysvars)
    else:
        return render_template("login.html")

@sysadmin.route("/userroles",methods=['GET','POST'])
def userroles():
    authOK=classes.checkAuth("sysroleaccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        dictform=formresult.to_dict(flat=True)
        # Obtain the relevant information from the database
        result=classes.roledbAction(dictform)
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            return render_template("roleadmin.html",result=result,formresult=formresult, totalentries=int(result['totalentries']),pageoffset=int(result['pageoffset']),entryperpage=int(result['entryperpage']), authOK=authOK, sysvars=sysvars)
        else:
            return render_template("noaccess.html",authOK=authOK, sysvars=sysvars)
    else:
        return render_template("login.html")


@sysadmin.route("/editrole",methods=['GET','POST'])
def editrole():
    formresult=request.form
    sysvars=classes.globalvars()
    queryStr="select * from sysrole where id='{}'".format(formresult['id'])
    # Obtain the relevant user role information from the database
    result=classes.sqlQuery(queryStr,"selectone")
    return json.dumps(result)


@sysadmin.route("/deviceattributes",methods=['GET','POST'])
def deviceattributes():
    authOK=classes.checkAuth("deviceattributesaccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        dictform=formresult.to_dict(flat=True)
        # Obtain the relevant information from the database
        result=classes.deviceattributesdbAction(dictform)
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            return render_template("deviceattributes.html",result=result,formresult=formresult, totalentries=int(result['totalentries']),pageoffset=int(result['pageoffset']),entryperpage=int(result['entryperpage']), authOK=authOK, sysvars=sysvars)
        else:
            return render_template("noaccess.html",authOK=authOK, sysvars=sysvars)
    else:
        return render_template("login.html")


@sysadmin.route("/editdeviceattribute",methods=['GET','POST'])
def editdeviceattribute():
    formresult=request.form
    sysvars=classes.globalvars()
    queryStr="select * from deviceattributes where id='{}'".format(formresult['id'])
    # Obtain the relevant device attribute information from the database
    result=classes.sqlQuery(queryStr,"selectone")
    return json.dumps(result)


@sysadmin.route("/sysconf",methods=['GET','POST'])
def sysconf():
    authOK=classes.checkAuth("sysadminaccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        try:
            if formresult['action']=="Submit changes":
                classes.submitsysConf(formresult)
                sysvars=classes.globalvars()
        except:
            pass
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            timezoneregion=["Africa","America","Asia","Europe","Indian","Pacific","Antarctica"]
            return render_template("sysconf.html",authOK=authOK, sysvars=sysvars, timezoneregion=timezoneregion)
        else:
            return render_template("noaccess.html",authOK=authOK, sysvars=sysvars)
    else:
        return render_template("login.html")


@sysadmin.route("/sysldap",methods=['GET','POST'])
def sysldap():
    authOK=classes.checkAuth("sysadminaccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        try:
            if formresult['action']=="Submit changes":
                classes.submitIntegration(formresult)             
        except:
            pass
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            ldapvars=classes.obtainVars('sysldap')
            if isinstance(ldapvars, str):
                ldapvars=json.loads(ldapvars)
            sysvars=classes.globalvars()
            return render_template("sysldap.html",authOK=authOK, ldapvars=ldapvars, sysvars=sysvars)
        else:
            return render_template("noaccess.html",authOK=authOK)
    else:
        return render_template("login.html")


@sysadmin.route("/sysipam",methods=['GET','POST'])
def sysipam():
    authOK=classes.checkAuth("sysadminaccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        try:
            if formresult['action']=="Submit changes":
                classes.submitIntegration(formresult)             
        except:
            pass
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            ipamvars=classes.obtainVars('sysipam')
            if isinstance(ipamvars, str):
                ipamvars=json.loads(ipamvars)
            sysvars=classes.globalvars()
            return render_template("sysipam.html",authOK=authOK, ipamvars=ipamvars, sysvars=sysvars)
        else:
            return render_template("noaccess.html",authOK=authOK)
    else:
        return render_template("login.html")


@sysadmin.route("/sysarubacentral",methods=['GET','POST'])
def sysarubacentral():
    authOK=classes.checkAuth("sysadminaccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        try:
            if formresult['action']=="Submit changes":
                classes.submitIntegration(formresult)             
        except:
            pass
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            arubacentralvars=classes.obtainVars('sysarubacentral')
            if isinstance(arubacentralvars, str):
                arubacentralvars=json.loads(arubacentralvars)
            sysvars=classes.globalvars()
            return render_template("sysarubacentral.html",authOK=authOK, arubacentralvars=arubacentralvars, sysvars=sysvars)
        else:
            return render_template("noaccess.html",authOK=authOK)
    else:
        return render_template("login.html")


@sysadmin.route("/sysafc",methods=['GET','POST'])
def sysafc():
    authOK=classes.checkAuth("sysadminaccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        try:
            if formresult['action']=="Submit changes":
                classes.submitIntegration(formresult)             
        except:
            pass
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            afcvars=classes.obtainVars('sysafc')
            if isinstance(afcvars, str):
                afcvars=json.loads(afcvars)
            sysvars=classes.globalvars()
            return render_template("sysafc.html",authOK=authOK, afcvars=afcvars, sysvars=sysvars)
        else:
            return render_template("noaccess.html",authOK=authOK)
    else:
        return render_template("login.html")


@sysadmin.route("/syspsm",methods=['GET','POST'])
def syspsm():
    authOK=classes.checkAuth("sysadminaccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        try:
            if formresult['action']=="Submit changes":
                classes.submitIntegration(formresult)             
        except:
            pass
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            psmvars=classes.obtainVars('syspsm')
            if isinstance(psmvars, str):
                psmvars=json.loads(psmvars)
            sysvars=classes.globalvars()
            return render_template("syspsm.html",authOK=authOK, psmvars=psmvars, sysvars=sysvars)
        else:
            return render_template("noaccess.html",authOK=authOK)
    else:
        return render_template("login.html")


@sysadmin.route("/sysmon",methods=['GET','POST'])
def sysmon():
    authOK=classes.checkAuth("servicesstatusaccess","submenu")
    if authOK!=0:
        sysvars=classes.globalvars()
        formresult=request.form
        if formresult:
            classes.processAction(formresult['name'],formresult['action'])
        if authOK['hasaccess']==True:
            authOK['hasaccess']="true"
            return render_template("sysmon.html",authOK=authOK, sysvars=sysvars)
        else:
            return render_template("noaccess.html",authOK=authOK, sysvars=sysvars)
    else:
        return render_template("login.html")

@sysadmin.route("/factory",methods=['GET','POST'])
def factory():
    formresult=request.form
    if formresult:
        classes.factoryDefault(formresult)    
        return render_template("login.html")
    else:
        return render_template("factorydefault.html")

@sysadmin.route("/monitorProcess",methods=['GET','POST'])
def monitorProcess():
    # Check whether the process is running and return this information in the rendered page
    sysvars=classes.globalvars()
    processInfo=classes.checkProcess(request.args.get('name'))
    return render_template("monitorprocess.html", sysvars=sysvars, name=request.args.get('name'), status=processInfo['status'], cpu=processInfo['cpu'], memory=processInfo['memory'])

@sysadmin.route("/getsysTime",methods=['GET','POST'])
def getsysTime():
    # Return system time to calling station
    sysTime=classes.sysTime()
    return json.dumps(sysTime)


@sysadmin.route("/clearprocessLog",methods=['GET','POST'])
def clearprocessLog():
    formresult=request.form
    with open("/var/www/html/log/{}.log".format(formresult['processName']), 'w') as logFile:
        # Write the timestamp
        timestamp=str(int(datetime.now().timestamp()))
        logFile.write("---"+timestamp+"---\n")
    logFile.close()
    return "{} Log is cleared".format(formresult['processName'])

@sysadmin.route("/downloadLog",methods=['GET','POST'])
def downloadLog():
    formresult=request.form
    logFile=open("/var/www/html/log/{}.log".format(formresult['processName'],"r"))
    logContent=logFile.read()
    logFile.close()
    return json.dumps([formresult['processName'],logContent])


@sysadmin.route("/testldap",methods=['GET','POST'])
def testldap():
    formresult=request.form
    result=classes.checkldap(formresult['ldapuser'], formresult['ldappassword'],formresult['ldapsource'], formresult['basedn'],"testldap")
    return json.dumps(result)


@sysadmin.route("/ipamStatus",methods=['GET','POST'])
def ipamStatus():
    # Check whether IPAM is online
    formresult=request.form
    if formresult['ipamsystem']=="PHPIPAM":
        result=classes.checkPhpipam(formresult)
    elif formresult['ipamsystem']=="Infoblox":
        result=classes.checkInfoblox(formresult)
    return result

@sysadmin.route("/afcStatus",methods=['GET','POST'])
def afcStatus():
    # Check whether AFC is online and reachable
    formresult=request.form
    afcvars=classes.obtainVars('sysafc')
    if isinstance(afcvars, str):
        afcvars=json.loads(afcvars)
    afcInfo=formresult.to_dict(flat=True)
    result=classes.checkAFC(afcvars, afcInfo['afcipaddress'], afcInfo['afcuser'], afcInfo['afcpassword'], afcInfo['afctoken'])
    return result


@sysadmin.route("/psmStatus",methods=['GET','POST'])
def psmStatus():
    # Check whether PSM is online and reachable
    formresult=request.form
    psmvars=classes.obtainVars('syspsm')
    if isinstance(psmvars, str):
        psmvars=json.loads(psmvars)
    psmInfo=formresult.to_dict(flat=True)
    result=classes.checkPSM(psmvars, psmInfo['psmipaddress'], psmInfo['psmuser'], psmInfo['psmpassword'], psmInfo['psmtoken'])
    return result


@sysadmin.route("/getuserinfo",methods=['GET','POST'])
def getuserinfo():
    formresult=request.form
    sysvars=classes.globalvars()
    queryStr="select * from sysuser where id='{}'".format(formresult['userid'])
    userinfo=classes.sqlQuery(queryStr,"selectone")
    userinfo['password']=classes.decryptPassword(sysvars['secret_key'], userinfo['password'])
    return json.dumps(userinfo)