import glob
import os, os.path
import cv2
import numpy as np
import os
from random import shuffle
#from tqdm import tqdm
import tensorflow as tf
import matplotlib.pyplot as plt
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

import pickle
import numpy as np
import matplotlib.pyplot as plt
import pickle
import numpy as np
import matplotlib.pyplot as plt
TestFolder ='E:/GP Code/Kaggle/Kaggle/New Plant Diseases Dataset(Augmented)/Demo/valid'
TrainFolder ='E:/GP Code/Kaggle/Kaggle/New Plant Diseases Dataset(Augmented)/Demo/train'
FP = 'E:/Train/Demo'
IMG_SIZE = 50
LR = 0.001
MODEL_NAME = 'Model-cnn'
Numlayers = 3

class Get_Features:
    # create_label for image
    def create_label(image_name,number):
        """ Create an one-hot encoded vector from image name """

        target=[]
        for i in range(0,number):
            target.append(0)
        target[image_name]=1

        return target
    # SaveMetaData in single plant
    def SaveMetaData(DataList):
        print('start create meta data file ')
        TypeName = str.split(DataList[0], '_')
        TypeName = TypeName[0]
        FileName = 'MetaData/' + TypeName + '.txt'
        FileName2 = 'Modeles Name/Names.txt'
        f = open(FileName, "w+")
        for i in range(0, len(DataList)):
            strng = str.split(DataList[i], '___')
            strng = strng[1]
            f.write(strng + '\n')
        f.close()
        f = open(FileName2,"w+")
        f.write(TypeName)
        f.close()
        print('Meta data file  created ')
    def LoadMetaData(FileName):
        print('start load meta data')
        DataList=[]
        f = open(FileName, "r+")
        counter = 0
        #g= f.readline()
        #print(g)
        #Datatmp = str.split()
        for x in f:
            Data = [counter , x[0:(len(x)-1)]]
            counter = counter+1
            DataList.append(Data)
        print('Meta data has been laoded')
        return DataList
    #ReadImages from folder
    def ReadImages(FolderPath):
        print('start read images from folder ')
        ImagesList = []
        FolderName = []
        for root, dirs, files in os.walk(FolderPath):
            for name in dirs:
                path = FolderPath + '/' + name + '/*.jpg'
                FolderOfImage = []
                FolderName.append(name)
                for f in glob.glob(path):
                    img1 = cv2.imread(f,1)
                    img = cv2.resize(img1, (IMG_SIZE, IMG_SIZE))
                    FolderOfImage.append(img)
                ImagesList.append(FolderOfImage)
        print('Images has been readed with count = ',len(ImagesList))
        return ImagesList, FolderName
    def Convert_Image_To_Vector(ListOfImages):
        '''this function take list of images features and convert it to
            list of vectors that have image features and image label        '''
        print('Start convert images to vector')
        ImagesFeatures = []
        print('start create label ')
        for i in range(0, len(ListOfImages[0])):
            FolderObject = ListOfImages[0][i]
            for j in range(0, len(FolderObject)):
                ImagesFeatures.append([np.array(FolderObject[j]),Get_Features.create_label(i,len(ListOfImages[0]))])
        print('label created')
        shuffle(ImagesFeatures)
        print('vector converted successfully')
        return ImagesFeatures


class DataSetFunctions:
    def new_Train(Train_path,Valid_path,model_name):
        '''this function take train ,test path and model name to genertate
            trained model for singl type of plant       '''
        folder_list_train=Get_Features.ReadImages(Train_path)
        folder_list_test=Get_Features.ReadImages(Valid_path)
        Get_Features.SaveMetaData(folder_list_train[1])
        image_labled_train=Get_Features.Convert_Image_To_Vector(folder_list_train)
        image_labled_test=Get_Features.Convert_Image_To_Vector(folder_list_test)
        DataSetFunctions.CreateModel(image_labled_train,image_labled_test,model_name)
        model=DataSetFunctions.load_model(model_name)
        Accuarcy=DataSetFunctions.calculate_accuracy(image_labled_test,model)
        print('accurecy is = ',Accuarcy)
        return Accuarcy



    #CreateModel for plant
    def CreateModel(Images_Features,ImagesFeatures_test,model_name):
        print('Start training with sample count  = ',len(Images_Features))
        X_train = np.array([i[0] for i in Images_Features]).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
        y_train = [i[1] for i in Images_Features ]
        X_test = np.array([i[0] for i in ImagesFeatures_test]).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
        y_test = [i[1] for i in ImagesFeatures_test]

        tf.reset_default_graph()
        conv_input = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')
        conv1 = conv_2d(conv_input, 32, 5, activation='relu')
        pool1 = max_pool_2d(conv1, 5)

        conv2 = conv_2d(pool1, 64, 5, activation='relu')
        pool2 = max_pool_2d(conv2, 5)

        conv3 = conv_2d(pool2, 128, 5, activation='relu')
        pool3 = max_pool_2d(conv3, 5)


        conv4 = conv_2d(pool3, 64, 5, activation='relu')
        pool4 = max_pool_2d(conv4, 5)

        conv5 = conv_2d(pool4, 32, 5, activation='relu')
        pool5 = max_pool_2d(conv5, 5)


        fully_layer = fully_connected(pool5, 1024, activation='relu')
        fully_layer = dropout(fully_layer, 0.8)

        fully_layer = fully_connected(pool5, 512, activation='relu')
        fully_layer = dropout(fully_layer, 0.9)

        cnn_layers = fully_connected(fully_layer, Numlayers, activation='softmax')
        cnn_layers = regression(cnn_layers, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy',
                                name='targets')
        model = tflearn.DNN(cnn_layers, tensorboard_dir='log', tensorboard_verbose=3)
        model_name=model_name+'.tfl'
        if (os.path.exists(model_name+'.meta')):
            model.load('./'+model_name)

        else:
            model.fit({'input': X_train}, {'targets': y_train}, n_epoch=30,
                      validation_set=({'input': X_test}, {'targets': y_test}),
                      snapshot_step=500, show_metric=True, run_id=MODEL_NAME)
            model.save(model_name)

    def load_model(model_name):
        print('start load model')
        tf.reset_default_graph()
        conv_input = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')
        conv1 = conv_2d(conv_input, 32, 5, activation='relu')
        pool1 = max_pool_2d(conv1, 5)

        conv2 = conv_2d(pool1, 64, 5, activation='relu')
        pool2 = max_pool_2d(conv2, 5)

        conv3 = conv_2d(pool2, 128, 5, activation='relu')
        pool3 = max_pool_2d(conv3, 5)

        conv4 = conv_2d(pool3, 64, 5, activation='relu')
        pool4 = max_pool_2d(conv4, 5)

        conv5 = conv_2d(pool4, 32, 5, activation='relu')
        pool5 = max_pool_2d(conv5, 5)

        fully_layer = fully_connected(pool5, 1024, activation='relu')
        fully_layer = dropout(fully_layer, 0.8)

        fully_layer = fully_connected(pool5, 512, activation='relu')
        fully_layer = dropout(fully_layer, 0.9)

        cnn_layers = fully_connected(fully_layer, Numlayers, activation='softmax')
        cnn_layers = regression(cnn_layers, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy',
                                name='targets')
        model = tflearn.DNN(cnn_layers, tensorboard_dir='log', tensorboard_verbose=3)
        model_name = model_name + '.tfl'
        if (os.path.exists(model_name + '.meta')):
            model.load('./' + model_name)
        print('model loaded')
        return model

    def single_image(ImagePath,model_name):
        '''this function test single image and return the disease of
            the plant'''
        print('Start test single image')
        model=DataSetFunctions.load_model(model_name)
        Meta_Data=Get_Features.LoadMetaData('MetaData/'+model_name+'.txt')
        img = cv2.imread(ImagePath, 1)
        test_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        test_img = test_img.reshape(IMG_SIZE, IMG_SIZE, 3)
        prediction = model.predict([test_img])[0]
        label = DataSetFunctions.ret_lable(prediction)
        des = DataSetFunctions.DesandTre(Meta_Data[label][1])
        print('image finished test')
        return Meta_Data[label][1], des

    def DesandTre(diseases):
        #print(diseases)
        if(diseases != 'healthy'):
            des_file='MetaData/'+diseases+'_description.txt'
            des=open(des_file,'r')
            desc=des.read()

            tre_file='MetaData/'+diseases+'_treatment.txt'
            tre=open(tre_file,'r')
            trea=tre.read()
            return desc,trea
        else:
            return diseases

    def ret_lable(predict):
        '''this function take the predict list that return from the output
            layer and return the label of the class that has the greatest
            prediction.                                         '''
        acc = 0
        lable = 0
        for i in range(0, len(predict)):
            if (predict[i] > acc):
                acc = predict[i]
                lable = i
        return lable
    def CheckFoledOfImages(ImageFeatures, ModelName, MetaDataFile):

        RatioOfDiseases = []
        model = DataSetFunctions.load_model(ModelName)
        for i in range(0, len(MetaDataFile)):
            tmp = MetaDataFile[i]
            RatioOfDiseases.append([tmp[1], 0])
        print(RatioOfDiseases)
        for i in range(0, len(ImageFeatures)):
            # print(i)
            test_img = cv2.resize(ImageFeatures[i], (IMG_SIZE, IMG_SIZE))
            test_img = test_img.reshape(IMG_SIZE, IMG_SIZE, 3)

            prediction = model.predict([test_img])[0]

            num = DataSetFunctions.ret_lable(prediction)
            # print(num)
            for j in range(0, len(MetaDataFile)):
                tmp = MetaDataFile[j]
                calc = 0
                if (num == tmp[0]):
                    tmp2 = RatioOfDiseases[j]
                    calc = tmp2[1] + 1
                    RatioOfDiseases[j] = [tmp[1], calc]
        # print('Ratio = ',RatioOfDiseases)
        list_Ratio = []
        for i in range(0, len(RatioOfDiseases)):
            tmpname = RatioOfDiseases[i][0]
            tmpcalc = RatioOfDiseases[i][1]
            # print(tmpcalc)
            tmpcalc = tmpcalc / len(ImageFeatures)
            RatioOfDiseases[i] = [tmpname, tmpcalc]
            list_Ratio.append(tmpcalc)
        max_dis = np.argmax(list_Ratio)

        dis = DataSetFunctions.DesandTre(RatioOfDiseases[max_dis][0])

        return RatioOfDiseases[max_dis], dis

    def correct(predict, lable):
        '''this function take as parameter the predict list and the
            correct label of the input image and check if the the
            prediction is correct then return 1 else return 0'''
        acc = 0
        max1 = 0
        ind = 0
        for i in range(0, len(predict)):
            if (predict[i] > max1):
                max1 = predict[i]
                ind = i
        if (lable[ind] == 1):
            acc = 1
        return acc


    def read_folder(folder_path):
        testing_data = []
        # Student code
        for img in os.listdir(folder_path):
            path = os.path.join(folder_path, img)
            img_data = cv2.imread(path, 1)
            testing_data.append(img_data)
        return testing_data

    def calculate_accuracy(X_test, model):

       '''this function take images features in testing folder
          and take model object as parameter and return the ratio
          of the performance for this model'''
       acc = 0
       print('start calculate accuracy with count of images =  ',len(X_test))
       for i in range(0, len(X_test)):
           # test_img = cv2.resize(X_test, (IMG_SIZE, IMG_SIZE))
           test_img = X_test[i][0].reshape(IMG_SIZE, IMG_SIZE, 3)
           prediction = model.predict([test_img])[0]
           acc += DataSetFunctions.correct(prediction, X_test[i][1])
       print('out')
       return acc / len(X_test)

class Tracking:
    def Create_New_Track(TrackName ,Plant_Type):
        '''This function Create New track Only'''
        print('start create Tracking file ')
        FileName = 'Tracking_Data/Traking_ID.txt'
        file = open(FileName, "r+")
        Data = []
        for x in file:
            Data.append(x)
        file.close()
        f = open(FileName, "w+")
        g = open('Tracking_Data/'+TrackName+'.txt',"w+")
        g.close()
        for p in Data:
            f.write(p)
        f.write(TrackName+'-'+ Plant_Type + '\n')

        f.close()
        print('Tracking file  created ')

    def get_Plant_type(TrackID):
        FileName = 'Tracking_Data/Traking_ID.txt'
        f = open(FileName, "r+")
        plant=''
        for x in f:
            line=str.split(x,'-')
            if TrackID == line[0]:
                plant=line[1]
                break
        f.close()
        return plant

    def Update_Tracking(TrackId ,Folder_Path):
        plant_type=Tracking.get_Plant_type(TrackId)
        plant=str.split(plant_type,'\n')
        model= DataSetFunctions.load_model(plant[0])
        ImageFeatures=DataSetFunctions.read_folder(Folder_Path)
        file='MetaData/' + plant[0] + '.txt'
        print(plant[0])
        print(file)

        MetaDataFile=Get_Features.LoadMetaData(file)
        RatioOfDiseases = []

        for i in range(0, len(MetaDataFile)):
            tmp = MetaDataFile[i]
            RatioOfDiseases.append([tmp[1], 0])

        for i in range(0, len(ImageFeatures)):
            # print(i)
            test_img = cv2.resize(ImageFeatures[i], (IMG_SIZE, IMG_SIZE))
            test_img = test_img.reshape(IMG_SIZE, IMG_SIZE, 3)

            prediction = model.predict([test_img])[0]

            num = DataSetFunctions.ret_lable(prediction)
            # print(num)
            for j in range(0, len(MetaDataFile)):
                tmp = MetaDataFile[j]
                calc = 0
                if (num == tmp[0]):
                    tmp2 = RatioOfDiseases[j]
                    calc = tmp2[1] + 1
                    RatioOfDiseases[j] = [tmp[1], calc]
        Tracking.Update_Track_file(RatioOfDiseases,TrackId)
        return RatioOfDiseases

    def Update_Track_file(list,TrackID):
        FileName = 'Tracking_Data/'+TrackID+'.txt'
        file=open(FileName,"r+")
        Data=[]
        for x in file:
            Data.append(x)
        file.close()
        f = open(FileName, "w+")
        total=0
        for i in list:
            total=total+i[1]

        string=list[0][0]+'-'+str(list[0][1]/total)+','
        for i in range(1,len(list)):
            if i == (len(list)-1):
                string = string + list[i][0] + '-' + str(list[i][1] / total)
            else:
                string =string + list[i][0] + '-' + str(list[i][1]/total) + ','

        Data.append(string)
        for i in range(0,len(Data)):

            f.write(Data[i])
        f.close()

    def Make_Combobox():
        FileName = 'Tracking_Data/Traking_ID.txt'
        file = open(FileName, "r+")
        x= file.read()
        x= x.split('\n')
        IDList = []
        for i in range(0 ,len(x)):
            IDList.append(x[i].split('-')[0])
        print(IDList)
        return IDList
    def statistical_graph(listofname, listofratio):
        print(listofratio)
        X = range(1, len(listofratio[0])+1)
        plt.figure('Improvement in time')
        for i in range(0, len(listofname)):
            plt.plot(X, listofratio[i])
        plt.legend(listofname, loc='upper left')
        plt.show()

    def create_graph(Track_Id):
        FileName = 'Tracking_Data/' + Track_Id + '.txt'
        file = open(FileName, "r+")
        Data = []
        for x in file:
            Data.append(x)
        file.close()
        oneline=str.split(Data[0],',')
        names=[]
        ratios=[]
        for i in range(0,len(oneline)):
            string=str.split(oneline[i],'-')
            names.append(string[0])
            ratios.append([])
        for i in range(0,len(Data)):
            line=str.split(Data[i],',')
            for j in range(0, len(oneline)):
                values=str.split(line[j],'-')
               # print(values)

                value = float(values[1])
                ratios[j].append(value)

        Tracking.statistical_graph(names,ratios)




#list=Tracking.Update_Tracking('sds_fool','Test')
#print(list)

'''this function is used to check folder contain images and return percentage for 
    unhealthy and healthy plant.
    it take as parameter images features ,model file name and Metadata txt file.
    '''



#Tracking.Make_Combobox()

'''
c = DataSetFunctions

if (os.path.exists('train_data.npy')): # If you have already created the dataset:
    Data =np.load('train_data.npy')
else: # If dataset is not created:
    IL = c.ReadImages(FP)
    Data = c.Convert_Image_To_Vector(IL[0])

if (os.path.exists('test_data.npy')):
    Data_test =np.load('test_data.npy')
else:
    L_test = c.ReadImages(TestFolder)
    Data_test = c.Convert_Image_To_Vector(L_test[0])




#print('len of Folders = ',len(IL[0]))
#print(IL[1])
#c.SaveMetaData(IL[1])


#MetaData = c.LoadMetaData('Apple.txt')
#print(MetaData)
#Acc = c.CheckFoledOfImages(Data[0],'SVM_Gender_Model.dat',MetaData)
#print(Acc)
model=c.CreateModel(Data,Data_test)

accy=c.calculate_accuracy(Data_test,model)
print('acc =',accy)
'''
'''
img = cv2.imread('4.jpg',0)
test_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
test_img = test_img.reshape(IMG_SIZE, IMG_SIZE, 1)
prediction = model.predict([test_img])[0]
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
ax.imshow(img,cmap='gray')
print(f"scab: {prediction[0]}, rot: {prediction[1]}, cedar: {prediction[2]}, health: {prediction[3]}")
print(max(prediction))

IL = c.ReadImages(FP)
c.SaveMetaData(IL[1])
MetaData = c.LoadMetaData('MetaData/Apple.txt')

print(MetaData)

Data=c.read_folder('Test')

Acc = c.CheckFoledOfImages(Data,'Apple',MetaData)
print(Acc)

'''

#c.TestModel(TestFolder,'SVM_Gender_Model.dat')
#DataSetFunctions.new_Train(TrainFolder,TestFolder,'Apple_Test')
#Tracking.Create_New_Track('Apdsd','Apple')


#DataSetFunctions.single_image('E:/GP/Test/0bc40cc3-6a85-480e-a22f-967a866a56a1___JR_FrgE.S 2784_270deg.JPG','Apple')
