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

        self.searchBtn.clicked.connect(self.searchBtnClicked)  # 검색 버튼 클릭 이벤트
        self.result_table.doubleClicked.connect(self.resultDoubleClicked)  # 테이블의 항목을 더블클릭 이벤트
        self.input_keyword.returnPressed.connect(self.searchBtnClicked)  # 키워드 입력 후 엔터 입력시 이벤트

    def resultDoubleClicked(self):  # 테이블 내 검색결과 더블클릭 시 호출
        selectRowNum = self.result_table.currentRow()  # 현재 선택되어 있는 행의 번호 반환
        newsUrl = self.result_table.item(selectRowNum, 1).text()  # 기사 중에서 링크만 추출
        # print(newsUrl)
        webbrowser.open(newsUrl)  # 선택된 링크를 웹브라우저에서 실행

    def searchBtnClicked(self):
        searchKeyword = self.input_keyword.text()  # 키워드 입력창에 입력된 키워드를 가져옴

        if searchKeyword == '':  # 사용자가 검색어를 입력하지 않았을때
            QMessageBox.warning(self, '경고!','검색어를 입력하신 후 실행해주세요.')
        else:
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
        # 테이블 내용 수정 금지
        self.result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

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