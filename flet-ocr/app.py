import flet as ft
import utils
import easyocr
from PIL import Image

def load_ocr():
    reader = easyocr.Reader(['en'])
    return reader

# todo: output as pdf | add error dialog to handle errors
def main(page: ft.Page):
    """
    App's entry point.

    :param page: The page object
    :type page: Page
    """
    global model
    model = load_ocr()

    page.title = "OCR"
    # page.window_always_on_top = True
    page.theme_mode = "dark"

    # set the minimum width and height of the window.
    page.window_min_width = 478
    page.window_min_height = 389

    # set the width and height of the window.
    page.window_width = 620
    page.window_height = 720

    # set the splash (a progress bar)
    page.splash = ft.ProgressBar(visible=False, color="yellow")

    page.file_picker = ft.FilePicker(on_result=utils.file_picker_result_import, on_upload=utils.on_upload_progress)
    # hide dialog in a overlay
    page.overlay.append(page.file_picker)

    # a dialog to be shown when saving/exporting (on web only)
    web_export_dialog = ft.AlertDialog(
        title=ft.Text("Save as..."),
        content=ft.Text("Choose a format for your file.\nTip: Press CANCEL to abort."),
        modal=True,
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions=[
            #ft.ElevatedButton(".md", on_click=lambda e: get_file_format(".md")),  # .md = Markdown file format
            ft.ElevatedButton(".txt", on_click=lambda e: get_file_format(".txt")),  # .txt = ft.Text file format
            #ft.ElevatedButton(".html", on_click=lambda e: get_file_format(".html")),  # .html = HTML file format
            # ft.TextButton(".pdf", on_click=lambda e: get_file_format(".pdf")),
            ft.TextButton("CANCEL", on_click=lambda e: get_file_format(None)),
        ],
    )

    def on_error(e):
        # page.dialog = utils.error_dialog
        # page.dialog.open = True
        # page.update()
        page.show_snack_bar(
            ft.SnackBar(ft.Text("Humm, seems like an error suddenly occurred! Please try again."), open=True),
        )

    page.on_error = on_error

    def get_file_format(file_format: str or None):
        """
        Closes the dialog, and calls the md_save with the file format specified by the user(in the alertdialog)

        :param file_format: The file format selected in the AlertDialog.

        Note:
            file_format=None, when the CANCEL button of the AlertDialog is triggered.
        """
        page.dialog.open = False
        page.update()
        if file_format is not None:
            md_save(file_format)
        else:
            page.show_snack_bar(ft.SnackBar(ft.Text("Operation cancelled successfully!"), open=True))

    def md_update(e):
        """
        Updates the markdown(preview) when the text in the Textfield changes.

        :param e: the event that triggered the function
        """
        page.md.value = page.text_field.value
        page.update()

    def extract_text(e):
        if page.image_field.src:
            page.text_field.value = "\n".join(model.readtext(page.image_field.src, detail=0, paragraph=True))
            page.update()
        else:
            on_error()

    def export_markdown_to_file(e):
        if page.web:
            page.dialog = web_export_dialog
            page.dialog.open = True
            page.update()
        else:
            page.file_picker.save_file(
                dialog_title="Save As...",
                file_type=ft.FilePickerFileType.CUSTOM,
                file_name="untitled.txt",
                allowed_extensions=["txt"]#, "md", 'html']
            )

    def md_save(file_format):
        """
        It takes the Text from the textarea (Left hand side section), saves it as a file in the assets' folder
        with the specified file_format, and opens the saved file in a new browser tab using a rel-path to the assets.

        :param file_format: The file format to be used when saving
        """
        try:
            file_name = "untitled"
            # to save as HTML file, we convert the Markdown to html using 'markdown2' library
            with open(f"assets/untitled{file_format}", "w") as f:  # save it in the assets folder
                if file_format == ".html":
                    import markdown2  # pip install markdown2
                    f.write(markdown2.markdown(page.text_field.value))
                else:
                    f.write(page.text_field.value)

            page.launch_url(f"/{file_name}{file_format}")  # open the file (already in the assets folder)
            page.show_snack_bar(ft.SnackBar(ft.Text(f"Success: File was saved to assets as '{file_name}'!"),
                                            open=True if not page.web else False))
        except ImportError as exc:
            print(exc)
            print("To create an HTML output, install the markdown2 python library, using `pip install markdown2!`")
        except Exception as exc:
            print(exc)
            page.show_snack_bar(ft.SnackBar(ft.Text(f"Error: {exc}!"), open=True))

    def change_theme(e):
        """
        When the button(to change theme) is clicked, the theme is changed, and the page is updated.

        :param e: The event that triggered the function
        """
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        page.update()

    # button to change theme_mode (from dark to light mode, or the reverse)
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

    page.appbar = ft.AppBar(
        title=ft.Text("OCR: Extracting Text From Image", color=ft.colors.WHITE),
        center_title=True,
        bgcolor=ft.colors.LIGHT_BLUE_700,
        actions=[theme_icon_button]
    )

    # you can move it to a file if you wish.
    test_image_file_path = f'assets/uploads/text.png'

    # the LHS of the editor
    page.image_field = ft.Image(
        src=test_image_file_path,
        expand=True,
        width=360,
        height=480,
        fit=ft.ImageFit.CONTAIN
    )

    # the RHS of the editor
    page.text_field = ft.Text(
        value="\n".join(model.readtext(test_image_file_path, detail=0, paragraph=True))
        #model.readtext(page.image_field.value),
    )

    page.add(
        ft.Row(
            [
                ft.Text("Import Image", style=ft.TextThemeStyle.TITLE_LARGE),
                ft.FilledButton(
                    "Import",
                    on_click=lambda _: page.file_picker.pick_files(
                        dialog_title="Import File...",
                        file_type=ft.FilePickerFileType.CUSTOM,
                        allow_multiple=False,
                        allowed_extensions=["png", "jpg", "jpeg"]
                    ),
                    tooltip="load a file",
                    icon=ft.icons.UPLOAD_FILE_ROUNDED
                ),
                ft.FilledButton(
                    "Export Text",
                    on_click=export_markdown_to_file,
                    tooltip="save as ft.Text file",
                    icon=ft.icons.SIM_CARD_DOWNLOAD_ROUNDED
                ),
                ft.Text("Preview", style=ft.TextThemeStyle.TITLE_LARGE)
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
        ft.Divider(thickness=1, color=ft.colors.LIGHT_BLUE_ACCENT),
        ft.Row(
            [
                page.image_field,
                ft.VerticalDivider(color=ft.colors.LIGHT_BLUE_ACCENT),
                ft.Container(
                    ft.Column(
                        [
                            page.text_field
                        ],
                        scroll=ft.ScrollMode.HIDDEN
                    ),
                    expand=True,
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.Padding(0, 12, 0, 0),
                )
                
            ],
            alignment=ft.alignment.top_left,
            height=page.window_height,
        ),
        ft.Divider(thickness=1, color=ft.colors.LIGHT_BLUE_ACCENT),
        ft.Row([
                ft.ElevatedButton(
                    "Extract Text",
                    on_click=extract_text,
                    tooltip="extract the text from an image",
                    icon=ft.icons.TEXT_FIELDS,
                )],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        ),
    )


# (running the app)
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets", upload_dir='assets/uploads')