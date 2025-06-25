import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP - Esame del 14/09/2022"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - Esame del 14/09/2022", color="red", size=24)
        self._page.controls.append(self._title)

        #ROW1
        self._txtInDurata = ft.TextField(label="Durata")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([
            ft.Container(self._txtInDurata, width=300),
            ft.Container(self._btnCreaGrafo, width=300)
        ], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        #ROW2
        self._ddAlbum = ft.Dropdown(label="Album")
        self._btnAnalisiComp = ft.ElevatedButton(text = "Analisi Componente",
                                                 on_click=self._controller.handleAnalisiComp)

        row2 = ft.Row([
            ft.Container(self._ddAlbum, width=300),
            ft.Container(self._btnAnalisiComp, width=300)
        ], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        #ROW3
        self._txtInSoglia = ft.TextField(label="Soglia")
        self._btnSetAlbum = ft.ElevatedButton(text="Set di Album",
                                               on_click=self._controller.handleGetSetAlbum)
        row3 = ft.Row([
            ft.Container(self._txtInSoglia, width=300),
            ft.Container(self._btnSetAlbum, width=300)
        ], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
