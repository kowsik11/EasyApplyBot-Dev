import os
import time
import random
import pickle
import hashlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

import utils, constants, config
from answers import get_answer, _DROPDOWN_DEFAULTS

class EasyApplyWizard:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait   = WebDriverWait(driver, timeout)

    def _scroll_modal(self):
        box = self.driver.find_element(By.CSS_SELECTOR, "div.artdeco-modal__content")
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", box)

    def _js_click(self, el):
        self.driver.execute_script("arguments[0].click();", el)

    def _click(self, label: str) -> bool:
        try:
            btn = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, f'button[aria-label="{label}"]')
            ))
            self._scroll_modal()
            try: btn.click()
            except ElementNotInteractableException: self._js_click(btn)
            return True
        except:
            return False

    def _click_by_text(self, text: str) -> bool:
        try:
            btn = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//button[normalize-space()='{text}']")))
            self._scroll_modal()
            self._js_click(btn)
            return True
        except:
            return False

    def _click_primary_button(self) -> bool:
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, "button.artdeco-button--primary")
            self._scroll_modal()
            self._js_click(btn)
            return True
        except:
            return False

    def _default_for(self, label: str, typ: str) -> str:
        return get_answer(label, typ)

    def _fill_modal(self):
        modal = self.driver.find_element(By.CSS_SELECTOR, "div.artdeco-modal__content")

        for inp in modal.find_elements(By.TAG_NAME, "input"):
            typ = (inp.get_attribute("type") or "text").lower()
            if typ in ("checkbox","radio","hidden","submit","button","image","file"):
                continue
            if not (inp.get_attribute("aria-required")=="true" or inp.get_attribute("required")):
                continue
            if inp.get_attribute("value"):
                continue
            label     = inp.get_attribute("aria-label") or inp.get_attribute("placeholder") or ""
            pattern   = inp.get_attribute("pattern") or ""
            inputmode = inp.get_attribute("inputmode") or ""

            if typ=="text" and (inputmode=="numeric" or "d" in pattern or "year" in label.lower()):
                inp.send_keys("0")
            else:
                inp.send_keys(self._default_for(label, typ))

        for ta in modal.find_elements(By.TAG_NAME, "textarea"):
            if not (ta.get_attribute("aria-required")=="true" or ta.get_attribute("required")):
                continue
            if ta.get_attribute("value"):
                continue
            label = ta.get_attribute("aria-label") or ta.get_attribute("placeholder") or ""
            ta.send_keys(self._default_for(label, "textarea"))

        all_radios = modal.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        groups = {}
        for r in all_radios:
            name = r.get_attribute("name")
            groups.setdefault(name, []).append(r)
        for grp in groups.values():
            choice = random.choice(grp)
            self._js_click(choice)
        for rg in modal.find_elements(By.CSS_SELECTOR, "[role='radiogroup']"):
            opts = rg.find_elements(By.CSS_SELECTOR, "[role='radio']")
            if opts:
                self._js_click(random.choice(opts))

        for cb in modal.find_elements(By.CSS_SELECTOR, "input[type='checkbox']"):
            if not cb.is_selected():
                self._js_click(cb)

        # ✅ Fixed scope to global instead of modal-limited
        for sel in modal.find_elements(By.TAG_NAME, "select"):
            try:
                selected_value = sel.get_attribute("value") or ""
                if selected_value.strip():
                    continue  # already selected

                # Collect visible options
                options = [o for o in sel.find_elements(By.TAG_NAME, "option") if o.text.strip()]
                option_texts = [o.text.strip() for o in options]

                picked = False
                if "Yes" in option_texts:
                    self.driver.execute_script("""
                        arguments[0].value = arguments[1];
                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    """, sel, "Yes")
                    picked = True
                elif len(option_texts) > 1:
                    self.driver.execute_script("""
                        arguments[0].value = arguments[1];
                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    """, sel, options[1].get_attribute("value"))
                    picked = True

                if not picked:
                    print("[⚠️ Dropdown] Could not pick value for select element.")

            except Exception as e:
                print("[⚠️ Select error]", e)


    def run(self) -> str:
        for _ in range(10):
            try:
                self._fill_modal()
            except:
                pass

            if   self._click("Submit application"):
                return "submitted"
            elif self._click("Review your application"):
                continue
            elif self._click("Continue to next step"):
                continue
            elif self._click("Next"):
                continue
            elif self._click_by_text("Next"):
                continue
            elif self._click_primary_button():
                continue
            else:
                break
        return "stopped"


class Linkedin:
    def __init__(self):
        utils.prYellow("🤖  Easy-Apply bot starting …")

        opts = webdriver.ChromeOptions()
        opts.add_argument("--disable-gpu")
        opts.add_argument("--disable-software-rasterizer")
        opts.add_argument("--enable-unsafe-swiftshader")

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=opts,
        )

        self.cookies_path = os.path.join("cookies", self._md5(config.email) + ".pkl")
        self.driver.get("https://www.linkedin.com")
        self._load_cookies()
        if not self._is_logged_in():
            self._login()
            self._save_cookies()
        self._generate_urls()
        self._main_loop()

    @staticmethod
    def _md5(s: str) -> str:
        return hashlib.md5(s.encode()).hexdigest()

    def _load_cookies(self):
        if os.path.exists(self.cookies_path):
            with open(self.cookies_path, "rb") as fh:
                for ck in pickle.load(fh):
                    self.driver.add_cookie(ck)

    def _save_cookies(self):
        os.makedirs("cookies", exist_ok=True)
        with open(self.cookies_path, "wb") as fh:
            pickle.dump(self.driver.get_cookies(), fh)

    def _is_logged_in(self) -> bool:
        self.driver.get("https://www.linkedin.com/feed")
        return "feed" in self.driver.current_url and "login" not in self.driver.current_url

    def _login(self):
        self.driver.get("https://www.linkedin.com/login")
        utils.prYellow("🔄  Logging in …")
        self.driver.find_element(By.ID, "username").send_keys(config.email)
        self.driver.find_element(By.ID, "password").send_keys(config.password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(30)

    def _generate_urls(self):
        os.makedirs("data", exist_ok=True)
        with open("data/urlData.txt", "w", encoding="utf-8") as fh:
            for url in utils.LinkedinUrlGenerate().generateUrlLinks():
                fh.write(url + "\n")
        utils.prGreen("✅ URL list written to data/urlData.txt")

    def _main_loop(self):
        total_seen = total_applied = 0
        for search_url in utils.getUrlDataFile():
            kw, loc = utils.urlToKeywords(search_url)
            utils.prYellow(f"\n🔎  {kw}  –  {loc}")
            self.driver.get(search_url)
            pages = utils.jobsToPages(self.driver.find_element(By.TAG_NAME, "small").text)
            for page in range(pages):
                self.driver.get(f"{search_url}&start={page*constants.jobsPerPage}")
                time.sleep(random.uniform(1, constants.botSpeed))
                offers = self.driver.find_elements(By.XPATH, "//li[@data-occludable-job-id]")
                ids    = {o.get_attribute("data-occludable-job-id").split(":")[-1] for o in offers}
                for job_id in ids:
                    total_seen += 1
                    url = f"https://www.linkedin.com/jobs/view/{job_id}"
                    self.driver.get(url)
                    time.sleep(random.uniform(1, constants.botSpeed))
                    header = self._job_header(total_seen)
                    btn    = self._easy_apply_btn()
                    if not btn:
                        utils.writeResults(f"{header} | 🥳 Already applied | {url}")
                        continue
                    if not self._safe_click(btn):
                        utils.writeResults(f"{header} | 🥵 Cannot click Easy-Apply | {url}")
                        continue
                    time.sleep(1)
                    self._choose_resume()
                    wizard = EasyApplyWizard(self.driver)
                    result = wizard.run()
                    if result == "submitted":
                        total_applied += 1
                        utils.writeResults(f"{header} | 🥳 Applied | {url}")
                    else:
                        utils.writeResults(f"{header} | 🥵 Stopped – extra Qs | {url}")
            utils.prYellow(f"==> Applied {total_applied}/{total_seen} this session.")
        utils.donate(self)

    def _job_header(self, n: int) -> str:
        title   = self._txt("h1")
        company = self._txt("a[href*='company']")
        loc     = self._txt("span.jobs-unified-top-card__bullet")
        return f"{n} | {title} | {company} | {loc}"

    def _txt(self, css: str) -> str:
        try:
            return self.driver.find_element(By.CSS_SELECTOR, css).text.strip()
        except:
            return ""

    def _easy_apply_btn(self):
        try:
            return self.driver.find_element(
                By.CSS_SELECTOR,
                "button.jobs-apply-button:not(.artdeco-button--disabled)"
            )
        except:
            return None

    def _safe_click(self, el) -> bool:
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            try: el.click()
            except ElementNotInteractableException: self.driver.execute_script("arguments[0].click();", el)
            return True
        except:
            return False

    def _choose_resume(self):
        try:
            modal = self.driver.find_element(By.CSS_SELECTOR, "div.artdeco-modal__content")
            pdfs = modal.find_elements(By.CSS_SELECTOR, "div.ui-attachment--pdf")
            if pdfs:
                pdfs[min(len(pdfs), config.preferredCv) - 1].click()
        except:
            pass

if __name__ == "__main__":
    t0 = time.time()
    Linkedin()
    utils.prYellow(f"\nFinished in {round((time.time()-t0)/60,1)} min")
