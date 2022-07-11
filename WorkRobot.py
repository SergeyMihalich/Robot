import requests

class WorkRobot():
    res_r_tok = None
    r_tok = None
    r_log = None
    res_my_tok = None

    def get_token_temporary(self, url_token_temporary):
        headers = {'Host': 'www.reddit.com'}
        self.r_tok = requests.get(url_token_temporary, headers=headers)
        if 'csrf_token' in self.r_tok.text and self.r_tok.status_code == 200:
            print('токен "csrf_token" найден, status_code - 200')
            teg_index = self.r_tok.text.index('csrf_token')
            self.res_r_tok = self.r_tok.text[teg_index + 19: teg_index + 59]
        else:
            raise AssertionError(f'токена "csrf_token" нет, status_code - {self.r_tok.status_code}')

    def login(self, username, password, url_token_temporary, url_login):
        self.get_token_temporary(url_token_temporary)
        headers = {'Host': 'www.reddit.com', 'Content-Length': '125'}
        body = f'csrf_token={self.res_r_tok}&otp=&password={password}&dest=https%3A%2F%2Fwww.reddit.com&username={username}'
        self.r_log = requests.post(url_login, headers=headers, cookies=self.r_tok.cookies, data=body)

    def get_my_token(self, url_my_token):
        headers = {'Host': 'www.reddit.com'}
        r_get_my_tok = requests.get(url_my_token, headers=headers, cookies=self.r_log.cookies)
        if 'accessToken' in r_get_my_tok.text and r_get_my_tok.status_code == 200:
            teg_index = r_get_my_tok.text.index('accessToken')
            self.res_my_tok = r_get_my_tok.text[teg_index + 14: teg_index + 58]
        else:
            raise AssertionError(f'токена "" нет, status_code - {r_get_my_tok.status_code}')

    def write_message(self, message_id, comment, url_write_message, url_my_token):
        res_my_tok = self.get_my_token(url_my_token)
        headers = {'Host': 'oauth.reddit.com', 'Content-Length': '203', 'Authorization': f'Bearer {res_my_tok}',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
        body = f'api_type=json&return_rtjson=true&thing_{message_id}&text&richtext_json=%7B%22document%22%3A%5B%7B%22e%22%3A%22par%22%2C%22c%22%3A%5B%7B%22e%22%3A%22text%22%2C%22t%22%3A%22{comment}%22%7D%5D%7D%5D%7D'
        requests.post(url_write_message, headers=headers, data=body)

    def del_message(self, message_id, url_del_message, url_my_token):
        res_my_tok = self.get_my_token(url_my_token)
        headers = {'Host': 'oauth.reddit.com', 'Authorization': f'Bearer {res_my_tok}',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'}
        body = f'id={message_id}'
        requests.post(url_del_message, headers=headers, data=body)

    def check_write_message(self, url_check_message, comment):
        headers = {'Host': 'www.reddit.com'}
        r_wr_mes = requests.get(url_check_message, headers=headers)
        if comment in r_wr_mes.text:
            print('комментарий написан')
        else:
            raise AssertionError("комментарий отсутствует")

    def check_del_message(self, url_check_message, comment):
        headers = {'Host': 'www.reddit.com'}
        r_del_mes = requests.get(url_check_message, headers=headers)
        if comment not in r_del_mes.text:
            print('комментарий удален')
        else:
            raise AssertionError("комментарий присутствует")