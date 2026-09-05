import flet as ft
from datetime import datetime, timedelta

horarios_ida = ["06:02", "06:17", "06:31", "06:45", "07:00", "07:20", "07:41", "08:09", "08:39", "09:14", "09:44", "10:26", "11:32", "12:29", "13:24", "14:24", "15:14", "16:19", "16:49", "17:24", "17:54", "18:26", "18:50", "19:14", "19:56"]
horarios_regreso = ["07:12", "07:42", "08:28", "09:20", "10:15", "11:12", "12:24", "13:24", "14:30", "15:00", "15:25", "15:50", "16:28", "16:48", "17:08", "17:33", "17:57", "18:22", "18:54", "19:35", "20:24"]

def main(page: ft.Page):
    page.title = "Ruta Dichato"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme = ft.Theme(color_scheme_seed="indigo")

    def cambiar_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if switch_tema.value else ft.ThemeMode.LIGHT
        page.update()

    def cambiar_color(e):
        colores = {
            "Índigo": "indigo",
            "Rosado": "pink",
            "Verde Bosque": "green"
        }
        page.theme = ft.Theme(color_scheme_seed=colores[dropdown_color.value])
        page.update()

    switch_tema = ft.Switch(label="Modo Oscuro")
    switch_tema.on_change = cambiar_tema
    
    dropdown_color = ft.Dropdown(
        label="Color Principal",
        options=[
            ft.DropdownOption("Índigo"),
            ft.DropdownOption("Rosado"),
            ft.DropdownOption("Verde Bosque"),
        ],
        value="Índigo",
        width=200
    )
    dropdown_color.on_change = cambiar_color

    page.appbar = ft.AppBar(
        title=ft.Text("Ruta Dichato", weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor="surfacevariant"
    )

    # Nuevo sistema de configuración integrado (sin ventanas flotantes)
    panel_config = ft.ExpansionTile(
        title=ft.Text("Personalización Visual", weight=ft.FontWeight.BOLD),
        subtitle=ft.Text("Ajusta los colores y el modo oscuro"),
        leading=ft.Icon(ft.Icons.PALETTE, color="primary"),
        controls=[
            ft.Container(
                padding=20,
                content=ft.Row(
                    [switch_tema, dropdown_color],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    wrap=True
                )
            )
        ]
    )

    usuario_dropdown = ft.Dropdown(
        label="Selecciona el viajero",
        options=[
            ft.DropdownOption("Mauro (UdeC)"),
            ft.DropdownOption("Bianca (Duoc)")
        ],
        value="Mauro (UdeC)",
        width=250,
        border_radius=10
    )
    
    hora_clase = ft.TextField(
        label="Hora de entrada (HH:MM)",
        value="08:15",
        width=250,
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        prefix_icon=ft.Icons.ACCESS_TIME
    )
    
    resultado_ida = ft.Text("", size=16, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)

    def calcular_ida(e):
        usuario = usuario_dropdown.value
        tiempo_viaje = 80
        tiempo_paradero = 4
        tiempo_caminata = 15 if "Mauro" in usuario else 35
        minutos_anticipacion = tiempo_viaje + tiempo_caminata + tiempo_paradero
        
        try:
            hora_c = datetime.strptime(hora_clase.value, "%H:%M")
            hora_limite_salida = hora_c - timedelta(minutes=minutos_anticipacion)
            
            micro_elegida = None
            for horario in reversed(horarios_ida):
                hora_micro = datetime.strptime(horario, "%H:%M")
                if hora_micro <= hora_limite_salida:
                    micro_elegida = horario
                    break
            
            if micro_elegida:
                hora_paradero = (datetime.strptime(micro_elegida, "%H:%M") + timedelta(minutes=tiempo_paradero)).strftime("%H:%M")
                resultado_ida.value = f"Toma la micro de las {micro_elegida} hrs.\nPasará por tu paradero a las {hora_paradero} aprox."
                resultado_ida.color = "green"
            else:
                resultado_ida.value = "No hay micros para llegar a esa hora."
                resultado_ida.color = "error"
        except ValueError:
            resultado_ida.value = "Formato inválido. Usa HH:MM."
            resultado_ida.color = "orange"
        page.update()

    btn_ida = ft.FilledButton("Calcular Viaje", on_click=calcular_ida, width=200)

    tarjeta_ida = ft.Card(
        elevation=2,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Hacia Concepción", size=20, weight=ft.FontWeight.BOLD, color="primary"),
                    usuario_dropdown,
                    hora_clase,
                    btn_ida,
                    resultado_ida
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )
    )

    resultado_regreso = ft.Text("", size=16, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)

    def calcular_regreso(e):
        hora_actual = datetime.now()
        encontrada = False
        for horario in horarios_regreso:
            hora_micro = datetime.strptime(horario, "%H:%M").replace(
                year=hora_actual.year, month=hora_actual.month, day=hora_actual.day
            )
            if hora_micro > hora_actual:
                resultado_regreso.value = f"Próxima micro: {horario} hrs.\n(Hora actual: {hora_actual.strftime('%H:%M')})"
                resultado_regreso.color = "primary"
                encontrada = True
                break
        if not encontrada:
            resultado_regreso.value = "Ya no hay más micros de regreso por hoy."
            resultado_regreso.color = "error"
        page.update()

    btn_regreso = ft.FilledButton("Ver Próxima Micro", on_click=calcular_regreso, width=200, icon=ft.Icons.DIRECTIONS_BUS)

    tarjeta_regreso = ft.Card(
        elevation=2,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Regreso a Dichato", size=20, weight=ft.FontWeight.BOLD, color="primary"),
                    btn_regreso,
                    resultado_regreso
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )
    )

    page.add(
        panel_config,
        ft.Container(height=5),
        tarjeta_ida,
        ft.Container(height=5),
        tarjeta_regreso
    )

ft.run(main)