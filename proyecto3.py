import requests
import json
import dateutil.parser
from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession
from pyspark import SQLContext
#url = "http://api.equipo1.tech/get?access_key=9d1f065a6a9816f9dd7667b0c9b26bab"
def sensores(fecha1,fecha2):
        fechai = dateutil.parser.parse(fecha1)
        fechal = dateutil.parser.parse(fecha2)
        url = "http://165.227.125.50:8001/get"
        response = requests.get(url)
        print(response)
        data= response.text
        #print(data)
        general=0
        parsed = json.loads(data)
        #print(parsed)
        parsed2 = json.loads(parsed)
        #print(type(parsed2))
        parsed3="["
        for p in parsed2:
                pf = dateutil.parser.parse(p["fecha"])
                if pf >= fechai and pf <= fechal:
                        parsed3+=(json.dumps(p)+",")
                        #print(parsed3,type(parsed3))
                #print(p["fecha"])
        p4 = len(parsed3)
        parsed3 = parsed3[:p4-1]
        parsed3+="]"
        parsed4 = json.loads(parsed3)
        #print(type(parsed4))
        pars=parsed3.split(",")
        pars2=parsed3.split("}")
        #print(pars)
        #print("hola",type(parsed))
        rdd= sc.parallelize(pars)
        rddd=sc.parallelize(pars2)
        #print("RDD")
        #print(rdd)
        rddCollect = rdd.collect()
        #print("collect")
        #print(rddCollect)

        #-------------------Ultrasonico-------------------------------------
        u_filter= rdd.filter(lambda x: "Ultrasonico" in x)
        #print(u_filter)
        ul_filtered = u_filter.collect()
        #print(ul_filtered)
        ul_filtered = sc.parallelize(ul_filtered)
        #print(ul_filtered)
        nul= ul_filtered.count()
        general=general+nul




        uu_filter= rddd.filter(lambda x: "Ultrasonico" in x)
        uu_filtered = uu_filter.collect()
        uufil=[]
        estados=[]
        for u in uu_filtered:
                uufil.append(u.split(","))

        #print("Ultrasonicos")
        #print(uufil)

        rd3= sc.parallelize(uufil)
        l=len(uufil)
        #print(l)
        i=0
        j=0
        for i in range(l):
                for j in range(4):
                        elemento=uufil[i][j]
                        #print(elemento,"elemento")
                        #estado=elemento[2:3]
                        filtro=elemento[0:23]
                        #print(filtro,"filtro")
                        estado=filtro[2:7]
                        #print(estado,"estado")
                        #print(estado)
                        if estado=="estad":
                                valor=elemento[12:18]
                                #print(valor,"valor")
                                #print(valor)
                                estados.append(valor)

        #-------MODA-------------------------------
        def moda(estados):
                if not estados:
                        return False
                repeticiones = 0
                moda = []

                for i in estados:
                        n = estados.count(i)
                        if n > repeticiones:
                                repeticiones = n

                for i in estados:
                        n = estados.count(i) # Devuelve el número de veces que x aparece enla lista.
                        if n == repeticiones and i not in moda:
                                moda.append(i)

                if len(moda) != len(estados):
                        pass
                #print("a ver si funciona")
                moda=moda[0]
                modaultra=moda.strip('"')
                #modaultra=moda
                return modaultra

        modaultra=moda(estados)

        #-----------------------Infrarrojo---------------------------------------
        i_filter= rdd.filter(lambda x: 'I' in x)
        in_filtered = i_filter.collect()
        in_filtered = sc.parallelize(in_filtered)
        nin= in_filtered.count()
        general=general+nin

        iu_filter= rddd.filter(lambda x: "Infrarrojo" in x)
        iu_filtered = iu_filter.collect()
        #print(iu_filtered)
        iufil=[]
        for iu in iu_filtered:
                iufil.append(iu.split(","))
        #print("iufil")
        #print(iufil)
        rd2= sc.parallelize(iufil)
        #print(rd2)
        iu_filtere= rd2.filter(lambda x: ' "estado": "1"' in x)
        #print(iu_filtere)
        iu_filtered = iu_filtere.collect()
        #print(iu_filtered)
        iu_filtered = sc.parallelize(iu_filtered)
        niu= iu_filtered.count()

        #---Apagados
        rd3= sc.parallelize(iufil)
        iu_filtere= rd3.filter(lambda x: ' "estado": "0"' in x)
        iu_filtered= iu_filtere.collect()
        iu_filtered= sc.parallelize(iu_filtered)
        nic= iu_filtered.count()

        #---------------------Temperatura-------------------------------
        """
        t_filter= rdd.filter(lambda x: 'p' in x)
        tem_filtered = t_filter.collect()
        tem_filtered = sc.parallelize(tem_filtered)
        ntem= tem_filtered.count()
        general=general+ntem
        """
        #Filtro
        temperatura_filter= rddd.filter(lambda x: "Temperatura" in x)
        tem_filtered = temperatura_filter.collect()
        temp_filtered= sc.parallelize(tem_filtered)
        ntem= temp_filtered.count()
        general=general+ntem


        #Estados
        tempfil=[]
        estados=[]
        for t in tem_filtered:
                tempfil.append(t.split(","))


        #print(tempfil)

        rd3= sc.parallelize(tempfil)
        l=len(tempfil)
        i=0
        j=0
        for i in range(l):
                for j in range(4):
                        elemento=tempfil[i][j]
                        #estado=elemento[2:3]
                        filtro=elemento[0:23]
                        #print(filtro)
                        estado=filtro[2:7]
                        #print(estado)
                        #print(estado)
                        if estado=="estad":
                                valor=elemento[12:16]
                                #print(valor)
                                #print(valor)
                                estados.append(valor)

        #print(estados)
        modatemp=moda(estados)




        #-------------Movimiento-------------------------------
        #---Encendidos
        m_filter= rdd.filter(lambda x: 'M' in x)
        mov_filtered = m_filter.collect()
        mov_filtered = sc.parallelize(mov_filtered)
        nmov= mov_filtered.count()
        general=general+nmov


        mu_filter= rddd.filter(lambda x: "Movimiento" in x)
        mu_filtered = mu_filter.collect()
        mufil=[]
        for mu in mu_filtered:
                mufil.append(mu.split(","))
        #print(mufil)
        rd2= sc.parallelize(mufil)
        #print(rd2)
        mu_filtere= rd2.filter(lambda x: ' "estado": "1"' in x)
        #print(mu_filtere)
        mu_filtered = mu_filtere.collect()
        #print(mu_filtered)
        mu_filtered = sc.parallelize(mu_filtered)
        nmu= mu_filtered.count()

        #---Apagados
        rd3= sc.parallelize(mufil)
        mu_filtere= rd3.filter(lambda x: ' "estado": "0"' in x)
        mu_filtered= mu_filtere.collect()
        mu_filtered= sc.parallelize(mu_filtered)
        nmc= mu_filtered.count()

        #-----------------------Humedad-----------------

        """h_filter= rdd.filter(lambda x: 'H' in x)
        hum_filtered = h_filter.collect()
        hum_filtered = sc.parallelize(hum_filtered)
        nhum= hum_filtered.count()
        general=general+nhum
        """


        #Filtro
        humedad_filter= rddd.filter(lambda x: "Humedad" in x)
        hum_filtered = humedad_filter.collect()
        humed_filtered= sc.parallelize(hum_filtered)
        nhum= humed_filtered.count()
        general=general+nhum



        #Estados
        humedfil=[]
        estados=[]
        for h in hum_filtered:
                humedfil.append(h.split(","))

        rd3= sc.parallelize(humedfil)
        l=len(humedfil)
        i=0
        j=0
        for i in range(l):
                for j in range(4):
                        elemento=humedfil[i][j]
                        #estado=elemento[2:3]
                        filtro=elemento[0:23]
                        estado=filtro[2:7]
                        #print(estado)
                        if estado=="estad":
                                valor=elemento[12:16]
                                #print(valor)
                                estados.append(valor)



        #print(estados)
        modahumed=moda(estados)




        #---Apagados--
        #amov_filter= mov_filtered(lambda x: '0' in x)
        print("Total de registros:",general)
        print("\n")
        print("--------Sensor de Humedad--------------")
        print("Registros de sensor de humedad:",nhum)
        print("Moda sensor de humedad:",modahumed)
        print("\n")
        print("--------Sensor de Temperatura--------------")
        print("Registros de sensor de temperatura:",ntem)
        print("Moda sensor de temperatura:",modatemp)
        print("\n")
        print("--------Sensor Infrarrojo--------------")
        if nin > 0:
                print("Registros de sensor de infrarrojo:",nin)
                print("Registros de sensor de infrarrojo prendidos:",niu)
                print("Porcentaje Infr  prendidos",(int((niu*100)/nin)),"%")
                print("Registros de sensor de infrarrojo apagados:",nic)
                print("Porcentaje Infr  apagados",(int((nic*100)/nin)),"%")
                print("\n")
        print("--------Sensor Ultrasonico-----------------")
        print("Registros de sensor de ultrasonico:",nul)
        print("Moda sensor Ultrasonico:",modaultra)

        print("\n")


        print("--------Sensor de Movimiento-----------------")
        if nmov > 0:
                print("Registros de sensor de movimiento:",nmov)
                print("Registros de sensor de movimiento prendidos:",nmu)
                print("Porcentaje Mov prendidos",(int((nmu*100)/nmov)),"%")
                print("Registros de sensor de movimiento apagados:",nmc)
                print("Porcentaje Mov apagados",(int((nmc*100)/nmov)),"%")


        return(main())
        """
        print("Porcentaje derecha",(int((nder*100)/general)),"%")
        print("Porcentaje izquierda",(int((niz*100)/general)),"%")
        print("Porcentaje apagado",(int((napagado*100)/general)),"%")
        """

def main():
        print('\nEscribe dos fechas entre las cuales se evaluara la informacion de los sensores: sensores("<fecha_inicial>","<fecha_limite>")\n')
        print("Para terminar el programa escribe 't'")
        terminar=False
        while not terminar:
                entrada = input("> ")
                if entrada == 't':
                        exit()
                print(eval(entrada))

if __name__ == "__main__":
        main()
