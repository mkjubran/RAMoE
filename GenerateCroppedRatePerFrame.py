import numpy as np
import os, os.path, sys, subprocess, pdb

if __name__ == '__main__':
  fname='../ucfTrainTestlist/trainlist01.txt'
  JMSNoTextPath='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMStats_NoTexture_Train01_QP40_MVSR16_MVRes8_A/'
  JMSOrigPath='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMStats_OrigJM_Train01_QP40_MVSR16_MVRes8_A/'
  JMSOutPath='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMSize_Cropped_Train01_QP40_MVSR16_MVRes8_A/'
  
  fname='../ucfTrainTestlist/testlist01.txt'
  JMSNoTextPath='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMStats_NoTexture_Test01_QP40_MVSR16_MVRes8_A/'
  JMSOrigPath='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMStats_OrigJM_Test01_QP40_MVSR16_MVRes8_A/'
  JMSOutPath='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMSize_Cropped_Test01_QP40_MVSR16_MVRes8_A/'

  cnt=0;
  with open(fname) as f:
    filenames = f.readlines()
    filenames = [x.strip() for x in filenames]
  filenames = [x.split("/")[1].split('.')[0] for x in filenames] 
  JMSNoTextfilenames = [JMSNoTextPath+'JMFrameStats_'+x+'.dat' for x in filenames]
  JMSOrigfilenames = [JMSOrigPath+'JMFrameStats_'+x+'.dat' for x in filenames]
  JMSOutfilenames = [JMSOutPath+'JMFrameSize_'+x+'.dat' for x in filenames]

  for cntf in range(len(JMSNoTextfilenames)):
    print("Processing Video #{} : {}").format(cntf,filenames[cntf]) 
    if ((os.path.isfile(JMSNoTextfilenames[cntf])) and (os.path.isfile(JMSOrigfilenames[cntf]))):
       with open(JMSNoTextfilenames[cntf]) as fNoT:
         ContentNoT = fNoT.readlines()
         ContentNoT = [x.strip() for x in ContentNoT]
         FNumNoT=[]
         SizeNoT=[]
       for cnt in range(len(ContentNoT)):
         if ContentNoT[cnt][0:5]=="Frame":
            temp=ContentNoT[cnt].replace(" ", "")
	    FNumNoT.append(int(temp.split(",")[0].split("=")[1]))
            SizeNoT.append(int(temp.split("=")[2]))
       if FNumNoT[0]==FNumNoT[1]:
          FNumNoT=FNumNoT[1:len(FNumNoT)]
          SizeNoT[1]=SizeNoT[0]+SizeNoT[1]
          SizeNoT=SizeNoT[1:len(SizeNoT)]
        
       with open(JMSOrigfilenames[cntf]) as fOrig:
         ContentOrig = fOrig.readlines()
         ContentOrig = [x.strip() for x in ContentOrig]
         FNumOrig=[]
         SizeOrig=[]
       for cnt in range(len(ContentOrig)):
         if ContentOrig[cnt][0:5]=="Frame":
            temp=ContentOrig[cnt].replace(" ", "")
	    FNumOrig.append(int(temp.split(",")[0].split("=")[1]))
            SizeOrig.append(int(temp.split("=")[2]))
       if FNumOrig[0]==FNumOrig[1]:
          FNumOrig=FNumOrig[1:len(FNumOrig)]
          SizeOrig[1]=SizeOrig[0]+SizeOrig[1]
          SizeOrig=SizeOrig[1:len(SizeOrig)]

       FNumCropped = FNumNoT
       SizeCropped = SizeNoT
       SizeCropped[0] = SizeOrig[0]

       fileOut = open(JMSOutfilenames[cntf], 'w')
       for cnt in range(len(FNumCropped)):
          fileOut.write("{} {}\n".format(FNumCropped[cnt],SizeCropped[cnt]))
   
    

  

  #pdb.set_trace()
