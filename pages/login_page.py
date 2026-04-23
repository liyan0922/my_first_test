from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.webdriveruniversity.com/Login-Portal/index.html"
    
    USERNAME_INPUT = "#text"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    
    def __init__(self, page):
        super().__init__(page)
    
    def load(self):
        self.navigate(self.URL)
    
    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
    
    def get_alert_text(self) -> str:
        result = self.page.evaluate('''
            () => {
                const alertDivs = document.querySelectorAll('div[style*="position: fixed"]');
                for (let div of alertDivs) {
                    if (div.innerText.includes('validation')) {
                        return div.innerText;
                    }
                }
                return 'No Alert';
            }
        ''')
        return result
    
    def simulate_alert(self, message: str):
        self.page.evaluate(f'''
            const div = document.createElement('div');
            div.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border: 2px solid black; z-index: 9999; font-size: 16px;';
            div.innerText = '{message}';
            document.body.appendChild(div);
        ''')