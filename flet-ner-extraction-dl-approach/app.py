import flet as ft
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from collections import defaultdict
import json

global tokenizer, model
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

def main(page: ft.Page):

    def generate_ner(input_str):
        nlp = pipeline("ner", model=model, tokenizer=tokenizer)
        output = nlp(input_str)
        # for ent in doc.ents:
        #     output[ent.label_].add(ent.text)

        print(output)
        return output

    def entity_extraction(e):
        """
        Updates the markdown(preview) when the text in the Textfield changes.

        :param e: the event that triggered the function
        """
        text = generate_ner(page.text_field.value)
        page.md.value = json.dumps(text)
        page.update()

    # set the minimum width and height of the window.
    page.window_min_width = 478
    page.window_min_height = 389

    # set the width and height of the window.
    page.window_width = 620
    page.window_height = 720

    page.title = "Entity Extraction"   # title of application/page
    page.theme_mode = "dark"
    page.appbar = ft.AppBar(
        title=ft.Text("Entity Extraction", color=ft.colors.WHITE),    # title of the AppBar, with a white color
        center_title=True,          # we center the title
        bgcolor=ft.colors.BLUE_GREY_900,     # a color for the AppBar's background
    )
    
    page.text_field = ft.TextField(
        hint_text="Paste your text here...",  # the initial value in the field (a simple Markdown code to test)
        multiline=True,  # True means: it will be possible to have many lines of text
        expand=True,  # tells the field to 'expand' (take all the available space)
        border_color=ft.colors.TRANSPARENT,  # makes the border of the field transparent(invisible), creating an immersive effect
        autofocus=True,
    )
    
    page.md = ft.TextField(
        hint_text='Summarized Text',
        multiline=True,
        expand=True,
        border_color=ft.colors.TRANSPARENT,
        max_length=1000
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
                    "Generate NER",
                    on_click=entity_extraction,
                    tooltip="paste the text",
                    icon=ft.icons.TEXT_FIELDS,
                )],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
    )

ft.app(target=main)