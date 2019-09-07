import make_folder

# Ghi list ra text, neu can index thi them bien i.
def list_to_txt_with_last_comma(List: list, folderName, name):
    make_folder.create_folder(folderName)
    if not List:
        print('Danh sach rong!')
        return
    
    with open(folderName + name, 'w', encoding = 'utf-8') as fout:
        for itemSet in List:
            for index in range(len(itemSet) - 1):
                fout.write('%s, ' % itemSet[index] )
            fout.write('%s' % itemSet[-1] )
            fout.write('\n')

def list_to_txt(List: list, folderName, name):
    make_folder.create_folder(folderName)
    if not List:
        print('Danh sach rong!')
        return
  
    with open(folderName + name, 'w', encoding = 'utf-8') as fout:
        for itemSet in List:
            fout.write('%s\n' % itemSet )
