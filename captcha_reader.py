from gradio_client import Client, handle_file

def captcha_extraction():
    client = Client("docparser/Text_Captcha_breaker")
    result = client.predict(
        img_org=handle_file('new_captcha.jpg'),
        api_name="/predict"
    )
    return result
