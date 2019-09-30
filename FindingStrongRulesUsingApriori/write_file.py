import make_folder

# Ghi list ra text, neu can index thi them bien i.
def list_to_txt_with_last_comma(List: list, folderName, name):
    make_folder.create_folder(folderName)
    if not List:
        print('Danh sach rong! ' + name)
        return
    
    with open(folderName + name, 'w', encoding = 'utf-8') as fout:
        for itemSet in List:
            for index in range(len(itemSet) - 1):
                fout.write('{0}, '.format(itemSet[index]) )
            fout.write('{0}'.format(itemSet[-1]) )
            fout.write('\n')

def list_to_txt(List: list, folderName, name):
    make_folder.create_folder(folderName)
    if not List:
        print('Danh sach rong! ' + name)
        return
  
    with open(folderName + name, 'w', encoding = 'utf-8') as fout:
        for item in List:
            fout.write('{0}\n'.format(item))

def dict_to_txt(Dict: dict, folderName, name):
    make_folder.create_folder(folderName)
    if not Dict:
        print('Dict rỗng!' + name)
        return

    with open(folderName + name, 'w', encoding = 'utf-8') as fout:
        for (key, values) in Dict.items():
            row = ''
            for indexItem in range(len(values) - 1):
                fout.write('{0}, '.format(values[indexItem]) )
            fout.write('{0}'.format(values[-1]) )
            fout.write('\n')
