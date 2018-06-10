import numpy as np
import os, os.path, sys, subprocess, pdb
import struct,argparse


parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('--vidlist', type=str, help='list of training/testing videos')
parser.add_argument('--MV_dir', type=str, help='JMMV directory')
parser.add_argument('--SNot_dir', type=str, help='JM NoTexture Stats directory')
parser.add_argument('--SOrig_dir', type=str, help='JM Original Stats directory')
parser.add_argument('--Out_dir', type=str, help='JM size of cropped videos output directory')
args = parser.parse_args()

listfilename  = args.vidlist
JMMVPathInput = args.MV_dir
JMSNoTextPath = args.SNot_dir
JMSOrigPath   = args.SOrig_dir
JMSOutPath    = args.Out_dir


if __name__ == '__main__':
  #listfilename='../ucfTrainTestlist/trainlist01.txt'
  #JMMVPathInput ='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMMV_Train01_QP40_MVSR16_MVRes8_NoStats/'
  #JMSNoTextPath ='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMStats_NoTexture_Train01_QP40_MVSR16_MVRes8_A/'
  #JMSOrigPath   ='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMStats_OrigJM_Train01_QP40_MVSR16_MVRes8_A/'
  #JMSOutPath    ='../JMMV/JM_QP40_MVSR16_MVRes8_A_Done/JMSize_Cropped_Train01_QP40_MVSR16_MVRes8_A/'

  # make out_dir if it doesn't exist
  if not os.path.exists(JMSOutPath):
     os.makedirs(JMSOutPath)
  
  cnt=0;
  with open(listfilename) as f:
    filenames = f.readlines()
    filenames = [x.strip() for x in filenames]
  filenames = [x.split("/")[1].split('.')[0] for x in filenames] 
  JMMVInputfilenames  = [JMMVPathInput +'JMMV_'        +x+'.bin' for x in filenames]
  JMSNoTextfilenames  = [JMSNoTextPath +'JMFrameStats_'+x+'.dat' for x in filenames]
  JMSOrigfilenames    = [JMSOrigPath   +'JMFrameStats_'+x+'.dat' for x in filenames]
  JMSOutfilenames     = [JMSOutPath    +'JMFrameSize_' +x+'.dat' for x in filenames]

  for cntf in range(len(JMSNoTextfilenames)):
    if ((os.path.isfile(JMMVInputfilenames[cntf])) and (os.path.isfile(JMSNoTextfilenames[cntf])) and (os.path.isfile(JMSOrigfilenames[cntf]))):
       print("Processing Video #{} : {}").format(cntf,filenames[cntf]) 
       
       ## Read the FrameNumbers from the MV.bins [[take care of shift in frame number associated with JM and mbmap]]
       with open(JMMVInputfilenames[cntf],"rb") as fMV:  
           Content = fMV.read()
       FInfoMV = struct.unpack('<IIIIc', Content[0:17])
       # width and height of the image
       FNumMV=[];
       FNumMV.append(int(FInfoMV[1]))
       width = int(FInfoMV[2])
       height = int(FInfoMV[3])
       frame_bytes = 16 + 1 + (height * width)
       FNumMV_Shift_minus1=[];
       FNumMV_Shift_minus1Dif=[];
       for i in range(frame_bytes, len(Content), frame_bytes):
         # <int FNumMV> <int FNumMV> <int xdim> <int ydim>  <char frameType> <int DATA>
         FInfoMV = struct.unpack('<IIIIc', Content[i:i + 17])
         FNumMV.append(int(FInfoMV[1]))
         FJump=FNumMV[len(FNumMV)-1]-FNumMV[len(FNumMV)-2]
         if FJump>1:
            FNumMV_Shift_minus1.append(len(FNumMV)-1)
            FNumMV_Shift_minus1Dif.append(FJump)
       FNumMV[len(FNumMV)-1]=FNumMV[len(FNumMV)-2]+1
       
       cntJump=0
       for i in FNumMV_Shift_minus1:
         FNumMV[i]=FNumMV[i]-FNumMV_Shift_minus1Dif[cntJump]+1;
         cntJump=cntJump+1

       ## Read the stats of the NoTexture Bitstream
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
          if FNumCropped[cnt] in FNumMV:
              fileOut.write("{} {}\n".format(FNumCropped[cnt],SizeCropped[cnt]))
              #print("{}..{}").format(FNumCropped[cnt],SizeCropped[cnt])
      
       #print(FNumCropped)
       #print(FNumMV)
   
    

  

  #pdb.set_trace()
