import flet as ft

def main(page: ft.Page):
    # 1. Configurações da página
    page.title = "Dashboard de Usuário"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    # 2. Elementos de texto e controle
    titulo = ft.Text(
        value="Painel de Controle", 
        size=28, 
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_400
    )
    
    mensagem_boas_vindas = ft.Text(
        value="Por favor, identifique-se abaixo.", 
        size=16, 
        color=ft.Colors.GREY_400
    )

    # Campo onde o usuário vai digitar o nome
    campo_nome = ft.TextField(
        label="Nome de Usuário",
        hint_text="Digite seu nome aqui...",
        border_color=ft.Colors.BLUE_400,
        width=300,
    )

    # Função que será chamada quando o botão for clicado
    def atualizar_dashboard(e):
        if campo_nome.value.strip() == "":
            mensagem_boas_vindas.value = "Por favor, digite um nome válido!"
            mensagem_boas_vindas.color = ft.Colors.RED_400
        else:
            mensagem_boas_vindas.value = f"Bem-vindo de volta, {campo_nome.value}! 🚀"
            mensagem_boas_vindas.color = ft.Colors.GREEN_400
            campo_nome.value = "" # Limpa o campo após inserir
            
        # O page.update() é essencial para aplicar as mudanças na tela
        page.update()

    # Botão de confirmação
    botao_inserir = ft.ElevatedButton(
        text="Inserir no Dashboard",
        icon=ft.Icons.CHECK,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_700,
        ),
        on_click=atualizar_dashboard
    )

    # 3. Layout do Dashboard (Card centralizado)
    dashboard_card = ft.Container(
        content=ft.Column(
            controls=[
                titulo,
                mensagem_boas_vindas,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # Espaçador
                campo_nome,
                botao_inserir
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        bgcolor=ft.Colors.SURFACE_VARIANT,
        padding=40,
        border_radius=15,
        animate_size=300, # Adiciona uma animação suave quando o texto mudar de tamanho
    )

    # 4. Adicionar o Dashboard à página
    page.add(dashboard_card)

if __name__ == "__main__":
    ft.app(target=main)
