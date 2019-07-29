#coding: utf-8
# File:          supervisor.py
# Date:          
# Description:   
# Author:        
# Modifications: 

#Python API
#https://www.cyberbotics.com/doc/reference/python-api

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
from controller import *
from controller import Robot
import ctypes
import os
import random as rd
#import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import math
#from controller import Field
#from controller import Node


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class supervisor (Supervisor, Node, Camera):
  
  
  testlib = ctypes.CDLL('./../../Blackboard/blackboard.so') #chama a lybrary que contem as funções em c++
  testlib.using_shared_memory()   #usando a função do c++
  testlib.leitura_int.restype = ctypes.c_int #define o tipo de retorno da função, neste caso a função retorna int 

  
  # User defined function for initializing and running
  # the supervisor class
  def run(self):
    print "teste1"
    #self.__init__()
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  led = self.getLed('ledname')
    count = 0
    espera_gol = 0
    fez_gol = 0
    File  = "/home/fei/webots/projects/objects/robotstadium/protos/RobotstadiumSoccerField.proto"
    File2 = "./../../protos/Darwin-op.proto"
    File3 = "/home/fei/webots/projects/objects/balls/protos/SoccerBall.proto"
    
    arrayFields = [ '            \"textures/field_quarter2014.jpg\"\n',
                    '            \"textures/2field_quarter2014.jpg\"\n',
                    #'            \"textures/3field_quarter2014.jpg\"\n',
                    #'            \"textures/4field_quarter2014.jpg\"\n',
                    #'            \"textures/5field_quarter2014.jpg\"\n',
                    #'            \"textures/6field_quarter2014.jpg\"\n',
                    '            \"textures/7field_quarter2014.jpg\"\n',
                    '            \"textures/8field_quarter2014.jpg\"\n',
                    '            \"textures/9field_quarter2014.jpg\"\n',
                    '            \"textures/10field_quarter2014.jpg\"\n',
                    '            \"textures/11field_quarter2014.jpg\"\n',
                    '            \"textures/12field_quarter2014.jpg\"\n',
                    '            \"textures/old_field_quarter2014.jpg\"\n' ]
    
    robot_node = self.getFromDef("ROBOTISOP2")
    ball_node = self.getFromDef("BALL")
    light1_node = self.getFromDef("LIGHT1")
    light2_node = self.getFromDef("LIGHT2")
    background_node = self.getFromDef("BACKGROUND")
    soccerfield_node = self.getFromDef("SoccerField")
    self.trans_field_ball = ball_node.getField("translation")
    self.trans_field_robot = robot_node.getField("translation")
    self.rot_field_robot = robot_node.getField("rotation")
    self.light1_intensity = light1_node.getField("intensity")
    self.light2_intensity = light2_node.getField("intensity")
    self.light1_Ambintensity = light1_node.getField("ambientIntensity")
    self.light2_Ambintensity = light2_node.getField("ambientIntensity")
    self.background_color = background_node.getField("skyColor")
    
    
    #change the soccer field--------------------------------------
    replace_line( File, 24, arrayFields[rd.randint(0, len(arrayFields)-1)])
    #-------------------------------------------------------------

    #change the fieldOfView---------------------------------------
    fieldOfView = "                    fieldOfView "+str(rd.uniform(1.6, 1.7))+"\n"
    replace_line( File2, 882, fieldOfView)
    #-------------------------------------------------------------

    #change the ball size--------------------------------------    
    ballsize = "  field SFFloat radius "+str(rd.uniform(0.045, 0.06))+"\n"
    replace_line( File3, 8, ballsize)
    #-------------------------------------------------------------    


    textureBall = ['              \"textures/football.jpg\"\n',
                   '              \"textures/football1.jpg\"\n',
                   '              \"textures/football2.jpg\"\n',
                   '              \"textures/football3.jpg\"\n',
                   '              \"textures/football4.jpg\"\n',
                   '              \"textures/football5.jpg\"\n',
                   '              \"textures/football6.jpg\"\n',
                   '              \"textures/football7.jpg\"\n',
                   '              \"textures/football8.jpg\"\n']

    #change the texture ball--------------------------------------    
    replace_line( File3, 25, textureBall[rd.randint(0, len(textureBall)-1)])
    #-------------------------------------------------------------    



    #change the ball size--------------------------------------    
    #ballcolor = "  field SFColor color "+str(rd.uniform(0.80, 1.0))+" "+str(rd.uniform(0.05, 0.4))+" "+str(rd.uniform(0.02, 0.08))+"\n"
    #replace_line( File3, 8, ballcolor)
    #------------------------------------------------------------- 

    #image = np.array([[self.testlib.leitura_int((x+1)*(y+1)*3), self.testlib.leitura_int((x+1)*(y+1)*3+1), self.testlib.leitura_int((x+1)*(y+1)*3+2)] for x in range(self.testlib.leitura_int(0)) for y in range(self.testlib.leitura_int(1)) ])
    #index = 2
    #image = np.zeros([self.testlib.leitura_int(1),self.testlib.leitura_int(0),3])
    #for y in range(self.testlib.leitura_int(0)):
      #for x in range(self.testlib.leitura_int(1)):
        #image[x,y,0] = self.testlib.leitura_int(index+2)   #B
        #image[x,y,1] = self.testlib.leitura_int(index+1) #G
        #image[x,y,2] = self.testlib.leitura_int(index) #R
        #index = index + 3
    

    #print image    
    #plt.imshow(image)
    #plt.show()
    #cv2.startWindowThread()
    #cv2.namedWindow("image")
    #cv2.imshow('image',image)
    #cv2.imwrite('color_img.jpg', image)
    #cv2.waitKey();
    #print image.size
 
    
    #cv2.imwrite('color_img.jpg', image)
    #cv2.imshow("image", image);
    #cv2.waitKey();
    
    #Inicia robo e bola em posições aleatorias no campo
    
    #==================================================
    random_x = rd.uniform(0, -2.5)
    random_y = rd.uniform(2, -2)
    #Inicia a bola em posiçao aleatoria----------------------
    initialBall  = list(self.trans_field_ball.getSFVec3f())
    initialBall[0]  = initialBall[0]-rd.uniform(0.06, -0.06) + random_x
    initialBall[2]  = initialBall[2]-rd.uniform(-0.06, 0.06) + random_y
    self.trans_field_ball.setSFVec3f(initialBall)
    #--------------------------------------------------------

    #Inicia o robo em posiçao aleatoria----------------------
    initialRobot  = list(self.trans_field_robot.getSFVec3f())
    initialRobot[0]  = initialRobot[0]-rd.uniform(0, -0.1) + random_x
    initialRobot[2]  = initialRobot[2]-rd.uniform(-0.35, 0.35) + random_y
    self.trans_field_robot.setSFVec3f(initialRobot)
    #--------------------------------------------------------
    
    #initialRobot = self.trans_field_robot.getSFVec3f()
    decision   = 1000000
    resetEnv   = 1000001
    respReset  = 1000002
    recompensa = 1000003
    finalizado = 1000004
    robotFall  = 1000005
    inicioSimu = 1000006
    acaoExecta = 1000007
    liberaAct  = 1000008
    #1000009 é utilizado para contar os goals
    countTouch = 1000010 #Conta quantas vezer alcançou a bola
    #1000011 é utilizado para contar as falhas
    stopRobot  = 1000012 #avisa q robo pode parar para esperar reward
        
    self.testlib.escreve_int(respReset, 0)
    self.testlib.escreve_int(resetEnv, 0)
    self.testlib.escreve_int(decision, 0)
    self.testlib.escreve_int(recompensa, 0)
    self.testlib.escreve_int(finalizado, 0)
    self.testlib.escreve_int(robotFall, 0)
    self.testlib.escreve_int(inicioSimu, 1)
    self.testlib.escreve_int(acaoExecta, 0)
    self.testlib.escreve_int(liberaAct, 0)
    self.testlib.escreve_int(stopRobot, 0)
    # Main loop
    
    #Modifica a cor do background-----------------------------------
    cor = np.array(self.background_color.getMFColor(0))
    #cor = cor*rd.uniform(0.7, 1.1)
    self.background_color.setMFColor(0, [cor[0]*rd.uniform(0.8, 1.1), 
                                         cor[1]*rd.uniform(0.8, 1.2),
                                         cor[2]*rd.uniform(0.8, 1.3)])
    #---------------------------------------------------------------
    
    
    #Modifica a iluminacao do campo-------------------------
    #print self.light1_intensity.getSFFloat()
    self.light1_intensity.setSFFloat(rd.uniform(0.2, 0.7))
    self.light2_intensity.setSFFloat(rd.uniform(0.2, 0.7))
    self.light1_Ambintensity.setSFFloat(rd.uniform(0.7, 1))
    self.light2_Ambintensity.setSFFloat(rd.uniform(0.7, 1))    
    #---------------------------------------------------------------
    
    #Esta linha é necessaria para capturar a posição devido reposição do robo
    translationValues   = list(initialBall) #Captura a posicao inicial da bola
    
    transRobot = list(initialRobot)         #Captura a posicao inicial do robo
    rotRobot = self.rot_field_robot.getSFRotation()

    #print "1-translationValues[0] " + str(translationValues)
    #print "1-initialBall[0] " +str(initialBall)

    #Calcula a distancia euclidiana entre a bola e o robo-----------
    euclid = math.sqrt((translationValues[0] - transRobot[0])**2 + (translationValues[2] - transRobot[2])**2)
    olddistance = distance = round( euclid, 2)
    #---------------------------------------------------------------
    
    #Inicia um array de 40 posicoes para caso o robo cair ele levantar na mesma posicao----      
    arraytrRobot = [transRobot for x in xrange(60)]
    arrayrRobot  = [rotRobot   for x in xrange(60)]
    #---------------------------------------------
    
    kickBall = False

    time.sleep(1)

    while True:

      # Perform a simulation step of 64 milliseconds
      # and leave the loop when the simulation is over
      if self.step(64) == -1:
        break
      #new = [translationValues[0]+0.01, 0.0550568,translationValues[2]+0.00]
      #print new
      #self.trans_field_ball.setSFVec3f(new)
      if self.testlib.leitura_int(resetEnv) == 1:
        self.testlib.escreve_int(respReset, 1)
        self.testlib.escreve_int(resetEnv, 0)
        self.simulationRevert()

      # Read the sensors:
      # Enter here functions to read sensor data, like:
      #  val = ds.getValue()
      
      
      #Verifica se ja executou uma acao================================================
      if self.testlib.leitura_int(acaoExecta) == 1:

          #verifica se a distancia da bola aumentou ou diminuiu=========
          translationValues = list(self.trans_field_ball.getSFVec3f())
          transRobot = list(self.trans_field_robot.getSFVec3f())
          rotRobot = list(self.rot_field_robot.getSFRotation())
          if self.testlib.leitura_int(robotFall) == 0:
            arraytrRobot.append(list(transRobot))
            arrayrRobot.append(list(rotRobot))
            del arraytrRobot[0]
            del arrayrRobot[0]
          olddistance = distance
          euclid = math.sqrt((translationValues[0] - transRobot[0])**2 + (translationValues[2] - transRobot[2])**2)
          distance = round( euclid, 2)
          #print "ball", translationValues
          #print "robot", transRobot
          #print "distance", distance, "old", olddistance
          #==============================================================
        
          #Calcula a recompensa para chegar ate a bola ==========================
          #bola_frente = translationValues[0] > 4.6
          #if (bola_frente and translationValues[2] > -0.76 and translationValues[2] < 0.76) or fez_gol == 1:
            #reward = 10 #Robo atingiu o objetivo -> fazer o gol
            #fez_gol = 1
            #initialBall[0]  = 40 #joga a bola la na casa do caralho
            #count+=1
            #self.trans_field_ball.setSFVec3f(initialBall)
          if (translationValues[0] > (initialBall[0] + 0.03) or translationValues[0] < (initialBall[0] - 0.03)) and not kickBall:
            reward = 10 #Chegou na bola
            self.testlib.escreve_int(countTouch, self.testlib.leitura_int(countTouch) + 1)
            kickBall = True
            count+=1
          elif (self.testlib.leitura_int(decision) == 5 or self.testlib.leitura_int(decision) == 6) and distance > 0.15:
            reward = -10 #Robo chutando a bola longe da bola
          #elif self.testlib.leitura_int(decision) > 6 and distance > 0.08:
            #reward = -10 #Robo chutando afastando da bola
#          elif transRobot[0] > -3.10 or transRobot[2] > 0.9 or transRobot[2] < -0.9:
#            reward = -10 #Robo se distanciando muito do gol
          elif  transRobot[0] > 4.5:
            reward = -10 #Robo esta dentro do gol   
          elif distance < olddistance:
            if rotRobot[3]<0 and (transRobot[0] < translationValues[0]): #Verifica se robo esta de costas para o campo
              reward = -3 #Robo esta chegando perto da bola
            else:
              reward = -10 #Robo esta de costas para a bola
          elif distance == olddistance:
            if rotRobot[3]<0: #Verifica se robo esta de costas para o campo
              reward = -5 #Robo esta parado no lugar de frente para a bola
            else:
              reward = -10 #Robo esta de costas para a bola
          else:
            reward = -10 #Robo esta se afastando da bola
          self.testlib.escreve_int(recompensa, reward)
          #print "reward", reward
          #==============================================================

          if kickBall == False:
            self.testlib.escreve_int(acaoExecta, 0)
            self.testlib.escreve_int(liberaAct, 0)
      #===========================================================================================
      
      #if kickBall:
        #espera_gol+=1
        #self.testlib.escreve_int(stopRobot, 1)
      
      #Verifica se a bola foi para fora do gol
      #E se a bola foi para as costas do robo
      #translationValues = self.trans_field_ball.getSFVec3f()
      #if translationValues[2] < -0.86 or translationValues[2] > 0.86 or translationValues[0] < 2.65 :
        #espera_gol = 500
      
      #print "translationValues[0] " + str(translationValues[0])
      #print "initialBall[0] " +str(initialBall[0])
      if (translationValues[0] > (initialBall[0] + 0.03) or translationValues[0] < (initialBall[0] - 0.03)):
        string = str(initialBall[0])+" "+ str(initialBall[2])+" "+str(initialRobot[0])+" "+str(initialRobot[2])+" "+str(translationValues[0])+" "+ str(translationValues[2])+"\n"
        with open('./../../positions_file.dat','a') as f:
          f.write(string)
        #if (bola_frente and translationValues[2] > -0.76 and translationValues[2] < 0.76) or fez_gol == 1:
        reward = 10 #Robo atingiu o objetivo -> chagar na bola
        self.testlib.escreve_int(recompensa, reward)
        print "========= reach the ball =========="
        self.testlib.escreve_int(acaoExecta, 0)
        self.testlib.escreve_int(liberaAct, 0)
        self.testlib.escreve_int(finalizado, 1)
        self.simulationRevert()
      
      #========Se robo caiu o supervisor levanta============
      if transRobot[1] < 0.25:
        self.trans_field_robot.setSFVec3f(arraytrRobot[0])
        self.rot_field_robot.setSFRotation(arrayrRobot[0])
        self.testlib.escreve_int(robotFall, 0)
        print "============Fall=============="
      #=====================================================
      
      # Process sensor data here.
      
      # Enter here functions to send actuator commands, like:
      #  led.set(1)
    
    # Enter here exit cleanup code


# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = supervisor()
controller.run()
