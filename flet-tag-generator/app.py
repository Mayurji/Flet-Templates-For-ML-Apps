import flet as ft
import spacy
from collections import Counter
from string import punctuation
global nlp
nlp = spacy.load("en_core_web_lg")

def main(page: ft.Page):

    def generate_tags(text):
        result = set()
        pos_tag = ['PROPN', 'ADJ', 'NOUN'] 
        doc = nlp(text.lower()) 
        for token in doc:
            if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
                continue
            if(token.pos_ in pos_tag):
                result.add(token.text)
        return ",".join(result)

    def update_md(e):
        """
        Updates the markdown(preview) when the text in the Textfield changes.

        :param e: the event that triggered the function
        """
        text = generate_tags(page.text_field.value)
        page.md.value = text
        page.update()

    # set the minimum width and height of the window.
    page.window_min_width = 478
    page.window_min_height = 389

    # set the width and height of the window.
    page.window_width = 620
    page.window_height = 720

    page.title = "Tag Generator"   # title of application/page
    page.theme_mode = "dark"
    page.appbar = ft.AppBar(
        title=ft.Text("Tag Generator", color=ft.colors.WHITE),    # title of the AppBar, with a white color
        center_title=True,          # we center the title
        bgcolor=ft.colors.BLUE_GREY_900,     # a color for the AppBar's background
    )
    
    page.text_field = ft.TextField(
        hint_text="Paste your text here...",  # the initial value in the field (a simple Markdown code to test)
        multiline=True,  # True means: it will be possible to have many lines of text
        expand=True,  # tells the field to 'expand' (take all the available space)
        border_color=ft.colors.TRANSPARENT,  # makes the border of the field transparent(invisible), creating an immersive effect
        autofocus=True
    )
    
    page.md = ft.TextField(
        hint_text='Tags',
        multiline=True,
        expand=True,
        border_color=ft.colors.TRANSPARENT,
        max_length=500
    )
    
    page.add(
        ft.Row(  # we use the row here, so everything fits on a line
            controls=[
                page.text_field, 
                ft.VerticalDivider(color=ft.colors.WHITE38),
                page.md,
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            height=page.window_height,
            #expand=True,  # we make it fill up all the available space
        ),  # a row containing our text_field on the LHS and Markdown on the RHS
        ft.Divider(thickness=1, color=ft.colors.WHITE),
        ft.Row([
                ft.ElevatedButton(
                    "Generate Tag",
                    on_click=update_md,
                    tooltip="paste the text",
                    icon=ft.icons.TEXT_FIELDS,
                )],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
    )

ft.app(target=main)