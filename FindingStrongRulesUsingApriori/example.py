import random
import write_file

def create_data():
        ## mỗi item random từ 0->50
    nameList = ['Bia', 'Nước uống có cồn', 'Nước ngọt', 'Nước suối', 'Nước ép trái cây', 'Nước yến', 'Cà phê', 'Trà', 'Sữa trái cây', 'Sữa tươi', 'Sữa đậu nành', 'Sữa đặc', 'Sữa chua', 'Phô mai', 'Sữa bột', 'Bột ăn dặm', 'Sữa bột pha sẵn', 'Mì ăn liền', 'Cháo ăn liền', 'Phở ăn liền', 'Dầu ăn', 'Nước tương', 'Nước mắm', 'Tương ớt', 'Tương cà', 'Tương ngọt', 'Đường', 'Muối', 'Bột ngọt', 'Hạt nêm', 'Dầu hào', 'Snack', 'Bánh quy', 'Bánh trứng', 'Bánh bông lan', 'donut', 'Bánh xốp', 'Bánh gạo', 'Bánh que', 'Bánh quế', 'Socola', 'Trái cây sấy', 'Kẹo', 'Khô bò', 'Hạt các loại', 'Dầu gội', 'Dầu xả', 'Sữa tắm', 'Sữa rửa mặt', 'Kem', 'Bàn chải đánh răng', 'Băng vệ sinh', 'Khăn giấy', 'Giấy vệ sinh', 'Khăn giấy ướt', 'Nước giặt', 'Bột giặt', 'Nước xả vải', 'Nước rửa chén', 'Tẩy rửa bồn cầu', 'Nước lau sàn', 'DD Lau bếp', 'DD Lau kính', 'Túi', 'Hộp đựng thực phẩm', 'Chén', 'Dĩa', 'Ly', 'Bình nước', 'Dao', 'Kéo', 'Thớt', 'Thau', 'Rổ', 'Túi đựng rác', 'Chổi', 'Cây lau nhà', 'Gạo', 'Ngũ cốc', 'Yến mạch', 'Mì', 'Nui' , 'Bún khô', 'Bột chế biến sẵn', 'Đồ đông lạnh', 'Đồ đóng hộp', 'Trái cây nhập khẩu']
    
    transDict = dict()
    for row in range(1000):
        numOfItem = random.randint(30, 50)
        transList = list()
        transList.append(row)
        for col in range(numOfItem):
            item = random.randint(0, len(nameList) - 1)
            transList.append(nameList[item])
        transDict[row] = transList

    fileName = 'generate.txt'
    fileDir = './input/'
    write_file.dict_to_txt(transDict, fileDir, fileName)# if fileName not in './Generate Input/' else fileName[]

def main():
    create_data()

if __name__=="__main__":main()