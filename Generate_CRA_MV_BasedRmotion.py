import numpy as np
import os, os.path, sys, subprocess, pdb
import struct,argparse


parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--vidlist', type=str, help='list of training/testing videos')
parser.add_argument('--SNot_dir', type=str, help='JM NoTexture Stats directory')
parser.add_argument('--SOrig_dir', type=str, help='JM Original Stats directory')
parser.add_argument('--Out_dir', type=str, help='JM size of cropped videos output directory')
args = parser.parse_args()

listfilename  = args.vidlist
JMSNoTextPath = args.SNot_dir
JMSOrigPath   = args.SOrig_dir
JMSOutPath    = args.Out_dir


if __name__ == '__main__':

  # make out_dir if it doesn't exist
  if not os.path.exists(JMSOutPath):
     os.makedirs(JMSOutPath)
  
  cnt=0;
  with open(listfilename) as f:
    filenames = f.readlines()
    filenames = [x.strip() for x in filenames]
  filenames = [x.split("/")[1].split('.')[0] for x in filenames] 
  JMSNoTextfilenames  = [JMSNoTextPath +'JMFrameStats_'+x+'.dat' for x in filenames]
  JMSOrigfilenames    = [JMSOrigPath   +'JMFrameStats_'+x+'.dat' for x in filenames]
  JMSOutfilenames     = [JMSOutPath    +'JMFrameSize_' +x+'.dat' for x in filenames]

  for cntf in range(len(JMSNoTextfilenames)):
    if ((os.path.isfile(JMSNoTextfilenames[cntf])) and (os.path.isfile(JMSOrigfilenames[cntf]))):
       print("Processing Video #{} : {}").format(cntf,filenames[cntf]) 
       
       ## Read the stats of the NoTexture Bitstream
       with open(JMSNoTextfilenames[cntf]) as fNoT:
         ContentNoT = fNoT.readlines()
         ContentNoT = [x.strip() for x in ContentNoT]
         FNumNoT=[]    
         SizeNoT=[]     ## Size for not tecture stats
         FNumRmValue=[] ## Rmotion per Frame
         FNumRm=[]     ## Frames with non zero Rmotion
         FNumRmZero=[] ## Frames with zero Rmotion
       for cnt in range(len(ContentNoT)):
          #To get Rmotion
          if ContentNoT[cnt][0:6]=="Motion":
            temp=ContentNoT[cnt].replace(" ", "")
	    FNumRmValue.append(int(float(temp.split("|")[2])))
          
          #To get frame number and size 
          if ContentNoT[cnt][0:5]=="Frame":
            temp=ContentNoT[cnt].replace(" ", "")
	    FNumNoT.append(int(temp.split(",")[0].split("=")[1]))
            SizeNoT.append(int(temp.split("=")[2]))

       [FNumRm.append(i) for i, e in enumerate(FNumRmValue) if e != 0]
       [FNumRmZero.append(i) for i, e in enumerate(FNumRmValue) if e == 0]
       if FNumNoT[0]==FNumNoT[1]:
          FNumNoT=FNumNoT[1:len(FNumNoT)]
          SizeNoT[1]=SizeNoT[0]+SizeNoT[1]
          SizeNoT=SizeNoT[1:len(SizeNoT)]
       
       ## Read the stats of the Original Bitstream
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
          if FNumCropped[cnt] in FNumRm:
              fileOut.write("{} {}\n".format(FNumCropped[cnt],SizeCropped[cnt]))
              #print("{}..{}").format(FNumCropped[cnt],SizeCropped[cnt])
      
       #print(FNumCropped)
       #print(FNumRmValue)
       #print(FNumRm)
       #print(FNumRmZero)
   
    

  

  #pdb.set_trace()
