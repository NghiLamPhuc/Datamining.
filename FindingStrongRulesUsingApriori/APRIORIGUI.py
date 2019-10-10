from PyQt5 import QtCore, QtGui, QtWidgets, uic
import read_file, write_file, Frequent_Itemset, Strong_rules, make_folder
from datetime import datetime, timedelta
import example
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('GUI.ui', self)

        openIcon = QtGui.QIcon('./GUIimage/openIcon')
        saveIcon = QtGui.QIcon('./GUIimage/saveIcon')
        createDataIcon = QtGui.QIcon('./GUIimage/randomFileIcon')
        runIcon = QtGui.QIcon('./GUIimage/runIcon')
        resIcon = QtGui.QIcon('./GUIimage/saveResIcon')
        pixmapLogo = QtGui.QPixmap('./GUIimage/logoIcon')
        
        self.btnImport.setIcon(openIcon)
        self.btnSave.setIcon(resIcon)
        self.btnExport.setIcon(saveIcon)
        self.btnGenerateData.setIcon(createDataIcon)
        self.btnApriori.setIcon(runIcon)
        self.labelLogo.setPixmap(pixmapLogo)

        self.btnApriori.clicked.connect(self.on_Apriori_clicked)
        self.btnSave.clicked.connect(self.on_Save_clicked)
        self.btnImport.clicked.connect(self.on_Import_clicked)
        self.btnExport.clicked.connect(self.on_Export_clicked)
        self.btnGenerateData.clicked.connect(self.on_Generate_clicked)
        
        self.doubleSpinBoxMinsupp.setValue(0.55)
        self.doubleSpinBoxMinconf.setValue(1.00)
    

    def on_Generate_clicked(self):
        example.create_data()
        self.plainTextInput.clear()
        fileDir = './input/generate.txt'
        if fileDir:
            with open(fileDir, 'r', encoding = 'utf-8') as f:
                count = 0
                for line in f:
                    row = '{}'.format(line)
                    count += 1
                    self.plainTextInput.insertPlainText(row)
            self.labelInput.setText('Có {} dòng.'.format(count) )
            self.labelInputName.setText('{}'.format(fileDir.split('/')[-1]) )

    def on_Export_clicked(self):
        inputDir = './input/'
        (dataPath, _) = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', inputDir, '*.txt')
        if dataPath:
            data = self.plainTextInput.toPlainText()
            with open(dataPath, 'w', encoding = 'utf-8') as f:
                f.write(data)

    def on_Import_clicked(self):
        self.labelLog.clear()
        self.labelFreqIS.clear()
        self.labelMaxIS.clear()
        self.labelRules.clear()
        self.labelInput.clear()
        self.labelInputName.setText('Dữ liệu')

        self.plainTextInput.clear()
        self.plainTextFreqIS.clear()
        self.plainTextMaxIS.clear()
        self.plainTextRules.clear()
        self.plainTextTopten.clear()
        inputDir = './input/'
        (dataPath, _) = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', inputDir, '*.txt')
        
        if dataPath:
            with open(dataPath, 'r', encoding = 'utf-8') as f:
                count = 0
                for line in f:
                    row = '{}'.format(line)
                    count += 1
                    self.plainTextInput.insertPlainText(row)
            self.labelInput.setText('Có {} dòng.'.format(count) )
            self.labelInputName.setText(dataPath.split('/')[-1])

    def on_Save_clicked(self):        
        minsupp = float(self.doubleSpinBoxMinsupp.text())
        minconf = float(self.doubleSpinBoxMinconf.text())
        inputName = self.labelInputName.text()
        outDir = './OUTPUT/minsup_{}_minconf_{}/{}/'.format(minsupp, minconf, inputName)
        freqISName = 'Tap_Phu_Pho_Bien.txt'
        maxISName = 'Tap_Phu_Toi_Dai.txt'
        rulesName = 'Luat_Ket_Hop.txt'
        topTenName = '10_Luat_conf_Cao_Nhat.txt'
        make_folder.create_folder(outDir)

        freqIS = self.plainTextFreqIS.toPlainText()
        maxIS = self.plainTextMaxIS.toPlainText()
        rules = self.plainTextRules.toPlainText()
        topTenRules = self.plainTextTopten.toPlainText()

        if freqIS == "" and maxIS == "" and rules == "" and topTenRules == "":
            # QtWidgets.QFileDialog.showEvent(,'Chưa có kết quả để lưu.')
            self.labelLog.setText('Chưa có kết quả.')
        else:
            with open(outDir + freqISName, 'w', encoding = 'utf-8') as freqFile:
                freqFile.write(str(freqIS))
            
            with open(outDir + maxISName, 'w', encoding = 'utf-8') as maxFile:
                maxFile.write(str(maxIS))

            with open(outDir + rulesName, 'w', encoding = 'utf-8') as ruleFile:
                ruleFile.write(str(rules))

            with open(outDir + topTenName, 'w', encoding = 'utf-8') as topTenFile:
                topTenFile.write(str(topTenRules))
    
            self.labelLog.setText('Đã lưu.')
        
    
    def on_Apriori_clicked(self):
        if self.plainTextInput.toPlainText() == "":
            self.labelLog.setText('Chưa tải dữ liệu lên.')
        else:
            # self.labelLog.setText('Chờ chút nheee.')
            # Plain Text 2
            self.plainTextFreqIS.clear()
            self.plainTextMaxIS.clear()
            self.plainTextRules.clear()
            self.plainTextTopten.clear()

            minsupp = float(self.doubleSpinBoxMinsupp.text())
            minconf = float(self.doubleSpinBoxMinconf.text())
            inputText = self.plainTextInput.toPlainText()
            inputDict = read_file.str_to_dict(inputText, ', ')
            
            start = datetime.now()

            freqISList = Frequent_Itemset.get_all_possible_itemset(inputDict, minsupp)
            maxISList = Frequent_Itemset.apriori(freqISList, minsupp)
            (ruleList, topTenRules) = Strong_rules.get_all_strong_rule_2(inputDict, maxISList, minconf)
            
            exeTime = (datetime.now() - start).total_seconds()
            
            self.labelLog.setText(str(timedelta(seconds = exeTime)))

            if not freqISList:
                self.labelLog.setText('Không có tập phủ phổ biến.')
            else:
                for iS in freqISList:
                    tempStr = ''
                    for item in range(len(iS) - 1):
                        tempStr += iS[item] + ', '
                    tempStr += iS[-1]
                    row = '{}\n'.format(tempStr)
                    self.plainTextFreqIS.insertPlainText(row)
                self.labelFreqIS.setText('Có {} tập phủ phổ biến.'.format(len(freqISList)) )

            # Plain Text 2
                # maxISList = Frequent_Itemset.apriori(freqISList, minsupp)
                if maxISList:
                    for iMax in maxISList:
                        tempStr = ''
                        for item in range(len(iMax) - 1):
                            tempStr += iMax[item] + ', '
                        tempStr += iMax[-1]
                        row = '{}\n'.format(tempStr)
                        self.plainTextMaxIS.insertPlainText(row)
                    self.labelMaxIS.setText('Có {} tập phủ phổ biến tối đại.'.format(len(maxISList)) )
            # Plain Text 3
                    # (ruleList, topTenRules) = Strong_rules.get_all_strong_rule_2(inputDict, maxISList, minconf)
                    
                    if ruleList:
                        for rule in ruleList:
                            row = '{}\n'.format(rule)
                            self.plainTextRules.insertPlainText(row)
                        
                        for rule10 in topTenRules:
                            row = '{}\n'.format(rule10)
                            self.plainTextTopten.insertPlainText(row)
                        
                        self.labelRules.setText('Có {} luật kết hợp.'.format(len(ruleList)) )

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.setWindowTitle('KHAI PHÁ LUẬT KẾT HỢP BẰNG APRIORI')
    window.show()
    sys.exit(app.exec_())

