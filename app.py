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
        color="blue400"  # String direta ao invés de ft.Colors
    )
    
    mensagem_boas_vindas = ft.Text(
        value="Por favor, identifique-se abaixo.", 
        size=16, 
        color="grey400"
    )

    # Campo onde o usuário vai digitar o nome
    campo_nome = ft.TextField(
        label="Nome de Usuário",
        hint_text="Digite seu nome aqui...",
        border_color="blue400",
        width=300,
    )

    # Função que será chamada quando o botão for clicado
    def atualizar_dashboard(e):
        if campo_nome.value.strip() == "":
            mensagem_boas_vindas.value = "Por favor, digite um nome válido!"
            mensagem_boas_vindas.color = "red400"
        else:
            mensagem_boas_vindas.value = f"Bem-vindo de volta, {campo_nome.value}! 🚀"
            mensagem_boas_vindas.color = "green400"
            campo_nome.value = "" # Limpa o campo após inserir
            
        # Atualiza a página para aplicar as mudanças
        page.update()

    # Botão de confirmação corrigido
    botao_inserir = ft.ElevatedButton(
        content=ft.Text("Inserir no Dashboard", color="white"),
        icon=ft.Icons.CHECK,
        style=ft.ButtonStyle(
            bgcolor="blue700",
        ),
        on_click=atualizar_dashboard
    )

    # 3. Layout do Dashboard (Card centralizado)
    dashboard_card = ft.Container(
        content=ft.Column(
            controls=[
                titulo,
                mensagem_boas_vindas,
                ft.Divider(height=20, color="transparent"), # Espaçador seguro
                campo_nome,
                botao_inserir
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        bgcolor="#20242C", # Cor escura customizada em Hexadecimal (substitui o SURFACE_VARIANT)
        padding=40,
        border_radius=15,
        animate_size=300,
    )

    # 4. Adicionar o Dashboard à página
    page.add(dashboard_card)

# Inicialização do App
if __name__ == "__main__":
    ft.app(target=main)
