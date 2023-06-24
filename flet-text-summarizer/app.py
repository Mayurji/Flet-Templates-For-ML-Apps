import flet as ft
from transformers import pipeline

def main(page: ft.Page):

    def load_model():
        model = pipeline("summarization", device=0, model='facebook/bart-large-cnn')
        return model

    def change_theme(e):
        """
        When the button(to change theme) is clicked, the theme is changed, and the page is updated.

        :param e: The event that triggered the function
        """
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        page.update()

    def generate_chunks(inp_str):
        max_chunk = 500
        inp_str = inp_str.replace('.', '.<eos>')
        inp_str = inp_str.replace('?', '?<eos>')
        inp_str = inp_str.replace('!', '!<eos>')
        
        sentences = inp_str.split('<eos>')
        current_chunk = 0 
        chunks = []
        for sentence in sentences:
            if len(chunks) == current_chunk + 1: 
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])

        return chunks

    def text_summarizer(e):
        """
        Updates the markdown(preview) when the text in the Textfield changes.

        :param e: the event that triggered the function
        """
        text = generate_chunks(page.text_field.value)
        page.md.value = model(text, max_length=750, min_length=30, do_sample=True)[0]['summary_text']
        page.update()


    theme_icon_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        selected_icon=ft.icons.DARK_MODE,
        icon_color=ft.colors.WHITE,
        selected_icon_color=ft.colors.BLACK,
        selected=False,
        icon_size=35,
        tooltip="change theme",
        on_click=change_theme,
    )

    global model 
    model = load_model()

    # set the minimum width and height of the window.
    page.window_min_width = 478
    page.window_min_height = 389

    # set the width and height of the window.
    page.window_width = 620
    page.window_height = 720

    page.title = "Text Summarizer"   # title of application/page
    page.theme_mode = "dark"
    page.appbar = ft.AppBar(
        title=ft.Text("Text Summarizer", color=ft.colors.WHITE),    # title of the AppBar, with a white color
        center_title=True,          # we center the title
        bgcolor=ft.colors.BLUE_GREY_900,     # a color for the AppBar's background
        actions=[theme_icon_button]
    )
    
    page.text_field = ft.TextField(
        hint_text="Paste your text here...",  # the initial value in the field (a simple Markdown code to test)
        multiline=True,  # True means: it will be possible to have many lines of text
        expand=True,  # tells the field to 'expand' (take all the available space)
        border_color=ft.colors.TRANSPARENT,  # makes the border of the field transparent(invisible), creating an immersive effect
        autofocus=True,
        max_length=1500,
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
                ft.VerticalDivider(color=ft.colors.BLACK),
                page.md,
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            height=page.window_height,
            #expand=True,  # we make it fill up all the available space
        ),  # a row containing our text_field on the LHS and Markdown on the RHS
        ft.Divider(thickness=1, color=ft.colors.BLACK),
        ft.Row([
                ft.ElevatedButton(
                    "Summarize",
                    on_click=text_summarizer,
                    tooltip="paste the text",
                    icon=ft.icons.TEXT_FIELDS,
                )],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
    )

ft.app(target=main)