#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from subprocess import call
def empezar():
	iniciar()
	arrancar()
	gluster()
	servidores()
	lb()
def iniciar():
	os.system("sudo vnx -f pfinal.xml --create")
def apagar():
	os.system("sudo vnx -f pfinal.xml --destroy")
def arrancar():
#CONFIGURACIÓN BASE DE DATOS
	os.system("sudo lxc-attach --clear-env -n bbdd -- apt update")
	os.system("sudo lxc-attach --clear-env -n bbdd -- apt -y install postgresql")
	os.system("sudo lxc-attach --clear-env -n bbdd -- bash -c \"echo 'listen_addresses='\\\"'10.1.4.31'\\\"'' >> /etc/postgresql/9.6/main/postgresql.conf \"")
	os.system("sudo lxc-attach --clear-env -n bbdd -- bash -c 'echo \"host all all 10.1.4.0/24 trust\" >> /etc/postgresql/9.6/main/pg_hba.conf'")
	os.system("sudo lxc-attach --clear-env -n bbdd -- bash -c \"echo 'CREATE USER crm with PASSWORD '\\\"'xxxx'\\\"';' | sudo -u postgres psql \" ")
	os.system("sudo lxc-attach --clear-env -n bbdd -- bash -c 'echo \"CREATE DATABASE crm;\" | sudo -u postgres psql'")
	os.system("sudo lxc-attach --clear-env -n bbdd -- bash -c 'echo \"GRANT ALL PRIVILEGES ON DATABASE crm to crm;\" | sudo -u postgres psql'")
	os.system("sudo lxc-attach --clear-env -n bbdd -- systemctl restart postgresql")
	
def servidores():
#CONFIGURACION DE SERVIDORES

	#PARA S1
	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
	os.system("sudo lxc-attach --clear-env -n s1 -- apt-get update")
	os.system("sudo lxc-attach --clear-env -n s1 -- bash -c 'curl -sL https://deb.nodesource.com/setup_9.x | bash -'")
	os.system("sudo lxc-attach --clear-env -n s1 -- apt-get install -y nodejs")
	os.system("sudo lxc-attach --clear-env -n s1 -- apt-get update")
	print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
	os.system("sudo lxc-attach --clear-env -n s1 -- git clone https://github.com/CORE-UPM/CRM_2017.git")
	os.system("sudo lxc-attach --clear-env -n s1 -- bash -c \""+"cd ./CRM_2017; "+"npm install; "+"npm install forever; "+" export DATABASE_URL=postgres://crm:xxxx@10.1.4.31:5432/crm; " + "mkdir public/uploads; " + "sudo mount -t glusterfs 10.1.4.21:/nas public/uploads; "+"npm run-script migrate_local; "+"npm run-script seed_local; "+"./node_modules/forever/bin/forever start ./bin/www" +"\"")
	
	#PARA S2
	print("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
	os.system("sudo lxc-attach --clear-env -n s2 -- apt-get update")
	os.system("sudo lxc-attach --clear-env -n s2 -- bash -c 'curl -sL https://deb.nodesource.com/setup_9.x | bash -'")
	os.system("sudo lxc-attach --clear-env -n s2 -- apt-get install -y nodejs")
	os.system("sudo lxc-attach --clear-env -n s2 -- apt-get update")
	print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
	os.system("sudo lxc-attach --clear-env -n s2 -- git clone https://github.com/CORE-UPM/CRM_2017.git")
	os.system("sudo lxc-attach --clear-env -n s2 -- bash -c \""+"cd ./CRM_2017; "+"npm install; "+"npm install forever; "+" export DATABASE_URL=postgres://crm:xxxx@10.1.4.31:5432/crm; "+ "mkdir public/uploads; " + "sudo mount -t glusterfs 10.1.4.21:/nas public/uploads; "+"./node_modules/forever/bin/forever start ./bin/www" +"\"")
	
	#PARA S3
	print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
	os.system("sudo lxc-attach --clear-env -n s3 -- apt-get update")
	os.system("sudo lxc-attach --clear-env -n s3 -- bash -c 'curl -sL https://deb.nodesource.com/setup_9.x | bash -'")
	os.system("sudo lxc-attach --clear-env -n s3 -- apt-get install -y nodejs")
	os.system("sudo lxc-attach --clear-env -n s3 -- apt-get update")
	print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
	os.system("sudo lxc-attach --clear-env -n s3 -- git clone https://github.com/CORE-UPM/CRM_2017.git")
	os.system("sudo lxc-attach --clear-env -n s3 -- bash -c \""+"cd ./CRM_2017; "+"npm install; "+"npm install forever; "+" export DATABASE_URL=postgres://crm:xxxx@10.1.4.31:5432/crm; "+ "mkdir public/uploads; " + "sudo mount -t glusterfs 10.1.4.21:/nas public/uploads; "+"./node_modules/forever/bin/forever start ./bin/www" +"\"")

def gluster():
#CONFIGURACION DEL GLUSTER

	#os.system("sudo lxc-attach --clear-env -n nas1 -- mkdir /nas")
	#os.system("sudo lxc-attach --clear-env -n nas2 -- mkdir /nas")
	#os.system("sudo lxc-attach --clear-env -n nas3 -- mkdir /nas")

	os.system("sudo lxc-attach -n nas1 -- gluster peer probe 10.1.4.22")
	os.system("sudo lxc-attach -n nas1 -- gluster peer probe 10.1.4.23")

	#hacemos replicas de cada uno
	os.system("sudo lxc-attach -n nas1 -- gluster volume create nas replica 3 10.1.4.21:/nas 10.1.4.22:/nas 10.1.4.23:/nas force")
	#arrancar lo anterior
	os.system("sudo lxc-attach -n nas1 -- gluster volume start nas")
	#montarlo hacia los servidores 1 2 y 3

def lb():
 #CONFIGURACION DEL LB
 	os.system("sudo cp scriptlb.py /var/lib/lxc/lb/rootfs/etc")
 	os.system("sudo lxc-attach --clear-env -n lb -- bash -c 'cd /etc; chmod +x scriptlb.py; python ./scriptlb.py;'")

def fw():
	os.system("sudo cp fw.fw /var/lib/lxc/fw/rootfs/etc")
	os.system("sudo lxc-attach --clear-env -n fw -- bash -c 'cd /etc; chmod +x fw.fw; ./fw.fw;'")

accion = sys.argv[1]
if accion == 'arrancar':
	arrancar()
if accion == 'servidores':
	servidores()
if accion == 'gluster':
	gluster()
if accion == 'lb':
	lb()
if accion == 'iniciar':
	iniciar()
if accion == 'apagar':
	apagar()
if accion == 'empezar':
	empezar()
if accion == 'firewall':
	fw()