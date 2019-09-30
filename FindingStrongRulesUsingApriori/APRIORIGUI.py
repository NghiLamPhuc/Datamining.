from PyQt5 import QtCore, QtGui, QtWidgets, uic
import read_file, write_file, Frequent_Itemset, Strong_rules, make_folder
from datetime import datetime

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('GUI.ui', self)
        
        openIcon = QtGui.QIcon('./GUIimage/openIcon')
        saveIcon = QtGui.QIcon('./GUIimage/saveIcon')
        self.btnImport.setIcon(openIcon)
        self.btnExport.setIcon(saveIcon)

        self.btnApriori.clicked.connect(self.on_Apriori_clicked)
        self.btnSave.clicked.connect(self.on_Save_clicked)
        self.btnImport.clicked.connect(self.on_Import_clicked)
        self.btnExport.clicked.connect(self.on_Export_clicked)
        self.doubleSpinBoxMinsupp.setValue(0.30)
        self.doubleSpinBoxMinconf.setValue(1.00)
    
    def on_Export_clicked(self):
        inputDir = './input/'
        (dataPath, _) = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', inputDir, '*.txt')
        if dataPath:
            data = self.plainTextInput.toPlainText()
            with open(dataPath, 'w', encoding = 'utf-8') as f:
                f.write(data)

    def on_Import_clicked(self):
        self.plainTextInput.clear()
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
            self.labelLog.setText('{}'.format(dataPath.split('/')[-1]) )

    def on_Save_clicked(self):        
        minsupp = float(self.doubleSpinBoxMinsupp.text())
        minconf = float(self.doubleSpinBoxMinconf.text())
        inputNameDir = self.labelLog.text()
        inputName = inputNameDir.split('/')[-1]
        
        outDir = './OUTPUT/minsup_{}_minconf_{}/{}/'.format(minsupp, minconf, inputName)
        freqISName = 'Tap_Phu_Pho_Bien.txt'
        maxISName = 'Tap_Phu_Toi_Dai.txt'
        rulesName = 'Luat_Ket_Hop.txt'
        topTenName = '10_Luat_conf_Cao_Nhat.txt'
        make_folder.create_folder(outDir)
        
        with open(outDir + freqISName, 'w', encoding = 'utf-8') as freqFile:
            freqFile.write(str(self.plainTextFreqIS.toPlainText()))
        
        with open(outDir + maxISName, 'w', encoding = 'utf-8') as maxFile:
            maxFile.write(str(self.plainTextMaxIS.toPlainText()))

        with open(outDir + rulesName, 'w', encoding = 'utf-8') as ruleFile:
            ruleFile.write(str(self.plainTextRules.toPlainText()))

        with open(outDir + topTenName, 'w', encoding = 'utf-8') as topTenFile:
            topTenFile.write(str(self.plainTextTopten.toPlainText()))
        
        # self.labelLog.setText('Đã lưu.')
        
    
    def on_Apriori_clicked(self):
        # Plain Text 2
        self.plainTextFreqIS.clear()
        self.plainTextMaxIS.clear()
        self.plainTextRules.clear()
        self.plainTextTopten.clear()

        minsupp = float(self.doubleSpinBoxMinsupp.text())
        minconf = float(self.doubleSpinBoxMinconf.text())
        inputText = self.plainTextInput.toPlainText()
        inputDict = read_file.str_to_dict(inputText, ', ')
        freqISList = Frequent_Itemset.get_all_possible_itemset(inputDict, minsupp)
        if not freqISList:
            self.plainTextFreqIS.insertPlainText('Không có tập phủ phổ biến.')
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
            maxISList = Frequent_Itemset.apriori(freqISList, minsupp)
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
                (ruleList, topTenRules) = Strong_rules.get_all_strong_rule_2(inputDict, maxISList, minconf)
                
                if ruleList:
                    for rule in ruleList:
                        row = '{}\n'.format(rule)
                        self.plainTextRules.insertPlainText(row)
                    
                    for rule10 in topTenRules:
                        row = '{}\n'.format(rule10)
                        self.plainTextTopten.insertPlainText(row)
                    
                    self.labelRules.setText('Có {} luật kết hợp.'.format(len(ruleList)) )




if __name__ == '__main__':
    import sys
    start = datetime.now()

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('Apriori')
    window.show()
    sys.exit(app.exec_())

    print(datetime.now() - start)
