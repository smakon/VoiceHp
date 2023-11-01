from PyQt5.QtWidgets import QApplication, QWidget
import sys
from PyQt5 import uic
import configparser

config = configparser.ConfigParser()
cmd_list_open = list()
cmd_list_kill = list()
cmd_list_say = list()
result = ''
massive_num = int()
class App(QWidget):

    def __init__(self):
        super(App, self).__init__()
        self.start()
        self.click()
        self.add_el_del()
        self.add_el_red()
        self.ui.stackedWidget.setCurrentIndex(2)

    def start(self):
        self.ui = uic.loadUi("main.ui")
        self.ui.show()
    def click(self):
        self.ui.cfg_bot.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.foo_creat.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.foo_del.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.foo_red_page_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.save_bot_name.clicked.connect(lambda: self.save_bot_name_change())
        self.ui.creat_cmd.clicked.connect(lambda: (self.craete_command(True), self.add_el_red(), self.add_el_del()))
        self.ui.creat_cmd_2.clicked.connect(lambda: (self.craete_command(False), self.add_el_red(), self.add_el_del()))
        self.ui.creat_cmd_3.clicked.connect(lambda: (self.craete_command(None), self.add_el_red(), self.add_el_del()))
        self.ui.del_foo_btn.clicked.connect(lambda: (self.delete_foo(1), self.add_el_red(), self.add_el_del()))
        self.ui.del_foo_btn_2.clicked.connect(lambda: (self.delete_foo(2), self.add_el_red(), self.add_el_del()))
        self.ui.del_foo_btn_3.clicked.connect(lambda: (self.delete_foo(3), self.add_el_red(), self.add_el_del()))
        self.ui.red_foo_btn_3.clicked.connect(lambda: (self.get_item(), self.add_el_red(), self.add_el_del()))
        self.ui.massiv_5.itemClicked.connect(self.listwidgetclicked_)
        self.ui.massiv_4.itemClicked.connect(self.listwidgetclicked_1)
        self.ui.massiv_6.itemClicked.connect(self.listwidgetclicked_2)
    def save_bot_name_change(self):
        config.read('example.ini', encoding='utf-8')
        config['DEFAULT'] = {'bot_n': f'{self.ui.name_line.text()}'}
        with open('example.ini', 'w', encoding='utf8') as configfile:
            config.write(configfile)

    def craete_command(self, bool):
        cmd_count = 0
        config.read("example.ini", encoding="utf-8")
        cmd_count += 1
        self.b = bool
        if self.b == True:
            cmd_count += int(config['DEFAULT']['cmd_count_save_open'])
            config['COMMANDS_OPEN_' + str(cmd_count - 1)] = {'cmd_name': f'{self.ui.cmd_name.text()}',
                                                             'prog_name': f'{self.ui.prog_n.text()}'}
            with open("example.ini", 'a+', encoding='utf8') as file:
                config.write(file)

            config['DEFAULT']['cmd_count_save_open'] = str(cmd_count)
            with open("example.ini", 'w', encoding='utf8') as file:
                config.write(file)
        elif self.b == False:
            cmd_count += int(config['DEFAULT']['cmd_count_save_kill'])
            config['COMMANDS_KILL_' + str(cmd_count - 1)] = {'cmd_name': f'{self.ui.cmd_name_2.text()}',
                                                             'prog_name': f'{self.ui.prog_n_2.text()}'}
            with open("example.ini", 'a+', encoding='utf8') as file:
                config.write(file)

            config['DEFAULT']['cmd_count_save_kill'] = str(cmd_count)
            with open("example.ini", 'w', encoding='utf8') as file:
                config.write(file)
        elif self.b == None:
            cmd_count += int(config['DEFAULT']['cmd_count_save_say'])
            config['COMMANDS_SAY_' + str(cmd_count - 1)] = {'cmd_name': f'{self.ui.cmd_name_3.text()}',
                                                            'prog_name': f'{self.ui.prog_n_3.text()}'}
            with open("example.ini", 'a+', encoding='utf8') as file:
                config.write(file)

            config['DEFAULT']['cmd_count_save_say'] = str(cmd_count)
            with open("example.ini", 'w', encoding='utf8') as file:
                config.write(file)

    def add_el_del(self):
        global cmd_list_open, cmd_list_say, cmd_list_kill

        cmd_list_open = []
        cmd_list_kill = []
        cmd_list_say = []
        self.ui.massiv.clear()
        self.ui.massiv_2.clear()
        self.ui.massiv_3.clear()

        config.read('example.ini', encoding='utf-8')
        for i in range(int(config['DEFAULT']['cmd_count_save_open'])):
            if config[f'COMMANDS_OPEN_{i}']['cmd_name'] != "None":
                cmd_list_open.append(config[f'COMMANDS_OPEN_{i}']['cmd_name'])
        for i in range(len(cmd_list_open)):
            self.ui.massiv.addItem(cmd_list_open[i])
        for i in range(int(config['DEFAULT']['cmd_count_save_kill'])):
            if config[f'COMMANDS_KILL_{i}']['cmd_name'] != "None":
                cmd_list_kill.append(config[f'COMMANDS_KILL_{i}']['cmd_name'])

        for i in range(len(cmd_list_kill)):
            self.ui.massiv_2.addItem(cmd_list_kill[i])

        for i in range(int(config['DEFAULT']['cmd_count_save_say'])):
            if config[f'COMMANDS_SAY_{i}']['cmd_name'] != "None":
                cmd_list_say.append(config[f'COMMANDS_SAY_{i}']['cmd_name'])

        for i in range(len(cmd_list_say)):
            self.ui.massiv_3.addItem(cmd_list_say[i])

        return cmd_list_open, cmd_list_kill, cmd_list_say


    def delete_foo(self, num):
        global cmd_list_open, cmd_list_say, cmd_list_kill
        if num == 1:
            current = self.ui.massiv.currentRow()
            if cmd_list_open[current] in cmd_list_open:
                for i in range(int(config['DEFAULT']['cmd_count_save_open'])):
                    if config[f'COMMANDS_OPEN_{i}']['cmd_name'] == cmd_list_open[current]:
                        config[f'COMMANDS_OPEN_{i}']['cmd_name'] = "None"
                        config[f'COMMANDS_OPEN_{i}']['prog_name'] = "None"
                        with open("example.ini", 'w', encoding='utf8') as file:
                            config.write(file)

            self.ui.massiv.takeItem(current)
        elif num == 2:
            current = self.ui.massiv_2.currentRow()
            if cmd_list_kill[current] in cmd_list_kill:
                for i in range(int(config['DEFAULT']['cmd_count_save_kill'])):
                    if config[f'COMMANDS_KILL_{i}']['cmd_name'] == cmd_list_kill[current]:
                        config[f'COMMANDS_KILL_{i}']['cmd_name'] = "None"
                        config[f'COMMANDS_KILL_{i}']['prog_name'] = "None"
                        with open("example.ini", 'w', encoding='utf8') as file:
                            config.write(file)

            self.ui.massiv_2.takeItem(current)
        elif num == 3:
            current = self.ui.massiv_3.currentRow()
            if cmd_list_say[current] in cmd_list_say:
                for i in range(int(config['DEFAULT']['cmd_count_save_say'])):
                    if config[f'COMMANDS_SAY_{i}']['cmd_name'] == cmd_list_say[current]:
                        config[f'COMMANDS_SAY_{i}']['cmd_name'] = "None"
                        config[f'COMMANDS_SAY_{i}']['prog_name'] = "None"
                        with open("example.ini", 'w', encoding='utf8') as file:
                            config.write(file)
            self.ui.massiv_3.takeItem(current)


    def add_el_red(self):
        global cmd_list_open, cmd_list_say, cmd_list_kill

        cmd_list_open = []
        cmd_list_kill = []
        cmd_list_say = []
        self.ui.massiv_4.clear()
        self.ui.massiv_5.clear()
        self.ui.massiv_6.clear()

        config.read('example.ini', encoding='utf-8')
        for i in range(int(config['DEFAULT']['cmd_count_save_open'])):
            cmd_list_open.append(config[f'COMMANDS_OPEN_{i}']['cmd_name'])

        for i in range(len(cmd_list_open)):
            self.ui.massiv_5.addItem(cmd_list_open[i])

        for i in range(int(config['DEFAULT']['cmd_count_save_kill'])):
            cmd_list_kill.append(config[f'COMMANDS_KILL_{i}']['cmd_name'])

        for i in range(len(cmd_list_kill)):
            self.ui.massiv_4.addItem(cmd_list_kill[i])

        for i in range(int(config['DEFAULT']['cmd_count_save_say'])):
            cmd_list_say.append(config[f'COMMANDS_SAY_{i}']['cmd_name'])

        for i in range(len(cmd_list_say)):
            self.ui.massiv_6.addItem(cmd_list_say[i])

        return cmd_list_open, cmd_list_kill, cmd_list_say

    def listwidgetclicked_(self, item):
        global massive_num
        self.ui.cmd_name_lab.setText(f'{item.text()}')
        massive_num = 5
        return massive_num

    def listwidgetclicked_1(self, item):
        global massive_num
        self.ui.cmd_name_lab.setText(f'{item.text()}')
        massive_num = 4
        return massive_num
    def listwidgetclicked_2(self, item):
        global massive_num
        self.ui.cmd_name_lab.setText(f'{item.text()}')
        massive_num = 6
        return massive_num

    def get_item(self):
        global massive_num
        config.read("example.ini", encoding="utf-8")
        if massive_num == 6:
            for i in range(int(config["DEFAULT"]["cmd_count_save_say"])):
                if self.ui.cmd_name_lab.text() == config[f'COMMANDS_SAY_{i}']['cmd_name']:
                    config[f'COMMANDS_SAY_{i}'] = {'cmd_name': f'{self.ui.cmd_name_red.text()}',
                                                'prog_name': f'{self.ui.prog_n_red.text()}'}

                    with open("example.ini", 'w', encoding='utf8') as file:
                        config.write(file)
        elif massive_num == 5:
            for i in range(int(config["DEFAULT"]["cmd_count_save_open"])):
                if self.ui.cmd_name_lab.text() == config[f'COMMANDS_OPEN_{i}']['cmd_name']:
                    config[f'COMMANDS_OPEN_{i}'] = {'cmd_name': f'{self.ui.cmd_name_red.text()}',
                                                'prog_name': f'{self.ui.prog_n_red.text()}'}

                    with open("example.ini", 'w', encoding='utf8') as file:
                        config.write(file)
        elif massive_num == 4:
            for i in range(int(config["DEFAULT"]["cmd_count_save_kill"])):
                if self.ui.cmd_name_lab.text() == config[f'COMMANDS_KILL_{i}']['cmd_name']:
                    config[f'COMMANDS_KILL_{i}'] = {'cmd_name': f'{self.ui.cmd_name_red.text()}',
                                                'prog_name': f'{self.ui.prog_n_red.text()}'}

                    with open("example.ini", 'w', encoding='utf8') as file:
                        config.write(file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()