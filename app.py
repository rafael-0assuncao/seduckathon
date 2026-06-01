import flet as ft

def main(page: ft.Page):
    # 1. Configurações básicas da janela/página
    page.title = "Meu Primeiro App Flet"
    page.theme_mode = ft.ThemeMode.DARK  # Pode ser DARK, LIGHT ou SYSTEM
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # 2. Criação dos componentes (Widgets)
    texto_boas_vindas = ft.Text(
        value="Olá, Flet!", 
        size=30, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.BLUE_ACCENT
    )
    
    botao_clique = ft.ElevatedButton(
        text="Clique aqui", 
        on_click=lambda e: print("Botão clicado!")
    )

    # 3. Adicionar os componentes à página
    page.add(
        texto_boas_vindas,
        botao_clique
    )

# 4. Inicialização do App
if __name__ == "__main__":
    # Para abrir como aplicativo nativo (Desktop/Mobile mockup)
    ft.app(target=main) 
    
    # Se preferir que abra direto no navegador, descomente a linha abaixo:
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER)
