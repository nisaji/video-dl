import argparse
import json
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


class VideoDownloader:
    """VideoDownloader
    サイト内を条件(ユーザー, 開始ページ, 終了ページ)に従ってクロールし
    ビデオを指定ディレクトリに保存する
    base_url: str
    user_id: str
    start_page: int
    end_page: int
    download_directory: str
    driver: WebDriver | None,
    headless: bool
    """

    def __init__(
        self,
        base_url,
        user_id,
        start_page=1,
        end_page=5,
        download_directory="./videos",  # noqa: E501
        driver=None,
        headless=True,
    ) -> None:
        self.base_url = base_url
        self.driver = driver
        self.user_id = str(user_id)
        self.start_page = start_page
        self.end_page = end_page
        self.download_directory = download_directory
        if driver is None:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = driver
        pass

    def run(self):
        """
        VideoDownloaderの実行用関数
        """
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)
        driver = self.driver
        base_url = self.base_url.rstrip("/") + "/"
        for page in range(self.start_page, self.end_page + 1):
            page_url = f"{base_url}{self.user_id}?page={page}"
            video_data = self.extract_video_data(driver, page_url)
            for e in video_data:
                video_title = e["tweet"].split(" ")[0].replace("/", "_")
                video_url = e["media_url"].split(" ")[0]
                save_path = os.path.join(
                    self.download_directory, f"{video_title}.mp4"
                )  # noqa: E501
                if not os.path.exists(save_path):
                    self.download_video(video_url, save_path)
                    print(f"Downloaded: {save_path}")
                else:
                    print(f"File already exists, skipped: {save_path}")
        driver.quit()

    @staticmethod
    def download_video(url, save_path):
        """
        指定されたURLからビデオをダウンロードし、指定されたパスに保存する。
        url: str
        save_path: str
        """
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
        return

    @staticmethod
    def extract_video_data(driver, page_url):
        """
        指定されたページのURLからビデオのデータを抽出する。
        driver : WebDriver
        page_url: str
        """
        driver.get(page_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if script_tag:
            json_data = json.loads(script_tag.string)
            tweets = (
                json_data.get("props", {})
                .get("pageProps", {})
                .get("tweets", [])  # noqa: E501
            )  # noqa: E501
            return [
                {"tweet": tweet["body"], "media_url": tweet["media_url"]}
                for tweet in tweets
            ]
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Webページからビデオをダウンロードするスクリプト")
    parser.add_argument("--base_url", "-b", required=True, help="ベースとなるURL")
    parser.add_argument("--user_id", "-u", required=True, help="ユーザーID")
    parser.add_argument(
        "--start_page", "-s", type=int, default=1, help="開始ページ"
    )  # noqa: E501
    parser.add_argument(
        "--end_page", "-e", type=int, default=5, help="終了ページ"
    )  # noqa: E501
    parser.add_argument(
        "--download_directory", "-d", default="./videos", help="ダウンロードするディレクトリ"
    )  # noqa: E501
    parser.add_argument(
        "--no_headless",
        action="store_true",
        help="非ヘッドレスモードで実行（デフォルトは無効）",  # noqa: E501
    )  # noqa: E501

    args = parser.parse_args()
    vd = VideoDownloader(
        base_url=args.base_url,
        user_id=args.user_id,
        start_page=args.start_page,
        end_page=args.end_page,
        download_directory=args.download_directory,
        headless=not args.no_headless,
    )
    vd.run()
