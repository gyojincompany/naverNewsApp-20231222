import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

from naverApi import *

import webbrowser

form_class = uic.loadUiType("ui/naverNewsSearchAppUi.ui")[0]

class NaverAppWin(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("네이버뉴스 검색 앱")
        self.setWindowIcon(QIcon("img/newspaper.png"))
        self.statusBar().showMessage("Naver News Application v1.0")

        self.searchBtn.clicked.connect(self.searchBtnClicked)

    def searchBtnClicked(self):
        searchKeyword = self.input_keyword.text()  # 키워드 입력창에 입력된 키워드를 가져옴

        naverApi = NaverApi()  # NaverApi 클래스 객체 생성

        searchResult = naverApi.naverSearch("news", searchKeyword, 1, 50)
        # print(searchResult)

        # QTableWidget에 뉴스 결과 출력하기
        items = searchResult['items']
        self.outputResult(items)  # 테이블에 뉴스 검색 결과를 출력하는 함수 호출
        

    def outputResult(self, items):
        self.result_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.result_table.setColumnCount(2)  # 출력 테이블의 열 갯수 설정
        self.result_table.setRowCount(len(items))
        # 출력 테이블의 행 갯수 설정(items 내 원소 갯수 만큼 줄 갯수를 설정)
        self.result_table.setHorizontalHeaderLabels(['기사제목', '기사링크'])
        self.result_table.setColumnWidth(0, 400)  # 첫번째 열의 가로 넓이 지정
        self.result_table.setColumnWidth(1, 220)  # 두번째 열의 가로 넓이 지정

        for i, news in enumerate(items):
            newsTitle = self.clearTitle(news['title'])  # html 태그 삭제 함수 호출
            newsLink = news['originallink']

            self.result_table.setItem(i, 0, QTableWidgetItem(newsTitle))
            self.result_table.setItem(i, 1, QTableWidgetItem(newsLink))

    #  불필요한 html 태그들을 기사제목에서 삭제하는 함수
    def clearTitle(self, title):
        resultStr = title.replace('&quot', '').replace('<b>', '').replace('</b>', '').replace(';', '')
        return resultStr




app = QApplication(sys.argv)
win = NaverAppWin()
win.show()
app.exec_()